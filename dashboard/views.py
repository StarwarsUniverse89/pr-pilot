import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView
from django_tables2 import SingleTableView
from django.urls import reverse
import stripe
from django.conf import settings

from accounts.models import UserBudget
from api.models import UserAPIKey

from dashboard.tables import TaskTable, EventTable, CostItemTable, EventUndoTable
from engine.models.task import Task
from engine.models.task_bill import TaskBill


class APIKeyForm(forms.Form):
    key_name = forms.CharField(
        label="Key Name (optional)",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter key name"}
        ),
    )


class APIKeyListView(LoginRequiredMixin, ListView):
    model = UserAPIKey
    template_name = "api_key_list.html"

    def get_queryset(self):
        # Filter the keys by the logged-in user's ID
        return UserAPIKey.objects.filter(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        budget = UserBudget.get_user_budget(self.request.user.username)
        context["budget"] = budget.formatted
        context["form"] = APIKeyForm()
        return context

    def post(self, request, *args, **kwargs):
        form = APIKeyForm(request.POST)
        if form.is_valid():
            api_key, key = UserAPIKey.objects.create_key(
                name=form.cleaned_data["key_name"], username=request.user.username
            )
            context = {
                "message": "API Key was successfully created!",
                "api_key_name": form.cleaned_data["key_name"],
                "api_key": key,
            }

            # Render the confirmation template with context
            return render(request, "api_key_confirmation.html", context)
        else:
            return self.get(self, request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, SingleTableView):
    model = Task
    table_class = TaskTable
    template_name = "task_list.html"

    def get_queryset(self):
        # Filter the tasks by the logged-in user's ID
        return Task.objects.filter(github_user=self.request.user.username)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        budget = UserBudget.get_user_budget(self.request.user.username)
        context["budget"] = budget.formatted
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        # Filter the queryset to only include tasks owned by the logged-in user
        return Task.objects.filter(github_user=self.request.user.username)

    def get_object(self, queryset=None):
        """Override get_object to ensure task ownership."""
        if queryset is None:
            queryset = self.get_queryset()
        # Make sure to catch the task based on the passed ID and check ownership
        pk = self.kwargs.get(self.pk_url_kwarg)
        task = get_object_or_404(queryset, pk=pk)

        # Check if the task belongs to the logged-in user
        if task.github_user != self.request.user.username:
            raise Http404("You do not have permission to view this task.")

        return task

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the task from the context
        task = context["task"]
        bill = TaskBill.objects.filter(task=task).first()
        discount_credits = 0
        if bill:
            discount_credits = (
                bill.total_credits_used * (1 / (100 - bill.discount_percent))
                if bill.discount_percent > 0
                else 0
            )
        # Create an EventTable instance with the task's events
        budget = UserBudget.get_user_budget(self.request.user.username)
        context["budget"] = budget.formatted
        context["event_table"] = EventTable(task.events.all())
        context["cost_item_table"] = CostItemTable(task.cost_items.all())
        context["task_result"] = mark_safe(markdown.markdown(task.result))
        context["total_cost"] = sum([item.credits for item in task.cost_items.all()])
        context["discount_credits"] = discount_credits
        context["bill"] = bill
        context["can_undo"] = (
            len(
                [
                    event
                    for event in task.events.all()
                    if event.reversible and not event.reversed
                ]
            )
            > 0
        )
        return context


class TaskUndoView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_undo.html"
    context_object_name = "task"

    def get_queryset(self):
        # Filter the queryset to only include tasks owned by the logged-in user
        return Task.objects.filter(github_user=self.request.user.username)

    def get_object(self, queryset=None):
        """Override get_object to ensure task ownership."""
        if queryset is None:
            queryset = self.get_queryset()
        # Make sure to catch the task based on the passed ID and check ownership
        pk = self.kwargs.get(self.pk_url_kwarg)
        task = get_object_or_404(queryset, pk=pk)

        # Check if the task belongs to the logged-in user
        if task.github_user != self.request.user.username:
            raise Http404("You do not have permission to view this task.")

        return task

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the task from the context
        task = context["task"]
        # Create an EventTable instance with the task's events
        budget = UserBudget.get_user_budget(self.request.user.username)
        context["budget"] = budget.formatted
        context["event_table"] = EventUndoTable(task.reversible_events)
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        marked_event_ids = request.POST.getlist("reversible")
        for event_id in marked_event_ids:
            event = task.events.get(pk=event_id)
            if event.reversible:
                # Process the reversible event
                event.undo()
        # Process the marked events here
        # Redirect to a confirmation page or back to the task detail page
        return redirect("task_detail", pk=task.pk)


@login_required
def create_stripe_payment_link(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("account_login"))

    # Get 'credits' query param
    credits = request.GET.get("credits")
    if not credits:
        return HttpResponseRedirect(reverse("task_list"))

    stripe.api_key = settings.STRIPE_API_KEY
    price = (
        "price_1OvuaJCyRBEZZGEuL8I9b308"
        if settings.DEBUG
        else "price_1OwBvgCyRBEZZGEuAbzUzfRF"
    )
    payment_link = stripe.PaymentLink.create(
        line_items=[{"price": price, "quantity": int(credits)}],
        after_completion={
            "type": "redirect",
            "redirect": {"url": "https://app.pr-pilot.ai/dashboard/tasks/"},
        },
        metadata={
            "github_user": request.user.username,
            "credits": int(credits),
        },
    )

    return HttpResponseRedirect(payment_link.url)

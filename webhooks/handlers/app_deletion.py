import logging

from django.http import JsonResponse

from webhooks.models import GitHubAppInstallation


logger = logging.getLogger(__name__)

def handle_app_deletion(payload):
    app_id = payload['installation']['app_id']
    logger.info(f'Uninstalling app {app_id}')
    GitHubAppInstallation.objects.filter(installation_id=payload['installation']['id']).delete()
    return JsonResponse({'status': 'success', 'message': 'Installation deleted'})
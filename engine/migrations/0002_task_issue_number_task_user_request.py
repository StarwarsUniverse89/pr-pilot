# Generated by Django 5.0.2 on 2024-03-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='issue_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='user_request',
            field=models.TextField(blank=True),
        ),
    ]
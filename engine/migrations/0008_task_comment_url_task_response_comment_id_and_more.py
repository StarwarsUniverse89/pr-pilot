# Generated by Django 5.0.2 on 2024-03-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0007_costitem_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='comment_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='response_comment_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='response_comment_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
# Generated by Django 4.1.6 on 2023-02-06 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(default='available', max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='translation',
            field=models.TextField(blank=True, null=True),
        ),
    ]

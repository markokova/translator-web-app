# Generated by Django 4.1.6 on 2023-02-07 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rating_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispute',
            name='bid',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.bid'),
            preserve_default=False,
        ),
    ]
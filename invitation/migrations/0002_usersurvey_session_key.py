# Generated by Django 5.0.4 on 2024-04-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersurvey',
            name='session_key',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]

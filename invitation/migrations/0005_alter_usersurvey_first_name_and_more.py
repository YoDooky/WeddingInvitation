# Generated by Django 5.0.4 on 2024-04-14 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0004_alter_usersurvey_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersurvey',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='usersurvey',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
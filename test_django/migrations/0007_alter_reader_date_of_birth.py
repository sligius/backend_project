# Generated by Django 4.2.5 on 2023-11-08 22:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0006_critic_organization_critic_years_of_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Дата рождения'),
        ),
    ]

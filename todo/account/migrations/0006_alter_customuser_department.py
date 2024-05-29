# Generated by Django 5.0.4 on 2024-05-04 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_customuser_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.department'),
        ),
    ]

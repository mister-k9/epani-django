# Generated by Django 4.0.8 on 2022-11-03 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='machine_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
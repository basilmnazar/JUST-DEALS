# Generated by Django 4.2.5 on 2024-08-30 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_app', '0023_voucher_dealer_alter_voucher_voucher_about_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='button_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.5 on 2024-09-09 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0002_vendor_alter_customuser_role'),
        ('deal_app', '0004_remove_vouchercoupon_voucher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealers',
            name='user',
        ),
        migrations.AddField(
            model_name='dealers',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts_app.vendor'),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='business_owner_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='merchant_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='merchant_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='merchant_type',
            field=models.CharField(choices=[('hotel', 'Hotel'), ('restaurant', 'Restaurant'), ('spa', 'Spa'), ('saloon', 'Saloon')], default='hotel', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='outlet_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='dealers',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

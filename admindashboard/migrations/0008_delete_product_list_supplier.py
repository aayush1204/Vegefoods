# Generated by Django 3.0.7 on 2020-06-28 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20200628_2343'),
        ('admindashboard', '0007_auto_20200628_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='delete_product_list',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Supplier'),
        ),
    ]
# Generated by Django 3.0.2 on 2020-06-19 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0004_auto_20200619_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addproductlist',
            name='product_image',
        ),
        migrations.RemoveField(
            model_name='addproductlist',
            name='supplier_username',
        ),
    ]
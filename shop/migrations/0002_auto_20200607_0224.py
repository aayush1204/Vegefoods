# Generated by Django 2.2.4 on 2020-06-06 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product_image', models.CharField(max_length=100)),
                ('is_ordered', models.BooleanField(default=False)),
                ('refunded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=20)),
                ('message', models.CharField(max_length=200)),
                ('is_addressed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('referral_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('apartmentno', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=6)),
                ('is_completed', models.BooleanField(default=False)),
                ('total_amount', models.IntegerField(default=0)),
                ('is_refunded', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_shipped', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='shop.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('society_name', models.CharField(max_length=30)),
                ('society_locality', models.CharField(max_length=30)),
                ('society_address', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='None', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='product_sku',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_code', models.CharField(max_length=10)),
                ('voucher_value', models.IntegerField(default=1)),
                ('society', models.ManyToManyField(to='shop.Society')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField(default='')),
                ('pincode', models.PositiveIntegerField(default=0)),
                ('GST_number', models.PositiveIntegerField(default=0)),
                ('Bank_Account_Details', models.TextField(default='')),
                ('store_name', models.CharField(max_length=50)),
                ('store_description', models.CharField(max_length=200)),
                ('store_address', models.TextField(default='')),
                ('is_approved', models.BooleanField(default=False)),
                ('supplier_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Refunds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_amount', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(to='shop.Cart')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pr', models.CharField(choices=[('S', 'Supplier'), ('C', 'Customer'), ('A', 'Admin')], max_length=1)),
                ('society', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Society')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ManyToManyField(to='shop.Supplier'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('apartmentno', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=6)),
                ('category', models.CharField(choices=[('1', 'Category1'), ('2', 'Category2')], max_length=1)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Supplier'),
        ),
    ]

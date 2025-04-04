# Generated by Django 5.1.7 on 2025-03-22 06:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_category_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=225, verbose_name='Покупатель')),
                ('product', models.CharField(max_length=225, verbose_name='Продукт')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('check_image', models.ImageField(upload_to='media/check', verbose_name='Чек')),
                ('total_price', models.PositiveIntegerField(verbose_name='Сумма')),
            ],
            options={
                'verbose_name': 'Оплата',
                'verbose_name_plural': 'Оплаты',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('qr_image', models.ImageField(upload_to='media/qr', verbose_name=' QR')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Способ оплаты',
                'verbose_name_plural': 'Способы оплаты',
            },
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('check_image', models.ImageField(upload_to='media/check', verbose_name='Чек')),
                ('total_price', models.PositiveIntegerField(verbose_name='Сумма')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на оплату',
                'verbose_name_plural': 'Заявки на оплаты',
            },
        ),
    ]

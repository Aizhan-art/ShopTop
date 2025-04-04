# Generated by Django 5.1.7 on 2025-03-24 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_favoriteproduct'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество товара')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='main.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]

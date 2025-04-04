# Generated by Django 5.1.7 on 2025-03-23 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_rating_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название цвета')),
                ('hex_code', models.CharField(blank=True, max_length=7, null=True, unique=True, verbose_name='HEX-код')),
            ],
            options={
                'verbose_name': 'Цвет продукта',
                'verbose_name_plural': 'Цвета продукт',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.color', verbose_name='Цвет'),
        ),
    ]

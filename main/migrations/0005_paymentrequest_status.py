# Generated by Django 5.1.7 on 2025-03-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_payment_paymentmethod_paymentrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='status',
            field=models.CharField(choices=[('in_processing', 'В обработке'), ('denied', 'Отклонено'), ('accepted', 'Принято')], default='in_processing', max_length=15, verbose_name='Статус оплаты'),
        ),
    ]

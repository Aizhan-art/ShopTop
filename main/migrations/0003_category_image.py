# Generated by Django 5.1.7 on 2025-03-20 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_user_rating_user_ratinganswer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/category_images', verbose_name='Изображение категории'),
        ),
    ]

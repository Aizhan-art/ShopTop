from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .choices import OrderStatusEnum
from django.conf import settings


User = get_user_model()

class Category(models.Model):
    title= models.CharField(
        max_length=123,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='media/category_images',
        null=True,
        blank=True,
        verbose_name='Изображение категории'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Image(models.Model):
    file = models.ImageField(
        upload_to='media/product_file',
        verbose_name='Файл'
    )

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'


class Color(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название цвета"
    )
    hex_code = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="HEX-код",
        blank=True,
        null=True
    )


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Цвет продукта'
        verbose_name_plural = 'Цвета продукт'


class Product(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models. CharField(
        max_length=123,
        verbose_name='Название'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    main_image = models.ImageField(
        upload_to='media/main_covers',
        verbose_name='Главное фото',
        help_text='Фото которое будет отображаться на обложке обьявления'
    )
    images = models.ManyToManyField(
        Image,
        verbose_name='Изображения'
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Цвет"
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    views = models.IntegerField(
        default=0,
        verbose_name='Популярные товары'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Rating(models.Model):
    user = models.ForeignKey(
         User,
         on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # <-- Исправлено
        verbose_name='Оценка'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Коментарий'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.user} -->{self.product}'


    class Meta:
         verbose_name = 'Отзыв'
         verbose_name_plural = 'Отзывы'


class RatingAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='rating_answers'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Коментарий'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    time_limit = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Ограничение по времени'
    )

    def __str__(self):
        return f'{self.user} -->{self.rating}'
    class Meta:
         verbose_name = 'Ответ на отзыв'
         verbose_name_plural = 'Ответы на отзывы'


class PaymentRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='orders'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name='Оплачено'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    check_image = models.ImageField(
        upload_to='media/check',
        verbose_name='Чек'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='Сумма'
    )
    status = models.CharField(
        choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.IN_PROCESSING,
        verbose_name='Статус оплаты',
        max_length=15
    )

    def __str__(self):
        return f'{self.user}-->{self.product}'

    class Meta:
        verbose_name = 'Заявка на оплату'
        verbose_name_plural = 'Заявки на оплаты'


class PaymentMethod(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    qr_image = models.ImageField(
        upload_to='media/qr',
        verbose_name=' QR'
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.user}-->{self.title}'

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

class Payment(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    user = models.CharField(
        max_length=225,
        verbose_name='Покупатель'
    )
    product = models.CharField(
        max_length=225,
        verbose_name='Продукт'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )
    check_image = models.ImageField(
        verbose_name='Чек',
        upload_to='media/check'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='Сумма'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Продукт'
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'product')  # Чтобы не было дубликатов

    def __str__(self):
        return f"{self.user} добавил в избранное {self.product}"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_carts",
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество товара'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} - {self.product} ({self.quantity})"
from django.contrib import admin
from .models import (Category, Image, Product, Rating,
                     RatingAnswer, PaymentMethod, PaymentRequest,
                     Payment, Color, FavoriteProduct, Cart)


admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(RatingAnswer)
admin.site.register(PaymentMethod)
admin.site.register(PaymentRequest)
admin.site.register(Payment)
admin.site.register(Color)
admin.site.register(FavoriteProduct)
admin.site.register(Cart)

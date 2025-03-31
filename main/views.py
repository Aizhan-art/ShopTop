from decimal import Decimal
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib import messages
from django.db.models import Avg, Sum
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import ProductCreateForm, ProductUpdateForm
from .filters import ProductListFilter
from .models import (Product, Category, Rating, RatingAnswer, PaymentMethod,
                     PaymentRequest, Payment, FavoriteProduct, Cart, Image)



def index_view(request):
    products = Product.objects.filter(is_active=True).order_by('-views')[:6]
    categories = Category.objects.all()
    popular_products = Product.objects.filter(is_active=True).order_by('-views')[:3]

    for product in products:
        product.avg_rating = product.rating_set.aggregate(avg_rating=Avg('count'))['avg_rating'] or 0

    return render(
        request,
        'main/index.html',
        {'products': products, 'categories': categories, 'popular_products': popular_products}
    )
def product_detail_view(request, product_id):
    product =  get_object_or_404(Product,id=product_id)
    product.views += 1
    product.save(update_fields=['views'])

    product_update_form =  ProductUpdateForm(instance=product)
    product_comments = Rating.objects.filter(product=product)
    rating_avg = product_comments.aggregate(Avg('count'))['count__avg']
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    return render(
        request=request,
        template_name='main/product_detail.html',
        context={
            'product': product,
            'similar_products': similar_products,
            'product_update_form': product_update_form,
            'product_comments': product_comments,
            'rating_avg': rating_avg
        })


def product_create_view(request):
    if not request.user.is_authenticated:
        raise Http404

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product_object = form.save(commit=False)
            product_object.user = request.user
            product_object.save()

            if request.FILES.getlist('images'):
                for img in request.FILES.getlist('images'):
                    image_obj = Image.objects.create(file=img)
                    product_object.images.add(image_obj)

            messages.success(request, 'Успешно создано!')
            return redirect('index')

    form = ProductCreateForm()
    return render(request, 'main/product_create.html', {'form': form})

def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.user:
        raise Http404

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно обновлен!')
        else:
            messages.error(request, 'Ошибка при обновлении продукта.')
    return redirect('product_detail', product_id=product.id)

def rating_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        messages.error(request, 'Только авторизованные пользователи могут оставлять отзывы!')
        return redirect('product_detail', product_id=product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        count_str = request.POST.get('count', '')
        try:
            count = int(count_str)
        except ValueError:
            messages.error(request, 'Пожалуйста, выберите оценку!')
            return redirect('product_detail', product_id=product_id)

        # Если значение рейтинга равно 0, можно также показать сообщение об ошибке
        if count == 0:
            messages.error(request, 'Пожалуйста, выберите оценку больше 0!')
            return redirect('product_detail', product_id=product_id)

        rating = Rating(
            user=request.user,
            product=product,
            count=count,
            comment=comment
        )
        rating.save()
        messages.success(request, 'Отзыв успешно отправлен!')
        return redirect('product_detail', product_id=product_id)

def rating_answer_create_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    if rating.product.user != request.user:
        messages.error(request, 'Нет доступа!')
        return redirect('product_detail', rating.product_id)
    if request.method == 'POST':
        comment = request.POST.get('comment', '')

        rating_answer = RatingAnswer(
            user=request.user,
            rating=rating,
            comment=comment
        )

        rating_answer.save()

        messages.success(request, 'Успешно отправлено!')
        return redirect('product_detail', rating.product_id)

def user_profile_view(request):
    payment_requests = PaymentRequest.objects.filter(product__user=request.user).order_by('-id')[:3]

    return render(
        request=request,
        template_name='main/user_profile.html',
        context={'payment_requests': payment_requests}
    )

def product_payment_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=product.user)

    if request.method == 'POST':
        check =request.FILES.get('check', '')
        quantity = request.POST.get('quantity', '1')

        try:
            quantity = Decimal(quantity)
        except:
            messages.error(request, 'Неверное количество')
            return redirect('index')

        price = product.price if product.price is not None else Decimal('0.00')
        total_price = quantity * price

        order = PaymentRequest(
            user=request.user,
            product=product,
            quantity=quantity,
            check_image=check,
            total_price=total_price
        )
        order.save()
        messages.success(request, 'Заявка на оплату отправлено продавцу')
        return redirect('index')

    return render(
        request=request,
        template_name='main/product_payment.html',
        context={'seller_payment_methods': seller_payment_methods}
    )

def product_list_view(request):
    queryset = Product.objects.filter(is_active=True).annotate(rating_avg=Avg('rating__count'))

    if 'product_search' in request.GET:
        product_name = request.GET.get('product_search')
        queryset = queryset.filter(title__icontains=product_name)

    products = ProductListFilter(request.GET, queryset=queryset)

    sorted_queryset = products.qs.order_by('id')

    paginator = Paginator(sorted_queryset, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request=request,
        template_name='main/product_list.html',
        context={'page_obj': page_obj}
    )

def payment_request_list_view(request):
    payment_requests = PaymentRequest.objects.filter(product__user=request.user).order_by('-id')

    return render(
        request=request,
        template_name='main/payment_request.html',
        context={'payment_requests': payment_requests}
    )


def payment_request_update_status(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        payment_request.status = status
        payment_request.save()

        if payment_request.status == 'accepted':
            payment = Payment(
                seller=payment_request.product.user,
                user=payment_request.user.first_name,
                product=payment_request.product.title,
                quantity=payment_request.quantity,
                check_image=payment_request.check_image,
                total_price=payment_request.total_price
            )
            payment.save()

        messages.success(request, 'Успешно изменено')

    return redirect('payment_requests')


def payment_list_view(request):
    payments = Payment.objects.filter(seller=request.user)

    total_payments = payments.aggregate(Sum('total_price'))['total_price__sum']

    return render(
        request=request,
        template_name='main/payments.html',
        context={
            "payments": payments,
            "total_payments": total_payments
        }
    )


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)

    return render(request, 'main/category_products.html', {
        'category': category,
        'products': products
    })

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({"is_favorite": is_favorite})

@login_required
def favorite_products(request):
    products = Product.objects.filter(favorited_by__user=request.user)

    return render(request, 'main/favorites.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += 1  # Увеличиваем количество, если товар уже в корзине
            cart_item.save()

        return JsonResponse({"status": "success", "message": "Товар добавлен в корзину"})

    return JsonResponse({"status": "error", "message": "Неверный метод запроса"}, status=400)



@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()

    if cart_item:
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Товар удален из корзины'})
    return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'})

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    return render(request, 'main/cart.html', {'cart_items': cart_items})


def search_results(request):
    query = request.GET.get('q')
    results = Product.objects.filter(title__icontains=query) if query else []
    return render(request, 'main/search_results.html', {'results': results, 'query': query})

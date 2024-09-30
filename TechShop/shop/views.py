from django.shortcuts import render, redirect
from .SupporPrograms.page_manager import page_manager
from main import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shop_page(request, page_number):
    if request.method == 'GET':
        products = models.Product.objects.all()
        PRODUCTS_ON_PAGE = 10  # Количество товаров на одной странице

        # Применяем пагинацию
        paginator = Paginator(products, PRODUCTS_ON_PAGE)

        try:
            paginated_products = paginator.page(page_number)
        except PageNotAnInteger:
            # Если номер страницы не является числом, возвращаем первую страницу
            paginated_products = paginator.page(1)
        except EmptyPage:
            # Если номер страницы превышает общее количество страниц, возвращаем последнюю страницу
            paginated_products = paginator.page(paginator.num_pages)

        # Добавляем первую картинку для каждого продукта
        for p in paginated_products:
            first_image = models.ImageProduct.objects.filter(product=p).first()
            p.image = first_image.image if first_image else None

        data = {
            'products': paginated_products,
        }

        return render(request, 'shop/shop.html', data)

    else:
        return redirect('shop_page')
    

def product_page(request, product_id):
    if request.method == 'GET':

        if request.user.is_authenticated:
            result = models.ViewProduct.objects.filter(user=request.user, product=models.Product.objects.get(id=product_id))
            if result:
                result.delete()

            new_view = models.ViewProduct(user=request.user, product=models.Product.objects.get(id=product_id))
            new_view.save()

        return render(request, 'shop/product_page.html', {'product': models.Product.objects.get(id=product_id)})

    else:
        return redirect('product_page')


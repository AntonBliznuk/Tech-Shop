from django.shortcuts import render, redirect
from .SupporPrograms.page_manager import page_manager
from main import models


def shop_page(request, page_number):
    if request.method == 'GET':

        products = models.Product.objects.all()
        PRODUCTS_ON_PAGE = 10

        # in the feature hear will be filters

        products = page_manager(products, page_number, PRODUCTS_ON_PAGE)

        data = {
            'current_page': page_number,
            'number_of_all_page': (len(products) // PRODUCTS_ON_PAGE) + 1,
            'products': products
        }
        return render(request, 'shop/shop_page.html', data)

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


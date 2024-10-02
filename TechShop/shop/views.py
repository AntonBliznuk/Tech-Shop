from django.shortcuts import render, redirect
from .SupporPrograms.page_manager import page_manager
from main import models
from user_profile.forms import OrderForm
from user_profile.models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shop_page(request, page_number):
    
    if request.method == 'GET':
        products = models.Product.objects.all()
        PRODUCTS_ON_PAGE = 3  

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
            products = products.filter(brand__icontains=search_query
            ) | products.filter(
                name__icontains=search_query
            )
        
        if request.GET.get('cat'):
            products = products.filter(category__name=request.GET.get('cat'))

        if request.GET.get('brand'):
            products = products.filter(brand=request.GET.get('brand'))

        if request.GET.get('price_min'):

            products_list = list(products)
            products = []

            for i in range(0, len(products_list)):

                if products_list[i].price >= int(request.GET.get('price_min')):
                    products.append(products_list[i])


        if request.GET.get('price_max'):

            products_list = list(products)
            products = []

            for i in range(0, len(products_list)):

                if products_list[i].price <= int(request.GET.get('price_max')):
                    products.append(products_list[i])
        
        

        all_brands = models.Product.objects.values_list('brand', flat=True)


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
            'categories': models.Category.objects.all(),
            'brand_names': list(set(all_brands)),
        }

        return render(request, 'shop/shop.html', data)

    else:
        return redirect('shop_page')
    


def product_page(request, product_id):
    if request.method == 'GET':

        if request.user.is_authenticated:
            is_liked = models.WhisList.objects.filter(user=request.user, product=models.Product.objects.get(id=product_id))
            if is_liked:
                is_liked = True
            else:
                is_liked = False

            result = models.ViewProduct.objects.filter(user=request.user, product=models.Product.objects.get(id=product_id))
            if result:
                result.delete()

            new_view = models.ViewProduct(user=request.user, product=models.Product.objects.get(id=product_id))
            new_view.save()

            if request.GET.get('like') is not None:
                if request.GET.get('like') == 'True':
                    whish = models.WhisList.objects.filter(user=request.user, product=models.Product.objects.get(id=product_id))
                    if whish:
                        whish.delete()

                    new_whish = models.WhisList(user=request.user, product=models.Product.objects.get(id=product_id))
                    new_whish.save()

                else:
                    whish = models.WhisList.objects.filter(user=request.user, product=models.Product.objects.get(id=product_id))
                    if whish:
                        whish.delete()
        else:
            is_liked = False

        prod = models.Product.objects.get(id=product_id)
        img = list(models.ImageProduct.objects.filter(product=prod))
        images = []
        for i in img:
            images.append(i.image)

        data = {
            'product': prod,
            'images': images,
            'main_image': images[0],
            'is_liked': is_liked
        }

        return render(request, 'shop/product_page.html', data)


    else:
        return redirect('product_page')
    



def order_page(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'shop/order_page.html', {'form': OrderForm()})
        
        elif request.method == 'POST':
            form = OrderForm(data=request.POST)
            if form.is_valid():
                new_order = Order(user=request.user, product=models.Product.objects.get(id=product_id), user_phone=form.cleaned_data['user_phone'])
                new_order.save()
                return redirect(f'/shop/product/{product_id}/')

    else:
        return redirect(f'/shop/product/{product_id}/')


from django.shortcuts import render
from .parser import parse_external_data
from .parser import parse_product_details


def home(request):
    result = parse_external_data()  
    
    categories_list = result.get('data', [])
    
    return render(request, 'main/index.html', {'categories': categories_list})


def category_detail_view(request, category_slug):
    result = parse_external_data(category_slug=category_slug)

    display_title = result.get('title') or category_slug.replace('-', ' ').capitalize()
    
    context = {
        'category_name': display_title,
        'data': result.get('data', [])  # безпечно беремо список даних
    }
    
    if result.get('type') == 'subcategories':
        return render(request, 'main/category_detail.html', context)
        
    elif result.get('type') == 'products':
        return render(request, 'main/products_list.html', context)
        
    else:
        return render(request, 'main/empty.html', context)

def product_page_view(request, product_slug):
    product_data = parse_product_details(product_slug)
    
    if not product_data:
        return render(request, 'main/empty.html', {'category_name': 'Товар не знайдено'})
        
    context = {
        'product': product_data
    }
    return render(request, 'main/product_page.html', context)
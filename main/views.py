from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

from .parser import parse_external_data


def home(request):
    parsed_items = parse_external_data()
    categories = [
        {
            'name': item.get('name') or 'Категорія',
            'image_url': item.get('image_url') or 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80',
            'link': item.get('link') or '#',
        }
        for item in parsed_items
    ]

    return render(request, 'main/index.html', {
        'categories': categories,
    })


def category_detail_view(request, category_slug):
    subcategories = parse_external_data(category_slug=category_slug)
    
    context = {
        'subcategories': subcategories,
        'category_name': category_slug.replace('-', ' ').capitalize()
    }
    return render(request, 'main/category_detail.html', context)
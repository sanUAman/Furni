# main/parser.py
import requests
from bs4 import BeautifulSoup

def parse_external_data(category_slug="krisla-stilci-pufi"):
    url = f"https://doloto.com.ua/ua/catalog/{category_slug}/1/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            category_elements = soup.select('div.catalog-categories__wrap a.catalog-categories__item')
            
            h1_tag = soup.select_one('h1.catalog__title')
            parsed_title = h1_tag.get_text(strip=True) if h1_tag else None

            if category_elements:
                subcategories = []
                for element in category_elements:
                    text_span = element.find('span', class_='catalog-categories__text')
                    name = text_span.get_text(strip=True) if text_span else None
                    link = element.get('href')
                    img_tag = element.find('img', class_='catalog-categories__img')
                    image_src = img_tag.get('src') if img_tag else None

                    if name:
                        subcategories.append({
                            'name': name,
                            'link': link,
                            'image_url': image_src
                        })
                return {'type': 'subcategories', 'data': subcategories}
            
            product_elements = soup.select('section.catalog__products-list div.product-card')
            
            if product_elements:
                products = []
                for element in product_elements:
                    title_tag = element.select_one('h5.product-card__title')
                    name = title_tag.get_text(strip=True) if title_tag else "Без назви"
                    
                    image_link_tag = element.select_one('a.product-card__image-link')
                    link = image_link_tag.get('href') if image_link_tag else "#"
                    
                    img_tag = image_link_tag.find('img') if image_link_tag else None
                    image_src = img_tag.get('src') if img_tag else None
                    
                    price_tag = element.select_one('span.product-card__price')
                    if price_tag:
                        price = price_tag.get_text(strip=True).replace('\xa0', ' ')
                    else:
                        price = "Ціну уточнюйте"
                    
                    products.append({
                        'name': name,
                        'link': link,
                        'image_url': image_src,
                        'price': price
                    })
                return {'type': 'products', 'data': products, 'title': parsed_title}
            
    except requests.RequestException as e:
        print(f"Помилка при запиті: {e}")
        
    return {'type': 'empty', 'data': []}

def parse_product_details(product_slug):
    url = f"https://doloto.com.ua/ua/product/{product_slug}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            h1_tag = soup.select_one('h1.product__title')
            title = h1_tag.get_text(strip=True) if h1_tag else "Назва відсутня"
            
            price_tag = soup.select_one('.product__price-current, .price')
            price = price_tag.get_text(strip=True) if price_tag else "Ціну уточнюйте"
            
            header_area = soup.select_one('div.product__content-header')

            context_search = header_area if header_area else soup
            
            brand_tag = context_search.select_one('span.product__brand-name')
            brand_name = brand_tag.get_text(strip=True) if brand_tag else "Без бренду"

            brand_image_link_tag = context_search.select_one('a.product__brand')
            link = brand_image_link_tag.get('href') if brand_image_link_tag else "#"
            
            img_tag = brand_image_link_tag.find('img') if brand_image_link_tag else None
            image_src = img_tag.get('src') if img_tag else None

            lot_blocks = context_search.select('div.product__lot')

            code_name = "—"
            article_name = "—"

            for block in lot_blocks:
                title_tag = block.select_one('span.product__lot-title')
                content_tag = block.select_one('span.product__lot-content')
                
                if title_tag and content_tag:
                    title_text = title_tag.get_text(strip=True)
                    content_text = content_tag.get_text(strip=True)
                    
                    if "Код" in title_text:
                        code_name = content_text
                    elif "Артикул" in title_text:
                        article_name = content_text

            gallery_container = soup.find('div', id='lightgallery')
            images_list = []

            if gallery_container:
                a_tags = gallery_container.select('a[href]')
                for a in a_tags:
                    img_url = a.get('href')
                    if img_url and img_url not in images_list:
                        images_list.append(img_url)

            price_now_tag = soup.select_one('span.product__price-sum')
            if price_now_tag:
                price_now = price_now_tag.get_text(strip=True).replace('\xa0', ' ') + " грн"
            else:
                price_now = "Ціну уточнюйте"

            price_old_tag = soup.select_one('span.product__price-old-sum')
            if price_old_tag:
                price_old = price_old_tag.get_text(strip=True).replace('\xa0', ' ') + " грн"
            else:
                price_old = None
            
            return {
                'title': title,
                'brand': brand_name,
                'lot': code_name,
                'article': article_name,
                'price_now': price_now,
                'price_old': price_old,
                'link': link,
                'brand_image_url': image_src,
                'images': images_list
            }
            
    except Exception as e:
        print(f"Помилка парсингу детальної сторінки: {e}")
        
    return None
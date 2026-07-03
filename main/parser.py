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
            
            all_categories = []
            category_elements = soup.select('div.catalog-categories__wrap a.catalog-categories__item')
            
            for element in category_elements:
                text_span = element.find('span', class_='catalog-categories__text')
                name = text_span.get_text(strip=True) if text_span else None

                link = element.get('href')
                
                img_tag = element.find('img', class_='catalog-categories__img')
                image_src = img_tag.get('src') if img_tag else None

                if name:
                    all_categories.append({
                        'name': name,
                        'link': link,
                        'image_url': image_src
                    })
                    
            return all_categories
    except requests.RequestException as e:
        print(f"Помилка при запиті: {e}")
        
    return []
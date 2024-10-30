import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def get_soup(url):
    headers = {
        'User-Agent': 'MinisoProductCrawler/1.0 (educational purposes)'
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

def is_product_url(url):
    return url.endswith('/p')

def extract_product_links(url):
    product_urls = set()
    soup = get_soup(url)
    
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        if is_product_url(link):
            product_urls.add(link)
    
    return product_urls

def crawl_miniso(base_url, max_pages=100):
    all_product_urls = set()
    visited_pages = set()
    pages_to_visit = [base_url]
    
    while pages_to_visit and len(visited_pages) < max_pages:
        url = pages_to_visit.pop(0)
        if url in visited_pages:
            continue
        
        print(f"Visitando: {url}")
        visited_pages.add(url)
        
        soup = get_soup(url)
        product_urls = extract_product_links(url)
        all_product_urls.update(product_urls)
        
        # Buscar más páginas de categoría
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if base_url in link and link not in visited_pages and not is_product_url(link):
                pages_to_visit.append(link)
        
        time.sleep(2)  # Pausa para ser respetuoso con el servidor
    
    return all_product_urls

# Uso del script
base_url = 'https://www.miniso.cl'
product_links = crawl_miniso(base_url)

# Guardar los links en un archivo
with open('miniso_product_links.txt', 'w') as f:
    for link in product_links:
        f.write(f"{link}\n")

print(f"Se han extraído {len(product_links)} links de productos.")

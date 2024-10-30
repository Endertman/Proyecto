import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import os

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

def load_existing_product_links(file_path):
    """Carga las URLs existentes desde el archivo."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_new_product_links(file_path, new_links):
    """Guarda solo las nuevas URLs en el archivo."""
    with open(file_path, 'a') as f:
        for link in new_links:
            f.write(f"{link}\n")

def crawl_miniso(base_url, file_path, max_pages=500):
    all_product_urls = set()
    visited_pages = set()
    pages_to_visit = [base_url]
    
    # Cargar URLs existentes
    existing_links = load_existing_product_links(file_path)
    
    while pages_to_visit and len(visited_pages) < max_pages:
        url = pages_to_visit.pop(0)
        if url in visited_pages:
            continue
        
        print(f"Visitando: {url}")
        visited_pages.add(url)
        
        soup = get_soup(url)
        product_urls = extract_product_links(url)
        
        # Filtrar URLs nuevas que no estén en el archivo existente
        new_product_urls = product_urls - existing_links
        if new_product_urls:
            print(f"Se encontraron {len(new_product_urls)} nuevas URLs.")
            save_new_product_links(file_path, new_product_urls)
        
        all_product_urls.update(new_product_urls)
        
        # Buscar más páginas de categoría
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if base_url in link and link not in visited_pages and not is_product_url(link):
                pages_to_visit.append(link)
        
        time.sleep(2)  # Pausa para ser respetuoso con el servidor
    
    return all_product_urls

# Uso del script
base_url = 'https://www.miniso.cl'
file_path = 'miniso_product_links.txt'

# Realizar el crawling, guardando nuevas URLs en el archivo
product_links = crawl_miniso(base_url, file_path)

print(f"Se han extraído {len(product_links)} nuevas links de productos.")

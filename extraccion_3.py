import requests
from bs4 import BeautifulSoup
import json
import os
import re

def extract_json_ld(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    json_ld = soup.find('script', type='application/ld+json')
    
    if json_ld:
        return json.loads(json_ld.string), soup
    return None, soup

def extract_product_identifier(soup):
    identifier_meta = soup.find('meta', property='product:retailer_item_id')
    if identifier_meta:
        return identifier_meta.get('content').strip()
    return None

def get_base_image_url(url):
    base_url = re.match(r'.*ids/(\d+)', url)
    if base_url:
        return base_url.group(1)
    return url

def get_existing_images(folder_path):
    """Obtener un conjunto de nombres de archivo existentes en la carpeta."""
    if not os.path.exists(folder_path):
        return set()
    return set(os.listdir(folder_path))

def extract_all_product_images(soup, product_identifier):
    product_images = soup.find_all('img', class_='vtex-store-components-3-x-productImageTag')
    
    # Diccionario para llevar registro de imágenes únicas
    unique_images = {}
    
    for img in product_images:
        main_src = img.get('src')
        if main_src:
            base_id = get_base_image_url(main_src)
            if base_id not in unique_images:
                unique_images[base_id] = main_src
            if img.get('srcset'):
                srcset = img['srcset'].split(',')
                for src in srcset:
                    url = src.split(' ')[0]
                    if '-1200-1200' in url:
                        unique_images[base_id] = url
    
    # Crear la carpeta para el product_identifier si no existe
    folder_path = os.path.join('images', str(product_identifier))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Obtener lista de imágenes existentes
    existing_images = get_existing_images(folder_path)
    
    # Descargar y guardar cada imagen única
    saved_paths = []
    new_downloads = 0
    skipped = 0
    
    for i, image_url in enumerate(unique_images.values()):
        file_name = f"{product_identifier}_{i+1}.jpg"
        
        # Verificar si la imagen ya existe
        if file_name in existing_images:
            image_path = os.path.join(folder_path, file_name)
            saved_paths.append(image_path)
            skipped += 1
            continue
            
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_path = os.path.join(folder_path, file_name)
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                saved_paths.append(image_path)
                new_downloads += 1
                print(f"Nueva imagen {i+1} guardada para ProductIdentifier {product_identifier}: {image_path}")
        except Exception as e:
            print(f"Error al descargar la imagen {i+1} para ProductIdentifier {product_identifier}: {e}")
    
    if new_downloads > 0:
        print(f"Se descargaron {new_downloads} nuevas imágenes para el producto {product_identifier}")
    if skipped > 0:
        print(f"Se omitieron {skipped} imágenes ya existentes para el producto {product_identifier}")
    
    return saved_paths

def process_product(url):
    _, soup = extract_json_ld(url)
    
    if not soup:
        print(f"No se pudo extraer datos de {url}")
        return
    
    product_identifier = extract_product_identifier(soup)
    if not product_identifier:
        print(f"No se encontró ProductIdentifier para {url}")
        return
    
    print(f"\nProcesando producto {product_identifier}...")
    image_paths = extract_all_product_images(soup, product_identifier)
    
    if not image_paths:
        print(f"No se encontraron imágenes para el producto {product_identifier}")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls if url.strip()]
    return urls

# Asegurarse de que existe el directorio principal de imágenes
if not os.path.exists('images'):
    os.makedirs('images')

# Archivo de texto con las URLs
file_path = 'miniso_product_links.txt'

# Procesar las URLs desde el archivo
product_urls = read_urls_from_file(file_path)

print(f"Iniciando procesamiento de {len(product_urls)} URLs...")

for i, url in enumerate(product_urls, 1):
    print(f"\nProcesando URL {i} de {len(product_urls)}")
    process_product(url)

print("\nProcesamiento completado!")
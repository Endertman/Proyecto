import requests
from bs4 import BeautifulSoup
import json
import os

# Función para extraer el JSON-LD desde la página web
def extract_json_ld(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Buscar el script que contiene el JSON-LD
    json_ld = soup.find('script', type='application/ld+json')
    
    if json_ld:
        return json.loads(json_ld.string), soup
    return None, soup

# Función para extraer el identificador del producto desde la etiqueta meta
def extract_product_identifier(soup):
    identifier_meta = soup.find('meta', property='product:retailer_item_id')
    
    if identifier_meta:
        return identifier_meta.get('content').strip()  # Extraer el valor del atributo content
    return None

# Función para descargar y guardar una imagen localmente
def download_and_save_image(image_url, sku):
    try:
        response = requests.get(image_url)
        file_name = f"{sku}.jpg"
        folder_path = 'images'  # Carpeta para guardar las imágenes
        
        # Crear la carpeta si no existe
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Guardar la imagen localmente
        image_path = os.path.join(folder_path, file_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        return image_path  # Devolver la ruta de la imagen local
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

# Función para actualizar un archivo JSON existente con el identificador de meta
def update_existing_product_file(sku, product_identifier):
    json_file = f"productos_{sku}.json"
    
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Actualizar el identificador del meta en el archivo JSON
        data['ProductIdentifier'] = product_identifier
        
        # Guardar los cambios en el archivo
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Producto {sku} actualizado con el identificador del meta.")
    else:
        print(f"No se encontró archivo existente para el SKU {sku}.")

# Función para procesar un producto y guardar los datos localmente
def process_product(url):
    product_data, soup = extract_json_ld(url)
    
    if not product_data:
        print(f"No se pudo extraer datos de {url}")
        return
    
    sku = product_data.get('sku')
    
    # Verificar si el archivo ya existe
    json_file = f"productos_{sku}.json"
    
    if os.path.exists(json_file):
        print(f"El archivo para el SKU {sku} ya existe, actualizando con el identificador del meta.")
        
        # Extraer el identificador del producto desde el meta tag
        product_identifier = extract_product_identifier(soup)
        
        # Actualizar solo el identificador en el archivo JSON existente
        update_existing_product_file(sku, product_identifier)
    
    else:
        # Procesar el producto completamente si no existe el archivo
        image_url = product_data.get('image')
        local_image_path = download_and_save_image(image_url, sku) if image_url else None
        
        # Extraer el identificador del producto desde el meta tag
        product_identifier = extract_product_identifier(soup)
        
        # Preparar los datos para guardar en un archivo JSON
        item = {
            'SKU': sku,
            'ProductIdentifier': product_identifier,  # El identificador extraído del meta tag
            'Name': product_data.get('name'),
            'Brand': product_data.get('brand', {}).get('name'),
            'Description': product_data.get('description'),
            'Category': product_data.get('category'),
            'MPN': product_data.get('mpn'),
            'ImagePath': local_image_path,
            'Price': product_data.get('offers', {}).get('lowPrice')
        }
        
        # Guardar los datos en un archivo JSON local
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)
        
        print(f"Producto {sku} procesado y guardado con éxito.")

# Leer las URLs de un archivo .txt
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    # Eliminar espacios o saltos de línea adicionales
    urls = [url.strip() for url in urls if url.strip()]
    return urls

# Archivo de texto con las URLs
file_path = 'miniso_product_links.txt'

# Procesar las URLs desde el archivo
product_urls = read_urls_from_file(file_path)

for url in product_urls:
    process_product(url)

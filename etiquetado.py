import os
import json

# Directorios de las imágenes y los JSON
image_dir = "images"
json_dir = "json"
csv_file = "labels.csv"

# Verificar que los directorios existan
if not os.path.exists(image_dir):
    raise Exception(f"El directorio de imágenes {image_dir} no existe.")
if not os.path.exists(json_dir):
    raise Exception(f"El directorio de archivos JSON {json_dir} no existe.")

# Crear el archivo CSV
with open(csv_file, "w", encoding="utf-8") as csv:
    csv.write("file,sku,name,price\n")  # Escribir encabezado del CSV
    
    # Recorrer las imágenes en el directorio de imágenes
    for image_file in os.listdir(image_dir):
        if image_file.endswith('.jpg') or image_file.endswith('.png'):
            # Obtener el SKU de la imagen (el número antes de la extensión)
            sku = os.path.splitext(image_file)[0]

            # Crear el nombre esperado del archivo JSON en base al SKU
            json_file = os.path.join(json_dir, f"productos_{sku}.json")

            # Imprimir las rutas para verificar que son correctas
            print(f"Procesando imagen: {image_file}")
            print(f"Buscando archivo JSON: {json_file}")

            # Verificar si el archivo JSON correspondiente existe
            if os.path.exists(json_file):
                try:
                    # Abrir y cargar el archivo JSON con codificación UTF-8
                    with open(json_file, encoding="utf-8") as f:
                        data = json.load(f)

                    # Obtener el ProductIdentifier del JSON
                    product_identifier = data.get("ProductIdentifier")
                    name = data.get("Name")
                    price = data.get("Price")
                    
                    # Verificar que el ProductIdentifier exista en el archivo JSON
                    if product_identifier:
                        # Escribir la imagen y el SKU en el archivo CSV
                        csv.write(f"{image_file},{product_identifier},{name},{price}\n")
                        print(f"Etiqueta creada para: {image_file} -> {product_identifier}")
                    else:
                        print(f"Advertencia: No se encontró 'ProductIdentifier' en {json_file}")
                except json.JSONDecodeError as e:
                    print(f"Error de JSON en {json_file}: {e}")
            else:
                print(f"Advertencia: No se encontró el archivo JSON para {image_file}")
        else:
            print(f"Advertencia: {image_file} no es un archivo de imagen válido (.jpg o .png)")

print(f"Archivo CSV '{csv_file}' generado correctamente.")
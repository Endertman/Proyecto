import boto3
import csv

# Inicializar cliente de Rekognition y S3
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# Nombre de la colección y del bucket
collection_id = "ProductCollection"
bucket_name = "miniso-products-imgs"

# Ruta al archivo CSV en tu máquina local
csv_file = "labels.csv"

# Indexar cada imagen en Rekognition
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        image_file = row['file']  # nombre del archivo de imagen
        product_identifier = row['sku']  # ProductIdentifier del CSV
        
        # Indexar la imagen en Rekognition
        response = rekognition.index_faces(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_file
                }
            },
            ExternalImageId=product_identifier,  # Asocia la imagen al SKU
            MaxFaces=1,
            QualityFilter="AUTO",
            DetectionAttributes=['ALL']
        )
        
        print(f"Indexada imagen {image_file} con SKU {product_identifier}")
import boto3

# Crear un cliente S3
s3 = boto3.client('s3')

# Listar los buckets
buckets = s3.list_buckets()

# Imprimir los nombres de los buckets
print("Buckets en S3:")
for bucket in buckets['Buckets']:
    print(bucket['Name'])
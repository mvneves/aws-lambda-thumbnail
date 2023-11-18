import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

# Cria um cliente S3
s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    # Abre a imagem, redimensiona (thumbnail) e salva no caminho especificado
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)

def lambda_handler(event, context):
    # Processa cada registro de evento do S3
    for record in event['Records']:
        # Obtém informações do bucket e da chave do objeto
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # Remove '/' do nome do arquivo e gera caminhos temporários
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)

        # Faz download do arquivo do S3 para o sistema de arquivos temporário
        s3_client.download_file(bucket, key, download_path)

        # Redimensiona a imagem e salva no caminho de upload temporário
        resize_image(download_path, upload_path)

        # Faz upload da imagem redimensionada para o S3 em um novo bucket
        s3_client.upload_file(upload_path, '{}-resized'.format(bucket), 'resized-{}'.format(key))

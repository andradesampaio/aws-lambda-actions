import json
import os
import boto3
from log import Log

s3 = boto3.client('s3')


def lambda_handler(event, context):
    logging = Log(event['headers'])
    logging.info(f"Lambda Python for the win!")

    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    print(f'Request = {record}')
    check_size(bucket, key, logging)

    return {
        'statusCode': 200,
        'idClient': os.environ['ID_CLIENT'],
        'body': json.dumps(event)
    }


def check_size(bucket, key, logging):
    logging.info(f'Verificando o tamanho do arquivo {key} no bucket {bucket}')
    objeto_s3 = s3.head_object(Bucket=bucket, Key=key)
    tamanho_arquivo_bytes = objeto_s3['ContentLength']

    tamanho_arquivo_mb = tamanho_arquivo_bytes / (1024 ** 2)

    if tamanho_arquivo_mb > 1:
        print("Objeto muito grande")
    else:
        print("Objeto dentro do tamanho")

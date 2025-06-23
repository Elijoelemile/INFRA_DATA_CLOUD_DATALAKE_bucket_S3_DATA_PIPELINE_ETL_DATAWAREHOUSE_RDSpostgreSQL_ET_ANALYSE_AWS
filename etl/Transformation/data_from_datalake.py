import os
from dotenv import load_dotenv
import boto3
import json
import pandas as pd

# Charger les variables du fichier .env
load_dotenv()

# Récupération des variables d'environnement
bucket_name = os.getenv('S3_BUCKET_NAME')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

key1 = 'job_data_api/jobs_20250622_023326.json'
key2 = 'jobs_data_scraping/jobs2025/06/23_000409.json'

# Connexion S3 (un seul client suffit)
s3 = boto3.client(
    's3',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Lecture et chargement des fichiers JSON
response1 = s3.get_object(Bucket=bucket_name, Key=key1)
data1 = json.loads(response1['Body'].read().decode('utf-8'))

response2 = s3.get_object(Bucket=bucket_name, Key=key2)
data2 = json.loads(response2['Body'].read().decode('utf-8'))

# Transformation en DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Aperçu
df1.head()
import sys
import os
import json
import boto3
from datetime import datetime

# Ajout du chemin vers le dossier racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from etl.Extraction.extractapi import JobAPIClient

# ÉTAPE 1 : Appel API
client = JobAPIClient("https://remotive.com/api/remote-jobs")
data_api = client.fetch_jobs()

# ÉTAPE 2 : Paramètres S3
BUCKET_NAME = "my-datalakeeli"
S3_KEY = f"job_data_api/jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"  # Exemple : job_data/jobs_20250620_143501.json

# ÉTAPE 3 : Upload vers S3
def upload_to_s3(data, bucket, key):
    try:
        s3 = boto3.client('s3')
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        s3.put_object(Body=json_data.encode("utf-8"), Bucket=bucket, Key=key)
        print(f" Données uploadées avec succès dans s3://{bucket}/{key}")
    except Exception as e:
        print(f" Erreur lors de l'upload vers S3 : {e}")

# ÉTAPE 4 : Exécution
if data_api:
    upload_to_s3(data_api, BUCKET_NAME, S3_KEY)
else:
    print("Aucune donnée extraite.")
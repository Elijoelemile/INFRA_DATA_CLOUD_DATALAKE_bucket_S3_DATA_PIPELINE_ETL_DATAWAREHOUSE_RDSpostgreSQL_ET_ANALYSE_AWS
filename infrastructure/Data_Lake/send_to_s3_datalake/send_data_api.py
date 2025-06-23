import os
import sys
import os
import json
import boto3
from dotenv import load_dotenv
from datetime import datetime

# ÉTAPE 1 : Charger le fichier .env depuis la racine du projet (2 niveaux au-dessus)
load_dotenv()

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")

# ÉTAPE 2 : Ajout du chemin vers le dossier racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from etl.Extraction.extractapi import JobAPIClient

# ÉTAPE 3 : Appel API
client = JobAPIClient("https://remotive.com/api/remote-jobs")
data_api = client.fetch_jobs()

# ÉTAPE 4 : Paramètres S3
BUCKET_NAME = "my-datalakeeli"
S3_KEY = f"job_data_api/jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"  # Exemple : job_data/jobs_20250620_143501.json

# ÉTAPE 5 : Upload vers S3
def upload_to_s3(data, bucket, key):
    try:
        s3 = boto3.client('s3')
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        s3.put_object(Body=json_data.encode("utf-8"), Bucket=bucket, Key=key)
        print(f" Données uploadées avec succès dans s3://{bucket}/{key}")
    except Exception as e:
        print(f" Erreur lors de l'upload vers S3 : {e}")

# ÉTAPE 6 : Exécution
if data_api:
    upload_to_s3(data_api, BUCKET_NAME, S3_KEY)
else:
    print("Aucune donnée extraite.")
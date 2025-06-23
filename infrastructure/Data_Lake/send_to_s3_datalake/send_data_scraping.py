import os
import sys
import time
import json
import boto3
#from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# ÉTAPE 1: Charger le fichier .env depuis la racine du projet (2 niveaux au-dessus)
dotenv_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path)

# ÉTAPE 2: Ajouter le chemin vers la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from etl.Extraction.extractscraping import ScrapingExtractor

# ÉTAPE 3: Clé API Mistral
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("La clé MISTRAL_API_KEY est introuvable. Vérifie ton fichier .env.")

# ÉTAPE 4: Paramètres S3
s3_bucket = os.getenv("S3_BUCKET_NAME")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# ÉTAPE 5: Générer un horodatage pour le nom du fichier
timestamp = datetime.now().strftime("%Y/%m/%d_%H%M%S")
s3_key = f"jobs_data_scraping/jobs{timestamp}.json"

# ÉTAPE 6: Configuration du scraping
BASE_URL = "https://www.welcometothejungle.com/fr/pages/emploi-business?page="  # Ici, tu dois remplacer l'URL
NB_PAGES = 100
results = []

# ÉTAPE 7: Scraping
for page in range(1, NB_PAGES + 1):
    url = f"{BASE_URL}{page}"
    print(f"Scraping {url}...")
    try:
        extractor = ScrapingExtractor(url, mistral_api_key)
        job_data = extractor.fetch()
        results.append(job_data)
        time.sleep(2)
    except Exception as e:
        print(f"Erreur sur la page {page} : {e}")

# ÉTAPE 8: Convertir les résultats en JSON
json_data = json.dumps(results, ensure_ascii=False, indent=4)

# ÉTAPE 9: Envoi vers S3
if all([s3_bucket, aws_access_key, aws_secret_key]):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    s3_client.put_object(
        Bucket=s3_bucket,
        Key=s3_key,
        Body=json_data.encode("utf-8"),
        ContentType="application/json"
    )

    print(f"Upload terminé sur s3://{s3_bucket}/{s3_key}")
else:
    raise ValueError("Informations S3 manquantes dans le fichier .env")
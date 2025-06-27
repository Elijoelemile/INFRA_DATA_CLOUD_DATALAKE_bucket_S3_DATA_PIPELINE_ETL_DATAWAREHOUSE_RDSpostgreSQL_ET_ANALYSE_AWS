import os
import json
import pandas as pd
import unicodedata
from typing import Callable, List, Dict, Union
import boto3
from dotenv import load_dotenv
import io  # pour le buffer mémoire

class DataTransformer:
    def __init__(self):
        self.dataframes = []

    def load_from_s3(self, keys: List[str]):
        """
        Charge plusieurs fichiers JSON depuis S3 et les stocke sous forme de DataFrames.
        """
        load_dotenv()

        bucket_name = os.getenv('S3_BUCKET_NAME')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = os.getenv('REGION_NAME')

        s3 = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        for key in keys:
            response = s3.get_object(Bucket=bucket_name, Key=key)
            raw_data = json.loads(response['Body'].read().decode('utf-8'))
            df = pd.DataFrame(raw_data)
            self.dataframes.append(df)

    def merge_data(self, how: str = 'concat'):
        """
        Fusionne les DataFrames chargés depuis S3.
        - how='concat' : concaténation simple
        - how='inner' ou 'outer' : jointures par colonnes communes
        """
        if not self.dataframes:
            raise ValueError("Aucune donnée chargée.")
        if how == 'concat':
            self.data = pd.concat(self.dataframes, ignore_index=True)
        else:
            from functools import reduce
            self.data = reduce(lambda left, right: pd.merge(left, right, how=how), self.dataframes)

    def normalize_text(self, columns: List[str]):
        """
        Nettoie les colonnes texte tout en conservant les signes utiles (UTC offsets, etc.).
        Supprime les accents, met en minuscules, normalise les espaces.
        """
        allowed_pattern = r'[^a-z0-9\s\+\-\:\(\)]'  # Autorise + - : ( )
        for col in columns:
            self.data[col] = (
                self.data[col]
                .astype(str)
                .str.lower()
                .apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
                .str.replace(allowed_pattern, ' ', regex=True)
                .str.replace(r'\s+', ' ', regex=True)
                .str.strip()
            )

    def fill_missing(self, strategy: str = 'mode', fill_value=None):
        """
        Remplit les valeurs manquantes selon la stratégie choisie.
        """
        for col in self.data.columns:
            if self.data[col].isnull().any():
                if strategy == 'mode':
                    self.data[col].fillna(self.data[col].mode()[0], inplace=True)
                elif strategy == 'constant':
                    self.data[col].fillna(fill_value, inplace=True)

    def convert_types(self, conversions: Dict[str, str]):
        """
        Convertit les colonnes selon les types définis.
        """
        for col, dtype in conversions.items():
            try:
                self.data[col] = self.data[col].astype(dtype)
            except Exception as e:
                print(f"Erreur de conversion pour '{col}' : {e}")

    def export_to_s3_csv(self, output_key: str):
        """
        Exporte le DataFrame transformé en fichier CSV dans S3.
        
        :param output_key: chemin + nom du fichier dans le bucket S3 (ex: 'exports/cleaned_jobs.csv')
        """
        load_dotenv()

        bucket_name = os.getenv('S3_BUCKET_NAME')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = os.getenv('REGION_NAME')

        # Buffer mémoire pour écrire le CSV
        csv_buffer = io.StringIO()
        self.data.to_csv(csv_buffer, index=False)

        # Client S3
        s3 = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Envoi dans S3
        s3.put_object(Bucket=bucket_name, Key=output_key, Body=csv_buffer.getvalue())
        print(f"Données exportées vers s3://{bucket_name}/{output_key}")

    def get_data(self):
        """Retourne le DataFrame final transformé."""
        return self.data

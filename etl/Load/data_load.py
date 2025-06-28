import boto3
import os
import psycopg2
import csv
from io import StringIO
from dotenv import load_dotenv

class Loading:
    def __init__(self):
        load_dotenv()

        # Connexion S3
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = os.getenv("REGION_NAME")

        self.s3 = boto3.client(
            's3',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        # Connexion PostgreSQL
        self.pg_host = os.getenv("PG_HOST")
        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")
        self.pg_db = os.getenv("PG_DB")
        self.pg_port = os.getenv("PG_PORT", 5432)

    def load_csv_as_string(self, s3_key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
        return response['Body'].read().decode('utf-8')

    def insert_csv_into_postgres(self, csv_string: str, table_name: str):
        conn = psycopg2.connect(
            host=self.pg_host,
            user=self.pg_user,
            password=self.pg_password,
            dbname=self.pg_db,
            port=self.pg_port
        )
        cur = conn.cursor()

        reader = csv.reader(StringIO(csv_string))
        headers = next(reader)
        columns = ', '.join([f'"{col}"' for col in headers])

        # Créer la table si elle n'existe pas
        columns_definition = ', '.join([f'"{col}" TEXT' for col in headers])
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});')

        # Insérer les données
        for row in reader:
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders});'
            cur.execute(insert_query, row)

        conn.commit()
        cur.close()
        conn.close()
        print(f"Données insérées dans la table {table_name} de la base {self.pg_db}.")
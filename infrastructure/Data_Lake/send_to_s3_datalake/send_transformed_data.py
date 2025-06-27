import sys
import os
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
print(f"Ajout du dossier racine : {project_root}")
sys.path.append(project_root)

from etl.Transformation.data_transformation import DataTransformer

def send_transformed_data():
    transformer = DataTransformer()

    s3_keys = [
        'job_data_api/jobs_20250622_023326.json',
        'jobs_data_scraping/jobs2025/06/23_000409.json'
    ]

    transformer.load_from_s3(s3_keys)
    transformer.merge_data()
    transformer.fill_missing(strategy='mode')

    cols_to_clean = ['Location']
    existing_cols = [col for col in cols_to_clean if col in transformer.data.columns]
    transformer.normalize_text(existing_cols)

    transformer.export_to_s3_csv(output_key='data_cleaned_20250627.csv')

    print("Script terminé avec succès.")

if __name__ == '__main__':
    send_transformed_data()

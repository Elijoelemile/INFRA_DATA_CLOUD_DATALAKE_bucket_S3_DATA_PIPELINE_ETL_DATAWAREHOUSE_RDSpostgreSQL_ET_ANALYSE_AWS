import os
import sys

# Ajouter le chemin racine du projet pour permettre les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from etl.Load.data_load import Loading  # Import de la classe Loading

if __name__ == "__main__":
    loader = Loading()
    csv_string = loader.load_csv_as_string('data_cleaned_20250627.csv')
    loader.insert_csv_into_postgres(csv_string, table_name='jobs_data')
    
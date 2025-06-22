import requests
import re

class JobAPIClient:
    def __init__(self, api_url, max_description_length=500):
        self.api_url = api_url
        self.max_description_length = max_description_length

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'&[a-z]+;', ' ', text)
        text = re.sub(r'[^ -~]', '', text)
        text = text.strip()
        if len(text) > self.max_description_length:
            text = text[:self.max_description_length].rstrip() + "..."
        return text

    def find_jobs_list(self, data):
        """
        Recherche récursive dans le JSON la première liste de dicts
        ressemblant à une liste d'offres d'emploi.
        """
        if isinstance(data, list):
            if all(isinstance(item, dict) for item in data) and len(data) > 0:
                return data
            else:
                # Pas une liste d'objets, chercher dans éléments
                for item in data:
                    res = self.find_jobs_list(item)
                    if res:
                        return res
        elif isinstance(data, dict):
            for key, val in data.items():
                res = self.find_jobs_list(val)
                if res:
                    return res
        return None

    def infer_field_mapping(self, job_obj):
        """
        Déduire un mapping clé interne <-> clé JSON à partir des champs disponibles
        """
        keys = set(job_obj.keys())
        mapping = {}

        # Clés candidates classiques
        if 'title' in keys:
            mapping["Job_Title"] = "title"
        elif 'position' in keys:
            mapping["Job_Title"] = "position"
        elif 'job_title' in keys:
            mapping["Job_Title"] = "job_title"

        if 'company_name' in keys:
            mapping["Company"] = "company_name"
        elif 'company' in keys:
            mapping["Company"] = "company"

        if 'location' in keys:
            mapping["Location"] = "location"
        elif 'candidate_required_location' in keys:
            mapping["Location"] = "candidate_required_location"

        # Description avec variantes fréquentes
        if 'description' in keys:
            mapping["Description"] = "description"
        elif 'job_description' in keys:
            mapping["Description"] = "job_description"
        elif 'contents' in keys:
            mapping["Description"] = "contents"

        return mapping

    def fetch_jobs(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Erreur lors de la requête API: {e}")
            return []

        jobs_list = self.find_jobs_list(data)
        if not jobs_list:
            print("Aucune liste d'offres d'emploi trouvée dans la réponse API.")
            return []

        # Inférence automatique du mapping
        field_mapping = self.infer_field_mapping(jobs_list[0])
        if not field_mapping:
            print("Impossible d'inférer un mapping de champs. Structure JSON inconnue.")
            return []

        results = []
        for job in jobs_list:
            item = {}
            for key, api_key in field_mapping.items():
                val = job.get(api_key, "")
                if key == "Description":
                    val = self.clean_text(val)
                item[key] = val
            results.append(item)

        return results
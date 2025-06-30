# 📊 Projet #2 – Mise en Place et Optimisation d'une Infrastructure Data sur le Cloud

## 👤 Auteur
**Nom Prénom** – Promo AIA01  
**Année 1 - L'École Multimédia**

---

## 🧭 Objectif du projet

Ce projet consiste à concevoir une infrastructure Data moderne en combinant :
- un **pipeline ETL local** pour collecter et transformer des données issues de **scraping** et **APIs**,
- un **Data Lake sur AWS S3** pour stocker les données brutes,
- un **Data Warehouse sur RDS (PostgreSQL)** pour les données nettoyées,
- et des **visualisations interactives** via Plotly et/ou Bokeh.

---

## 🗂️ Arborescence du projet

```
├── etl/                # DonScripts de scraping, API, traitement, upload vers AWS
├── infrastructure/     # Requêtage et envoi de données sur Data Lake et Data warehouse(AWS)
├── Livrable/           # Ensemble du travail effectué
├── notebooks/          # Analyses exploratoires (Jupyter)
├── venv/               # Environnement virtuel
├── README.md           # Ce fichier
├── requirements.txt    # Dépendances Python
```

---

## 🔧 Pipeline ETL (local)

### Étapes :
1. **Scraping** d'offres d'emploi via `etl/extractsraping.py`
2. **Requête API** (Remotive) via `etl/extractapi.py`
3. **Nettoyage et transformation** des données (Pandas)
4. **Enregistrement** :
   - Données brutes ➜ `S3`
   - Données transformées ➜ `RDS PostgreSQL`

### Exécution :
```bash
python etl/main_etl.py
```

---

## ☁️ Infrastructure Cloud (AWS)

### Services utilisés :
- **S3** : stockage brut (Data Lake)
- **RDS PostgreSQL** : stockage structuré (Data Warehouse)
- **IAM** : sécurité des accès (via rôles et policies)
- **(Sans Glue ni Lambda)** – Pipeline entièrement local

👉 Voir le dossier [`infrastructure/`](infrastructure/) pour :
- Architecture Data Clouud(AWS) (`diagramme_infra.pdf`)
- scripts d'envoie de données sur S3 et RDS

---

## 📊 Analyse

- Librairies utilisées : `Plotly`, `Pandas`
- Analyses réalisées :
  - Top 10 des jobs les plus demandés
  - Top 10 des jobs moyennement demandés
  - Top 10 des jobs les moins demandés
  - Top 5 des pays avec le plus d'offres

---

## 💾 Accès aux données

- Données brutes accessibles dans S3 (`my-datalakeeli`)
- Données nettoyées dans la base PostgreSQL (`data_cleaned_20250627.csv`)
- Notebooks disponibles dans [`notebook/`](notebook/)

---

## 🔐 Sécurité & bonnes pratiques

- S3 avec **chiffrement activé**
- RDS accessible uniquement depuis une IP spécifique
- IAM configuré pour limiter les droits
- CloudTrail activé pour audit
- GitHub utilisé pour le versionnage (commits fréquents)

---

## 📎 Dépendances

Liste dans `requirements.txt`, ex :
```
requests
pandas
sqlalchemy
psycopg2
plotly
bokeh
python-dotenv
```

---

## 📁 Livraison

Le projet est livré sous forme d’une archive :
```
ESSONO-NZOGHE Eli-joël-emile_projet2_AIA01.zip
```
Incluant :
- tous les scripts, notebooks, dashboards
- le dépôt complet GitHub
- une documentation complète (`infrastructure/`)
- une présentation PowerPoint du projet

---

## 📌 Auteur & contact

**Nom Prénom**  
Promo AIA01  
Email : nzoghessono@gmail.com  

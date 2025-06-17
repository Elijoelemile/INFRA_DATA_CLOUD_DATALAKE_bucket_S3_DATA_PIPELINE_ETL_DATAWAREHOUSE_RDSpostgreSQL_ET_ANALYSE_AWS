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
├── data/               # Données locales (brutes et transformées)
├── etl/                # Scripts de scraping, API, traitement, upload vers AWS
├── dashboard/          # Visualisations et dashboards interactifs
├── notebooks/          # Analyses exploratoires (Jupyter)
├── infrastructure/     # Configs AWS, scripts CLI, diagrammes, IAM
├── README.md           # Ce fichier
├── requirements.txt    # Dépendances Python
```

---

## 🔧 Pipeline ETL (local)

### Étapes :
1. **Scraping** d'offres d'emploi via `etl/scraper_wttj.py`
2. **Requête API** (Adzuna ou Pôle Emploi) via `etl/api_adzuna.py`
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
- **CloudTrail** : journalisation des accès
- **(Sans Glue ni Lambda)** – Pipeline entièrement local

👉 Voir le dossier [`infrastructure/`](infrastructure/) pour :
- diagramme d’architecture (`diagramme_infra.png`)
- scripts CLI de création S3 et RDS
- configurations IAM JSON
- captures écran (CloudTrail)

---

## 📊 Visualisation & Analyse

- Dashboard interactif : `dashboard/jobs_dashboard.py`
- Librairies utilisées : `Plotly`, `Bokeh`, `Seaborn`, `Pandas`
- Analyses réalisées :
  - Répartition géographique des offres
  - Technologies les plus demandées
  - Évolution temporelle des publications

---

## 💾 Accès aux données

- Données brutes accessibles dans S3 (`data-lake-emploi`)
- Données nettoyées dans la base PostgreSQL (`jobs_analytics_db`)
- Notebooks disponibles dans [`notebooks/`](notebooks/)

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
prenom_nom_projet2_AIA01.zip
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

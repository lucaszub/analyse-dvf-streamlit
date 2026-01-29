# DVF Analytics

Dashboard Streamlit pour analyser les données DVF (Demandes de Valeurs Foncières) - prix immobiliers en France.

## Fonctionnalités

- Carte choroplèthe interactive des prix médians par département
- Filtrage par type de bien (Tous / Appartements / Maisons)
- KPIs France avec prix médian et nombre de ventes
- Tableau récapitulatif par type de bien
- Graphique d'évolution des prix sur 5 ans

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration

Créer un fichier `config.py` à la racine du projet :

```python
SNOWFLAKE_URL = "snowflake://USER:PASSWORD@ACCOUNT/VALFONC_ANALYTICS_DBT/BRONZE?warehouse=WH_DBT_VALFONC"
```

## Lancement

```bash
streamlit run app.py
```

L'application sera accessible sur http://localhost:8501

## Structure du projet

```
├── app.py                 # Application Streamlit principale
├── config.py              # Configuration Snowflake (gitignored)
├── requirements.txt       # Dépendances Python
└── db/
    ├── base.py            # Base SQLAlchemy
    ├── crud.py            # Fonctions d'accès aux données
    └── table/             # Modèles ORM
        ├── GOLDKPIFRANCE.py
        └── GOLD_KPI_DEPARTEMENT.py
```

## Source des données

Les données proviennent des tables Snowflake dans le schéma `VALFONC_ANALYTICS_DBT.GOLD` :
- `GOLD_KPI_FRANCE` : KPIs nationaux par année
- `GOLD_KPI_DEPARTEMENT` : KPIs par département et par année

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.table.GOLDKPIFRANCE import GOLDKPIFRANCE
from db.table.GOLD_KPI_DEPARTEMENT import GOLD_KPI_DEPARTEMENT
from config import SNOWFLAKE_URL

engine = create_engine(SNOWFLAKE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_gold_kpi_france() -> pd.DataFrame:
    """Retourne le DataFrame France"""
    with SessionLocal() as db:
        kpis = db.query(GOLDKPIFRANCE).all()
        data = [
            {
                "annee": row.annee,
                "prix_median_m2": row.prix_median_m2,
                "nb_ventes": row.nb_ventes,
                "prix_median_appartement": row.prix_median_appartement,
                "nb_ventes_appartement": row.nb_ventes_appartement,
                "prix_median_maison": row.prix_median_maison,
                "nb_ventes_maison": row.nb_ventes_maison
            }
            for row in kpis
        ]
        return pd.DataFrame(data)


def get_dep() -> pd.DataFrame:
    """Retourne le DataFrame Département"""
    with SessionLocal() as db:
        kpis_dep = db.query(GOLD_KPI_DEPARTEMENT).all()
        data_dep = [
            {
                "annee": row.annee,
                "prix_median_m2": row.prix_median_m2,
                "nb_ventes": row.nb_ventes,
                "prix_median_appartement": row.prix_median_appartement,
                "nb_ventes_appartement": row.nb_ventes_appartement,
                "prix_median_maison": row.prix_median_maison,
                "nb_ventes_maison": row.nb_ventes_maison,
                "latitude_centroid": row.latitude_centroid,
                "longitude_centroid": row.longitude_centroid
            }
            for row in kpis_dep
        ]
        return pd.DataFrame(data_dep)

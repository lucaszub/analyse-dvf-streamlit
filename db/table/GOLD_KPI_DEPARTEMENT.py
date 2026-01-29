from sqlalchemy import Column, Integer, Numeric, Float, String
from db.base import Base  # <-- centralisé

class GOLD_KPI_DEPARTEMENT(Base):
    __tablename__ = "GOLD_KPI_DEPARTEMENT"
    __table_args__ = {
        "schema": "GOLD",
        "info": {"database": "VALFONC_ANALYTICS_DBT"},
    }

    code_departement = Column("CODE_DEPARTEMENT", String, primary_key=True)
    annee = Column("ANNEE", Integer, primary_key=True)
    nom_departement = Column("NOM_DEPARTEMENT", String)

    prix_median_m2 = Column("PRIX_MEDIAN_M2", Numeric(38, 9))
    nb_ventes = Column("NB_VENTES", Integer)

    prix_median_appartement = Column("PRIX_MEDIAN_APPARTEMENT", Numeric(38, 9))
    nb_ventes_appartement = Column("NB_VENTES_APPARTEMENT", Integer)

    prix_median_maison = Column("PRIX_MEDIAN_MAISON", Numeric(38, 9))
    nb_ventes_maison = Column("NB_VENTES_MAISON", Integer)

    latitude_centroid = Column("LATITUDE_CENTROID", Float)
    longitude_centroid = Column("LONGITUDE_CENTROID", Float)

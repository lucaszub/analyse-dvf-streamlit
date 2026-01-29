from sqlalchemy import Column, Numeric, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import PrimaryKeyConstraint

Base = declarative_base()

class GoldKpiDepartement(Base):
    __tablename__ = "GOLD_KPI_DEPARTEMENT"
    __table_args__ = (
        PrimaryKeyConstraint("CODE_DEPARTEMENT", "ANNEE"),
        {"schema": "GOLD", "info": {"database": "VALFONC_ANALYTICS_DBT"}}
    )

    code_departement = Column("CODE_DEPARTEMENT", String(16777216))
    nom_departement = Column("NOM_DEPARTEMENT", String(16777216))
    annee = Column("ANNEE", Integer)
    prix_median_m2 = Column("PRIX_MEDIAN_M2", Numeric(38, 9))
    nb_ventes = Column("NB_VENTES", Integer)
    prix_median_appartement = Column("PRIX_MEDIAN_APPARTEMENT", Numeric(38, 9))
    nb_ventes_appartement = Column("NB_VENTES_APPARTEMENT", Integer)
    prix_median_maison = Column("PRIX_MEDIAN_MAISON", Numeric(38, 9))
    nb_ventes_maison = Column("NB_VENTES_MAISON", Integer)
    latitude_centroid = Column("LATITUDE_CENTROID", Float)
    longitude_centroid = Column("LONGITUDE_CENTROID", Float)

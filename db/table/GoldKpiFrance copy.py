from sqlalchemy import Column, Numeric, Integer
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()

class GOLDKPIFRANCE(base):
    __tablename__ = "GOLD_KPI_FRANCE"
    __table_args__ = {"schema": "GOLD", "info":{"database":"VALFONC_ANALYTICS_DBT"}}
    
    annee = Column("ANNEE", Integer, primary_key=True)  # <- obligatoire
    prix_median_m2 = Column("PRIX_MEDIAN_M2", Numeric(38, 9))
    nb_ventes = Column("NB_VENTES", Integer)
    prix_median_appartement = Column("PRIX_MEDIAN_APPARTEMENT", Numeric(38, 9))
    nb_ventes_appartement = Column("NB_VENTES_APPARTEMENT", Integer)
    prix_median_maison = Column("PRIX_MEDIAN_MAISON", Numeric(38, 9))
    nb_ventes_maison = Column("NB_VENTES_MAISON", Integer)
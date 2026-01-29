import streamlit as st
from db.crud import get_dep

# import plotly.express as px

df_dep = get_dep()

# Convert Decimal -> float
for col in ["prix_median_m2", "prix_median_appartement", "prix_median_maison"]:
    df_dep[col] = df_dep[col].astype(float)

df_dep["size_normalized"] = df_dep["prix_median_m2"].astype(float) / 100

st.map(
    df_dep,
    latitude="latitude_centroid",
    longitude="longitude_centroid",
    size="size_normalized",  # maintenant float
)

import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from db.crud import get_dep, get_gold_kpi_france

st.set_page_config(page_title="DVF Analytics", layout="wide")

st.title("DVF Analytics - Prix immobilier en France")

# Chargement des données
@st.cache_data
def load_data():
    df_dep = get_dep()
    df_france = get_gold_kpi_france()
    return df_dep, df_france

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
    response = requests.get(url)
    return response.json()

df_dep, df_france = load_data()
geojson = load_geojson()

# Conversion des types Decimal -> float
for col in ["prix_median_m2", "prix_median_appartement", "prix_median_maison"]:
    if col in df_dep.columns:
        df_dep[col] = df_dep[col].astype(float)
    if col in df_france.columns:
        df_france[col] = df_france[col].astype(float)

# Sidebar : Message de bienvenue
with st.sidebar:
    st.markdown("### Bonjour !")
    st.markdown("**Bienvenue**")
    st.markdown(
        "Suivez l'évolution des prix de l'immobilier et trouvez le prix des ventes "
        "immobilières sur les 5 dernières années."
    )

# Agrégation par département (toutes années)
df_dep_agg = df_dep.groupby("code_departement").agg({
    "nom_departement": "first",
    "prix_median_m2": "mean",
    "prix_median_appartement": "mean",
    "prix_median_maison": "mean",
    "nb_ventes": "sum",
    "nb_ventes_appartement": "sum",
    "nb_ventes_maison": "sum"
}).reset_index()

# Formater le code département pour matcher le GeoJSON (ex: "1" -> "01")
df_dep_agg["code_departement"] = df_dep_agg["code_departement"].astype(str).str.zfill(2)

# Palette de couleurs : Vert (pas cher) → Rouge (cher)
color_palette = {
    "1 - Très abordable": "#1a9641",  # Vert foncé
    "2 - Abordable": "#a6d96a",        # Vert clair
    "3 - Modéré": "#ffffbf",           # Jaune pâle
    "4 - Élevé": "#fdae61",            # Orange
    "5 - Très élevé": "#d7191c"        # Rouge foncé
}

# Titre et filtre sur la même ligne
col_titre, col_vide, col_filtre = st.columns([3, 1, 1])
with col_titre:
    st.markdown("### Prix médian par département")
with col_filtre:
    type_bien = st.selectbox(
        "Type de bien",
        options=["Tous", "Appartements", "Maisons"],
        index=0
    )

# Sélection de la colonne de prix selon le filtre
if type_bien == "Appartements":
    prix_col = "prix_median_appartement"
    nb_col = "nb_ventes_appartement"
    prix_col_france = "prix_median_appartement"
    nb_col_france = "nb_ventes_appartement"
elif type_bien == "Maisons":
    prix_col = "prix_median_maison"
    nb_col = "nb_ventes_maison"
    prix_col_france = "prix_median_maison"
    nb_col_france = "nb_ventes_maison"
else:
    prix_col = "prix_median_m2"
    nb_col = "nb_ventes"
    prix_col_france = "prix_median_m2"
    nb_col_france = "nb_ventes"

# KPI France selon le filtre
prix_median_france = df_france[prix_col_france].mean()
nb_ventes_france = df_france[nb_col_france].sum()

# Agrégation des données France pour le tableau
total_ventes_appt = df_france["nb_ventes_appartement"].sum()
total_ventes_maison = df_france["nb_ventes_maison"].sum()
prix_median_appt = df_france["prix_median_appartement"].mean()
prix_median_maison = df_france["prix_median_maison"].mean()

# Création du tableau récapitulatif
df_recap = pd.DataFrame({
    "": ["Ventes", "Prix médian m²"],
    "Appt.": [
        f"{total_ventes_appt:,.0f}".replace(",", " "),
        f"{prix_median_appt:,.0f} €".replace(",", " ")
    ],
    "Maisons": [
        f"{total_ventes_maison:,.0f}".replace(",", " "),
        f"{prix_median_maison:,.0f} €".replace(",", " ")
    ],
    "Locaux": [
        "—",
        "—"
    ]
})

# Sidebar : KPIs filtrés + Tableau récapitulatif
with st.sidebar:
    st.markdown("---")
    st.markdown(f"### France ({type_bien})")
    st.metric("Prix médian au m²", f"{prix_median_france:,.0f} €/m²".replace(",", " "))
    st.metric("Nombre de ventes", f"{nb_ventes_france:,.0f}".replace(",", " "))
    st.markdown("---")
    st.markdown("### Récapitulatif par type de bien")
    st.table(df_recap.set_index(""))

# Calcul des quintiles (5 niveaux) selon le type sélectionné
df_dep_agg["quintile"] = pd.qcut(
    df_dep_agg[prix_col],
    q=5,
    labels=["1 - Très abordable", "2 - Abordable", "3 - Modéré", "4 - Élevé", "5 - Très élevé"]
)

# Préparer les données pour le hover
df_dep_agg["prix_affiche"] = df_dep_agg[prix_col]
df_dep_agg["nb_ventes_affiche"] = df_dep_agg[nb_col]

fig = px.choropleth_mapbox(
    df_dep_agg,
    geojson=geojson,
    locations="code_departement",
    featureidkey="properties.code",
    color="quintile",
    color_discrete_map=color_palette,
    category_orders={"quintile": ["1 - Très abordable", "2 - Abordable", "3 - Modéré", "4 - Élevé", "5 - Très élevé"]},
    mapbox_style="carto-positron",
    zoom=4.5,
    center={"lat": 46.6, "lon": 2.5},
    opacity=0.7,
    hover_name="nom_departement",
    hover_data={
        "code_departement": False,
        "prix_affiche": ":.0f",
        "nb_ventes_affiche": ":,.0f",
        "quintile": False
    },
    labels={
        "prix_affiche": "Prix médian (€/m²)",
        "nb_ventes_affiche": "Nombre de ventes",
        "quintile": "Niveau de prix"
    }
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    legend_title_text="Niveau de prix"
)

st.plotly_chart(fig, use_container_width=True)

# Graphique d'évolution du prix médian
st.markdown("### Évolution du prix médian au m² (France)")

df_france_sorted = df_france.sort_values("annee")

fig_evolution = px.line(
    df_france_sorted,
    x="annee",
    y="prix_median_m2",
    markers=True,
    labels={
        "annee": "Année",
        "prix_median_m2": "Prix médian (€/m²)"
    }
)

fig_evolution.update_layout(
    xaxis=dict(tickmode="linear", dtick=1),
    height=400,
    showlegend=False
)

fig_evolution.update_traces(line_color="#1f77b4", name="Tous biens")

st.plotly_chart(fig_evolution, use_container_width=True)

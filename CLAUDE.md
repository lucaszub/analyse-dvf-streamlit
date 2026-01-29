# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DVF Analytics is a Streamlit dashboard for analyzing French real estate transaction data (DVF - Demandes de Valeurs Foncières). It displays median prices per square meter and sales volumes at both national and departmental levels, with an interactive choropleth map visualization.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Architecture

**Data Flow:** Snowflake (GOLD schema) → SQLAlchemy ORM → Pandas DataFrames → Streamlit/Plotly

**Key Components:**
- `app.py` - Main Streamlit application with map visualization using Plotly choropleth
- `db/crud.py` - Data access layer with `get_gold_kpi_france()` and `get_dep()` functions
- `db/table/` - SQLAlchemy ORM models mapping to Snowflake tables in `VALFONC_ANALYTICS_DBT.GOLD` schema
- `config.py` - Snowflake connection URL (gitignored, contains credentials)

**Database Tables:**
- `GOLD_KPI_FRANCE` - National-level KPIs by year
- `GOLD_KPI_DEPARTEMENT` - Department-level KPIs by year with geographic centroids

## Configuration

Create `config.py` with:
```python
SNOWFLAKE_URL = "snowflake://USER:PASSWORD@ACCOUNT/VALFONC_ANALYTICS_DBT/BRONZE?warehouse=WH_DBT_VALFONC"
```

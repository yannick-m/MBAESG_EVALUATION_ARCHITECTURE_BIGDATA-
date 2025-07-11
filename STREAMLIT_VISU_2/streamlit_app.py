import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

# Fonction pour exécuter la requête SQL
def run_query(query):
    conn = snowflake.connector.connect(
        user="MARISKA23",
        password="Daniel123@?*",
        account="VIB22035",
        warehouse="LINKEDIN_WH",
        database="LINKEDIN",
        schema="PUBLIC"
    )
    cs = conn.cursor()
    try:
        cs.execute(query)
        df = pd.DataFrame(cs.fetchall(), columns=[col[0] for col in cs.description])
    finally:
        cs.close()
        conn.close()
    return df

# Configuration de la page
st.set_page_config(
    page_title="Top 10 postes les mieux rémunérés",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("💼 Top 10 des postes les mieux rémunérés par industrie")

# Requête SQL
query = """
SELECT 
    ji.industry_id AS industrie,
    jp.title AS titre_poste,
    MAX(jp.max_salary) AS salaire_max
FROM job_postings_clean jp
JOIN job_industries_csv ji ON jp.job_id = ji.job_id
WHERE jp.max_salary IS NOT NULL
GROUP BY ji.industry_id, jp.title
ORDER BY salaire_max DESC
LIMIT 10;
"""

# Exécution de la requête
df = run_query(query)

# Renommer les colonnes pour plus de clarté
df.columns = ["industrie", "titre_poste", "salaire_max"]

# Vérification si dataframe vide
if df.empty:
    st.warning("⚠️ Aucune donnée à afficher.")
else:
    # Affichage tableau
    st.subheader("Données des postes")
    st.dataframe(df, use_container_width=True)

    # Création du graphique Altair
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=30)
        .encode(
            y=alt.Y('titre_poste:N', sort='-x', title='Titre du poste', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            x=alt.X('salaire_max:Q', title='Salaire maximum', axis=alt.Axis(format=',d', labelFontSize=12, titleFontSize=14)),
            color=alt.Color('industrie:N', legend=alt.Legend(title="Industrie"), scale=alt.Scale(scheme='category10')),
            tooltip=[
                alt.Tooltip('titre_poste:N', title='Poste'),
                alt.Tooltip('industrie:N', title='Industrie'),
                alt.Tooltip('salaire_max:Q', title='Salaire max', format=',d')
            ]
        )
        .properties(
            width=900,
            height=500,
            title="Top 10 des postes avec les salaires maximums par industrie"
        )
        .configure_title(fontSize=20, anchor='start', color='darkblue')
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_legend(labelFontSize=12, titleFontSize=14)
        .configure_view(strokeWidth=0)
    )

    st.altair_chart(chart, use_container_width=True)
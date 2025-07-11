import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

# Fonction d'exécution SQL
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

# Titre de l’application
st.title("📊 Répartition des offres d'emploi par secteur d'activité")

# Requête SQL
query = """
SELECT 
    i.industry_name AS secteur_activite,
    COUNT(DISTINCT jp.job_id) AS nombre_offres
FROM job_postings_clean jp
JOIN job_industries_csv ji ON jp.job_id = ji.job_id
JOIN industries_csv i ON ji.industry_id = i.industry_id
GROUP BY i.industry_name
ORDER BY nombre_offres DESC;
"""

# Exécution
df = run_query(query)

# Vérification et affichage
if df.empty:
    st.warning("⚠️ Aucune donnée disponible pour cette analyse.")
else:
    # Harmoniser les noms de colonnes en minuscules
    df.columns = [col.lower() for col in df.columns]

    # Conversion des types
    df['secteur_activite'] = df['secteur_activite'].astype(str)
    df['nombre_offres'] = df['nombre_offres'].astype(int)

    # Affichage du tableau avec un titre
    st.subheader("Données des offres par secteur")
    st.dataframe(df.sort_values(by='nombre_offres', ascending=False), use_container_width=True)

    # Construction du graphique Altair
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            y=alt.Y('secteur_activite:N', sort='-x', title="Secteur d'activité"),
            x=alt.X('nombre_offres:Q', title="Nombre d'offres", axis=alt.Axis(format=",d")),
            tooltip=[
                alt.Tooltip('secteur_activite:N', title="Secteur d'activité"),
                alt.Tooltip('nombre_offres:Q', title="Nombre d'offres", format=",d"),
            ],
            color=alt.Color('secteur_activite:N', legend=None, scale=alt.Scale(scheme='category20'))
        )
        .properties(
            width=800,
            height=600,
            title="Répartition des offres d'emploi par secteur d'activité"
        )
        .configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        .configure_title(
            fontSize=20,
            anchor='start',
            color='darkblue'
        )
        .configure_view(
            strokeWidth=0
        )
    )

    st.altair_chart(chart, use_container_width=True)
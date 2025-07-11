import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

st.set_page_config(
    page_title="Analyse LinkedIn - Postes par Industrie",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Analyse LinkedIn : Top 10 des titres de postes par industrie")

st.markdown("""
Ce tableau et graphique présentent le **Top 10 des titres de postes par industrie** les plus publiés sur LinkedIn, classés par industrie.  
Sélectionnez une industrie dans la liste déroulante pour voir les résultats correspondants.
""")

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

query = """
WITH postes_par_industrie AS (
    SELECT 
        ji.industry_id AS industrie,
        jp.title AS titre_poste,
        COUNT(*) AS nombre_offres,
        ROW_NUMBER() OVER (PARTITION BY ji.industry_id ORDER BY COUNT(*) DESC) AS rang
    FROM job_postings_clean jp
    JOIN job_industries_csv ji ON jp.job_id = ji.job_id
    WHERE jp.title IS NOT NULL
    GROUP BY ji.industry_id, jp.title
)
SELECT industrie, titre_poste, nombre_offres
FROM postes_par_industrie
WHERE rang <= 10
ORDER BY industrie, nombre_offres DESC;
"""

df = run_query(query)

if df.empty:
    st.warning("⚠️ Aucune donnée trouvée pour le moment.")
else:
    industries = df["INDUSTRIE"].unique()
    selected_industry = st.selectbox("🔍 Choisissez une industrie", industries)

    filtered_df = df[df["INDUSTRIE"] == selected_industry]

    st.subheader(f"📄 Postes les plus publiés pour l'industrie : `{selected_industry}`")
    st.dataframe(filtered_df, use_container_width=True)

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('NOMBRE_OFFRES:Q', title='Nombre d’offres'),
        y=alt.Y('TITRE_POSTE:N', sort='-x', title='Titre du poste'),
        color=alt.Color('TITRE_POSTE:N', legend=None),
        tooltip=['TITRE_POSTE', 'NOMBRE_OFFRES']
    ).properties(
        width=800,
        height=400,
        title="📈 Top 10 des titres de poste"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        anchor='start',
        color='gray'
    )

    st.altair_chart(chart, use_container_width=True)

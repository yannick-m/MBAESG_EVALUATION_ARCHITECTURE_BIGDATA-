import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

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

st.title("📊 Répartition des offres d’emploi par taille d’entreprise")

query = """
SELECT 
    c.company_size AS taille_entreprise, 
    COUNT(*) AS nombre_offres
FROM job_postings_clean jp
JOIN companies_csv c 
    ON TRY_TO_NUMBER(jp.company_name) = c.company_id
WHERE c.company_size IS NOT NULL
  AND TRY_TO_NUMBER(jp.company_name) IS NOT NULL
GROUP BY c.company_size
ORDER BY c.company_size;
"""

df = run_query(query)

if df.empty:
    st.warning("Aucune donnée disponible pour cette analyse.")
else:
    # Supprimer les lignes où taille_entreprise ou nombre_offres sont nuls
    df = df.dropna(subset=['TAILLE_ENTREPRISE', 'NOMBRE_OFFRES'])

    # Supprimer les lignes où nombre_offres est 0 (optionnel)
    df = df[df['NOMBRE_OFFRES'] > 0]

    # Arrondir nombre_offres au plus proche entier (utile si float)
    df['NOMBRE_OFFRES'] = df['NOMBRE_OFFRES'].round().astype(int)

    # Convertir taille_entreprise en string
    df['TAILLE_ENTREPRISE'] = df['TAILLE_ENTREPRISE'].astype(str)

    # Création du graphique Altair
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X('TAILLE_ENTREPRISE:N', title="Taille d'entreprise", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('NOMBRE_OFFRES:Q', title="Nombre d'offres", axis=alt.Axis(format=',d')),
        color=alt.Color('TAILLE_ENTREPRISE:N', legend=None, scale=alt.Scale(scheme='tableau10')),
        tooltip=[
            alt.Tooltip('TAILLE_ENTREPRISE:N', title='Taille d’entreprise'),
            alt.Tooltip('NOMBRE_OFFRES:Q', title='Nombre d’offres', format=',d')
        ]
    ).properties(
        width=700,
        height=400,
        title="Répartition des offres par taille d'entreprise"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=18,
        anchor='start',
        color='darkblue'
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(chart, use_container_width=True)
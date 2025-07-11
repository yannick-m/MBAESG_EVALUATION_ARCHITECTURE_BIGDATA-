import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

st.set_page_config(page_title="Répartition Offres par Type d'Emploi", layout="wide")

st.title("📊 Répartition des offres d’emploi par type d’emploi")

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

# Requête SQL
query = """
SELECT 
    compensation_type AS type_emploi,
    COUNT(*) AS nombre_offres
FROM job_postings_clean
WHERE compensation_type IS NOT NULL
GROUP BY compensation_type
ORDER BY nombre_offres DESC;
"""

df = run_query(query)

# Gestion du filtre avec option "Tout"
options = ["Tout"] + sorted(df['TYPE_EMPLOI'].unique().tolist())

if "selected_types" not in st.session_state:
    st.session_state.selected_types = ["Tout"]

def update_selection():
    selected = st.session_state.multiselect
    if "Tout" in selected and len(selected) > 1:
        selected.remove("Tout")
        st.session_state.selected_types = selected
        st.session_state.multiselect = selected
    elif len(selected) == 0:
        st.session_state.selected_types = ["Tout"]
        st.session_state.multiselect = ["Tout"]
    else:
        st.session_state.selected_types = selected

selected = st.multiselect(
    "Sélectionnez un ou plusieurs types d'emploi :",
    options=options,
    default=st.session_state.selected_types,
    key="multiselect",
    on_change=update_selection
)

# Filtrer le DataFrame selon sélection (si "Tout" sélectionné, affiche tout)
if "Tout" not in st.session_state.selected_types:
    filtered_df = df[df['TYPE_EMPLOI'].isin(st.session_state.selected_types)]
else:
    filtered_df = df.copy()

# Affichage tableau
st.subheader("Données filtrées")
st.dataframe(filtered_df.set_index('TYPE_EMPLOI'), use_container_width=True)

# Graphique Altair designé
chart = alt.Chart(filtered_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X('TYPE_EMPLOI:N', title="Type d'emploi", sort=options[1:]),
    y=alt.Y('NOMBRE_OFFRES:Q', title="Nombre d'offres", axis=alt.Axis(format=',d')),
    color=alt.Color('TYPE_EMPLOI:N', legend=None, scale=alt.Scale(scheme='tableau10')),
    tooltip=[
        alt.Tooltip('TYPE_EMPLOI:N', title='Type d’emploi'),
        alt.Tooltip('NOMBRE_OFFRES:Q', title='Nombre d’offres', format=',d')
    ]
).properties(
    width=800,
    height=400,
    title="Répartition des offres par type d'emploi"
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

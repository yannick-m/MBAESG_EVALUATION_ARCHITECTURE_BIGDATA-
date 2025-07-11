 Problèmes rencontrés et solutions proposées

1. Colonnes manquantes ou mal nommées

Problème : Des erreurs comme invalid identifier 'company_id' ou salary_year_avg non reconnue apparaissaient.

Cause : Les noms de colonnes utilisés dans les requêtes ne correspondaient pas à ceux des tables Snowflake.

Solution : Exécution de SELECT * FROM company LIMIT 1 pour afficher les colonnes disponibles. Ajustement des requêtes en utilisant les bons noms (company_name, max_salary, etc.).


 2. Colonnes contenant uniquement des valeurs NULL

Problème : Les visualisations ne s'affichaient pas car certaines colonnes comme posting_domain ou company_size contenaient uniquement des NULL.

Solution : Ajout de conditions SQL pour exclure les valeurs NULL :
WHERE company_size IS NOT NULL

3. Mauvaise jointure entre les tables

Problème : Les jointures entre job_postings_clean et companies_csv échouaient à cause d’un lien incorrect (ex : company_id manquant).

Solution :
Utilisation de company_name comme clé de jointure.

Nettoyage avec TRY_TO_NUMBER ou LOWER(TRIM(...)) pour harmoniser les formats.

4. Table ou objet inexistant

Problème : Erreur Object 'industries_csv' does not exist.

Solution : Vérification des tables existantes via :
SHOW TABLES;

et adaptation des requêtes aux tables réellement présentes (job_industries_csv, etc.).

5. Erreur lors du clonage du repository GitHub
Problème : Échec de clonage depuis GitHub avec l’erreur invalid value [GITHUB] for parameter 'API_PROVIDER'.

Cause : Snowflake n’accepte que certains providers prédéfinis.

Solution :

Utilisation de git_https_api comme API_PROVIDER.

Exemple correct :
CREATE OR REPLACE API INTEGRATION github_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/user/repo')
  ALLOWED_AUTHENTICATION_SECRETS = (linkedin)
  ENABLED = TRUE;

6. Erreur lors de la création du Secret
Problème : Syntaxe invalide ou PAT mal configuré.

Solution :Création d’un SECRET bien formaté :

CREATE OR REPLACE SECRET linkedin
  TYPE = PASSWORD
  USERNAME = 'ton_username'
  PASSWORD = 'ton_personal_access_token';
Le PAT doit inclure le scope repo.

7. Nom d’objet déjà existant lors du clonage
Problème : Object already exists.

Solution :Supprimer ou renommer le dossier :
REMOVE @~/repos/NOM_DU_PROJET;

8. Erreur push not permitted
Problème : Erreur lors de la tentative de commit/push vers GitHub.

Cause : PAT GitHub mal configuré ou ne contenant pas les droits repo.

Solution : Générer un nouveau PAT avec les bons scopes, et recréer le SECRET.

9. Graphiques vides dans Streamlit
Problème : Streamlit affiche “Aucune donnée disponible pour cette analyse”.

Cause : Requête renvoyant un DataFrame vide.

Solution :Vérification des filtres NULL, des jointures et des données disponibles.

Ajout de conditions dans l’app :
if df.empty:
    st.warning("Aucune donnée disponible.")

10. Erreur set_index dans pandas
Problème :

KeyError: 'None of [Index(['titre_poste']...)] are in the [columns]'
Cause : Mauvais renommage des colonnes ou index inexistant.

Solution : Ajouter une ligne :
st.write(df.columns)  # pour inspecter les noms réels

11. Syntax error dans les requêtes SQL
Exemple : unexpected keyword 'distinct' ou erreurs de guillemets.

Solution : Vérification stricte de la syntaxe SQL, et évitement des alias inutiles.
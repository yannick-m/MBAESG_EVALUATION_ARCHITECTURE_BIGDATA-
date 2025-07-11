## Problèmes rencontrés et solutions proposée

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

6. Erreur lors de la création du Secret
Problème : Syntaxe invalide ou PAT mal configuré.

Solution :Création d’un SECRET bien formaté 

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

Solution :Supprimer ou renommer le dossier 

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


## Étapes du projet avec commentaires explicatifs

1. Création de la base de données et du schéma
Préparer un environnement dédié dans Snowflake pour stocker et organiser toutes les données liées au projet. Cela facilite la gestion, la sécurité et la maintenance des données.

2. Mise en place d’un stage externe vers le cloud (bucket S3)
Configurer un point d’accès (stage) dans Snowflake qui pointe vers un stockage cloud (ex : AWS S3). Cela permet d’importer facilement les fichiers sources dans Snowflake sans transfert manuel.

3. Définition des formats de fichiers (CSV, JSON)
Décrire précisément comment les fichiers externes doivent être interprétés lors de leur chargement (délimiteurs, encodages, présence d’en-têtes, etc.), pour éviter les erreurs d’import et garantir l’intégrité des données.

4. Création des tables dans Snowflake
Modéliser et créer les tables nécessaires à partir des schémas des fichiers sources. Choisir des types de données adaptés pour assurer la cohérence et optimiser les performances des requêtes.

5. Chargement des données dans les tables Snowflake
Importer les données brutes depuis le stage vers les tables Snowflake à l’aide de la commande COPY INTO, automatisant ainsi l’ingestion de gros volumes de données.

6. Nettoyage et transformation des données
Appliquer des règles de nettoyage (suppression des valeurs nulles, correction des formats, standardisation des textes) et des transformations nécessaires pour rendre les données exploitables et fiables pour l’analyse.

7. Analyse des données - Extraction des insights
Réaliser des requêtes SQL pour répondre aux questions métiers : par exemple, quels sont les postes les plus publiés, quelle est la répartition des offres par secteur ou type d’emploi, quels postes sont les mieux rémunérés, etc.

8. Visualisation des résultats avec Streamlit
Développer une application interactive en Python avec Streamlit pour présenter visuellement les résultats sous forme de graphiques et tableaux, facilitant la compréhension et la prise de décision.

!![alt text](</CAPTURE_VISUALISATION/visualization (3).png>)
![alt text](</CAPTURE_VISUALISATION/visualization (2).png>) 
![alt text](</CAPTURE_VISUALISATION/visualization (1).png>) 
![alt text](/CAPTURE_VISUALISATION/visualization.png) 
![alt text](</CAPTURE_VISUALISATION/visualization (4).png>)


9. Gestion des erreurs et validation des résultats
Mettre en place des contrôles pour gérer les cas où les données sont manquantes ou insuffisantes, et s’assurer que les résultats affichés sont cohérents à travers la création des vues avec les attentes métier.


10.Étapes de connexion entre Snowflake et GitHub
a. Créer un Personal Access Token (PAT) sur GitHub
 Ce token est une sorte de mot de passe sécurisé qui permet à Snowflake d’accéder à ton dépôt GitHub.
 Si ton dépôt est privé, c’est indispensable.
 Il doit avoir au minimum les permissions repo (et workflow si tu utilises GitHub Actions).

b. Créer un secret dans Snowflake
 Le secret contient ton nom d'utilisateur GitHub et ton token personnel.
 Ce secret sera utilisé pour authentifier la connexion entre Snowflake et GitHub.

c. Créer une API Integration dans Snowflake
C’est un objet de configuration qui indique à Snowflake comment se connecter au dépôt Git.
Tu dois spécifier le lien du dépôt, le nom du secret à utiliser et autoriser les opérations.


d. Cloner le dépôt GitHub dans Snowflake
Cette commande importe les fichiers de ton dépôt GitHub dans un dossier interne (stage) de Snowflake.
Une fois cloné, tu peux utiliser le code SQL, Python ou Streamlit directement dans tes feuilles de travail ou projets Snowflake.

e. Lire ou exécuter le code du dépôt
Tu peux maintenant parcourir les fichiers du dépôt, les ouvrir dans Worksheets ou les exécuter (dans le cas des scripts .sql, .py ou .streamlit).

f. Résoudre les erreurs fréquentes
Par exemple :
Si l’erreur mentionne API_PROVIDER, c’est souvent parce que la valeur est mal écrite (git_https_api est la bonne).
Si tu ne peux pas cloner, vérifie que l’URL du dépôt est correcte et que le token a bien les bons droits.
Si Snowflake dit que l’objet existe déjà, change le nom du stage ou supprime l’ancien.

g. Sécuriser l’intégration
Gère les accès aux secrets et API integrations avec les rôles utilisateurs dans Snowflake.
Ne partage jamais ton token dans du code.
Solution : Vérification stricte de la syntaxe SQL, et évitement des alias inutiles.

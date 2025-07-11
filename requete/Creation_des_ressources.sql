-- création ou remplacement la base de donnée linkedin 
CREATE or replace DATABASE linkedin;

-- utilisation de la base de donnée linkedin
use database linkedin;

-- création du stage linkedin
CREATE OR REPLACE STAGE linkedin_stage URL = 's3://snowflake-lab-bucket/';

--lister le stage
list @linkedin_stage;

-- creation format de type csv
CREATE or replace FILE FORMAT csv_format 
TYPE = 'CSV' 
FIELD_DELIMITER = ',' 
RECORD_DELIMITER = '\n' 
SKIP_HEADER = 1
field_optionally_enclosed_by = '\042'
null_if = ('');

-- Création format de fichier JSON
CREATE OR REPLACE FILE FORMAT json_format
TYPE = 'JSON'
STRIP_OUTER_ARRAY = TRUE;

-- creation de la table job_industries_json
CREATE OR REPLACE TABLE job_industries_json (
  v VARIANT
);

--chargement des données depuis le stage
COPY INTO job_industries_json
FROM @linkedin_stage/job_industries.json
FILE_FORMAT = (FORMAT_NAME = json_format);

-- vérification de l'import de donnée du stage dans la table 
select * from job_industries_json;

--création de la vue JOB_INDUSTRIES_JSON
CREATE OR REPLACE VIEW job_industries_csv AS
SELECT
  v:"job_id"::STRING AS job_id,
  v:"industry_id"::STRING AS industry_id
FROM job_industries_json;

-- création table compagnie_json
create or replace table companies_json (v variant);

-- chargement des donnée de companies depuis le stage
COPY INTO companies_json
FROM @linkedin_stage/companies.json
FILE_FORMAT = (FORMAT_NAME = json_format);

-- vérification de l'import de donnée du stage dans la table 
select * from companies_json;

-- création de la vue companies
CREATE OR REPLACE VIEW companies_csv AS
SELECT 
    v:"company_id" AS company_id,
    v:"name" AS name,
    v:"description" AS description,
    v:"company_size" AS company_size,
    v:"state" AS state,
    v:"country" AS country,
    v:"city" AS city,
    v:"zip_code" AS zip_code,
    v:"address" AS address,
    v:"url" AS url
FROM companies_json;
-- création table company_specialities_json
create or replace table company_specialities_json (v variant);

-- chargement des donnée de company_speciality depuis le stage
COPY INTO company_specialities_json
FROM @linkedin_stage/company_specialities.json
FILE_FORMAT = (FORMAT_NAME = json_format);

-- vérification de l'import de donnée du stage dans la table 
select * from company_specialities_json;

-- création de vue company_specialities
create or replace view company_specialities_csv as
select 
        
        v:"company_id" as "company_id",
        v:"speciality" as "speciality"
from company_specialities_json;

-- création table company_indutries_json
create or replace table company_indutries_json (v variant);

-- chargement des donnée de company_speciality depuis le stage
COPY INTO company_indutries_json
FROM @linkedin_stage/company_industries.json
FILE_FORMAT = (FORMAT_NAME = json_format);

-- vérification de l'import de donnée du stage dans la table 
select * from company_indutries_json;

-- création de la vue company_industries
create or replace view company_indutries_csv as
select 
        
        v:"company_id" as "company_id",
        v:"industry" as "industry"
from company_indutries_json;


-- création de la table benefits
CREATE OR REPLACE TABLE benefits (
  job_id STRING,
  inferred BOOLEAN,
  type STRING
);

-- chargement des donnée de benefits depuis le stage
COPY INTO benefits
FROM @linkedin_stage/benefits.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')

ON_ERROR = 'CONTINUE';

-- création de la vue  benefits_clean
CREATE OR REPLACE VIEW benefits_clean AS
SELECT
  job_id,
  CASE 
    WHEN LOWER(inferred) IN ('true', 'yes', '1') THEN TRUE
    ELSE FALSE
  END AS inferred,
  type
FROM benefits;


-- création de la table employee_count
CREATE OR REPLACE TABLE employee_counts (
  company_id STRING,
  employee_count INTEGER,
  follower_count INTEGER,
  time_recorded INTEGER
);

-- chargement des donnée de employee_count depuis le stage
COPY INTO employee_counts
FROM @linkedin_stage/employee_counts.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- création de la vue employee_counts_clean
CREATE OR REPLACE VIEW employee_counts_clean AS
SELECT
  company_id,
  TRY_TO_NUMBER(employee_count) AS employee_count,
  TRY_TO_NUMBER(follower_count) AS follower_count,
  TO_TIMESTAMP_NTZ(time_recorded) AS time_recorded
FROM employee_counts;

-- création de la table job_skills
CREATE OR REPLACE TABLE job_skills (
  job_id STRING,
  skill_abr STRING
);

-- chargement des donnée de job_skills depuis le stage
COPY INTO job_skills
FROM @linkedin_stage/job_skills.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- création de la table job_postings
CREATE OR REPLACE TABLE job_postings (
  job_id STRING,
  company_name STRING,
  title STRING,
  description STRING,
  max_salary STRING,
  pay_period STRING,
  formatted_work_type STRING,
  location STRING,
  applies STRING,
  original_listed_time STRING,
  remote_allowed STRING,
  views STRING,
  job_posting_url STRING,
  application_url STRING,
  application_type STRING,
  expiry STRING,
  closed_time STRING,
  formatted_experience_level STRING,
  skills_desc STRING,
  listed_time STRING,
  posting_domain STRING,
  sponsored STRING,
  work_type STRING,
  currency STRING,
  compensation_type STRING,
  company_email STRING,
  company_website STRING,
  job_tags STRING
);


-- creation format de type csv
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;

-- chargement des donnée de job_postings depuis le stage
COPY INTO job_postings
FROM @linkedin_stage/job_postings.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';


-- création de la vue pour le traitement ou le nettoyage de la table job_posting
CREATE OR REPLACE VIEW job_postings_clean AS
SELECT
  job_id,
  company_name,
  title,
  description,
  TRY_TO_DOUBLE(max_salary) AS max_salary,
  pay_period,
  formatted_work_type,
  location,
  TRY_TO_NUMBER(applies) AS applies,
  TRY_TO_TIMESTAMP(original_listed_time) AS original_listed_time,
  CASE WHEN LOWER(remote_allowed) IN ('true', 'yes', '1') THEN TRUE ELSE FALSE END AS remote_allowed,
  TRY_TO_NUMBER(views) AS views,
  job_posting_url,
  application_url,
  application_type,
  TRY_TO_TIMESTAMP(expiry) AS expiry,
  TRY_TO_TIMESTAMP(closed_time) AS closed_time,
  formatted_experience_level,
  skills_desc,
  TRY_TO_TIMESTAMP(listed_time) AS listed_time,
  posting_domain,
  CASE WHEN LOWER(sponsored) IN ('true', 'yes', '1') THEN TRUE ELSE FALSE END AS sponsored,
  work_type,
  currency,
  compensation_type,
  company_email,
  company_website,
  job_tags
FROM job_postings;

-- création  de la table industries_csv
CREATE OR REPLACE TABLE industries_csv (
    industry_id string,
    industry_name STRING
);

-- insertion des données dans la table industries_csv
INSERT INTO industries_csv (industry_id, industry_name) VALUES
(1, 'Technologies de l\'information'),
(2, 'Finance'),
(3, 'Santé'),
(4, 'Éducation'),
(5, 'Distribution et Commerce de détail'),
(6, 'Transports et Logistique'),
(7, 'Industrie manufacturière'),
(8, 'Énergie et Environnement'),
(9, 'Marketing et Publicité'),
(10, 'Consulting'),
(11, 'Assurance'),
(12, 'Immobilier'),
(13, 'Services juridiques'),
(14, 'Tourisme et Hôtellerie'),
(15, 'Alimentation et Boissons'),
(16, 'Télécommunications'),
(17, 'Médias et Divertissement'),
(18, 'Recherche et Développement'),
(19, 'Mode et Luxe'),
(20, 'Organisations à but non lucratif');


-- Compte le nombre d''offres distinctes associées à chaque secteur d''activité en utilisant les tables nettoyées et les jointures entre offres et secteurs.
SELECT 
    i.industry_name AS secteur_activite,
    COUNT(DISTINCT jp.job_id) AS nombre_offres
FROM job_postings_clean jp
JOIN job_industries_csv ji ON jp.job_id = ji.job_id
JOIN industries_csv i ON ji.industry_id = i.industry_id
GROUP BY i.industry_name
ORDER BY nombre_offres DESC;

-- Affiche tout le contenu de la table des secteurs d''activité
SELECT * FROM industries_csv;


-- Identifie les 10 paires secteur + poste les plus fréquentes dans les données brutes
SELECT 
    ji.industry_id,
    jp.title,
    COUNT(*) AS job_count
FROM job_postings jp
JOIn job_industries ji ON jp.job_id = ji.job_id
GROUP BY ji.industry_id, jp.title
ORDER BY job_count DESC
LIMIT 10;
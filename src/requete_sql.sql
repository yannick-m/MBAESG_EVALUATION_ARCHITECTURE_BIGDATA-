-- création de la base de donnée  linkedin
CREATE OR REPLACE DATABASE linkedin;

--utilisation de la base de donnée  linkedin
USE DATABASE linkedin;

-- creation de l'entrepot  de donnée  linkedin
CREATE OR REPLACE WAREHOUSE linkedin_wh
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;
USE WAREHOUSE linkedin_wh;
/* -------------------------------------------------------------- */
      -- Check and Work on gans Database --
/* -------------------------------------------------------------- */

-- Use the database
USE gans;

DROP TABLE cities;
DROP TABLE countries;
DROP TABLE populations;
DROP TABLE weather;

ALTER TABLE cities DROP COLUMN city;
ALTER TABLE weather DROP COLUMN city;
ALTER TABLE cities ADD new_columns varchar(255);
ALTER TABLE weather ADD data_retrieved DATETIME NOT NULL;

-- Check tables
SELECT * FROM cities;
SELECT * FROM countries;
SELECT * FROM populations;
SELECT * FROM weather;
SELECT * FROM airports;
SELECT * FROM flights;

SELECT * FROM weather;

-- Modify columns if necessary
ALTER TABLE cities MODIFY COLUMN latitude DECIMAL(10, 4);
ALTER TABLE cities MODIFY COLUMN longitude DECIMAL(10, 4);
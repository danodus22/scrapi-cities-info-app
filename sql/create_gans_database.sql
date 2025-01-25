/* ------------------------------------------------------------------------------------------------------
# Create gans Database
------------------------------------------------------------------------------------------------------ */

-- 1. Drop the database if it already exists
DROP DATABASE IF EXISTS gans;

-- 2. Create the database
CREATE DATABASE gans;

-- 3. Use the database
USE gans;

-- 4. CREATE tables for cities_df --
CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    latitude DECIMAL(8, 5) NOT NULL,
    longitude DECIMAL(8, 5) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE
);

CREATE TABLE populations (
    population_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    population INT,
    population_year INT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id) ON DELETE CASCADE
);

-- 5. CREATE table for weather_df --
CREATE TABLE weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    forecast_time DATETIME NOT NULL,
    sunrise DATETIME,
    sunset DATETIME,
    temperature DECIMAL(5, 2),
    feels_like DECIMAL(5, 2),
    humidity INT,
    weather_description VARCHAR(255),
    wind_speed DECIMAL(5, 2),
    wind_direction DECIMAL(5, 2),
    rain DECIMAL(5, 2),
    FOREIGN KEY (city_id) REFERENCES cities(city_id) ON DELETE CASCADE
);

-- 6. CREATE table for airports_df --
CREATE TABLE airports (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    icao VARCHAR(10) NOT NULL UNIQUE,
    iata VARCHAR(10),
    airportName VARCHAR(255) NOT NULL,
    shortName VARCHAR(255),
    municipalityName VARCHAR(255),
    countryCode CHAR(2) NOT NULL,
    timeZone VARCHAR(50),
    latitude DECIMAL(8, 5) NOT NULL,
    longitude DECIMAL(8, 5) NOT NULL,
    city_id INT NOT NULL
 -- FOREIGN KEY (city_id) REFERENCES airport_city(city_id) ON DELETE CASCADE
);

-- 7. CREATE table for flights_df --
CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_id INT NOT NULL,
    FlightNumber VARCHAR(10),
    Airline VARCHAR(100),
    Aircraft VARCHAR(50),
    OriginAirport VARCHAR(100),
    OriginIATA VARCHAR(10),
    Terminal VARCHAR(255),
    ScheduledArrival DATETIME,
    ActualArrival DATETIME,
    Note VARCHAR(50),
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE
);

-- 8. CREATE a Junction table for airports & cities (many-to-many relationship)
CREATE TABLE airport_city (
    airport_id INT NOT NULL,
    city_id INT NOT NULL,
    PRIMARY KEY (airport_id, city_id),
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES cities(city_id) ON DELETE CASCADE
);

/* ------------------------------------------------------------------------------------------------------
# OPTIONAL - Expand weather: create more relations (normalisation) to avoid redundancies
------------------------------------------------------------------------------------------------------ */
CREATE TABLE weather_descriptions (
    description_id INT AUTO_INCREMENT PRIMARY KEY,
    description_text VARCHAR(255) NOT NULL UNIQUE
);

ALTER TABLE weather
DROP COLUMN weather_description,
ADD COLUMN description_id INT NOT NULL,
ADD FOREIGN KEY (description_id) REFERENCES weather_descriptions(description_id) ON DELETE CASCADE;

CREATE TABLE wind_data (
    wind_id INT AUTO_INCREMENT PRIMARY KEY,
    wind_speed DECIMAL(5, 2) NOT NULL,
    wind_direction DECIMAL(5, 2) NOT NULL
);

ALTER TABLE weather
DROP COLUMN wind_speed,
DROP COLUMN wind_direction,
ADD COLUMN wind_id INT NOT NULL,
ADD FOREIGN KEY (wind_id) REFERENCES wind_data(wind_id) ON DELETE CASCADE;

CREATE TABLE weather_times (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    forecast_time DATETIME NOT NULL,
    data_retrieved DATETIME NOT NULL
);

ALTER TABLE weather
DROP COLUMN forecast_time,
DROP COLUMN data_retrieved,
ADD COLUMN time_id INT NOT NULL,
ADD FOREIGN KEY (time_id) REFERENCES weather_times(time_id) ON DELETE CASCADE;

CREATE TABLE weather_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    temperature DECIMAL(5, 2) NOT NULL,
    feels_like DECIMAL(5, 2),
    humidity INT,
    rain DECIMAL(5, 2)
);

ALTER TABLE weather
DROP COLUMN temperature,
DROP COLUMN feels_like,
DROP COLUMN humidity,
DROP COLUMN rain,
ADD COLUMN detail_id INT NOT NULL,
ADD FOREIGN KEY (detail_id) REFERENCES weather_details(detail_id) ON DELETE CASCADE;

CREATE TABLE weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    description_id INT NOT NULL,
    wind_id INT NOT NULL,
    time_id INT NOT NULL,
    detail_id INT NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id) ON DELETE CASCADE,
    FOREIGN KEY (description_id) REFERENCES weather_descriptions(description_id) ON DELETE CASCADE,
    FOREIGN KEY (wind_id) REFERENCES wind_data(wind_id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES weather_times(time_id) ON DELETE CASCADE,
    FOREIGN KEY (detail_id) REFERENCES weather_details(detail_id) ON DELETE CASCADE
);

/* ------------------------------------------------------------------------------------------------------
# OPTIONAL - Expand airports & flights: create more relations (normalisation) to avoid redundancies 
------------------------------------------------------------------------------------------------------ */
-- CREATE table airlines
CREATE TABLE airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_name VARCHAR(100) NOT NULL UNIQUE,
    airline_code VARCHAR(10) UNIQUE -- Optional: IATA/ICAO Code
);

-- ALTER table flights (drop / add columns)
ALTER TABLE flights
DROP COLUMN Airline,
ADD COLUMN airline_id INT NOT NULL,
ADD FOREIGN KEY (airline_id) REFERENCES airlines(airline_id) ON DELETE CASCADE;

-- CREATE table aircrafts
CREATE TABLE aircrafts (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    aircraft_type VARCHAR(50) NOT NULL UNIQUE,
    manufacturer VARCHAR(100) -- Optional: Hersteller
);

-- ALTER table flights (drop / add columns)
ALTER TABLE flights
DROP COLUMN Aircraft,
ADD COLUMN aircraft_id INT NOT NULL,
ADD FOREIGN KEY (aircraft_id) REFERENCES aircrafts(aircraft_id) ON DELETE CASCADE;

-- CREATE table terminals
CREATE TABLE terminals (
    terminal_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_id INT NOT NULL,
    terminal_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id) ON DELETE CASCADE
);

-- ALTER table flights
ALTER TABLE flights
DROP COLUMN Terminal,
ADD COLUMN terminal_id INT,
ADD FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id) ON DELETE CASCADE;

-- CREATE table flight_status
CREATE TABLE flight_status (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE -- z. B. "Scheduled", "Delayed", "Cancelled"
);

-- ALTER table flights
ALTER TABLE flights
DROP COLUMN Status_,
ADD COLUMN status_id INT NOT NULL,
ADD FOREIGN KEY (status_id) REFERENCES flight_status(status_id) ON DELETE CASCADE;
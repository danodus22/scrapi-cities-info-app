# scrapi-cities-info-app
## Combine web scraping & API data for cities worldwide

## Project description

This project tests the interaction between web scraping and querying two APIs. It forms the basis for learning how to use web scraping and API queries.</br>
The main goals of the project are:

- To collect information about different cities (worldwide) from [Wikipedia](https://www.wikipedia.org/). This information then forms the data basis for all further steps and API queries.
- The two APIs are used to retrieve weather forecasts as well as airport and flight data for these cities.
- All collected data is stored in a relational data model in a MySQL database and can be continuously updated and saved.

### APIs used

- **[OpenWeatherMap API](https://openweathermap.org/api)**: Is used to retrieve current weather forecasts and climatic data for cities.
- **[AeroDataBox API](https://rapidapi.com/aerodatabox/api/aerodatabox)** (via RapidAPI): Is used to provide information about airports and flight data for incoming flights.

Both APIs are protected by API keys that must be stored in the configuration. These keys are not included in the project published here and must be obtained independently.

### Data flow

![From a source to MySQL](https://github.com/user-attachments/assets/b993b993-181a-4dfd-bd38-ad7b4a1160ab)

---

## Technologies and libraries 📖

- **programming language:** Python 🐍

- **Libraries:**
  - `requests`: For API queries
  - `re`: Regular Expressions for Data Processing
  - `BeautifulSoup`: For web scraping
  - `pandas`: For data analysis and transformation
  - `datetime`: For date and time manipulation
  - `SQLAlchemy`: For interaction with the MySQL database
  - `pymysql`: For interaction with the MySQL database
- **Database:** MySQL

---

## Possible future extensions
The project offers a functioning application and can be expanded
- Extensions to the data model (division of airport and flights into further relations)
- Targeted error handling
- Avoiding web scraping and using additional APIs to query the city information
- Expanding the modularity to run the code in a cloud application

---

## Installation and execution

### Prerequisites
- Python 3.9 or higher (3.12.7 was used during development)
- MySQL server 8.0 or higher installed and configured
- API keys for:
- [OpenWeatherMap](https://openweathermap.org/api)
- [AeroDataBox](https://rapidapi.com/aerodatabox/api/aerodatabox)

### Next steps
1. Clone the repository or download it:
   ```bash
   git clone https://github.com/danodus22/scrapi-cities-info-app.git
   cd scrapi-cities-info-app
2. Install the dependencies:
   pip install -r requirements.txt
3. Create the MySQL database:
   Load the database schema (sql/create_gans_database.sql) into your MySQL server.
4. Adjust the configuration files to store the API keys and the MySQL connection.
5. Start with the **cities_of_the_world.ipynb** notebook to get a first overview of the functionalities.
6. If you like: check the "One-Click" version within the **one_click.ipynb** notebook to save all information to Excel file.

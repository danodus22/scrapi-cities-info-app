from utils import *

def get_city_data(city):
    """
    Scrapes data for a given city from Wikipedia.
    Args:
        city (str): Name of the city to scrape.
    Returns:
        dict: A dictionary containing city data.
    """
    url = f'https://en.wikipedia.org/wiki/{city}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # 1. Extracting Data
    city_dict = {}
    city_dict['city'] = soup.select_one('.firstHeading').get_text() if soup.select_one(".firstHeading") else city
    city_dict['country'] = soup.select(".infobox-data")[0].get_text() if len(soup.select(".infobox-data")) else "N/A"
    city_dict['latitude'] = soup.select_one(".latitude").get_text() if soup.select_one(".latitude") else "N/A"
    city_dict['longitude'] = soup.select_one(".longitude").get_text() if soup.select_one(".longitude") else "N/A"

    # Extract and process population data
    population_header = soup.select_one('th.infobox-header:-soup-contains("Population")')
    if population_header:
        population_data = population_header.parent.find_next_sibling()
        city_dict['population'] = population_data.find(string=re.compile(r'\d+')) if population_data else "N/A"

        population_year_div = population_header.find("div", class_="ib-settlement-fn")
        if population_year_div:
            for sup in population_year_div.find_all("sup"):
                sup.decompose()  # Remove sup elements and extract year
            year_str = population_year_div.get_text(strip=True).strip("()")
            city_dict['population_year'] = extract_year(year_str)
        else:
            city_dict['population_year'] = 0
    else:
        city_dict['population'] = 0
        city_dict['population_year'] = 0
    return city_dict

def extract_year(value):
    match = re.search(r'\b(\d{4,})\b', value)
    if match:
        year = int(match.group(1))
        if 1900 <= year <= 2100:
            return year
    return None

def dms_to_decimal(coord):
    match = re.match(r"(\d+)°(\d+)?′?(\d+)?(?:″)?([NSEW])", coord)
    if not match:
        return None

    degrees = int(match.group(1))
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    direction = match.group(4)
    decimal = degrees + (minutes / 60) + (seconds / 3600)

    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def webscraping_function(cities):
    """
    Scrapes data for a list of cities and returns it as a DataFrame.
    Args:
        cities (list): List of city names to scrape.
    Returns:
        pd.DataFrame: A DataFrame containing city data.
    """
    city_list = []
    for city in cities:
        city_data = get_city_data(city)
        city_list.append(city_data)
    cities_df = pd.DataFrame(city_list)

    # Data Cleaning
    cities_df['latitude'] = cities_df['latitude'].apply(dms_to_decimal)
    cities_df['longitude'] = cities_df['longitude'].apply(dms_to_decimal)
    cities_df['population'] = pd.to_numeric(cities_df['population'].str.replace(',', ''), errors='coerce')
    cities_df['country'] = cities_df['country'].str.replace('\xa0', '', regex=False)

    return cities_df

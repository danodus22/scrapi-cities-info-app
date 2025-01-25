from utils import *
from config import load_config

# Load configuration
config = load_config('../config.yml')

def get_airports(cities_df, config_path='config.yml', radius=35, limit=10):
  """
  Fetches airport data for cities in the given DataFrame.
  Args:
      cities_df (pd.DataFrame): DataFrame with city data including latitude and longitude.
      config_path (str): Path to the configuration file.
      radius (int): Search radius around the city in kilometers.
      limit (int): Maximum number of airports to retrieve.
  Returns:
      pd.DataFrame: DataFrame containing airport data.
  """
  # Load API configuration
  config = load_config(config_path)
  aerodatabox_config = config.get("apis", {}).get("aerodatabox", {}).get("airports", {})
  url = aerodatabox_config.get("url", "")
  headers = aerodatabox_config.get("headers", {})

  def get_airports_from_coords(lat, lon):
    querystring = {
        "lat": lat,
        "lon": lon,
        "radiusKm": radius,
        "limit": limit,
        "withFlightInfoOnly": "true"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        airports = response.json().get('items', [])
        return pd.json_normalize(airports) if airports else pd.DataFrame()
    else:
        print(f"API request failed for {lat}, {lon} with status code: {response.status_code}")
        return pd.DataFrame()

  # Group cities by unique coordinates
  unique_coords = cities_df[['latitude', 'longitude', 'city']].drop_duplicates()

  # Call up airport information
  all_airports = []
  for _, row in unique_coords.iterrows():
      lat, lon, city = row['latitude'], row['longitude'], row['city']
      airport_data = get_airports_from_coords(lat, lon)
      if not airport_data.empty:
          airport_data['city'] = city
          all_airports.append(airport_data)

  # Merge results
  return pd.concat(all_airports, ignore_index=True) if all_airports else pd.DataFrame()

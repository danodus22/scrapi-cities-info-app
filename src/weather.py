from utils import *
from config import load_config

# Load Configuration
config = load_config('../config.yml')

def convert_to_local_time(timestamp, timezone_offset):
    """
    Converts a UTC timestamp to local time based on the timezone offset.
    Args:
        timestamp (int): The UTC timestamp.
        timezone_offset (int): The offset in seconds from UTC.
    Returns:
        datetime: Local time.
    """
    utc_time = datetime.fromtimestamp(timestamp, tz=dt_timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time

def get_weather_data(cities_df, config_path='config.yml'):
  """
  Queries weather data from the OpenWeatherMap API for a list of cities.
  Args:
      cities_df (pd.DataFrame): DataFrame containing city names.
      config_path (str): Path to the configuration file.
  Returns:
      pd.DataFrame: DataFrame containing weather forecast information.
  """
  # Load API configuration
  config = load_config(config_path)
  if not config:
    raise ValueError("The configuration file could not be loaded.")
  
  api_config = config.get("apis", {}).get("openweathermap", {})
  APIkey = api_config.get("api_key", "")
  base_url = api_config.get("base_url", "")
  if not APIkey or not base_url:
    raise ValueError("API key and base_url must be specified in the configuration.")
  
  weather_infos = []
  cities = cities_df['city'].dropna().unique()

  for city in cities:
    # API Request
    params = {'q': city, 'appid': APIkey, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error when retrieving data for {city}: {response.status_code}")
        continue
      
    weather_json = response.json()
    city_info = weather_json.get('city', {})
    city_name = city_info.get('name', city)
    sunrise = city_info.get('sunrise')
    sunset = city_info.get('sunset')
    timezone_offset = city_info.get('timezone', 0)  # Offset in seconds

    # Convert sunrise and sunset times to local time
    sunrise_local = convert_to_local_time(sunrise, timezone_offset) if sunrise else None
    sunset_local = convert_to_local_time(sunset, timezone_offset) if sunset else None

    # Process forecast data
    forecasts = weather_json.get('list', [])
    for forecast in forecasts:
      forecast_time_utc = datetime.strptime(forecast.get('dt_txt'), "%Y-%m-%d %H:%M:%S")
      forecast_time_local = forecast_time_utc + timedelta(seconds=timezone_offset)
        
      weather_infos.append({
        'city': city_name,
        'forecast_time': forecast_time_local.strftime("%Y-%m-%d %H:%M:%S"),
        'sunrise': sunrise_local.strftime("%Y-%m-%d %H:%M:%S") if sunrise_local else None,
        'sunset': sunset_local.strftime("%Y-%m-%d %H:%M:%S") if sunset_local else None,
        'temperature': forecast.get('main', {}).get('temp'),
        'feels_like': forecast.get('main', {}).get('feels_like'),
        'humidity': forecast.get('main', {}).get('humidity'),
        'weather_description': (forecast.get('weather', [{}])[0]).get('description'),
        'wind_speed': forecast.get('wind', {}).get('speed'),
        'wind_direction': forecast.get('wind', {}).get('deg'),
        'rain': forecast.get('rain', {}).get('3h', 0),
      })
  weather_df = pd.DataFrame(weather_infos)
  # Convert specific columns to datetime
  weather_df['forecast_time'] = pd.to_datetime(weather_df['forecast_time'])
  weather_df['sunrise'] = pd.to_datetime(weather_df['sunrise'])
  weather_df['sunset'] = pd.to_datetime(weather_df['sunset'])

  return weather_df

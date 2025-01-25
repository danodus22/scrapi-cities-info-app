from utils import *
from config import load_config

# Load configuration
config = load_config('../config.yml')

def get_querystring_for_nextday():
    
    # Generates a querystring for retrieving flight data for the next day.
    now = datetime.now()
    next_day = now + timedelta(days=1)
    start_time = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=12)
    
    return {
        "withLeg": "true",
        "direction": "Arrival",
        "withCancelled": "false",
        "withCodeshared": "true",
        "withCargo": "false",
        "withPrivate": "false",
        "start": start_time.strftime('%Y-%m-%dT%H:%M'),
        "end": end_time.strftime('%Y-%m-%dT%H:%M'),
    }

def get_flights(airport_code, querystring):

    # Retrieves flight data for a specific airport using the AeroDataBox API.
    aerodatabox_config = config.get("apis", {}).get("aerodatabox", {}).get("flights", {})
    url_template = aerodatabox_config.get("url", "")
    headers = aerodatabox_config.get("headers", {})

    if not url_template or not headers:
        print("Error: Invalid API configuration.")
        return None

    url = url_template.format(airport_code=airport_code, start=querystring["start"], end=querystring["end"])
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        print(f"No flights for Airport: {airport_code}. Skipped.")
        return None
    else:
        print(f"Error {response.status_code} for Airport: {airport_code}")
        return None

def flights_to_dataframe(flights_data):
    
    # Converts flight data into a Pandas DataFrame.
    if not flights_data or 'arrivals' not in flights_data:
        print("No flight data available.")
        return None

    arrivals = flights_data['arrivals']
    flight_list = [{
        "FlightNumber": flight.get('number', 'N/A'),
        "Airline": flight.get('airline', {}).get('name', 'N/A'),
        "Aircraft": flight.get('aircraft', {}).get('model', 'N/A'),
        "OriginAirport": flight.get('departure', {}).get('airport', {}).get('name', 'N/A'),
        "OriginIATA": flight.get('departure', {}).get('airport', {}).get('iata', 'N/A'),
        "Terminal": flight.get('arrival', {}).get('terminal', 'N/A'),
        "ScheduledArrival": flight.get('arrival', {}).get('scheduledTime', {}).get('local', 'N/A'),
        "ActualArrival": flight.get('arrival', {}).get('revisedTime', {}).get('local', 'N/A'),
        "Note": flight.get('status', 'N/A'),
    } for flight in arrivals]

    return pd.DataFrame(flight_list)

def get_flight_data_for_airports(airports_df):
        
    # Retrieves flight data for all airports in the given DataFrame and combines it.
    all_flights_df = []

    for _, row in airports_df.iterrows():
        airport_code = row['iata']
        querystring = get_querystring_for_nextday()
        flights_data = get_flights(airport_code, querystring)

        if flights_data:
            flights_df = flights_to_dataframe(flights_data)
            if flights_df is not None and not flights_df.empty:
                flights_df['AirportName'] = airport_code
                all_flights_df.append(flights_df)
    
    # Combine results into a single DataFrame
    flights_df = pd.concat(all_flights_df, ignore_index=True) if all_flights_df else pd.DataFrame()
    
    # Correct date format for arrival times
    if not flights_df.empty:
        flights_df['ScheduledArrival'] = flights_df['ScheduledArrival'].str[:-6]
        flights_df['ActualArrival'] = flights_df['ActualArrival'].str[:-6]
        flights_df['ScheduledArrival'] = pd.to_datetime(flights_df['ScheduledArrival'])
        flights_df['ActualArrival'] = pd.to_datetime(flights_df['ActualArrival'])

    return flights_df
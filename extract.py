import requests
import pandas as pd
from config import API_KEY, cities

def extract_weather_data():
    """
    OpenWeather API se specified cities ka live weather aur pollution data fetch karta hai.
    Returns: pd.DataFrame containing raw master data.
    """

    print("Extraction starting API data fetch...")
    all_raw_data = []
    for city, coords in cities.items():
        try:
            lat, lon = coords['lat'], coords['lon']
            # weather CAll
            w_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
            # pollution call
            p_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            
            w_res = requests.get(w_url).json()
            p_res = requests.get(p_url).json()
            master_data = {
                "city": city,
                "weather_raw": w_res,
                "pollution_raw": p_res
            }
            all_raw_data.append(master_data)
            print(f"Complete Data: {city}")
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

    df_master = pd.DataFrame(all_raw_data)
    df_master.to_csv("master_raw_data.csv", index=False)
    return df_master

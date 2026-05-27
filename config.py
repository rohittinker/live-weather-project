import os
from dotenv import load_dotenv

API_KEY = "ce5f1d665c4571fb02717b6b4a1d9068"
cities = {
    "Jaipur": {"lat": 26.91, "lon": 75.78},
    "Delhi": {"lat": 28.61, "lon": 77.20},
    "Mumbai": {"lat": 19.07, "lon": 72.87},
    "Bangalore": {"lat": 12.97, "lon": 77.59},
    "Chennai": {"lat": 13.08, "lon": 80.27},
    "Kolkata": {"lat": 22.57, "lon": 88.36},
    "Shimla": {"lat": 31.10, "lon": 77.17},
    "Guwahati": {"lat": 26.14, "lon": 91.73}
}

# Database connections
load_dotenv(dotenv_path="weather.env")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv ("DB_NAME")
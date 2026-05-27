from datetime import datetime
from extract import extract_weather_data
from transform import transform_weather_data
from load import load_data_to_warehouse

def main():
    print(f"\n============================== ETL PIPELINE START:{datetime.now()}================================")
    # Extract
    raw_data = extract_weather_data()

    # Transform
    processed_data = transform_weather_data(raw_data)

    #Load
    load_data_to_warehouse(processed_data)

    print("=============================ETL PIPELINE COMPLETED SUCCESSFULLY====================================\n")

if __name__ == "__main__":
    main()
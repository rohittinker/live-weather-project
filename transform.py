import pandas as pd

def transform_weather_data(df_master):
    """
    Raw weather aur pollution JSON data ko clean, process aur format karta hai.
    """
    if df_master.empty:
        print("Transformation input dataframe is empty. Skipping.")
        return pd.DataFrame()
    
    print("Transformation Processing Raw Data into Gold Layer...")

    # 'weather_raw' column ke andar 'main' dictionary se data nikalna
    df_weather = pd.json_normalize(df_master['weather_raw'])

    # Pollution data 'list' ke andar hota hai, isliye pehla element [0] uthayenge
    df_pollution = pd.json_normalize(df_master['pollution_raw'].apply(lambda x: x['list'][0]))

    #Data Merging (Silver State)
    # 3. Sabko ek sath jodo (City + Weather + Pollution)
    df_silver = pd.concat([
        df_master['city'],
        df_weather[['main.temp', 'main.humidity','wind.speed', 'dt']],
        df_pollution[['main.aqi', 'components.pm2_5', 'components.no2']]
    ], axis=1)

    # Temperature conversion (kelvin to Celsius, 'Unix to readable','time to India's Timezone' )
    df_silver['temp_celsius'] = (df_silver['main.temp']-273.15).round(2)
    df_silver['timestamp_utc'] = pd.to_datetime(df_silver['dt'], unit='s', utc=True)
    df_silver['timestamp']=df_silver['timestamp_utc'].dt.tz_convert('Asia/Kolkata')

    # drop all irrelavent column
    df_gold =df_silver.drop(columns=['main.temp','dt'])

    # remaining the column name
    df_gold.rename(columns={
        'main.humidity' : 'humidity_percent',
        'wind.speed':'wind_speed_kmph',
        'main.aqi': 'aqi_level',
        'components.pm2_5': 'pm2_5',
        'components.no2': 'no2_level'
    }, inplace=True)

    # seperate date and time column
    df_gold['date'] =df_gold['timestamp'].dt.date
    df_gold['time'] =df_gold['timestamp'].dt.time

    # drop timestamp colummn
    df_gold = df_gold.drop(columns=['timestamp'])

    # arrange column in right order
    columns_order = ['city', 'date', 'time', 'temp_celsius', 'humidity_percent', 'wind_speed_kmph', 'aqi_level', 'pm2_5', 'no2_level']
    df_gold = df_gold[columns_order]

    print("Transformation Gold dataframe prepared successfully.")
    return df_gold




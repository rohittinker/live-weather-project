import os
import pandas as pd
from sqlalchemy import create_engine, text
import config

def load_data_to_warehouse(df_gold):
    """
    City names ko dim_city se map karke city_id banata hai aur data ko fact table me load karta hai.
    """
    if df_gold.empty:
        print("No data to load.")
        return
    print("Connecting to Online TiDB Cloud Warehouse...")
    try:
        username =config.username
        password = config.password
        host = config.host
        port = config.port
        database = config.database

        engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',
                               connect_args={"ssl":{"ssl_mode":"PREFERRED"}}
                               )
        print("Connecting to Database successfully using config variables!")
        
        # Database se DIM_CITY ko READ KARNA
        print("Fetching city IDs from dim_city table...") 
        df_dim_city = pd.read_sql("Select id, name from dim_city", con=engine)

        #Yeh check krega city column hain ya nhi
        if 'city' in df_gold.columns:
            # text name ko id mein convert krna
            df_gold = pd.merge(df_gold, df_dim_city, left_on='city', right_on='name', how='inner')
        
            # 'id' column ko rename karke 'city_id' kiya
            df_gold = df_gold.rename(columns={'id':'city_id'})
        
            # drop city and name column 
            df_gold = df_gold.drop(columns=['city','name'], errors='ignore')
            
            #colummn ko naye structure (with city_id) arrange karna
            columns_order = ['city_id','date','time','temp_celsius','humidity_percent','wind_speed_kmph', 'aqi_level', 'pm2_5', 'no2_level']
            df_gold =df_gold[columns_order]
            print("Successfully mapped city_name to city_id")
        elif 'city_id' in df_gold.columns:
            print("'city_id' already processed and present. Proceeding to database insert.")
        else:
            print("Warning: Neither 'city' or 'city_id' found. Please re-run the API cells from the top.")
        
        
        #-------------------------------------------------------------------------------------------------------------
        # Safe Connection block
        #-------------------------------------------------------------------------------------------------------------
        if 'city_id' in df_gold.columns:
            #rolling 48 hours cleanup
            with engine.begin() as connection:
                print("Executing Rolling Rention Policy...")

                cleanup_query = text("Delete From fact_live_weather " \
                                    "Where date < CURDATE() - INTERVAL 1 DAY;")
                connection.execute(cleanup_query)
                print("Historical records older than 48 hours delete successfully.")

                # ab data insert bhi safely isi ke andr hoga
                df_gold.to_sql(name='fact_live_weather', con=connection, if_exists='append', index=False)
                print("Live weather data safely appened to 'fact_live_weather'.")
    except Exception as e:
        print(f" Error occured: {e}")

        
       

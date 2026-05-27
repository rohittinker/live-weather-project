
import pandas as pd
from sqlalchemy import create_engine


local_engine = create_engine("mysql+pymysql://root:8529843296@localhost:3306/weather_db")

cloud_engine = create_engine(
    "mysql+pymysql://rovBB5c3weeYxvg.root:3WwVeAxawiXFT8t9@gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com:4000/weather_db",
    connect_args={"ssl": {"ssl_mode": "PREFERRED"}}
)

print ("Data transfer shuru ho raha hai... Thoda sabra rakhein ⏳")
try:
    # A. Sabse pehle City Table copy hogi
    df_city = pd.read_sql("SELECT * FROM dim_city", local_engine)
    df_city.to_sql(name='dim_city', con=cloud_engine, if_exists='append', index=False)
    print("1. dim_city ka data cloud par load ho gaya! ✅")

    # B. Phir NASA Historical Table copy hogi
    df_nasa = pd.read_sql("SELECT * FROM dim_nasa_historical", local_engine)
    df_nasa.to_sql(name='dim_nasa_historical', con=cloud_engine, if_exists='append', index=False, chunksize=500)
    print("2. dim_nasa_historical ka data cloud par load ho gaya! ✅")

    # C. Aakhiri mein Live Weather Table copy होगी
    df_live = pd.read_sql("SELECT * FROM fact_live_weather", local_engine)

    df_live['time'] = df_live['time'].astype(str).str.split().str[-1]

    df_live.to_sql(name='fact_live_weather', con=cloud_engine, if_exists='append', index=False, chunksize=500)
    print("3. fact_live_weather ka data cloud par load ho gaya! POORA DATA LIVE HAI! 🚀")
    print(f"sara data safely load ho gaya")
except Exception as e:
    print(f"{e}")
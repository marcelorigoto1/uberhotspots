import pandas as pd

# 1. Load CSV
df = pd.read_csv("uber-raw-data-may14.csv")

# 2. convert 'Date/Time' to datetime
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# 3. create 'hour' and 'weekday' columns
df['hour'] = df['Date/Time'].dt.hour
df['weekday'] = df['Date/Time'].dt.day_name()

# 4. rename columns for consistency
df = df.rename(columns={
    'Date/Time': 'datetime',
    'Lat': 'lat',
    'Lon': 'lon',
    'Base': 'base'
})

# 5. drop unnecessary columns
df.to_csv("uber_data_clean.csv", index=False)

print('Executado com sucesso.')
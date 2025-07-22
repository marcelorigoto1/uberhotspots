# prepare_data.py

import pandas as pd

# 1. Carregar o arquivo CSV
df = pd.read_csv("uber-raw-data-may14.csv")

# 2. Converter para datetime
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# 3. Criar colunas auxiliares para análise temporal
df['hour'] = df['Date/Time'].dt.hour
df['weekday'] = df['Date/Time'].dt.day_name()

# 4. Renomear colunas para padrão Django/PostgreSQL amigável
df = df.rename(columns={
    'Date/Time': 'datetime',
    'Lat': 'lat',
    'Lon': 'lon',
    'Base': 'base'
})

# 5. Exportar para CSV limpo (para importar no banco de dados depois)
df.to_csv("uber_data_clean.csv", index=False)

print('Executado com sucesso.')
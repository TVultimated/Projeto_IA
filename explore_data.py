import pandas as pd
import os

# Caminho para os ficheiros do dataset
DATA_PATH = "archive"

# Carregar os ficheiros CSV
user_info = pd.read_csv(os.path.join(DATA_PATH, "UserInfo.csv"))
sensors_data = pd.read_csv(os.path.join(DATA_PATH, "Sensors.csv"))

# Pré-visualizar os ficheiros
print("\nPrimeiras linhas de UserInfo:")
print(user_info.head())

print("\nPrimeiras linhas de Sensors:")
print(sensors_data.head())

# Informações gerais sobre os dados
print("\nInformações de UserInfo:")
print(user_info.info())

print("\nInformações de Sensors:")
print(sensors_data.info())
import pandas as pd
import os

# Caminho para os ficheiros do dataset
DATA_PATH = "archive"

# Carregar o ficheiro de sensores
sensors_data = pd.read_csv(os.path.join(DATA_PATH, "Sensors.csv"))

# Selecionar colunas relevantes
relevant_columns = [
    'SENSORGPS_LATITUDE', 'SENSORGPS_LONGITUDE',  # GPS
    'ACCELEROMETER_X', 'ACCELEROMETER_Y', 'ACCELEROMETER_Z',  # Acelerómetro
    'GYROSCOPE_X', 'GYROSCOPE_Y', 'GYROSCOPE_Z',  # Giroscópio
    'Light_v',  # Nível de ruído (simulado pela luz)
    'Date_time'  # Data e hora
]
sensors_data = sensors_data[relevant_columns]

# Simular contexto com base em GPS (exemplo: cinema)
sensors_data['context'] = sensors_data.apply(
    lambda row: 'cinema' if 23.7960 <= row['SENSORGPS_LATITUDE'] <= 23.7980 and 
    90.3620 <= row['SENSORGPS_LONGITUDE'] <= 90.3640 else 'outro', 
    axis=1
)

# Criar rótulos (labels) com base no contexto
def generate_label(context):
    if context == 'cinema':
        return 'silenciar'
    else:
        return 'não alterar'

sensors_data['label'] = sensors_data['context'].apply(generate_label)

# Remover valores nulos (se existirem)
sensors_data.dropna(inplace=True)

# Guardar os dados limpos num novo ficheiro
OUTPUT_PATH = os.path.join(DATA_PATH, "cleaned_sensors.csv")
sensors_data.to_csv(OUTPUT_PATH, index=False)

print(f"Dados pré-processados salvos em: {OUTPUT_PATH}")
import csv
import random
from datetime import datetime, timedelta
import json
import pandas as pd

# Carregar configurações do JSON
with open("config.json", "r") as file:
    CONFIG = json.load(file)

def gerar_localizacao():
    """Gera uma localização (GPS) com base no ficheiro config.json."""
    local = random.choice(list(CONFIG["locais"].keys()))
    latitude = round(random.uniform(*CONFIG["locais"][local]["latitude"]), 6)
    longitude = round(random.uniform(*CONFIG["locais"][local]["longitude"]), 6)
    return local, latitude, longitude

def gerar_nivel_ruido(local):
    """Gera um nível de ruído com base no local."""
    ruido_min, ruido_max = CONFIG["locais"][local]["ruido"]
    ruido = random.uniform(ruido_min, ruido_max)
    if ruido < 30:
        categoria = "silencio"
    elif 30 <= ruido < 70:
        categoria = "moderado"
    else:
        categoria = "ruidoso"
    return round(ruido, 2), categoria

def gerar_movimento(local):
    """Gera movimento com base no local e acelerómetro."""
    estado = random.choice(CONFIG["locais"][local]["movimento"])
    if estado == "estatico":
        acelerometro = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 9.8 + random.uniform(-0.1, 0.1)]
    elif estado == "movimento lento":
        acelerometro = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(8, 10)]
    else:  # movimento rapido
        acelerometro = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(5, 15)]
    return estado, acelerometro

def gerar_giroscopio_aleatorio():
    """Gera dados aleatórios de giroscópio para X, Y e Z."""
    # Dados realistas para giroscópio
    gyroscope_x = round(random.uniform(-5, 5), 2)  # Eixo X do giroscópio
    gyroscope_y = round(random.uniform(-5, 5), 2)  # Eixo Y do giroscópio
    gyroscope_z = round(random.uniform(-10, 10), 2)  # Eixo Z do giroscópio
    return gyroscope_x, gyroscope_y, gyroscope_z

def gerar_orientacao_gyroscope(gyroscope_z):
    """Define a orientação do giroscópio com base no valor do eixo Z."""
    if gyroscope_z > 0:  # Qualquer valor positivo significa "virado para cima"
        return "virado para cima"
    else:  # Se for negativo ou distante de 0, indica "virado para baixo"
        return "virado para baixo"

def gerar_data_aleatoria():
    """Gera uma data/hora aleatória entre 01/01/2024 e 31/12/2024."""
    data_inicio = datetime(2024, 1, 1)
    data_fim = datetime(2024, 12, 31)
    delta = data_fim - data_inicio
    segundos_aleatorios = random.randrange(delta.days * 24 * 60 * 60)
    return data_inicio + timedelta(seconds=segundos_aleatorios)

def adicionar_outliers(dataset, num_outliers=50):
    """Adiciona outliers (valores extremos) aleatoriamente no dataset."""
    for _ in range(num_outliers):
        index = random.choice(dataset.index)
        # Adiciona outliers aos dados, como valores extremos para algumas colunas
        dataset.at[index, 'latitude'] = random.uniform(50, 100)  # Outlier em latitude
        dataset.at[index, 'longitude'] = random.uniform(-100, -50)  # Outlier em longitude
        dataset.at[index, 'noise_level'] = random.uniform(100, 200)  # Outlier em ruído
        dataset.at[index, 'acceleration_x'] = random.uniform(10, 20)  # Outlier em aceleração
        dataset.at[index, 'acceleration_y'] = random.uniform(10, 20)  # Outlier em aceleração
        dataset.at[index, 'acceleration_z'] = random.uniform(20, 30)  # Outlier em aceleração

def criar_dataset_csv(nome_arquivo="dataset_sintetico.csv", num_amostras=1000, num_outliers=50):
    """Cria um dataset sintético com os dados necessários para o projeto."""
    with open(nome_arquivo, mode="w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Cabeçalho
        writer.writerow([ 
            "id", "datetime", "location", "latitude", "longitude",
            "noise_level", "noise_category", "acceleration_x", "acceleration_y", "acceleration_z",
            "gyroscope_x", "gyroscope_y", "gyroscope_z", "gyroscope_orientation", "movement_state"
        ])
        
        for i in range(1, num_amostras + 1):
            data_criacao = gerar_data_aleatoria()
            local, latitude, longitude = gerar_localizacao()
            ruido, categoria_ruido = gerar_nivel_ruido(local)
            movimento, acelerometro = gerar_movimento(local)
            gyroscope_x, gyroscope_y, gyroscope_z = gerar_giroscopio_aleatorio()
            giroscopio_orientacao = gerar_orientacao_gyroscope(gyroscope_z)

            # Escrever no CSV
            writer.writerow([
                i, data_criacao.strftime("%Y-%m-%d %H:%M:%S"), local, latitude, longitude,
                ruido, categoria_ruido,
                acelerometro[0], acelerometro[1], acelerometro[2],
                gyroscope_x, gyroscope_y, gyroscope_z, giroscopio_orientacao, movimento
            ])

    # Criar outliers
    dataset = pd.read_csv(nome_arquivo)
    adicionar_outliers(dataset, num_outliers)
    
    # Salvar o dataset com outliers
    dataset.to_csv(nome_arquivo, index=False)
    print(f"Dataset sintético criado com sucesso: {nome_arquivo} ({num_amostras} amostras)")

if __name__ == "__main__":
    criar_dataset_csv("dataset_sintetico.csv", 1000, 50)
import csv
import random
from datetime import datetime, timedelta

def gerar_localizacao():
    """Gera uma localização (GPS) categorizada."""
    locais = {
        "cinema": {"latitude": (23.7960, 23.7980), "longitude": (90.3620, 90.3640)},
        "casa": {"latitude": (23.7950, 23.7960), "longitude": (90.3610, 90.3620)},
        "trabalho": {"latitude": (23.7980, 23.7990), "longitude": (90.3640, 90.3650)}
    }
    local = random.choice(list(locais.keys()))
    latitude = round(random.uniform(*locais[local]["latitude"]), 6)
    longitude = round(random.uniform(*locais[local]["longitude"]), 6)
    return local, latitude, longitude

def gerar_nivel_ruido():
    """Gera um nível de ruído categorizado."""
    return random.choice(["silêncio", "moderado", "ruidoso"])

def gerar_movimento():
    """Gera dados de acelerómetro e giroscópio categorizados."""
    estado = random.choice(["estático", "movimento lento", "movimento rápido"])
    if estado == "estático":
        accelerometer = [0, 0, 9.8]
        gyroscope = [0, 0, 0]
    elif estado == "movimento lento":
        accelerometer = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(8, 10)]
        gyroscope = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
    else:  # movimento rápido
        accelerometer = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(5, 15)]
        gyroscope = [random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-3, 3)]
    return estado, accelerometer, gyroscope

def gerar_evento_agenda(data):
    """Gera eventos de calendário com base no horário e local."""
    eventos = ["Reunião", "Sessão de cinema", "Trabalho", "Estudo", "Descanso"]
    probabilidade_evento = 0.5  # 50% de chance de haver um evento
    return random.choice(eventos) if random.random() < probabilidade_evento else "Nenhum evento"

def gerar_data_aleatoria():
    """Gera uma data/hora aleatória entre 01/01/2024 e 31/12/2024."""
    data_inicio = datetime(2024, 1, 1)
    data_fim = datetime(2024, 12, 31)
    delta = data_fim - data_inicio
    segundos_aleatorios = random.randrange(delta.days * 24 * 60 * 60)
    return data_inicio + timedelta(seconds=segundos_aleatorios)

def criar_dataset_csv(nome_arquivo="dataset_sintetico.csv", num_amostras=1000):
    """Cria um dataset sintético com os dados necessários para o projeto."""
    with open(nome_arquivo, mode="w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Cabeçalho
        writer.writerow([
            "id", "datetime", "location", "latitude", "longitude",
            "noise_level", "movement_state",
            "acceleration_x", "acceleration_y", "acceleration_z",
            "gyroscope_x", "gyroscope_y", "gyroscope_z", "calendar_event"
        ])

        for i in range(1, num_amostras + 1):  # ID começa em 1 e vai até num_amostras
            # Gerar dados
            data_criacao = gerar_data_aleatoria()
            local, latitude, longitude = gerar_localizacao()
            nivel_ruido = gerar_nivel_ruido()
            movimento, accelerometer, gyroscope = gerar_movimento()
            evento = gerar_evento_agenda(data_criacao)

            # Escrever no CSV
            writer.writerow([
                i, data_criacao.strftime("%Y-%m-%d %H:%M:%S"), local, latitude, longitude,
                nivel_ruido, movimento,
                accelerometer[0], accelerometer[1], accelerometer[2],
                gyroscope[0], gyroscope[1], gyroscope[2], evento
            ])

    print(f"Dataset sintético criado com sucesso: {nome_arquivo} ({num_amostras} amostras)")

if __name__ == "__main__":
    criar_dataset_csv("dataset_sintetico.csv", 1000)
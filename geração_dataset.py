import csv
import random
from datetime import datetime, timedelta

def gerar_localizacao():
    """Gera uma localização (GPS) categorizada."""
    locais = {
        "cinema": {"latitude": (23.7960, 23.7980), "longitude": (90.3620, 90.3640)},
        "casa": {"latitude": (23.7950, 23.7960), "longitude": (90.3610, 90.3620)},
        "trabalho": {"latitude": (23.7980, 23.7990), "longitude": (90.3640, 90.3650)},
        "parque": {"latitude": (23.7990, 23.8000), "longitude": (90.3650, 90.3660)},
        "centro comercial": {"latitude": (23.8000, 23.8010), "longitude": (90.3660, 90.3670)},
        "restaurante": {"latitude": (23.8010, 23.8020), "longitude": (90.3670, 90.3680)},
        "escola": {"latitude": (23.8020, 23.8030), "longitude": (90.3680, 90.3690)},
        "universidade": {"latitude": (23.8030, 23.8040), "longitude": (90.3690, 90.3700)},
        "ginásio": {"latitude": (23.8040, 23.8050), "longitude": (90.3700, 90.3710)},
        "igreja": {"latitude": (23.8050, 23.8060), "longitude": (90.3710, 90.3720)},
        "praia": {"latitude": (23.8060, 23.8070), "longitude": (90.3720, 90.3730)},
        "hospital": {"latitude": (23.8070, 23.8080), "longitude": (90.3730, 90.3740)},
        "biblioteca": {"latitude": (23.8080, 23.8090), "longitude": (90.3740, 90.3750)},
        "museu": {"latitude": (23.8090, 23.8100), "longitude": (90.3750, 90.3760)},
        "teatro": {"latitude": (23.8100, 23.8110), "longitude": (90.3760, 90.3770)},
        "auditório": {"latitude": (23.8110, 23.8120), "longitude": (90.3770, 90.3780)},
        "loja": {"latitude": (23.8120, 23.8130), "longitude": (90.3780, 90.3790)},
        "farmácia": {"latitude": (23.8130, 23.8140), "longitude": (90.3790, 90.3800)},
        "estação": {"latitude": (23.8140, 23.8150), "longitude": (90.3800, 90.3810)},
        "aeroporto": {"latitude": (23.8150, 23.8160), "longitude": (90.3810, 90.3820)},
    }
    local = random.choice(list(locais.keys()))
    latitude = round(random.uniform(*locais[local]["latitude"]), 6)
    longitude = round(random.uniform(*locais[local]["longitude"]), 6)
    return local, latitude, longitude

def gerar_nivel_ruido():
    """Gera um nível de ruído como número e categoriza."""
    ruido = random.uniform(0, 100)  # Nível de ruído em decibéis
    if ruido < 30:
        categoria = "silêncio"
    elif 30 <= ruido < 70:
        categoria = "moderado"
    else:
        categoria = "ruidoso"
    return round(ruido, 2), categoria

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

def gerar_evento_agenda():
    """Gera eventos de calendário entre várias opções."""
    eventos = [
        "Reunião", "Sessão de cinema", "Trabalho", "Estudo", "Descanso",
        "Consulta médica", "Jantar com amigos", "Viagem de negócios", "Aniversário",
        "Apresentação", "Conferência", "Treino", "Compras", "Entrega de trabalho",
        "Exame", "Lazer", "Passeio", "Voluntariado", "Entrevista", "Manutenção"
    ]
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
            "noise_level", "noise_category", "movement_state",
            "acceleration_x", "acceleration_y", "acceleration_z",
            "gyroscope_x", "gyroscope_y", "gyroscope_z", "calendar_event"
        ])

        for i in range(1, num_amostras + 1):
            # Gerar dados
            data_criacao = gerar_data_aleatoria()
            local, latitude, longitude = gerar_localizacao()
            ruido, categoria_ruido = gerar_nivel_ruido()
            movimento, accelerometer, gyroscope = gerar_movimento()
            evento = gerar_evento_agenda()

            # Escrever no CSV
            writer.writerow([
                i, data_criacao.strftime("%Y-%m-%d %H:%M:%S"), local, latitude, longitude,
                ruido, categoria_ruido, movimento,
                accelerometer[0], accelerometer[1], accelerometer[2],
                gyroscope[0], gyroscope[1], gyroscope[2], evento
            ])

    print(f"Dataset sintético criado com sucesso: {nome_arquivo} ({num_amostras} amostras)")

if __name__ == "__main__":
    criar_dataset_csv("dataset_sintetico.csv", 1000)
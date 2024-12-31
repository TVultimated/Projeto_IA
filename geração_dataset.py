import csv
import random
from datetime import datetime, timedelta

def gerar_localizacao():
    """Gera uma localização (GPS) categorizada."""
    locais = {
        "Cinema NOS Colombo": {"latitude": (38.7513, 38.7514), "longitude": (-9.1974, -9.1973)},
        "Casa": {"latitude": (38.7151, 38.7153), "longitude": (-9.1603, -9.1601)},
        "Escritório": {"latitude": (38.7369, 38.7371), "longitude": (-9.1398, -9.1396)},
        "Parque Eduardo VII": {"latitude": (38.7108, 38.7110), "longitude": (-9.1374, -9.1372)},
        "Amoreiras Shopping": {"latitude": (38.7277, 38.7279), "longitude": (-9.1638, -9.1636)},
        "Restaurante Portugália (Av. Almirante Reis)": {"latitude": (38.7323, 38.7325), "longitude": (-9.1291, -9.1290)},
        "Escola Secundária Rainha Dona Amélia": {"latitude": (38.7436, 38.7438), "longitude": (-9.1832, -9.1830)},
        "Universidade Autónoma de Lisboa": {"latitude": (38.7165, 38.7167), "longitude": (-9.1452, -9.1450)},
        "Ginásio Lemonfit Olaias": {"latitude": (38.7430, 38.7432), "longitude": (-9.1250, -9.1248)},
        "Sé de Lisboa": {"latitude": (38.7223, 38.7225), "longitude": (-9.1393, -9.1391)},
        "Praia": {"latitude": (38.6916, 38.6918), "longitude": (-9.2160, -9.2158)},
        "Hospital da Luz": {"latitude": (38.7516, 38.7518), "longitude": (-9.2033, -9.2031)},
        "Biblioteca Nacional de Portugal": {"latitude": (38.7380, 38.7382), "longitude": (-9.1622, -9.1620)},
        "Museu de Belém": {"latitude": (38.6912, 38.6914), "longitude": (-9.2166, -9.2164)},
        "Teatro Politeama": {"latitude": (38.7101, 38.7103), "longitude": (-9.1379, -9.1377)},
        "Auditório Camões": {"latitude": (38.7242, 38.7244), "longitude": (-9.1501, -9.1499)},
        "Bertrand do Chiado": {"latitude": (38.7106, 38.7108), "longitude": (-9.1398, -9.1396)},
        "Farmácia Benfica": {"latitude": (38.7396, 38.7398), "longitude": (-9.1656, -9.1654)},
        "Estação do Rossio": {"latitude": (38.7322, 38.7324), "longitude": (-9.1418, -9.1416)},
        "Aeroporto Humberto Delgado": {"latitude": (38.7680, 38.7682), "longitude": (-9.1288, -9.1286)},
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

        # Dentro do loop principal que gera os dados
        for i in range(1, num_amostras + 1):
            # Gerar dados
            data_criacao = gerar_data_aleatoria()
            local, latitude, longitude = gerar_localizacao()
            ruido, categoria_ruido = gerar_nivel_ruido()
            movimento, accelerometer, gyroscope = gerar_movimento()

            # Escrever no CSV
            writer.writerow([
                i, data_criacao.strftime("%Y-%m-%d %H:%M:%S"), local, latitude, longitude,
                ruido, categoria_ruido, movimento,
                accelerometer[0], accelerometer[1], accelerometer[2],
                gyroscope[0], gyroscope[1], gyroscope[2]
            ])

    print(f"Dataset sintético criado com sucesso: {nome_arquivo} ({num_amostras} amostras)")

if __name__ == "__main__":
    criar_dataset_csv("dataset_sintetico.csv", 1000)
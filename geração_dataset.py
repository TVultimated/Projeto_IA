import csv
import random
import json
import pandas as pd

# Carregar configurações do JSON
with open("config.json", "r") as file:
    CONFIG = json.load(file)

def gerar_localizacao():
    """Gera uma localização aleatória com base no ficheiro config.json."""
    return random.choice([local for categoria in CONFIG["categorias_de_locais"].values() for local in categoria])

def gerar_nivel_ruido():
    """Gera um nível de ruído com base nos padrões gerais."""
    ruido_min, ruido_max = CONFIG["padroes_gerais"]["ruido"]["silencio"][0], CONFIG["padroes_gerais"]["ruido"]["ruidoso"][1]
    ruido = random.uniform(ruido_min, ruido_max)
    if ruido < CONFIG["padroes_gerais"]["ruido"]["silencio"][1]:
        categoria = "silencio"
    elif ruido < CONFIG["padroes_gerais"]["ruido"]["moderado"][1]:
        categoria = "moderado"
    else:
        categoria = "ruidoso"
    return round(ruido, 2), categoria

def gerar_movimento():
    """Gera um estado de movimento com base nos padrões gerais."""
    movimento = random.choice(list(CONFIG["padroes_gerais"]["movimento"].keys()))
    if movimento == "estatico":
        acelerometro = [random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), 9.8 + random.uniform(-0.2, 0.2)]
    elif movimento == "movimento lento":
        acelerometro = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), random.uniform(8, 10)]
    else:  # movimento rapido
        acelerometro = [random.uniform(-5.5, 5.5), random.uniform(-5.5, 5.5), random.uniform(5, 15)]
    return movimento, acelerometro

def gerar_giroscopio_aleatorio():
    """Gera dados aleatórios de giroscópio para X, Y e Z."""
    gyroscope_x = round(random.uniform(-5, 5), 2) + random.uniform(-0.1, 0.1)
    gyroscope_y = round(random.uniform(-5, 5), 2) + random.uniform(-0.1, 0.1)
    gyroscope_z = round(random.uniform(-10, 10), 2) + random.uniform(-0.1, 0.1)
    return gyroscope_x, gyroscope_y, gyroscope_z

def gerar_orientacao_gyroscope(gyroscope_z):
    """Define a orientação do giroscópio com base no valor do eixo Z."""
    if gyroscope_z > 0:  # Qualquer valor positivo significa "virado para cima"
        return "virado para cima"
    else:  # Se for negativo ou distante de 0, indica "virado para baixo"
        return "virado para baixo"

def determinar_estado(local, ruido_categoria, movimento, giroscopio):
    categorias_locais = CONFIG["categorias_de_locais"]

    # Identificar a categoria do local
    categoria_local = next(
        (categoria for categoria, locais in categorias_locais.items() if local in locais),
        "Desconhecido"
    )

    # Lógica de decisão
    if categoria_local in ["Religioso", "Educacional", "Entretenimento", "Saude", "Conferencias"] and ruido_categoria == "silencio" and movimento == "estatico" and giroscopio == "virado para baixo":
        return "desligar"
    elif (ruido_categoria in ["silencio", "moderado"] and movimento in ["estatico", "movimento lento"]):
        return "silenciar"
    else:
        return "não alterar"


def criar_dataset_csv(nome_arquivo="dataset_sintetico.csv", num_amostras_por_estado=3000):
    """Cria um dataset com distribuição balanceada entre os estados."""
    estados_possiveis = ["desligar", "silenciar", "não alterar"]
    contadores = {estado: 0 for estado in estados_possiveis}
    amostras_geradas = set()  # Para evitar duplicados
    limite_total = num_amostras_por_estado * len(estados_possiveis)

    with open(nome_arquivo, mode="w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Cabeçalho
        writer.writerow([
            "id", "location", "noise_level", "noise_category",
            "acceleration_x", "acceleration_y", "acceleration_z",
            "gyroscope_x", "gyroscope_y", "gyroscope_z",
            "gyroscope_orientation", "movement_state", "estado"
        ])

        id_amostra = 1  # Contador de IDs para as amostras

        while sum(contadores.values()) < limite_total:  # Continuar até atingir o número total de amostras
            local = gerar_localizacao()
            ruido, categoria_ruido = gerar_nivel_ruido()
            movimento, acelerometro = gerar_movimento()
            gyroscope_x, gyroscope_y, gyroscope_z = gerar_giroscopio_aleatorio()
            giroscopio_orientacao = gerar_orientacao_gyroscope(gyroscope_z)
            estado = determinar_estado(local, categoria_ruido, movimento, giroscopio_orientacao)

            # Garantir que não excedemos o número desejado por estado
            if estado and contadores[estado] < num_amostras_por_estado:
                # Gerar hash único da amostra para evitar duplicados
                amostra_hash = hash((local, ruido, categoria_ruido, tuple(acelerometro), gyroscope_x, gyroscope_y, gyroscope_z, estado))

                if amostra_hash not in amostras_geradas:
                    # Adicionar a amostra ao conjunto para evitar duplicados
                    amostras_geradas.add(amostra_hash)

                    # Escrever a amostra no CSV
                    writer.writerow([
                        id_amostra, local, ruido, categoria_ruido,
                        acelerometro[0], acelerometro[1], acelerometro[2],
                        gyroscope_x, gyroscope_y, gyroscope_z, giroscopio_orientacao, movimento, estado
                    ])
                    contadores[estado] += 1
                    id_amostra += 1

    print(f"Dataset criado com sucesso: {nome_arquivo}")
    print(f"Distribuição final: {contadores}")

if __name__ == "__main__":
    criar_dataset_csv("dataset_sintetico.csv", num_amostras_por_estado=3000)
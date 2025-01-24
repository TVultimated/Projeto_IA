import os
import json
import pandas as pd
from datetime import datetime
from sklearn.metrics import classification_report
from Models import model_cnn, model_logistic, model_nn, model_rf

# Carregar configuração inicial
def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

# Selecionar e carregar o modelo
MODELS = {
    'cnn': model_cnn,
    'logistic': model_logistic,
    'nn': model_nn,
    'rf': model_rf
}

def load_model(model_name):
    if model_name in MODELS:
        return MODELS[model_name]
    else:
        raise ValueError(f"Modelo '{model_name}' não encontrado. Escolha entre: {list(MODELS.keys())}")

# Função para reaplicar o modelo
# Simula a aplicação do modelo com resultados fictícios
# Adiciona uma coluna "Prediction" ao dataset para representar o resultado
def apply_model(input_data, model_name):
    print(f"Executando o modelo '{model_name}' com o dataset atualizado...")
    input_data = input_data.copy()
    if model_name == 'cnn':
        input_data['Prediction'] = input_data['noise_level'] * 1.1  # Exemplo fictício
    elif model_name == 'logistic':
        input_data['Prediction'] = input_data['noise_level'] * 0.9
    elif model_name == 'nn':
        input_data['Prediction'] = input_data['noise_level'] * 1.05
    elif model_name == 'rf':
        input_data['Prediction'] = input_data['noise_level'] * 0.95
    else:
        input_data['Prediction'] = 0  # Caso o modelo não seja identificado
    return input_data[['id', 'estado', 'Prediction']]

# Função para validar entradas
def validate_input(prompt, expected_type, options=None):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Valor não pode estar vazio. Tente novamente.")
            continue
        if options and value not in options:
            print(f"Entrada inválida. Escolha entre: {', '.join(options)}. Tente novamente.")
            continue
        try:
            if expected_type == float:
                return float(value)
            elif expected_type == int:
                return int(value)
            else:
                return value
        except ValueError:
            print(f"Entrada inválida. Esperava um valor do tipo {expected_type.__name__}. Tente novamente.")

# Função para limpar dados inválidos do dataset
def clean_dataset(dataset):
    numeric_columns = ['latitude', 'longitude', 'noise_level', 'acceleration_x', 'acceleration_y',
                       'acceleration_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z']
    for column in numeric_columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')
    dataset = dataset.dropna()
    return dataset

# Função para obter novos dados do utilizador
def get_user_data(existing_data):
    new_data = []
    next_id = existing_data['id'].max() + 1 if not existing_data.empty else 1

    # Obter categorias únicas do dataset
    noise_categories = existing_data['noise_category'].dropna().unique().tolist()
    movement_states = existing_data['movement_state'].dropna().unique().tolist()
    estados = existing_data['estado'].dropna().unique().tolist()
    gyro_orientations = existing_data['gyroscope_orientation'].dropna().unique().tolist()

    print("Insira novos dados (deixe em branco para não adicionar mais entradas):")
    while True:
        data_entry = {
            'id': next_id,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'location': input("Localização: ").strip(),
            'latitude': validate_input("Latitude: ", float),
            'longitude': validate_input("Longitude: ", float),
            'noise_level': validate_input("Nível de ruído (em decibéis): ", int),
            'noise_category': validate_input(f"Categoria de ruído ({', '.join(noise_categories)}): ", str, noise_categories),
            'acceleration_x': validate_input("Aceleração X: ", float),
            'acceleration_y': validate_input("Aceleração Y: ", float),
            'acceleration_z': validate_input("Aceleração Z: ", float),
            'gyroscope_x': validate_input("Giroscópio X: ", float),
            'gyroscope_y': validate_input("Giroscópio Y: ", float),
            'gyroscope_z': validate_input("Giroscópio Z: ", float),
            'gyroscope_orientation': validate_input(f"Orientação do giroscópio ({', '.join(gyro_orientations)}): ", str, gyro_orientations),
            'movement_state': validate_input(f"Estado de movimento ({', '.join(movement_states)}): ", str, movement_states),
            'estado': validate_input(f"Estado ({', '.join(estados)}): ", str, estados)
        }

        new_data.append(data_entry)
        next_id += 1

        add_more = input("Deseja adicionar mais entradas? (s/n): ").strip().lower()
        if add_more != 's':
            break

    return pd.DataFrame(new_data)

# Interface principal
def main():
    print("Bem-vindo à interface do projeto de IA!")

    # Carregar configuração
    config = load_config('config.json')
    dataset_path = config.get('dataset_path', 'dataset_sintetico.csv')

    # Loop contínuo até o utilizador decidir parar
    while True:
        # Validar modelo escolhido
        model_name = None
        while model_name not in MODELS:
            model_name = input(f"Escolha o modelo ({', '.join(MODELS.keys())}): ").strip().lower()
            if model_name not in MODELS:
                print(f"Modelo inválido. Escolha entre: {', '.join(MODELS.keys())}.")

        # Carregar dataset
        try:
            if os.path.exists(dataset_path):
                dataset = pd.read_csv(dataset_path)
            else:
                dataset = pd.DataFrame(columns=[
                    'id', 'datetime', 'location', 'latitude', 'longitude', 'noise_level', 'noise_category',
                    'acceleration_x', 'acceleration_y', 'acceleration_z',
                    'gyroscope_x', 'gyroscope_y', 'gyroscope_z', 'gyroscope_orientation',
                    'movement_state', 'estado'
                ])
            print(f"Dataset '{dataset_path}' carregado com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar o dataset: {e}")
            return

        # Exibir informações iniciais do dataset
        print("\nDistribuição das classes:")
        print(dataset['estado'].value_counts())
        print("\nDimensões dos dados:")
        print(f"X shape: {dataset.shape}")

        # Obter novos dados do utilizador
        new_data = get_user_data(dataset)
        if not new_data.empty:
            dataset = pd.concat([dataset, new_data], ignore_index=True)
            dataset.to_csv(dataset_path, index=False)
            print("Novos dados adicionados ao dataset.")

        # Limpar dados inválidos
        dataset = clean_dataset(dataset)
        if dataset.empty:
            print("Erro: Todos os dados são inválidos após limpeza. Verifique os inputs.")
            return

        # Reaplicar o modelo
        try:
            results = apply_model(dataset, model_name)
            print("Resultados do modelo:")
            print(results)

            # Gerar relatório fictício de classificação
            print("\nRelatório de Classificação:")
            fake_labels = dataset['estado'].sample(len(dataset), replace=True).values
            fake_predictions = results['Prediction'].apply(lambda x: 'silenciar' if x < 50 else 'não alterar').values
            print(classification_report(fake_labels, fake_predictions))

        except Exception as e:
            print(f"Erro durante o processamento: {e}")

        # Perguntar se o utilizador deseja continuar
        continue_program = input("Deseja continuar? (s/n): ").strip().lower()
        if continue_program != 's':
            print("Encerrando o programa.")
            break

if __name__ == "__main__":
    main()

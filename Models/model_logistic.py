import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def train_model(data):
    print("Iniciando treinamento do modelo de Regressão Logística...")

    # 1. Selecionar features sensoriais
    selected_features = [
        'latitude', 'longitude',
        'acceleration_x', 'acceleration_y', 'acceleration_z',
        'gyroscope_x', 'gyroscope_y', 'gyroscope_z',
        'noise_level'
    ]

    if not all(feature in data.columns for feature in selected_features):
        raise ValueError("O dataset não contém todas as features necessárias para o treinamento.")

    # 2. Preparar dados
    X = data[selected_features]
    y = data['estado']

    # 3. Normalizar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Preparar target
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # 5. Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, 
        y_encoded,
        test_size=0.2, 
        random_state=42,
        stratify=y_encoded
    )

    # 6. Criar e treinar modelo de Regressão Logística
    logistic_model = LogisticRegression(max_iter=200, random_state=42)
    logistic_model.fit(X_train, y_train)

    # 7. Avaliar modelo
    y_pred = logistic_model.predict(X_test)

    print('\nRelatório de Classificação:')
    print(classification_report(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nPrecisão final do modelo: {accuracy:.4f}")

    # Retornar previsões para integração com a interface
    return pd.DataFrame({
        'id': data['id'].iloc[X_test.shape[0] * -1:].values,  # Últimas IDs do conjunto de teste
        'Prediction': label_encoder.inverse_transform(y_pred)
    })

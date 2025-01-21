# model_logistic.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.utils import to_categorical

# 1. Carregar o dataset
print("Carregando dados...")
data = pd.read_csv('../dataset_sintetico.csv')

# 2. Selecionar features sensoriais
selected_features = [
    'latitude', 'longitude',
    'acceleration_x', 'acceleration_y', 'acceleration_z',
    'gyroscope_x', 'gyroscope_y', 'gyroscope_z',
    'noise_level'
]

# 3. Preparar dados
X = data[selected_features]
y = data['estado']

# 4. Análise inicial dos dados
print("\nDistribuição das classes:")
print(y.value_counts())
print("\nDimensões dos dados:")
print(f"X shape: {X.shape}")

# 5. Normalizar features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Preparar target
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 7. Dividir dados
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, 
    y_encoded,
    test_size=0.2, 
    random_state=42,
    stratify=y_encoded
)

# 8. Criar e treinar modelo Regressão Logística
logistic_model = LogisticRegression(max_iter=200, random_state=42)
logistic_model.fit(X_train, y_train)

# 9. Avaliar modelo
y_pred = logistic_model.predict(X_test)

print('\nRelatório de Classificação:')
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print(f"\nPrecisão final do modelo: {accuracy:.4f}")

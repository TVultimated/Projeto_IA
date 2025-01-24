# model_rf.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.utils import to_categorical

# 1. Carregar o dataset
print("Carregando dados...")
data = pd.read_csv('dataset_sintetico.csv')  

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
y_categorical = to_categorical(y_encoded)

# 7. Dividir dados
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, 
    y_categorical, 
    test_size=0.2, 
    random_state=42,
    stratify=y_encoded
)

# 8. Criar e treinar modelo Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 9. Avaliar modelo
y_pred = rf_model.predict(X_test)

# Converter para labels originais
y_pred_labels = label_encoder.inverse_transform(np.argmax(y_pred, axis=1))
y_test_labels = label_encoder.inverse_transform(np.argmax(y_test, axis=1))

print('\nRelatório de Classificação:')
print(classification_report(y_test_labels, y_pred_labels))

accuracy = accuracy_score(y_test_labels, y_pred_labels)
print(f"\nPrecisão final do modelo: {accuracy:.4f}")
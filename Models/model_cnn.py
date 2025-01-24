import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, accuracy_score

def train_model(data):
    print("Iniciando treinamento do modelo CNN...")

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
    y_categorical = to_categorical(y_encoded)

    # 5. Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y_categorical,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    # 6. Criar e compilar o modelo CNN
    def create_cnn_model():
        model = Sequential([
            Conv1D(64, 3, activation='relu', input_shape=(X_train.shape[1], 1)),
            MaxPooling1D(2),
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(y_categorical.shape[1], activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    # 7. Reshape para 1D para entrada na CNN
    X_train_cnn = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_cnn = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # 8. Treinamento do modelo CNN
    cnn_model = create_cnn_model()
    cnn_model.fit(
        X_train_cnn,
        y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )

    # 9. Avaliar o modelo CNN
    y_pred = cnn_model.predict(X_test_cnn)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)

    # Converter para labels originais
    y_pred_labels = label_encoder.inverse_transform(y_pred_classes)
    y_test_labels = label_encoder.inverse_transform(y_test_classes)

    print('\nRelatório de Classificação:')
    print(classification_report(y_test_labels, y_pred_labels))

    accuracy = accuracy_score(y_test_labels, y_pred_labels)
    print(f"\nPrecisão final do modelo: {accuracy:.4f}")

    # Retornar previsões para integração com a interface
    return pd.DataFrame({
        'id': data['id'].iloc[X_test_cnn.reshape(-1, X_test.shape[0]).astype(int).flatten()].values,
        'Prediction': y_pred_labels
    })

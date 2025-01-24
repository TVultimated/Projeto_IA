import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report, accuracy_score

def train_model(data):
    print("Iniciando treinamento do modelo Neural Network...")

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

    # 6. Configurar callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    # 7. Criar e compilar modelo
    def create_model():
        model = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer=l2(0.01)),
            Dropout(0.3),
            Dense(32, activation='relu', kernel_regularizer=l2(0.01)),
            Dropout(0.3),
            Dense(y_categorical.shape[1], activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    # 8. Treinar modelo com validação cruzada
    n_splits = 5
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    cv_scores = []

    for fold, (train_idx, val_idx) in enumerate(kfold.split(X_scaled)):
        print(f'\nFold {fold + 1}/{n_splits}')

        # Preparar dados do fold
        X_train_fold = X_scaled[train_idx]
        y_train_fold = y_categorical[train_idx]
        X_val_fold = X_scaled[val_idx]
        y_val_fold = y_categorical[val_idx]

        # Criar e treinar modelo
        model = create_model()
        model.fit(
            X_train_fold,
            y_train_fold,
            epochs=20,
            batch_size=32,
            validation_data=(X_val_fold, y_val_fold),
            callbacks=[early_stopping],
            verbose=1
        )

        # Avaliar modelo
        score = model.evaluate(X_val_fold, y_val_fold, verbose=0)
        cv_scores.append(score[1])

    print(f'\nMédia da precisão na validação cruzada: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})')

    # 9. Treinar modelo final
    print('\nTreinando modelo final...')
    final_model = create_model()
    final_model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=1
    )

    # 10. Avaliar modelo final
    y_pred = final_model.predict(X_test)
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
        'id': data['id'].iloc[X_test.shape[0] * -1:].values,
        'Prediction': y_pred_labels
    })
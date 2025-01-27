import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, auc
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar o dataset
data = pd.read_csv('dataset_sintetico.csv')

# 2. Selecionar features sensoriais e categóricas
selected_features = [
    'location',
    'noise_level', 'noise_category',
    'acceleration_x', 'acceleration_y', 'acceleration_z',
    'gyroscope_x', 'gyroscope_y', 'gyroscope_z',
    'gyroscope_orientation', 'movement_state'
]

X = data[selected_features]

# 3. Codificar as features categóricas
location_encoder = LabelEncoder()
noise_category_encoder = LabelEncoder()
gyroscope_orientation_encoder = LabelEncoder()
movement_state_encoder = LabelEncoder()

X['location'] = location_encoder.fit_transform(X['location'])
X['noise_category'] = noise_category_encoder.fit_transform(X['noise_category'])
X['gyroscope_orientation'] = gyroscope_orientation_encoder.fit_transform(X['gyroscope_orientation'])
X['movement_state'] = movement_state_encoder.fit_transform(X['movement_state'])

y = data['estado']
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 5. Treinar o modelo Random Forest
print("Treinando o modelo Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf_model.fit(X_train, y_train)

# 6. Avaliar o modelo
y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)

print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 7. Matriz de confusão
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel("Previsão")
plt.ylabel("Verdadeiro")
plt.title("Matriz de Confusão")
plt.show()

# 8. Curva ROC e AUC para múltiplas classes
plt.figure(figsize=(10, 8))
ohe = OneHotEncoder()
y_test_ohe = ohe.fit_transform(y_test.reshape(-1, 1)).toarray()

for i, class_name in enumerate(label_encoder.classes_):
    fpr, tpr, _ = roc_curve(y_test_ohe[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'Classe {class_name} (AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('Falso Positivo')
plt.ylabel('Taxa de Verdadeiro Positivo')
plt.title('Curva ROC para Múltiplas Classes')
plt.legend(loc='lower right')
plt.show()

# 9. Importância das Features
importancias = rf_model.feature_importances_
indices = np.argsort(importancias)[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(X.shape[1]), importancias[indices], align="center")
plt.xticks(range(X.shape[1]), [selected_features[i] for i in indices], rotation=45, ha='right')
plt.xlabel('Features')
plt.ylabel('Importância')
plt.title('Importância das Features no Random Forest')
plt.tight_layout()
plt.show()


# 10. Função para prever novos dados
def prever_novos_dados_rf(novos_dados, modelo, location_encoder, noise_category_encoder,
                          gyroscope_orientation_encoder, movement_state_encoder):
    """
    Recebe novos dados, processa e retorna previsões, considerando o contexto.
    """
    # Garantir que as classes desconhecidas sejam tratadas
    for col, encoder in zip(
        ['location', 'noise_category', 'gyroscope_orientation', 'movement_state'],
        [location_encoder, noise_category_encoder, gyroscope_orientation_encoder, movement_state_encoder]
    ):
        classes_conhecidas = encoder.classes_
        novos_dados[col] = novos_dados[col].apply(
            lambda x: x if x in classes_conhecidas else "Desconhecido"
        )
        if "Desconhecido" not in classes_conhecidas:
            encoder.classes_ = np.append(encoder.classes_, "Desconhecido")

    # Codificar as features categóricas
    novos_dados.loc[:, 'location'] = location_encoder.transform(novos_dados['location'])
    novos_dados.loc[:, 'noise_category'] = noise_category_encoder.transform(novos_dados['noise_category'])
    novos_dados.loc[:, 'gyroscope_orientation'] = gyroscope_orientation_encoder.transform(novos_dados['gyroscope_orientation'])
    novos_dados.loc[:, 'movement_state'] = movement_state_encoder.transform(novos_dados['movement_state'])

    # Fazer previsões
    previsoes = modelo.predict(novos_dados)
    previsoes_labels = label_encoder.inverse_transform(previsoes)

    return previsoes_labels

# Função para solicitar dados de entrada na consola
def obter_dados_input():
    print("\nInsira os dados para previsão:")
    location = input("Localização: ")
    noise_level = float(input("Nível de ruído: "))
    noise_category = input("Categoria de ruído: ")
    acceleration_x = float(input("Aceleração em X: "))
    acceleration_y = float(input("Aceleração em Y: "))
    acceleration_z = float(input("Aceleração em Z: "))
    gyroscope_x = float(input("Giroscópio em X: "))
    gyroscope_y = float(input("Giroscópio em Y: "))
    gyroscope_z = float(input("Giroscópio em Z: "))
    gyroscope_orientation = input("Orientação do giroscópio: ")
    movement_state = input("Estado de movimento: ")

    novos_dados = pd.DataFrame({
        'location': [location],
        'noise_level': [noise_level],
        'noise_category': [noise_category],
        'acceleration_x': [acceleration_x],
        'acceleration_y': [acceleration_y],
        'acceleration_z': [acceleration_z],
        'gyroscope_x': [gyroscope_x],
        'gyroscope_y': [gyroscope_y],
        'gyroscope_z': [gyroscope_z],
        'gyroscope_orientation': [gyroscope_orientation],
        'movement_state': [movement_state]
    })

    return novos_dados

# Solicitar dados de entrada do usuário
novos_dados_entrada = obter_dados_input()

# Prever com os novos dados inseridos
previsao = prever_novos_dados_rf(
    novos_dados_entrada, rf_model, location_encoder, noise_category_encoder,
    gyroscope_orientation_encoder, movement_state_encoder
)

print("\nPrevisão para os dados inseridos:")
print(previsao)
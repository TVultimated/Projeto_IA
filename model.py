import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, accuracy_score

# Carregar o dataset
data = pd.read_csv('dataset_sintetico.csv')

# Leitura do dataset inicial
def explore_data(data):
    print("Visualização inicial dos dados:")
    print(data.head())
    print("\nInformações gerais:")
    print(data.info())
    print("\nDistribuição das classes:")
    print(data['estado'].value_counts())

explore_data(data)

# Separação entre características (X) e rótulos (y)
X = data.drop(columns=['estado','datetime']) 
y = data['estado']

# Transformar categorias em números
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

categorical_columns = X.select_dtypes(include=['object']).columns

onehot_encoder = OneHotEncoder(sparse_output=False)
encoded_categorical_data = onehot_encoder.fit_transform(X[categorical_columns])
X = X.drop(columns=categorical_columns)
X = pd.concat([X.reset_index(drop=True), pd.DataFrame(encoded_categorical_data)], axis=1)

X.columns = X.columns.astype(str)

# One-hot encoding para as saídas
y_categorical = to_categorical(y)

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42) #random_state permite uma divisão consistente

# Normalização dos dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Construção do modelo de rede neural
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')  # 3 classes e ativação softmax
])

# Compilar o modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinamento do modelo
model.fit(X_train, y_train, epochs=20)

# Avaliação do modelo
y_pred = model.predict(X_test)
y_pred_labels = y_pred.argmax(axis=1)
y_test_labels = y_test.argmax(axis=1)

print("Relatório de Classificação:\n", classification_report(y_test_labels, y_pred_labels))
accuracy = accuracy_score(y_test_labels, y_pred_labels)
print(f"Precisão do modelo: {accuracy:.2f}")
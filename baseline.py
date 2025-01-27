import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar o dataset
data = pd.read_csv('dataset_sintetico.csv')

# 2. Pré-processamento
selected_features = ['location', 'noise_level', 'noise_category', 'acceleration_x', 
                     'acceleration_y', 'acceleration_z', 'gyroscope_x', 
                     'gyroscope_y', 'gyroscope_z', 'gyroscope_orientation', 'movement_state']

X = data[selected_features]
y = data['estado']

label_encoder = LabelEncoder()

X['location'] = LabelEncoder().fit_transform(X['location'])
X['noise_category'] = LabelEncoder().fit_transform(X['noise_category'])
X['gyroscope_orientation'] = LabelEncoder().fit_transform(X['gyroscope_orientation'])
X['movement_state'] = LabelEncoder().fit_transform(X['movement_state'])

y_encoded = label_encoder.fit_transform(y)

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 3. Baseline - Random
print("\nBaseline: Random")
dummy_random = DummyClassifier(strategy="uniform", random_state=42)
dummy_random.fit(X_train, y_train)
y_dummy_random = dummy_random.predict(X_test)

print("\nRelatório de Classificação - Random:")
print(classification_report(y_test, y_dummy_random, target_names=label_encoder.classes_))

# 4. Baseline - Logistic Regression
print("\nBaseline: Logistic Regression")
logistic_model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
logistic_model.fit(X_train, y_train)
y_logistic = logistic_model.predict(X_test)

print("\nRelatório de Classificação - Logistic Regression:")
print(classification_report(y_test, y_logistic, target_names=label_encoder.classes_))

# 5. Matriz de confusão para Logistic Regression
conf_matrix = confusion_matrix(y_test, y_logistic)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel("Previsão")
plt.ylabel("Verdadeiro")
plt.title("Matriz de Confusão - Logistic Regression")
plt.show()
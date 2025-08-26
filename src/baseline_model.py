import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, hamming_loss, accuracy_score, multilabel_confusion_matrix
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar datos (ajusta el nombre del archivo CSV)
file_path = "clasificacion_medica_1756164675997.csv"  # cambia según el que quieras usar
df = pd.read_csv(file_path)

# Inspeccionar columnas disponibles
print(df.head())

# 2. Preparar texto y etiquetas
# Asumo que tienes columnas 'title', 'abstract', 'labels' (ajustar si tienen otros nombres)
df["text"] = df["title"].fillna("") + ". " + df["abstract"].fillna("")

# Separar etiquetas (asumo separadas por ";")
df["labels"] = df["labels"].apply(lambda x: str(x).split(";"))

mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df["labels"])

# 3. Vectorizar texto
vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=20000)
X = vectorizer.fit_transform(df["text"])

# 4. Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 5. Entrenar modelo baseline
clf = OneVsRestClassifier(LogisticRegression(max_iter=300, class_weight="balanced"))
clf.fit(X_train, y_train)

# 6. Evaluación
y_pred = clf.predict(X_test)

print("F1 weighted:", f1_score(y_test, y_pred, average="weighted"))
print("F1 micro:", f1_score(y_test, y_pred, average="micro"))
print("F1 macro:", f1_score(y_test, y_pred, average="macro"))
print("Precision weighted:", precision_score(y_test, y_pred, average="weighted"))
print("Recall weighted:", recall_score(y_test, y_pred, average="weighted"))
print("Hamming Loss:", hamming_loss(y_test, y_pred))
print("Exact Match (Subset Accuracy):", accuracy_score(y_test, y_pred))

# 7. Matriz de confusión por clase
cm = multilabel_confusion_matrix(y_test, y_pred)
for idx, label in enumerate(mlb.classes_):
    plt.figure(figsize=(4,3))
    sns.heatmap(cm[idx], annot=True, fmt="d", cmap="Blues", xticklabels=["No", "Yes"], yticklabels=["No", "Yes"])
    plt.title(f"Matriz de confusión - {label}")
    plt.ylabel("True")
    plt.xlabel("Pred")
    plt.show()

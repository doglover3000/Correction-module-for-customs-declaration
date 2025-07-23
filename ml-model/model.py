import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Загрузка данных
df = pd.read_csv("goods.csv")

# # Удалим строки без кода
df = df.dropna(subset=["name", "tnved"])

# Делим данные
X_train, X_test, y_train, y_test = train_test_split(
    df["name"], df["tnved"], test_size=0.2, random_state=42
)

# Сборка пайплайна: векторизация + модель
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Обучение
model.fit(X_train, y_train)

# Тест
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
joblib.dump(model, "tnved_model.pkl")


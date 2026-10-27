import pandas as pd  # Librería para cargar y manipular datos tabulares (DataFrames)
from sklearn.model_selection import train_test_split  # Función para dividir datos en train/test
from sklearn.preprocessing import StandardScaler, OneHotEncoder  # Escalador numérico y codificador de categorías
from sklearn.compose import ColumnTransformer  # Permite aplicar transformaciones distintas por columna
from sklearn.linear_model import LogisticRegression  # Modelo de regresión logística
from sklearn.metrics import classification_report, confusion_matrix  # Métricas de evaluación

# 1. Load and Clean Data (Direct mapping now that we know the columns)
df = pd.read_csv('heart_attack_prediction_dataset.csv')  # Carga el CSV completo en un DataFrame
X = df.drop(columns=['Patient ID', 'Heart Attack Risk'])  # Features: se quita el ID (no predictivo) y la etiqueta
y = df['Heart Attack Risk']  # Variable objetivo binaria (0 = sin riesgo, 1 = riesgo)

# Feature Engineering: Split Blood Pressure text into numbers
X[['Systolic_BP', 'Diastolic_BP']] = X['Blood Pressure'].str.split('/', expand=True).astype(float)  # Separa "120/80" en dos columnas numéricas
X = X.drop(columns=['Blood Pressure'])  # Elimina la columna de texto original ya reemplazada

# 2. Setup Preprocessing Pipeline
num_cols = X.select_dtypes(include=['number']).columns.tolist()  # Lista de columnas numéricas detectadas automáticamente
cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()  # Lista de columnas categóricas/texto

preprocessor = ColumnTransformer([  # Combina distintas transformaciones en un solo objeto
    ('num', StandardScaler(), num_cols),  # A las numéricas: estandarizar (media 0, desviación 1)
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)  # A las categóricas: one-hot, quitando 1a categoría y tolerando valores nuevos
])

# 3. Stratified Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)  # 80/20 manteniendo proporción de clases, semilla fija

X_train_proc = preprocessor.fit_transform(X_train)  # Aprende parámetros de escalado/codificación SOLO con train y los aplica
X_test_proc = preprocessor.transform(X_test)  # Aplica a test los mismos parámetros aprendidos (sin re-aprender, evita fuga de datos)

# 4. Train Optimized Logistic Regression
model = LogisticRegression(solver='liblinear', class_weight='balanced', random_state=42)  # Solver apto para datasets medianos; balanced compensa clases desiguales
model.fit(X_train_proc, y_train)  # Ajusta los coeficientes β del modelo con los datos de entrenamiento

# 5. Generate Predictions with 0.4 Safety Threshold
probabilities = model.predict_proba(X_test_proc)[:, 1]  # Probabilidad estimada P(riesgo=1|x) para cada paciente de test
y_pred = (probabilities >= 0.45).astype(int)  # Convierte probabilidad en clase 0/1 usando umbral 0.45 en vez del 0.5 por defecto

# 6. Print Consolidated Results
print("--- CONFUSION MATRIX ---")  # Encabezado de la matriz de confusión
print(confusion_matrix(y_test, y_pred))  # Imprime TP, TN, FP, FN comparando etiquetas reales vs predichas

print("\n--- PERFORMANCE METRICS ---")  # Encabezado de métricas
print(classification_report(y_test, y_pred, zero_division=0))  # Imprime precisión, recall, F1 y accuracy por clase

print("\n--- MODEL COEFFICIENTS ---")  # Encabezado de coeficientes
feature_names = num_cols + preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols).tolist()  # Reconstruye nombres de columnas tras el one-hot
coef_df = pd.DataFrame({'Feature': feature_names, 'Coef': model.coef_[0]}).sort_values(by='Coef', key=abs, ascending=False)  # Tabla feature-coeficiente ordenada por impacto absoluto
print(coef_df.to_string(index=False))  # Imprime la tabla completa sin la columna de índice

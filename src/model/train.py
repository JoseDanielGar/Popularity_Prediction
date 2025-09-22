import pickle
import pandas as pd
import os
import warnings
import yaml

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, classification_report, precision_score, recall_score, roc_auc_score
from xgboost import XGBClassifier
import numpy as np

# Suprimir los warnings para una salida más limpia
warnings.filterwarnings('ignore')

print("✓ Librerías importadas exitosamente!")
print(f"Pandas versión: {pd.__version__}")
print(f"NumPy versión: {np.__version__}")

# ## 1. Cargar Configuración desde params.yaml

config = yaml.safe_load(open("params.yaml"))["train"]
random_seed = config["seed"]

# ## 2. Cargar Datos de Entrenamiento
# 
# Cargar las características y variables objetivo desde los archivos CSV generados en el proceso de preparación de datos.

# Definir rutas de los archivos
X_train_path = config["x_train_path"]
y_train_path = config["y_train_path"]
X_test_path = config["x_test_path"]
y_test_path = config["y_test_path"]

def load_features_labels(X_path, y_path):
    try:
        X = pd.read_csv(X_path)
        print(f"✓ Características cargadas desde: {X_path}")
        print(f"  • Forma: {X.shape}")
        print(f"  • Características: {X.shape[1]}")
        print(f"  • Total de registros: {len(X):,}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {X_path}")

    try:
        y = pd.read_csv(y_path)
        # Si es un DataFrame con una columna, convertir a Series
        #if isinstance(y, pd.DataFrame):
        #    y = y.iloc[:, 0]
        print(f"✓ Variable objetivo cargada desde: {y_path}")
        print(f"  • Forma: {y.shape}")
        print(f"  • Total de registros: {len(y):,}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {y_path}")
    
    return X, y

print("CARGA DE DATOS DE ENTRENAMIENTO")
print("=" * 50)
# Cargar conjunto de entrenamiento
X_train, y_train = load_features_labels(X_train_path, y_train_path)

print("CARGA DE DATOS DE PRUEBA")
print("=" * 50)
# Cargar conjunto de prueba
X_test, y_test = load_features_labels(X_test_path, y_test_path)

# ## 3. Categorización de la variable objetivo
# La categorización de la popularidad se realiza por género musical.
# Teniendo en cuenta que en la descripción de los datos se evidenció que había mayor presencia de unos géneros que de otros.
# Por lo cual, al hacer la categorización por género se asegura que independientemente del género, la clasificación entre diferentes niveles de popularidad sea equitativa. 
# De esta manera, la categorización se llevó a cabo teniendo en cuenta los percentiles y el género musical, de tal forma que las piezas con valor de 0 se clasifican como: 
# - 'no populares' y se codifican en 0
# - las piezas con una popularidad menor a la mediana del género musical se clasifican como 'bajo' y se codifican en 1.
# - las piezas con popularidad del género entre la mediana y el percentil 75 se clasifican como 'medio' y se codifican con '2'.
# - las piezas con popularidad superior al percentil 75 del género se clasifican como altas y se codifican con 3.
# De esta manera, tenemos mayor granularidad pára definir la popularidad de la canciones,
# teniendo en cuenta que hay mayor representacion de ciertos géneros que de otros,
# y que así mismo la popularidad para géneros poco comunes puede ser menor en comparación de uno más comun,
# pero significativa dentro del mismo género.
# 
def categorize_popularity(group):
    # calculamos mediana y p75 para ese género
    median = group['popularity'].median()
    p75 = np.percentile(group['popularity'], 75)
    
    def assign_category(x):
        if x == 0:
            return 0
        elif x < median:
            return 1
        elif median <= x <= p75:
            return 2
        else:
            return 3
    
    return group['popularity'].apply(assign_category)

df_train=X_train.copy()
df_test=X_test.copy()



df_train['popularity']=y_train['popularity']
df_test['popularity']=y_test['popularity']
df_train['popularity_cat']=df_train.groupby('track_genre_Ordinal_Encoding__track_genre', group_keys=False).apply(categorize_popularity)
df_filtrado = df_train.groupby("track_genre_Ordinal_Encoding__track_genre").filter(lambda x: len(x) > 5)
df_test['popularity_cat']=df_test.groupby('track_genre_Ordinal_Encoding__track_genre', group_keys=False).apply(categorize_popularity)
X_train_c=df_train.drop(['popularity', 'popularity_cat'], axis=1)
X_test_c=df_test.drop(['popularity', 'popularity_cat'], axis=1)
y_train_c=df_train['popularity_cat']
y_test_c=df_test['popularity_cat']

print(X_train_c.head())

print("ENTRENAMIENTO DEL MODELO")
print("=" * 50)
# Crear el modelo base
params = config["params"]

model = XGBClassifier(random_state=random_seed, **params)
model.fit(X_train_c, y_train_c)
print(f"✓ Modelo entrenado: XGBoost Classifier")

# Calcular métricas para los top 3 modelos
print("EVALUACIÓN DE MÉTRICAS EN CONJUNTO DE VALIDACIÓN")
print("=" * 50)

metrics_results = []


# Predicciones en conjunto de validación
y_pred = model.predict(X_test_c)
y_pred_proba = model.predict_proba(X_test_c)
# Calcular métricas de clasificación
precision = precision_score(y_test_c, y_pred, average='weighted')
recall = recall_score(y_test_c, y_pred, average='weighted')
f1 = f1_score(y_test_c, y_pred, average='weighted')
roc_auc = roc_auc_score(y_test_c, y_pred_proba, multi_class='ovr', average='weighted')
accuracy = accuracy_score(y_test_c, y_pred)

# Guardar resultados
metrics = {
    'Modelo': f'XGboost',
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'ROC AUC': roc_auc,
    'Accuracy': accuracy,
    'Parámetros': str(params)
}
metrics_results.append(metrics)

print(f"\nModelo XGboost - Métricas en Validación:")
print(f"  • Precision: {precision:.6f}")
print(f"  • Recall: {recall:.6f}")
print(f"  • F1 Score: {f1:.6f}")
print(f"  • ROC AUC: {roc_auc:.6f}")
print(f"  • Accuracy: {accuracy:.6f}")

# Crear DataFrame con todas las métricas
metrics_df = pd.DataFrame(metrics_results)
print(f"\n✓ Métricas calculadas para todos los modelos")


# Diagrama matriz de confusión
print("DIAGRAMA DE MATRIZ DE CONFUSIÓN")
print("=" * 50)
# --- IGNORE ---
y_test_pred = model.predict(X_test_c)
# Imprimir la matriz de confusión en formato de texto
cm = confusion_matrix(y_test_c, y_test_pred)
print(cm)
# --- IGNORE ---
# Imprimir reporte de clasificación
print("Reporte de Clasificación:")
print(classification_report(y_test_c, y_test_pred, target_names=['No Popular', 'Baja', 'Media', 'Alta']))

# Guardar resultados y modelos
print("GUARDANDO RESULTADOS Y MODELOS")
print("=" * 50)

# Crear directorio para resultados
results_dir = config["model_output_path"]
os.makedirs(results_dir, exist_ok=True)

# Guardar el mejor modelo
best_model_path = os.path.join(results_dir, 'modelo_popularidad.pkl')
with open(best_model_path, 'wb') as file:
    pickle.dump(model, file)
print(f"✓ Modelo guardado: {best_model_path}")
# Resumen final del entrenamiento y resultados
print("🎉 ENTRENAMIENTO COMPLETADO")
print("=" * 60)

print(f"📊 ESTADÍSTICAS DEL ENTRENAMIENTO:")
print(f"  • Algoritmo utilizado: XGBoost Classifier")
print(f"  • Conjunto de entrenamiento: {len(X_train_c):,} registros")
print(f"  • Conjunto de validación: {len(X_test_c):,} registros")
print(f"  • Número de características: {X_train_c.shape[1]}")

# Mostrar las mejores métricas en validación
best_metrics = metrics_results[0]
print(f"\n📈 MÉTRICAS EN VALIDACIÓN:")
print(f"  • F1 Score: {best_metrics['F1 Score']:.6f}")
print(f"  • ROC AUC: {best_metrics['ROC AUC']:.6f}")
print(f"  • Precision: {best_metrics['Precision']:.6f}")
print(f"  • Recall: {best_metrics['Recall']:.6f}")
print(f"  • Accuracy: {best_metrics['Accuracy']:.6f}")

print(f"\n💾 ARCHIVOS GENERADOS:")
print(f"  • {best_model_path}")

print(f"✅ El modelo está listo para implementación en producción!")

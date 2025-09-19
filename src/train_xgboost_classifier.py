# %% [markdown]
# ## 1. Importar Librerías Requeridas
#
# Importar todas las librerías necesarias para el entrenamiento del modelo de clasificación con XGBoost.

# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import (
    train_test_split, 
    cross_val_score, 
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

import xgboost as xgb
import os
import pickle
import yaml

# Configuración de pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

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

print("CARGA DE DATOS DE ENTRENAMIENTO")
print("=" * 50)

# Cargar características (X_train)
try:
    X_train_full = pd.read_csv(X_train_path)
    print(f"✓ Características cargadas desde: {X_train_path}")
    print(f"  • Forma: {X_train_full.shape}")
    print(f"  • Características: {X_train_full.shape[1]}")
except FileNotFoundError:
    raise FileNotFoundError(f"Archivo no encontrado: {X_train_path}")

# Cargar variable objetivo (y_train)
try:
    y_train_full = pd.read_csv(y_train_path)
    # Si es un DataFrame con una columna, convertir a Series
    if isinstance(y_train_full, pd.DataFrame):
        y_train_full = y_train_full.iloc[:, 0]
    print(f"✓ Variable objetivo cargada desde: {y_train_path}")
    print(f"  • Forma: {y_train_full.shape}")
except FileNotFoundError:
    raise FileNotFoundError(f"Archivo no encontrado: {y_train_path}")

print(f"\n✓ Datos cargados exitosamente!")
print(f"Total de registros: {len(X_train_full):,}")

# %%
# Codificar la variable objetivo para que sea binaria.
# Asumimos que la clase positiva es '1' y la negativa es '0'.
# Si el valor de la variable objetivo es menor a 30, se considera como 0 (no popular),
# y si es mayor o igual a 300, se considera como 1 (popular).
y_train_full = (y_train_full >= 30).astype(int)
print("✓ Variable objetivo codificada como binaria (0: no popular, 1: popular)")
print(y_train_full.value_counts())

# %% [markdown]
# ## 3. División de datos para Validación
# 
# Crear una división balanceada del 15% del conjunto de entrenamiento para validación final.

# %%
# División balanceada para validación (15% del dataset balanceado)
print("DIVISIÓN BALANCEADA PARA VALIDACIÓN")
print("=" * 50)

validation_size = 0.15

X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=validation_size, random_state=random_seed, shuffle=True)

print(f"División completada:")
print(f"  • Conjunto de entrenamiento: {len(X_train):,} registros ({(1-validation_size)*100:.0f}%)")
print(f"  • Conjunto de validación: {len(X_val):,} registros ({validation_size*100:.0f}%)")

print(f"\nBalanceo en conjunto de entrenamiento:")
train_dist = y_train.value_counts().sort_index()
for value, count in train_dist.items():
    print(f"  • Clase {value}: {count:,} registros ({count/len(y_train)*100:.1f}%)")

print(f"\nBalanceo en conjunto de validación:")
val_dist = y_val.value_counts().sort_index()
for value, count in val_dist.items():
    print(f"  • Clase {value}: {count:,} registros ({count/len(y_val)*100:.1f}%)")

print(f"\n✓ División balanceada completada exitosamente!")


# Crear el modelo base
params = config["params"]

model = xgb.XGBClassifier(random_state=random_seed, **params)
model.fit(X_train, y_train)

# %% [markdown]
# ## 8. Evaluación de Métricas de Clasificación
# 
# Calcular y comparar métricas de clasificación para los top 3 modelos en el conjunto de validación.

# %%
# Calcular métricas para los top 3 modelos
print("EVALUACIÓN DE MÉTRICAS EN CONJUNTO DE VALIDACIÓN")
print("=" * 50)

metrics_results = []


# Predicciones en conjunto de validación
y_pred = model.predict(X_val)

# Calcular métricas de clasificación
precision = precision_score(y_val, y_pred)
recall = recall_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)
roc_auc = roc_auc_score(y_val, y_pred)

# Para accuracy, convertir predicciones a clases binarias
y_pred_binary = (y_pred > 0.5).astype(int)
accuracy = accuracy_score(y_val, y_pred)

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


# %% [markdown]
# ## 10. Análisis de Validación Cruzada
# 
# Realizar validación cruzada adicional en el mejor modelo para verificar su robustez.

# %%
# Validación cruzada del mejor modelo
print("VALIDACIÓN CRUZADA DEL MEJOR MODELO")
print("=" * 50)
# Definir métricas para validación cruzada
cv_metrics = {
    'f1': 'F1 Score',
    'roc_auc': 'ROC AUC',
    'accuracy': 'Accuracy',
    'precision': 'Precision',
    'recall': 'Recall'
}

cv_folds = config["cv_folds"]
cv_results = {}

for scoring, metric_name in cv_metrics.items():
    scores = cross_val_score(model, X_train, y_train, 
                           cv=cv_folds, scoring=scoring)
    
    # Para métricas negativas, convertir a positivas
    if 'neg_' in scoring:
        scores = -scores
    
    cv_results[metric_name] = scores
    
    print(f"{metric_name}:")
    print(f"  • Media: {scores.mean():.6f}")
    print(f"  • Desviación estándar: {scores.std():.6f}")
    print(f"  • Rango: [{scores.min():.6f}, {scores.max():.6f}]")
    print()

print(f"✓ Validación cruzada completada")
print(f"El modelo muestra {'alta' if max([cv_results[m].std() for m in cv_results]) < 0.1 else 'moderada'} estabilidad")

# %%
# Diagrama matriz de confusión
print("DIAGRAMA DE MATRIZ DE CONFUSIÓN")
print("=" * 50)
# --- IGNORE ---
y_val_pred = model.predict(X_val)
# Imprimir la matriz de confusión en formato de texto
cm = confusion_matrix(y_val, y_val_pred)
print(cm)
# --- IGNORE ---
# Imprimir reporte de clasificación
print("Reporte de Clasificación:")
print(classification_report(y_val, y_val_pred, target_names=['No Popular', 'Popular']))

# %% [markdown]
# ## 11. Guardar Resultados y Modelos
# 
# Guardar el mejor modelo y los resultados de la búsqueda de hiperparámetros.

# %%
# Guardar resultados y modelos
print("GUARDANDO RESULTADOS Y MODELOS")
print("=" * 50)

# Crear directorio para resultados
results_dir = config["model_output_path"]
os.makedirs(results_dir, exist_ok=True)

# Guardar el mejor modelo
best_model_path = os.path.join(results_dir, 'classifier_model.pkl')
with open(best_model_path, 'wb') as file:
    pickle.dump(model, file)
print(f"✓ Modelo guardado: {best_model_path}")

# %%
# Resumen final del entrenamiento y resultados
print("🎉 ENTRENAMIENTO COMPLETADO")
print("=" * 60)

print(f"📊 ESTADÍSTICAS DEL ENTRENAMIENTO:")
print(f"  • Algoritmo utilizado: XGBoost Classifier")
print(f"  • Dataset original: {len(X_train_full):,} registros")
print(f"  • Conjunto de entrenamiento: {len(X_train):,} registros")
print(f"  • Conjunto de validación: {len(X_val):,} registros")
print(f"  • Número de características: {X_train.shape[1]}")

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
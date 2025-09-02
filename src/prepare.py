# %% [markdown]
# # Preparación de Datos para Modelado
# 
# Este notebook realiza la preparación final de los datos para el entrenamiento de modelos de machine learning:
# 
# - Cargar librerías necesarias
# - Identificar y codificar variables categóricas
# - Dividir el conjunto de datos en entrenamiento y prueba
# - Guardar los conjuntos de datos procesados
# 
# **Nota:** Se asume que los datos ya han sido limpiados previamente.

# %% [markdown]
# ## 1. Cargar Librerías Requeridas
# 
# Importar todas las librerías necesarias para la preparación de datos y codificación de variables.

# %%
import pandas as pd
import numpy as np
import yaml
import os
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, RobustScaler
import joblib
from datetime import datetime

# Suprimir warnings para una salida más limpia
warnings.filterwarnings('ignore')

# Configuración de pandas para mejor visualización
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

print("✓ Librerías importadas exitosamente!")
print(f"Pandas versión: {pd.__version__}")
print(f"NumPy versión: {np.__version__}")

# %% [markdown]
# ## 2. Cargar Configuración y Datos
# 
# Cargar los parámetros desde el archivo `params.yaml` y el conjunto de datos limpio.

# %%
# Cargar configuración desde params.yaml
config = yaml.safe_load(open("params.yaml"))["prepare"]

print("Configuración cargada:")
print("=" * 40)
for key, value in config.items():
    print(f"{key}: {value}")

# Extraer parámetros
input_path = config["input_path"]
output_path_train = config["output_path_train"]
output_path_test = config["output_path_test"]
test_split = config["split"]
random_seed = config["seed"]

print(f"\n✓ Configuración cargada exitosamente!")
print(f"✓ División de test: {test_split*100}%")
print(f"✓ Semilla aleatoria: {random_seed}")

# %%
# Cargar el conjunto de datos limpio
print(f"Cargando datos desde: {input_path}")

if os.path.exists(input_path):
    df = pd.read_csv(input_path)
    print(f"✓ Datos cargados exitosamente!")
    print(f"✓ Forma del conjunto de datos: {df.shape}")
    print(f"✓ Total de registros: {len(df):,}")
    print(f"✓ Total de características: {df.shape[1]}")
else:
    raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

# Establecer semilla para reproducibilidad
np.random.seed(random_seed)
print(f"\n✓ Semilla aleatoria establecida: {random_seed}")

# %% [markdown]
# ## 3. Exploración de Variables
# 
# Analizar el conjunto de datos para identificar tipos de variables y su distribución.

# %%
# Mostrar información general del conjunto de datos
print("INFORMACIÓN GENERAL DEL CONJUNTO DE DATOS")
print("=" * 50)
print(f"Forma: {df.shape}")
print(f"\nPrimeras 5 filas:")
print(df.head())

print(f"\nInformación de tipos de datos:")
print(df.info())

# %%
df.describe(include='all')

# %%
# Identificar tipos de variables
print("ANÁLISIS DE TIPOS DE VARIABLES")
print("=" * 50)

# Variables categóricas (object y category)
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
categorical_columns += ['key', 'mode', 'time_signature']
print(f"\nVariables categóricas ({len(categorical_columns)}):")
for col in categorical_columns:
    unique_values = df[col].nunique()
    print(f"  - {col}: {df[col].dtype} (valores únicos: {unique_values})")

# Variables numéricas
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
# Excluir columnas numéricas que están en categorical_columns
numeric_columns = [col for col in numeric_columns if col not in categorical_columns]
print(f"Variables numéricas ({len(numeric_columns)}):")
for col in numeric_columns:
    print(f"  - {col}: {df[col].dtype}")

# Variables booleanas
boolean_columns = df.select_dtypes(include=['bool']).columns.tolist()
print(f"\nVariables booleanas ({len(boolean_columns)}):")
for col in boolean_columns:
    print(f"  - {col}: {df[col].dtype}")

# %% [markdown]
# ## 4. Normalización de Variables Numéricas
# 
# Analizar y normalizar las variables numéricas para mejorar el rendimiento de los algoritmos de machine learning que son sensibles a la escala de las características.

# %%
# Análisis estadístico de variables numéricas
columns_to_normalize = ['duration_ms','loudness', 'tempo']

print("ANÁLISIS ESTADÍSTICO DE VARIABLES NUMÉRICAS A NORMALIZAR")
print("=" * 50)

# Estadísticas descriptivas de variables numéricas
numeric_stats = df[columns_to_normalize].describe()
print(numeric_stats)

print(f"\nRangos de valores para cada variable numérica a normalizar:")
print("-" * 50)
for col in columns_to_normalize:
    min_val = df[col].min()
    max_val = df[col].max()
    mean_val = df[col].mean()
    std_val = df[col].std()
    print(f"{col}:")
    print(f"  • Rango: [{min_val:.3f}, {max_val:.3f}]")
    print(f"  • Media: {mean_val:.3f}, Desv. Estándar: {std_val:.3f}")
    ratio = max_val / min_val if min_val != 0 else 'Inf'
    if isinstance(ratio, str):
        print(f"  • Ratio (max/min): {ratio}")
    else:
        print(f"  • Ratio (max/min): {ratio:.2f}")
    print()

# %%
# Determinación de estrategia de normalización
if columns_to_normalize:
    print("DETERMINACIÓN DE ESTRATEGIA DE NORMALIZACIÓN")
    print("=" * 50)
    
    # Análisis de distribuciones para determinar el mejor método
    variables_to_normalize = []
    normalization_strategy = {}
    
    for col in columns_to_normalize:
        # Calcular estadísticas para determinar el método apropiado
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        
        # Detectar outliers usando IQR
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        outlier_percentage = len(outliers) / len(df) * 100
        
        # Determinar el rango de valores
        min_val = df[col].min()
        max_val = df[col].max()
        range_ratio = max_val / min_val if min_val > 0 else float('inf')
        
        # Decidir método de normalización
        if outlier_percentage > 5:  # Si hay muchos outliers, usar RobustScaler
            method = "RobustScaler"
            scaler = RobustScaler()
        elif range_ratio > 100:  # Si el rango es muy amplio, usar StandardScaler
            method = "StandardScaler"
            scaler = StandardScaler()
        else:  # Para rangos moderados, usar MinMaxScaler
            method = "MinMaxScaler"
            scaler = MinMaxScaler()
        
        variables_to_normalize.append(col)
        normalization_strategy[col] = {'method': method, 'scaler': scaler, 'outlier_pct': outlier_percentage}
        
        print(f"✓ {col}: {method}")
        print(f"  • Outliers: {outlier_percentage:.1f}%")
        print(f"  • Ratio rango: {range_ratio:.2f}")
        print()
    
    print(f"Total de variables a normalizar: {len(variables_to_normalize)}")
else:
    variables_to_normalize = []
    normalization_strategy = {}
    print("✓ No hay variables numéricas para normalizar.")

# %%
# Aplicar normalización a las variables numéricas
df_normalized = df.copy()
scalers = {}  # Diccionario para guardar los scalers

if variables_to_normalize:
    print("APLICANDO NORMALIZACIÓN")
    print("=" * 50)
    
    for col in variables_to_normalize:
        method = normalization_strategy[col]['method']
        scaler = normalization_strategy[col]['scaler']
        
        # Aplicar normalización
        original_values = df[col].values.reshape(-1, 1)
        normalized_values = scaler.fit_transform(original_values)
        df_normalized[col] = normalized_values.flatten()
        
        # Guardar el scaler para uso futuro
        scalers[f'{col}_scaler'] = scaler
        
        # Mostrar estadísticas antes y después
        original_mean = df[col].mean()
        original_std = df[col].std()
        normalized_mean = df_normalized[col].mean()
        normalized_std = df_normalized[col].std()
        
        print(f"✓ {col} ({method}):")
        print(f"  • Antes: μ={original_mean:.3f}, σ={original_std:.3f}")
        print(f"  • Después: μ={normalized_mean:.3f}, σ={normalized_std:.3f}")
        print(f"  • Rango después: [{df_normalized[col].min():.3f}, {df_normalized[col].max():.3f}]")
        print()
    
    print(f"✓ Normalización completada!")
    print(f"✓ Variables normalizadas: {len(variables_to_normalize)}")
    print(f"✓ Scalers guardados: {len(scalers)}")
else:
    print("✓ No hay variables para normalizar.")

# %% [markdown]
# ## 5. Identificar y Codificar Variables Categóricas
# 
# Procesar las variables categóricas utilizando técnicas de codificación apropiadas.

# %%
# Análisis detallado de variables categóricas
if categorical_columns:
    print("ANÁLISIS DETALLADO DE VARIABLES CATEGÓRICAS")
    print("=" * 50)
    
    for col in categorical_columns:
        unique_count = df[col].nunique()
        sample_values = df[col].value_counts().head(10)
        
        print(f"\nVariable: {col}")
        print(f"Valores únicos: {unique_count}")
        print(f"Top 10 valores más frecuentes:")
        print(sample_values)
        print("-" * 30)
else:
    print("✓ No se encontraron variables categóricas para procesar.")

# %%
# Determinar estrategia de codificación para cada variable categórica
if categorical_columns:
    print("ESTRATEGIA DE CODIFICACIÓN")
    print("=" * 50)
    
    # Separar variables por cardinalidad
    low_cardinality = []  # Para One-Hot Encoding (<=10 categorías)
    high_cardinality = [] # Para Label Encoding (>10 categorías)
    
    for col in categorical_columns:
        unique_count = df[col].nunique()
        if unique_count <= 10:
            low_cardinality.append(col)
            print(f"✓ {col}: One-Hot Encoding (cardinalidad: {unique_count})")
        else:
            high_cardinality.append(col)
            print(f"✓ {col}: Label Encoding (cardinalidad: {unique_count})")
    
    print(f"\nResumen:")
    print(f"Variables para One-Hot Encoding: {len(low_cardinality)}")
    print(f"Variables para Label Encoding: {len(high_cardinality)}")
else:
    low_cardinality = []
    high_cardinality = []
    print("✓ No hay variables categóricas para codificar.")

# %%
# Aplicar codificación a variables categóricas
df_encoded = df_normalized.copy()  # Usar el dataframe normalizado
encoders = {}  # Diccionario para guardar los encoders

print("APLICANDO CODIFICACIÓN")
print("=" * 50)

# Label Encoding para variables de alta cardinalidad
if high_cardinality:
    print("Aplicando Label Encoding...")
    for col in high_cardinality:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_normalized[col].astype(str))
        encoders[f'{col}_label_encoder'] = le
        print(f"  ✓ {col}: {df_normalized[col].nunique()} categorías → valores numéricos")

# One-Hot Encoding para variables de baja cardinalidad
if low_cardinality:
    print("\nAplicando One-Hot Encoding...")
    for col in low_cardinality:
        # Crear variables dummy
        dummies = pd.get_dummies(df_normalized[col], prefix=col, drop_first=True)
        
        # Remover columna original y agregar las nuevas
        df_encoded = df_encoded.drop(columns=[col])
        df_encoded = pd.concat([df_encoded, dummies], axis=1)
        
        # Guardar las columnas creadas para referencia
        encoders[f'{col}_dummy_columns'] = dummies.columns.tolist()
        print(f"  ✓ {col}: {df_normalized[col].nunique()} categorías → {len(dummies.columns)} variables dummy")

print(f"\n✓ Codificación completada!")
print(f"✓ Forma después de normalización: {df_normalized.shape}")
print(f"✓ Forma después de codificación: {df_encoded.shape}")
print(f"✓ Nuevas características creadas: {df_encoded.shape[1] - df_normalized.shape[1]}")

# %% [markdown]
# ## 6. División en Conjuntos de Entrenamiento y Prueba
# 
# Dividir el conjunto de datos codificado en conjuntos de entrenamiento y prueba según los parámetros configurados.

# %%
# Verificar si existe una columna objetivo (target)
print("IDENTIFICACIÓN DE VARIABLE OBJETIVO")
print("=" * 50)

target_column = 'popularity'
print(f"✓ Variable objetivo seleccionada: {target_column}")

# Separar características (X) y variable objetivo (y)
X = df_encoded.drop(columns=[target_column])
y = df_encoded[target_column]

print(f"\nForma de características (X): {X.shape}")
print(f"Forma de variable objetivo (y): {y.shape}")
print(f"\nDistribución de la variable objetivo:")
print(y.value_counts().sort_index())

# %%
# Realizar la división train/test
print("DIVISIÓN EN CONJUNTOS DE ENTRENAMIENTO Y PRUEBA")
print("=" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=test_split, 
    random_state=random_seed,
    #stratify=y if len(y.unique()) > 1 and len(y.unique()) < len(y) else None
)

print(f"✓ División completada con semilla: {random_seed}")
print(f"✓ Tamaño de división de prueba: {test_split*100}%")
print(f"\nTamaños de conjuntos:")
print(f"  - Entrenamiento: {len(X_train):,} registros ({len(X_train)/len(X)*100:.1f}%)")
print(f"  - Prueba: {len(X_test):,} registros ({len(X_test)/len(X)*100:.1f}%)")

print(f"\nDistribución en conjunto de entrenamiento:")
print(y_train.value_counts().sort_index())

print(f"\nDistribución en conjunto de prueba:")
print(y_test.value_counts().sort_index())

# %% [markdown]
# ## 7. Guardar Conjuntos de Datos Procesados
# 
# Exportar los conjuntos de entrenamiento y prueba a los directorios especificados en la configuración.

# %%
# Crear directorios de salida
print("GUARDANDO CONJUNTOS DE DATOS PROCESADOS")
print("=" * 50)

os.makedirs(output_path_train, exist_ok=True)
os.makedirs(output_path_test, exist_ok=True)

print(f"✓ Directorios creados:")
print(f"  - Entrenamiento: {output_path_train}")
print(f"  - Prueba: {output_path_test}")

# %%
# Guardar conjunto de entrenamiento
train_features_path = os.path.join(output_path_train, 'X_train.csv')
train_target_path = os.path.join(output_path_train, 'y_train.csv')

X_train.to_csv(train_features_path, index=False)
y_train.to_csv(train_target_path, index=False)

print(f"✓ Conjunto de entrenamiento guardado:")
print(f"  - Características: {train_features_path}")
print(f"  - Variable objetivo: {train_target_path}")
print(f"  - Registros: {len(X_train):,}")
print(f"  - Características: {X_train.shape[1]}")

# %%
# Guardar conjunto de prueba
test_features_path = os.path.join(output_path_test, 'X_test.csv')
test_target_path = os.path.join(output_path_test, 'y_test.csv')

X_test.to_csv(test_features_path, index=False)
y_test.to_csv(test_target_path, index=False)

print(f"✓ Conjunto de prueba guardado:")
print(f"  - Características: {test_features_path}")
print(f"  - Variable objetivo: {test_target_path}")
print(f"  - Registros: {len(X_test):,}")
print(f"  - Características: {X_test.shape[1]}")

# %%
# Guardar encoders, scalers y metadata
encoders_path = os.path.join(output_path_train, 'encoders.joblib')
scalers_path = os.path.join(output_path_train, 'scalers.joblib')
metadata_path = os.path.join(output_path_train, 'metadata.yaml')

# Guardar encoders
if encoders:
    joblib.dump(encoders, encoders_path)
    print(f"✓ Encoders guardados: {encoders_path}")

# Guardar scalers
if scalers:
    joblib.dump(scalers, scalers_path)
    print(f"✓ Scalers guardados: {scalers_path}")

# Crear metadata
metadata = {
    'original_shape': df.shape,
    'encoded_shape': df_encoded.shape,
    'target_column': target_column,
    'numeric_columns': numeric_columns,
    'categorical_columns': categorical_columns,
    'low_cardinality_encoded': low_cardinality,
    'high_cardinality_encoded': high_cardinality,
    'train_size': len(X_train),
    'test_size': len(X_test),
    'test_split_ratio': test_split,
    'random_seed': random_seed,
    'feature_count': X_train.shape[1],
    'encoding_date': datetime.now().strftime('%Y-%m-%d')
}

with open(metadata_path, 'w') as f:
    yaml.dump(metadata, f, default_flow_style=False)

print(f"✓ Metadata guardada: {metadata_path}")

# %% [markdown]
# ## 8. Resumen Final
# 
# Resumen completo del proceso de preparación de datos.

# %%
# Resumen final del proceso
print("🎉 PREPARACIÓN DE DATOS COMPLETADA EXITOSAMENTE")
print("=" * 60)

print(f"📊 ESTADÍSTICAS GENERALES:")
print(f"  • Conjunto de datos original: {df.shape}")
print(f"  • Conjunto de datos normalizado: {df_normalized.shape}")
print(f"  • Conjunto de datos codificado: {df_encoded.shape}")
print(f"  • Nuevas características creadas: {df_encoded.shape[1] - df.shape[1]}")

print(f"\n🔧 PROCESAMIENTO REALIZADO:")
print(f"  • Variables numéricas: {len(numeric_columns)}")
print(f"  • Variables normalizadas: {len(variables_to_normalize)}")
print(f"  • Variables categóricas procesadas: {len(categorical_columns)}")
print(f"  • One-Hot Encoding aplicado a: {len(low_cardinality)} variables")
print(f"  • Label Encoding aplicado a: {len(high_cardinality)} variables")

if variables_to_normalize:
    print(f"\n📏 NORMALIZACIÓN APLICADA:")
    for col in variables_to_normalize:
        method = normalization_strategy[col]['method']
        print(f"  • {col}: {method}")

print(f"\n📁 DIVISIÓN DE DATOS:")
print(f"  • Conjunto de entrenamiento: {len(X_train):,} registros ({len(X_train)/len(X)*100:.1f}%)")
print(f"  • Conjunto de prueba: {len(X_test):,} registros ({len(X_test)/len(X)*100:.1f}%)")
print(f"  • Variable objetivo: {target_column}")
print(f"  • Semilla utilizada: {random_seed}")

print(f"\n💾 ARCHIVOS GENERADOS:")
print(f"  • {train_features_path}")
print(f"  • {train_target_path}")
print(f"  • {test_features_path}")
print(f"  • {test_target_path}")
if encoders:
    print(f"  • {encoders_path}")
if scalers:
    print(f"  • {scalers_path}")
print(f"  • {metadata_path}")

print(f"\n✅ Los datos están listos para el entrenamiento de modelos de machine learning!")



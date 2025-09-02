# %% [markdown]
# # Preparación de los datos
# 
# En este notebook se realiza las siguientes acciones de limpieza de datos sobre el conjunto de datos base:
# 
# - Cargar el conjunto de datos desde archivos .csv
# - Identificar y remover duplicados.
# - Identificar y remover registros con valores nulos.
# - Remover variables con información sensible o fuera del alcance en futuras etapas.
# - Verificaciones de calidad sobre el conjunto de datos de salida.

# %% [markdown]
# ## 1. Importar librerías requeridas
# 
# Importar pandas y otras librerías necesarias para la manipulación y análisis de datos.

# %%
import pandas as pd
import numpy as np
import os
import warnings
import yaml

# Suprimir los warnings para una salida más limpia
warnings.filterwarnings('ignore')

# Opciones para una mejor visualización
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

print("¡Bibliotecas importadas con éxito!")

# %% [markdown]
# ## 2. Carga del conjunto de datos

# %%
# Define the path to the dataset
config = yaml.safe_load(open("params.yaml"))["cleaning"]
dataset_path = config["input_path"]

# Check if the file exists
if os.path.exists(dataset_path):
    print(f"✓ Dataset found at: {dataset_path}")
else:
    print(f"✗ Dataset not found at: {dataset_path}")
    print("Please ensure the dataset.csv file is in the correct location.")

# Load the dataset
try:
    df = pd.read_csv(dataset_path)
    print(f"\n✓ Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
except Exception as e:
    print(f"✗ Error loading dataset: {e}")

# %% [markdown]
# ## 3. Exploración de la estructura del conjunto de datos.
# 
# Muestra información acerca del conjunto de datos cargado como son: forma, nombres de columnas, tipos de datos y estadísticas generales.
# 

# %%
# Store original dataset information for comparison
original_shape = df.shape
print(f"Original Dataset Shape: {original_shape}")
print(f"Total records: {original_shape[0]:,}")
print(f"Total features: {original_shape[1]}")
print("\n" + "="*50)

# %%
# Display first few rows
print("First 5 rows of the dataset:")
print("="*50)
df.head()

# %%
# Display dataset information
print("Dataset Information:")
print("="*50)
print(df.info())
print("\nColumn names:")
print(df.columns.tolist())

# %%
# Check for missing values
print("Missing Values Analysis:")
print("="*50)
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100

missing_df = pd.DataFrame({
    'Column': missing_values.index,
    'Missing Count': missing_values.values,
    'Missing Percentage': missing_percentage.values
})

# Show only columns with missing values
missing_with_nulls = missing_df[missing_df['Missing Count'] > 0]
if len(missing_with_nulls) > 0:
    print(missing_with_nulls)
else:
    print("✓ No missing values found in the dataset!")

print(f"\nTotal missing values: {missing_values.sum():,}")

# %%
# Check for duplicate records
print("Duplicate Records Analysis:")
print("="*50)
duplicate_count = df.duplicated().sum()
duplicate_percentage = (duplicate_count / len(df)) * 100

print(f"Number of duplicate records: {duplicate_count:,}")
print(f"Percentage of duplicate records: {duplicate_percentage:.2f}%")

if duplicate_count > 0:
    print("\nExample of duplicate records:")
    duplicates = df[df.duplicated(keep=False)]
    print(duplicates.head(10))
else:
    print("✓ No duplicate records found!")

# %% [markdown]
# ## 4. Remover registros duplicados
# 
# Identificar y remover los registros duplicados.

# %%
# Remove duplicate records
print("Removing Duplicate Records...")
print("="*50)

# Count duplicates before removal
duplicates_before = df.duplicated().sum()
print(f"Duplicates before removal: {duplicates_before:,}")

# Remove duplicates
df_cleaned = df.drop_duplicates()

# Count duplicates after removal
duplicates_after = df_cleaned.duplicated().sum()
records_removed = len(df) - len(df_cleaned)

print(f"Duplicates after removal: {duplicates_after:,}")
print(f"Records removed: {records_removed:,}")

if records_removed > 0:
    print(f"✓ Successfully removed {records_removed:,} duplicate records!")
else:
    print("✓ No duplicate records found to remove.")

# %% [markdown]
# ## 5. Remover valores faltantes.
# 
# Identificar los registros con valores faltantes y removerlos.

# %%
# Remove records with missing values
print("Removing Records with Missing Values...")
print("="*50)

# Count missing values before removal
missing_before = df_cleaned.isnull().sum().sum()
records_with_nulls_before = df_cleaned.isnull().any(axis=1).sum()

print(f"Total missing values before removal: {missing_before:,}")
print(f"Records with at least one missing value: {records_with_nulls_before:,}")

# Remove records with any missing values
df_final = df_cleaned.dropna()

# Count missing values after removal
missing_after = df_final.isnull().sum().sum()
records_with_nulls_after = df_final.isnull().any(axis=1).sum()
null_records_removed = len(df_cleaned) - len(df_final)

print(f"\nTotal missing values after removal: {missing_after:,}")
print(f"Records with missing values after removal: {records_with_nulls_after:,}")
print(f"Records removed due to missing values: {null_records_removed:,}")

if null_records_removed > 0:
    print(f"✓ Successfully removed {null_records_removed:,} records with missing values!")
else:
    print("✓ No records with missing values found to remove.")

# %% [markdown]
# # 6. Remover varaibles que no serán usadas.

# %%
# Remove specified columns before saving
columns_to_remove = ['index', 'track_id', 'artists', 'album_name', 'track_name']
print(f"Removing columns: {columns_to_remove}")

# Check which columns exist in the dataset
existing_columns_to_remove = [col for col in columns_to_remove if col in df_final.columns]
missing_columns = [col for col in columns_to_remove if col not in df_final.columns]

if existing_columns_to_remove:
    print(f"Columns found and will be removed: {existing_columns_to_remove}")
    df_final_for_saving = df_final.drop(columns=existing_columns_to_remove)
    print(f"✓ Successfully removed {len(existing_columns_to_remove)} columns")
else:
    df_final_for_saving = df_final.copy()
    print("✓ No specified columns found to remove")

if missing_columns:
    print(f"Columns not found in dataset: {missing_columns}")

print(f"Shape after column removal: {df_final_for_saving.shape}")
print(f"Remaining columns: {list(df_final_for_saving.columns)}")

# %% [markdown]
# ## 7. Revisar los resultados de la limpieza.
# 
# Muestra el resultados final de la limpieza y compara el antes y después para verificar que haya sido existosa.

# %%
# Create comprehensive cleaning summary
print("DATA CLEANING SUMMARY")
print("="*60)

# Calculate total records removed
total_records_removed = len(df) - len(df_final)
percentage_removed = (total_records_removed / len(df)) * 100
percentage_retained = ((len(df_final)) / len(df)) * 100

print(f"Original dataset shape: {df.shape}")
print(f"Final dataset shape: {df_final.shape}")
print(f"\nRecords removed: {total_records_removed:,} ({percentage_removed:.2f}%)")
print(f"Records retained: {len(df_final):,} ({percentage_retained:.2f}%)")

print(f"\nBreakdown of records removed:")
print(f"  - Duplicate records: {records_removed:,}")
print(f"  - Records with missing values: {null_records_removed:,}")
print(f"  - Total removed: {total_records_removed:,}")

# %%
# Verify final dataset quality
print("FINAL DATASET QUALITY CHECK")
print("="*60)

# Check for duplicates in final dataset
final_duplicates = df_final.duplicated().sum()
print(f"Duplicate records in final dataset: {final_duplicates:,}")

# Check for missing values in final dataset
final_missing = df_final.isnull().sum().sum()
print(f"Missing values in final dataset: {final_missing:,}")

# Data quality status
if final_duplicates == 0 and final_missing == 0:
    print("\n✅ DATA CLEANING SUCCESSFUL!")
    print("✓ No duplicate records")
    print("✓ No missing values")
    print("✓ Dataset is ready for analysis and modeling")
else:
    print("\n⚠️ WARNING: Data cleaning may not be complete")
    if final_duplicates > 0:
        print(f"⚠️ Still {final_duplicates:,} duplicate records remain")
    if final_missing > 0:
        print(f"⚠️ Still {final_missing:,} missing values remain")

# %% [markdown]
# ## 8. Guardar el conjunto de datos limpio.

# %%
# Optional: Save the cleaned dataset
print("SAVE CLEANED DATASET")
print("="*60)

# Create output directory if it doesn't exist
output_dir = config["output_path"]
os.makedirs(output_dir, exist_ok=True)

# Save the cleaned dataset
output_path = os.path.join(output_dir, 'dataset_cleaned.csv')
df_final_for_saving.to_csv(output_path, index=False)

print(f"\n✓ Cleaned dataset saved to: {output_path}")
print(f"✓ File size: {os.path.getsize(output_path):,} bytes")
print(f"✓ Records saved: {len(df_final_for_saving):,}")
print(f"✓ Features saved: {len(df_final_for_saving.columns)}")

print("\n🎉 Data preprocessing completed successfully!")

# %%




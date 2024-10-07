import pandas as pd
import numpy as np

def column_summary(df):
    """
    Genera un resumen de cada columna en el DataFrame dado.

    Parámetros:
    df (pandas.DataFrame): El DataFrame a resumir.

    Retorna:
    pandas.DataFrame: Un DataFrame que contiene el resumen de cada columna, incluyendo:
        - col_name: Nombre de la columna.
        - col_dtype: Tipo de dato de la columna.
        - num_of_nulls: Número de valores nulos en la columna.
        - num_of_non_nulls: Número de valores no nulos en la columna.
        - num_of_distinct_values: Número de valores distintos en la columna.
        - distinct_values_counts: Un diccionario de los valores más comunes y sus conteos. 
          Si la columna tiene 10 o menos valores distintos, se incluyen todos. De lo contrario, se incluyen los 10 más comunes.
    """
    summary_data = []
    
    for col_name in df.columns:
        col_data = df[col_name]
        col_dtype = col_data.dtype
        num_of_nulls = col_data.isnull().sum()
        num_of_non_nulls = col_data.count()  # Más eficiente que notnull().sum()
        num_of_distinct_values = col_data.nunique()
        
        # Obtener los valores más comunes si hay más de 10 valores únicos, de lo contrario obtener todos
        if num_of_distinct_values <= 10:
            distinct_values_counts = col_data.value_counts().to_dict()
        else:
            distinct_values_counts = col_data.value_counts().head(10).to_dict()

        summary_data.append({
            'col_name': col_name,
            'col_dtype': col_dtype,
            'num_of_nulls': num_of_nulls,
            'num_of_non_nulls': num_of_non_nulls,
            'num_of_distinct_values': num_of_distinct_values,
            'distinct_values_counts': distinct_values_counts
        })
    
    # Convertir los resultados a un DataFrame
    summary_df = pd.DataFrame(summary_data)
    return summary_df

def column_summary_plus(df):
    """
    Genera un resumen detallado de cada columna en el DataFrame dado.

    Parámetros:
    df (pandas.DataFrame): El DataFrame a resumir.

    Retorna:
    pandas.DataFrame: Un DataFrame que contiene el resumen de cada columna, incluyendo:
        - col_name: Nombre de la columna.
        - col_dtype: Tipo de dato de la columna.
        - num_distinct_values: Número de valores distintos en la columna.
        - min_value: Valor mínimo en la columna (para columnas numéricas).
        - max_value: Valor máximo en la columna (para columnas numéricas).
        - median_no_na: Mediana de los valores no nulos en la columna (para columnas numéricas).
        - average_no_na: Promedio de los valores no nulos en la columna (para columnas numéricas).
        - average_non_zero: Promedio de los valores no nulos y no cero en la columna (para columnas numéricas).
        - null_present: Indica si hay valores nulos en la columna.
        - nulls_num: Número de valores nulos en la columna.
        - non_nulls_num: Número de valores no nulos en la columna.
        - distinct_values: Un diccionario con los 10 valores más comunes y sus conteos.
    """
    summary_data = []

    for column in df.columns:
        print(f"Processing column: {column} (dtype: {df[column].dtype})")
        
        col_data = df[column]
        col_dtype = col_data.dtype
        value_counts = col_data.value_counts()
        distinct_values = value_counts.index.tolist()
        num_distinct_values = len(distinct_values)

        # Obtener valores mínimo y máximo
        if np.issubdtype(col_data.dtype, np.number):
            min_value = col_data.min(skipna=True)
            max_value = col_data.max(skipna=True)
        else:
            min_value, max_value = None, None

        # Obtener mediana, promedio y promedio_no_cero para columnas numéricas
        if np.issubdtype(col_data.dtype, np.number):
            non_null_values = col_data.dropna()
            median = non_null_values.median() if not non_null_values.empty else None
            average = non_null_values.mean() if not non_null_values.empty else None

            non_zero_values = non_null_values[non_null_values > 0]
            average_non_zero = non_zero_values.mean() if not non_zero_values.empty else None
        else:
            median, average, average_non_zero = None, None, None

        # Presencia y conteo de valores nulos
        null_present = col_data.isnull().any()
        num_nulls = col_data.isnull().sum()
        num_non_nulls = col_data.notnull().sum()

        # Top 10 valores distintos
        top_10_distinct = value_counts.head(10).to_dict()

        # Agregar datos a la lista de resumen
        summary_data.append({
            'col_name': column,
            'col_dtype': col_dtype,
            'num_distinct_values': num_distinct_values,
            'min_value': min_value,
            'max_value': max_value,
            'median_no_na': median,
            'average_no_na': average,
            'average_non_zero': average_non_zero,
            'null_present': null_present,
            'nulls_num': num_nulls,
            'non_nulls_num': num_non_nulls,
            'distinct_values': top_10_distinct
        })

    # Convertir la lista de diccionarios a DataFrame
    result_df = pd.DataFrame(summary_data)
    return result_df

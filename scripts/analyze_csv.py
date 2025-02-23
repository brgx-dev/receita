import pandas as pd
import sys
import os  # Import os module to use os.path.splitext

def get_table_name(file_path):
    extension_mapping = {
        '.EMPRESCSV': 'empresa_table',
        '.ESTABELE': 'estabele_table',
        '.SOCIOCSV': 'socio_table',
        '.SIMPLES.CSV': 'simples_table',
        '.CNAECSV': 'cnae_table',
        '.MOTICSV': 'motivos_table',
        '.MUNICCSV': 'municipions_table',
        '.NATJUCSV': 'naturezas_table',
        '.PAISCSV': 'pais_table',
        '.QUALSCSV': 'qual_table',
    }
    extension = os.path.splitext(file_path)[1].upper()  # Get the file extension and convert to uppercase
    return extension_mapping.get(extension, 'unknown_table')

def analyze_csv(file_path):
    table_name = get_table_name(file_path)
    print("Table name:", table_name)
    df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
    # Analyze the first 100,000 rows to suggest column names and types
    sample_df = pd.read_csv(file_path, nrows=100000)
    suggested_columns = {}
    
    for column in sample_df.columns:
        column_data = sample_df[column]
        if column_data.dtype == 'object':
            # Suggest a name based on the first few unique values
            unique_values = column_data.unique()
            suggested_name = f"{column}_name"  # Default suggestion
            if len(unique_values) > 0:
                suggested_name = f"{unique_values[0]}_name"  # Use the first unique value as a suggestion
            suggested_columns[column] = {
                'suggested_name': suggested_name,
                'type': 'string'
            }
        else:
            suggested_columns[column] = {
                'suggested_name': f"{column}_value",
                'type': str(column_data.dtype)
            }
    
    print("Suggested column names and types:")
    for col, suggestion in suggested_columns.items():
        print(f"Column: {col}, Suggested Name: {suggestion['suggested_name']}, Type: {suggestion['type']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_csv.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_csv(file_path)

def analyze_csv(file_path):
    table_name = get_table_name(file_path)
    print("Table name:", table_name)
    df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
    # Analyze the first 100,000 rows to suggest column names and types
    sample_df = pd.read_csv(file_path, nrows=100000)
    suggested_columns = {}
    
    for column in sample_df.columns:
        column_data = sample_df[column]
        if column_data.dtype == 'object':
            # Suggest a name based on the first few unique values
            unique_values = column_data.unique()
            suggested_name = f"{column}_name"  # Default suggestion
            if len(unique_values) > 0:
                suggested_name = f"{unique_values[0]}_name"  # Use the first unique value as a suggestion
            suggested_columns[column] = {
                'suggested_name': suggested_name,
                'type': 'string'
            }
        else:
            suggested_columns[column] = {
                'suggested_name': f"{column}_value",
                'type': str(column_data.dtype)
            }
    
    print("Suggested column names and types:")
    for col, suggestion in suggested_columns.items():
        print(f"Column: {col}, Suggested Name: {suggestion['suggested_name']}, Type: {suggestion['type']}")

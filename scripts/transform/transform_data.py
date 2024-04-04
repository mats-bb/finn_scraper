import json
import pandas as pd

# Constants
# Extracted files directory
EXTRACTED_DIR = '/opt/airflow/data/extracted'
# Transformed files directory
TRANSFORMED_DIR = '/opt/airflow/data/transformed'

def load_from_json(dir_, filename):
    """Load json file from directory."""
    with open(fr'{dir_}/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def df_to_csv(transformed_df, path, filename):
    """Save transformed dataframe to csv file."""
    transformed_df.to_csv(fr'{path}/{filename}.csv', columns=transformed_df.columns, header=True, index=False)

def normalize(dict_):
    """Normalize a dictionary containing 'Bransje' and 'Stillingsfunksjon' into a pandas dataframe."""

    # Check if both 'Bransje' and 'Stillingsfunksjon' contain multiple elements
    # If so, normalize each element and merge
    if isinstance(dict_['Bransje'], list) and isinstance(dict_['Stillingsfunksjon'], list):
        df1 = pd.json_normalize(dict_, record_path=['Bransje'], meta=['Arbeidsgiver', 'Stillingstittel', 'Ansettelsesform', 'Sektor', 'url', 'date_added'])
        df2 = pd.json_normalize(dict_, record_path=['Stillingsfunksjon'], meta=['Arbeidsgiver'])

        df3 = df1.merge(df2, on='Arbeidsgiver', how='inner')
        df3 = df3.rename(columns={'0_x': 'Bransje', '0_y': 'Stillingsfunksjon'})
        return df3
    
    # Check if neither 'Bransje' nor 'Stillingsfunksjon' contain multiple elements
    # If so, return a dataframe with a single row
    elif not isinstance(dict_['Bransje'], list) and not isinstance(dict_['Stillingsfunksjon'], list):
        return pd.DataFrame(dict_, columns=dict_.keys(), index=[0])  
    # Check if either 'Bransje' or 'Stillingsfunksjon' contain multiple elements
    # If so, return dataframe
    else:
        return pd.DataFrame(dict_)

def transform_dicts(dict_list):
    """Transform a list of dictionaries into a pandas dataframe."""
    # Create empty dataframe
    transformed_df = pd.DataFrame()

    # Loop through each dictionary in the list
    # Normalize each dictionary and append to the dataframe
    for dict_ in dict_list:
        normalized_dict = normalize(dict_)
        transformed_df = pd.concat([transformed_df, normalized_dict], ignore_index=True)

    return transformed_df

def run():
    """Run the transformation process."""
    dict_list = load_from_json(EXTRACTED_DIR, 'terms_dict')
    transformed_df = transform_dicts(dict_list)
    df_to_csv(transformed_df, TRANSFORMED_DIR, 'transformed_list')

run()
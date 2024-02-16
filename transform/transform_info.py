import os
import sys
import pandas as pd

root = os.getcwd()
sys.path.insert(1, root)

from helper_funcs.helpers import load_from_json

def normalize(dict_):

    if isinstance(dict_['Bransje'], list) and isinstance(dict_['Stillingsfunksjon'], list):
        df1 = pd.json_normalize(dict_, record_path=['Bransje'], meta=['Arbeidsgiver', 'Stillingstittel', 'Ansettelsesform', 'Sektor', 'url', 'date_added'])
        df2 = pd.json_normalize(dict_, record_path=['Stillingsfunksjon'], meta=['Arbeidsgiver'])

        df3 = df1.merge(df2, on='Arbeidsgiver', how='inner')
        df3 = df3.rename(columns={'0_x': 'Bransje', '0_y': 'Stillingsfunksjon'})
        return df3
    
    if not isinstance(dict_['Bransje'], list) and not isinstance(dict_['Stillingsfunksjon'], list):
        return pd.DataFrame(dict_, columns=dict_.keys(), index=[0])
    
    else:
        return pd.DataFrame(dict_)

def transform(dict_list):
    transformed_df = pd.DataFrame()

    for dict_ in dict_list:
        normalized_dict = normalize(dict_)
        transformed_df = pd.concat([transformed_df, normalized_dict], ignore_index=True)

    transformed_df.fillna('None')
    transformed_df.drop(0, axis='columns', inplace=True)

    return transformed_df

def df_to_csv(transformed_df, path, filename):
    transformed_df.to_csv(fr'{path}\{filename}.csv', columns=transformed_df.columns, header=True, index=False)

def run():
    extracted_dir = r'extract\files'
    dict_list = load_from_json(extracted_dir, 'dict_list')
    transformed_df = transform(dict_list)
    transformed_dir = r'transform\files'
    df_to_csv(transformed_df, transformed_dir, 'transformed_list')

    return transformed_df

a = run()

a.info()
import pandas as pd
import json

def load_from_json():
    with open('dict_list.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_to_json(dict_list):
    with open('transformed_list.json', 'w', encoding='utf-8') as f:
        json.dump(dict_list, f, indent=4, ensure_ascii=False)

def normalize(dict_):

    if isinstance(dict_['Bransje'], list) and isinstance(dict_['Stillingsfunksjon'], list):
        df1 = pd.json_normalize(dict_, record_path=['Bransje'], meta=['Arbeidsgiver', 'Stillingstittel', 'Ansettelsesform', 'Sektor', 'url'])
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


    transformed_df.to_csv('transformed_list.csv', columns=transformed_df.columns, header=True, index=False)

def run():
    dict_list = load_from_json()
    transform(dict_list)

run()
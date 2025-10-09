from utils.config_loader import chartsTitle, seriesTitle
import pandas as pd
import numpy as np
from utils.data_loader import all_data_df

def add_title_column(df):
    # Merge with chartsTitle to add the complete table name
    df = pd.merge(
        df,
        chartsTitle,
        left_on='tableName',
        right_on='tableName',
        how='left'
    )
    df.rename(columns={0: 'tableTitle'}, inplace=True)

    # Merge with seriesTitle to add the complete series name
    df = pd.merge(
        df,
        seriesTitle,
        left_on='seriesName',
        right_on='seriesName',
        how='left'
    )
    df.rename(columns={0: 'seriesTitle'}, inplace=True)
    df['tableTitle'] = df['tableTitle'].replace({np.nan: 'nan'})
    df['seriesTitle'] = df['seriesTitle'].replace({np.nan: 'nan'})

    return df

def melt_dataframe(all_data_df):
    expected_id_vars = ['tableName', 'seriesName', 'label', 'Scenario']
    id_vars = [col for col in expected_id_vars if col in all_data_df.columns]
    if not all_data_df.empty:
        years = [col for col in all_data_df.columns if col.isdigit()]
    else:
        years = []
    all_data_melted = all_data_df.melt(
        id_vars=id_vars,
        value_vars=years,
        var_name='Year',
        value_name='Value'
    )

    all_data_melted['Year'] = all_data_melted['Year'].astype(int)
    all_data_melted = add_title_column(all_data_melted)
    all_data_melted["category"]= all_data_melted['tableName'].apply(lambda x: x.split("_"))
    all_data_melted['category'] = all_data_melted['category'].apply(
        lambda cat: [c.lower() for c in cat] if isinstance(cat, list) else cat
    )
    scenarios = sorted(all_data_melted['Scenario'].unique())
    return all_data_melted, scenarios

all_data_melted, scenarios = melt_dataframe(all_data_df)

def get_data_melted():
    return all_data_melted
def get_scenarios():
    return scenarios
from dash import dcc
from dash import html
from utils.filter_dataframe import filter_df_by_category

def emissionCO2_layout(all_data_melted):
    emissions_df = filter_df_by_category(all_data_melted, ['Emission'])
    # emissions_df = all_data_melted[all_data_melted['category'].apply(lambda x: any("Emission" in item for item in x))]
    table_options = emissions_df['tableName'].unique()
    return (html.Div([
                        dcc.RadioItems(
                            id='CO2-emissions-radio',
                            options= table_options,
                            value = table_options[0],
                            labelStyle={'display': 'block'}
                        ),
                        dcc.Graph(id='CO2-emissions-chart') # Added the graph component with the correct ID
                    ])
    )
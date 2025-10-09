from dash import html, dcc
from utils.filter_dataframe import filter_df_by_category

def subsector_transport (df):
    df_filtered_FC = filter_df_by_category(df, ['TRA','Fuel'])
    df_filtered_VS = filter_df_by_category(df, ['TRA', 'TYPE'],['Fuel'])
    df_filtered_VA = filter_df_by_category(df, ['TRA', 'Land'])
    return( 
        html.Div([
            html.H3("Transport Sector"),
                html.Div([
                html.Label('Fuel consumption by:'),
                dcc.Dropdown(
                    id = 'transport-fuel-cons-dropdown',
                    options = [k for k in df_filtered_FC['tableTitle'].unique()],
                    # options = ['Fuel Consumption - Domestic Aviation',
                    #             'Fuel Consumption - International Aviation',
                    #             'Fuel Consumption - Land Transport (F)',
                    #             'Fuel Consumption - Navigation', 'Fuel Consumption - Unspecified',
                    #             'Fuel Consumption - Land Transport (P)',
                    #             'Fuel Consumption - Tourism'],
                    value = 'Fuel Consumption - Domestic Aviation',
                    multi = False
                ),
                dcc.Graph(id = 'transport-fuel-cons-chart')
            ]),
            html.Div([
                html.Label('vehicle sales and stock by mode:'),
                dcc.Dropdown(
                    id='transport-vehicle-type-dropdown',
                    options=[k for k in df_filtered_VS['tableTitle'].unique()],
                    # options=['New HGV - Stock by Type', 'HGV - Stock by Type',
                    #         'New LGV - Stock by Type', 'LGV - Stock by Type',
                    #         'New MGV - Stock by Type', 'MGV - Stock by Type',
                    #         'New Private Cars - Stock by Type', 'Private Cars - Stock by Type'],
                    value='New HGV - Stock by Type',
                    multi=False
                ),
                dcc.Graph(id='transport-vehicle-type-chart')
            ]),
            html.Div([
                html.Label('vehicle activity'),
                dcc.Dropdown(
                    id='transport-vehicle-activity-dropdown',
                    options=[k for k in df_filtered_VA['tableTitle'].unique()],
                    # options=['Land Transport - Lump Sum Investment Cost',
                    #         'Land Transport (F) by Mode', 'Land Transport (P) by Distance',
                    #         'Land Transport (P) by Mode', 'Land Transport (P) - Long',
                    #         'Land Transport (P) - Medium', 'Land Transport (P) - Short'],
                    value='Land Transport (F) by Mode',
                    multi=False
                ),
                dcc.Graph(id='transport-vehicle-activity-chart')
            ]),
            html.Div([
                html.Label('Other:'),
                dcc.Dropdown(
                    id='transport-other-dropdown',
                    options=['CO2 emission', 'Land TransportLump Sum Investment Cost'],
                    value='CO2 emission',
                    multi=False
                )
            ]),dcc.Graph(id = 'transport-other-chart')
        ])
    )
from dash import html, dcc
# from utils.data_loader import load_data
from utils.filter_dataframe import filter_df_by_category
# df = load_data('data_all/all_data_melted.csv')
# df_filtered = filter_df_by_category(df,  ['SYS', 'Sector'],['Cost', 'Lump'])
def subsector_overview(all_data_melted):
    df_filtered = filter_df_by_category(all_data_melted,['SYS','Sector', 'FEC'],['Cost', 'Lump'])
    dic_filtered = dict(zip(df_filtered['tableTitle'].unique(),df_filtered['tableName'].unique()))
    
    return ( html.Div([
                html.H3("Sector Overview"),
                html.Div([
                    html.Label("Select Sectors:"),
                    dcc.Dropdown(
                        id='FEC-sector-dropdown',
                        options=["Transport", "Residential", "Services", "Industry", "Agriculture"],
                        value="Transport",
                        multi=False
                    ),
                ]),
                dcc.Graph(id="FEC_by_sector_chart"),
                html.Hr(), # Add a separator
                html.Div([
                    html.Label("Select source:"),
                        dcc.Dropdown(
                        id='source-by-sector-dropdown',
                        options= [k for k, v in dic_filtered.items()],
                        # options= ['FEC of Biodiesel by Sector', 'FEC of Ethanol by Sector',
                        #         'FEC of Biogas by Sector', 'FEC of Biomass by Sector',
                        #         'FEC of Coal by Sector', 'FEC of Electricity by Sector',
                        #         'FEC of Nat. Gas by Sector', 'FEC of Hydrogen by Sector',
                        #         'FEC of Heat by Sector', 'FEC of HFO by Sector',
                        #         'FEC of LPG by Sector', 'FEC of Diesel by Sector',
                        #         'FEC of Gasoline by Sector', 'FEC of Kerosene by Sector',
                        #         'FEC of Peat by Sector'],
                        value= ['FEC of Biodiesel by Sector'],
                        multi=True
                    ),
                    dcc.Graph(id="source-by-sector-chart")
                ])
            ])
    )

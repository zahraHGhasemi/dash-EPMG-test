

import pandas as pd
import numpy as np

import dash
from dash import dcc, html, Input, Output
import plotly

import plotly.express as px
import dash_bootstrap_components as dbc
import glob
import os

def load_and_concat_data(directory_path):
    all_files = glob.glob(os.path.join(directory_path, "*.csv"))
    df_list = []

    for file_path in all_files:
        try:
            df = pd.read_csv(file_path)
            # Extract scenario name from filename
            file_name = os.path.basename(file_path)
            scenario_name = file_name.replace("mitigation_cb2024-", "").replace(".csv", "")
            df['Scenario'] = scenario_name
            df_list.append(df)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if df_list:
        concatenated_df = pd.concat(df_list, ignore_index=True)
        return concatenated_df
    else:
        return pd.DataFrame() 
all_data_df = load_and_concat_data('data')
print(all_data_df.columns)
# 
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
print(all_data_melted.columns)


scenarios = sorted(all_data_melted['Scenario'].unique())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)
app.title = "Energy Scenarios Dashboard"


sector_nav = dbc.Nav(
    [
        dbc.NavLink("Overview", id="nav-overview", active=True),
        dbc.NavLink("Transport", id="nav-transport"),
        dbc.NavLink("Residential", id="nav-residential"),
        dbc.NavLink("Services", id="nav-services"),
        dbc.NavLink("Industry", id="nav-industry"),
    ],
    vertical=True,
    pills=True,
)

def create_metric_card(title, value, subtitle, color="primary"):
    """
    Create a metric card component
    """
    return dbc.Card([
        dbc.CardBody([
            html.H4(title, className="card-title text-muted mb-3"),
            html.H1(value, className="display-4 fw-bold mb-2"),
            html.P(subtitle, className="text-muted mb-3")
        ])
    ], className="h-100 shadow-sm")

def create_energy_overview_section():
    """
    Create the energy overview section with metrics cards
    """
    return html.Div([
        dbc.Row([
            # Top row - 3 cards
            dbc.Col([
                create_metric_card(
                    title="Electricity consumption per capita",
                    value="↑16%",
                    subtitle="change 2000-2023",
                )
            ], xs=12, md=4, className="mb-4"),

            dbc.Col([
                create_metric_card(
                    title="Energy intensity of the economy",
                    value="↓69%",
                    subtitle="change 2000-2023",
                )
            ], xs=12, md=4, className="mb-4"),

            dbc.Col([
                create_metric_card(
                    title="Renewables",
                    value="38.9%",
                    subtitle="share of power generation, 2022",
                )
            ], xs=12, md=4, className="mb-4"),
        ]),

        dbc.Row([
            # Bottom row - 3 cards
            dbc.Col([
                create_metric_card(
                    title="Oil",
                    value="45%",
                    subtitle="of total energy supply, 2023",
                )
            ], xs=12, md=4, className="mb-4"),

            dbc.Col([
                create_metric_card(
                    title="Natural gas",
                    value="32%",
                    subtitle="of total energy supply, 2023",
                )
            ], xs=12, md=4, className="mb-4"),

            dbc.Col([
                create_metric_card(
                    title="Coal",
                    value="5%",
                    subtitle="of total energy supply, 2023",
                )
            ], xs=12, md=4, className="mb-4"),
        ])
    ], className="container-fluid")

app.layout = html.Div([
    html.Div([
        html.Label("Select Scenario:", className="control-label"),
        dcc.Dropdown(
            id='scenario-dropdown',
            options=[{'label': s, 'value': s} for s in scenarios],
            value=scenarios[0] if len(scenarios) > 0 else None,
            placeholder="Select a scenario...",
            className="dropdown"
        )
    ], className="control-item"),
    dcc.RangeSlider(
        id='year-slider',
        min= all_data_melted['Year'].min(),
        max= all_data_melted['Year'].max()-1,
        value=[2018, 2050],
        marks={str(year): str(year) for year in range(all_data_melted['Year'].min(), all_data_melted['Year'].max(), 1)},
        step=1
    ),
    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            # html.Div([
            #     create_energy_overview_section()
            # ]),



            # dbc.Row([
            #     # Left card (Energy Mix)
            #     dbc.Col(
            #         dbc.Card([
            #             dbc.CardHeader("Energy mix"),
            #             dbc.CardBody([
            #                 html.H6("Total energy supply, Ireland, 2023"),
            #                 dcc.Graph(id='energy-mix-chart',
            #                     figure=px.bar(
            #                         x=["Coal", "Oil", "Natural gas", "Renewables"],
            #                         y=[5.4, 46.2, 32.3, 8.5],
            #                         labels={"x": "Source", "y": "Percent"},
            #                         title="Energy Mix"
            #                     )
            #                 )
            #             ])
            #         ]),style={
            #             'backgroundColor': '#3498DB',
            #             'color': 'white',
            #             'padding': '20px',
            #             'borderRadius': '10px',
            #             'textAlign': 'center',
            #             'margin': '10px'
            #         }
            #     ),

            #     # Right card (Emissions)
            #     dbc.Col(
            #         dbc.Card([
            #             dbc.CardHeader("Emissions"),
            #             dbc.CardBody([
            #                 html.H6("Energy-related CO2 emissions, Ireland, 2022"),
            #                 html.H2("33 Mt CO2"),
            #                 html.P("0.1% of global emissions"),
            #                 html.P("↓19% since 2000"),
            #             ])
            #         ]), style={
            #             'backgroundColor': 'aqua',
            #             'color': 'balck',
            #             'padding': '20px',
            #             'borderRadius': '10px',
            #             'textAlign': 'center',
            #             'margin': '10px'
            #         }
            #     ),
            # ]),

            # dbc.Row([
            #     dbc.Label("Select Year:"),
            #     dbc.Input(type="number", min=2018, max= 2051, step=1, placeholder = 'Enter a year between 2018 to 2051', id ='year-input'),
            #     dbc.Col(
            #         dbc.Card([
            #             dbc.CardHeader("Import"),
            #             dbc.CardBody([
            #                 dcc.Graph(id='import-chart')
            #             ])
            #         ])
            #     ),
            #     dbc.Col(
            #         dbc.Card([
            #             dbc.CardHeader("Export"),
            #             dbc.CardBody([
            #                 dcc.Graph(id='export-chart')
            #             ])
            #         ])
            #     ),
            # ], style={
            #     "textAlign": 'center'
            # })


        ]),
        dcc.Tab(label ="Supply", children = [
            html.Div([
                html.Label("Select suuply by source:"),
                dcc.Dropdown(
                    id = 'supply-source-dropdown',
                    options = ['Biodiesel', 'Ethanol', 'Biogas'],
                    value = 'Biodiesel',
                    multi = False
                ),
                dcc.Graph(id = 'supply-chart'),
                dcc.Graph(id = "Hydrogen Production")
            ])

        ]),
        dcc.Tab(label='Power', children=[
            html.Div([
                dcc.Dropdown(
                id='capacity-dropdown',
                options=['installed','new'],
                value='installed',
                placeholder="Select the capacity...",
                multi = False
                ),
                dcc.Graph(id='capacity-chart'),
                dcc.Graph(id='CO2-emission-power'),
                dcc.Graph(id='Electricity-generation-PP')
            ])

        ]),
        dcc.Tab(label ="Sector" , children=[
            dbc.Row([
            # Left side: Radio buttons
              dbc.Col(
                  dcc.RadioItems(
                      id="sector-radio",
                      options=[
                          {"label": "Overview", "value": "overview"},
                          {"label": "Transport", "value": "transport"},
                          {"label": "Residential", "value": "residential"},
                          {"label": "Services", "value": "services"},
                          {"label": "Industry", "value": "industry"},
                      ],
                      value="overview",  # Default
                      labelStyle={"display": "block"}  # Vertical layout
                  ),
                  width=2
              ),
              # Right side: dynamic content
              dbc.Col(html.Div(id="sector-content"), width=10)
          ])

        ]),
        dcc.Tab(label='CO2 Emissions', children=[
            html.Div([
                dcc.RadioItems(
                    id='CO2-emissions-radio',
                    options=['Domestic CO2 Emissions by Sector','SYS_Emissions_CO2_Domestic_Cumulative','Power','Transport','Residential by service', 'Industry'],
                    value = 'Domestic CO2 Emissions by Sector',
                    labelStyle={'display': 'block'}
                ),
                dcc.Graph(id='CO2-emissions-chart') # Added the graph component with the correct ID
            ])
        ])

    ])

])

@app.callback(
    Output('import-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-input', 'value')
)
def update_import_chart(scenario, year):
    filtered_df = all_data_melted[(all_data_melted['Year']== year) &
                                 (all_data_melted['Scenario'] == scenario) &
                                 (all_data_melted['tableName'] == 'SYS_NRG-Import')]
    fig = px.pie(filtered_df, values='Value', names='seriesName', title=f'Import ({year})')
    return fig

@app.callback(
    Output('export-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-input', 'value')
)
def update_export_chart(scenario, year):
    filtered_df = all_data_melted[(all_data_melted['Year'] >= year) &
                                 (all_data_melted['Scenario'] == scenario) &
                                 (all_data_melted['tableName'] == 'SYS_NRG-Export')]
    fig = px.pie(filtered_df, values='Value', names='seriesName', title=f'Export ({year})')
    return fig

@app.callback(
    Output('CO2-emissions-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('CO2-emissions-radio', 'value')
)
def CO2_emissions(scenario, year_range, CO2_emissions_radio):
  dic_CO2_emissions ={'Domestic CO2 Emissions by Sector':'SYS_Emissions_CO2_Domestic',
                      'SYS_Emissions_CO2_Domestic_Cumulative':'SYS_Emissions_CO2_Domestic_Cumulative',
                      'Power':'PWR_Emissions-CO2',
                      'Transport':'TRA_Emissions-CO2',
                      'Residential by service':'RSD_Services_CO2Emissions',
                      'Industry':'IND_Emissions-CO2'}
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'] == dic_CO2_emissions[CO2_emissions_radio])]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='CO2 Emissions'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output("sector-content", "children"),
    Input("sector-radio", "value")
)

def display_sector_content(active_sector):

    if active_sector == "overview":
        return html.Div([
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
                    options=['Biodiesel', 'Ethanol', 'Biogas', 'Biomass', 'Coal', 'Electricity', 'Nat. Gas', 'Hydrogen', 'Heat', 'Gasoline', 'HFO', 'Kerosene', 'Diesel', 'LPG', 'Peat'],
                    value= ['Biodiesel'],
                    multi=True
                ),
                dcc.Graph(id="source-by-sector-chart")
            ])
        ])

    elif active_sector == "transport":
        return html.Div([
            html.H3("Transport Sector"),
             html.Div([
                html.Label('Fuel consumption by:'),
                dcc.Dropdown(
                    id = 'transport-fuel-cons-dropdown',
                    options = ['Land transport(F)', 'Land Transport (P)', 'Domestic Aviation',  'International Aviation',  'Navigation',  'Unspecified', 'Tourism'],
                    value = 'Land transport(F)',
                    multi = True
                ),
                dcc.Graph(id = 'transport-fuel-cons-chart')
            ]),
            html.Div([
                html.Label('vehicle sales and stock by mode:'),
                dcc.Dropdown(
                    id='transport-vehicle-type-dropdown',
                    options=['new private cars' , 'private cars', 'new HGV', 'new MGV', 'new LGV','HGV', 'MGV', 'LGV'],
                    value='new private cars',
                    multi=False
                ),
                dcc.Graph(id='transport-vehicle-type-chart')
            ]),
            html.Div([
                html.Label('vehicle activity'),
                dcc.Dropdown(
                    id='transport-vehicle-activity-dropdown',
                    options=['Land Transport F', 'Land Transport P distance','Land Transport p Mode', 'Land Transport (P) - Long',
                             'Land Transport (P) - Medium', 'Land Transport (P) - Short'],
                    value='Land Transport F',
                    multi=True
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

    elif active_sector == "residential":
        return html.Div([
            html.H3("Residential Sector"),
            html.Div([
                html.Label("FEC by subsector:"),
                dcc.Dropdown(
                    id = "residential-FEC-bysector-dropdown",
                    options=['Water and Space Heating', 'Space/Water in Apartments', 'Space/Water in Attached', 'Space/Water in Detached',  'Other Services'],
                    value = 'Water and Space Heating',
                    multi = False
                ),dcc.Graph(id ="residential-FEC-bysector-chart")
            ]),
            html.Div([
                html.Label("FEC by service"),
                dcc.Graph(id = 'residential-FEC-by-service-chart')
            ]),
            html.Div([
                html.Label('Retrofits'),
                dcc.Dropdown(
                    id = 'residential-retrofit-dropdown',
                    options= [{'label': 'apartment', 'value': 'apartment'}, {'label': 'attached', 'value': 'attached'}, {'label': 'detached', 'value': 'detached'},{'label': 'energy saving', 'value': 'energy saving'}],
                    value = 'apartment',
                ),dcc.Graph(id = "residential-retrofit-chart")
            ]),
            html.Div([
                html.Label("House stock"),
                dcc.Dropdown(
                    id="residential-house-stock-dropdown",
                    options= ['Number of Dwellings by Type', 'New Dwellings by Type'],
                    value= 'Number of Dwellings by Type'
                ),dcc.Graph(id= 'residential-house-stock-chart')
            ])
        ])

    elif active_sector == "services":
        return html.Div([
            html.H3("Services Sector"),
            html.Div([
                html.Label("TFC"),
                dcc.Dropdown(
                    id = 'services-tfc-dropdown',
                    options=['comercial space/water heating', 'public space water heating', 'by service'],
                    value='by service'
                ),dcc.Graph(id ='services-tfc-chart')
            ]),
            html.Div([
                html.Label('Data center'),
                dcc.Dropdown(
                    id= 'service-datacenter-dropdown',
                    options= ['electricity demand', 'excess heat potential', 'dc exccess heat supply to DH grid'],
                    value= 'electricity demand'
                ),dcc.Graph(id='service-datacenter-chart')
            ])
        ])

    elif active_sector == "industry":
        return html.Div([
            html.H3("Industry Sector"),
            html.Div([
                html.Label("Subsector:"),
                dcc.Dropdown(
                    id= 'industry-subsector-dropdown',
                    options=['wood and wood product','other non-metalix mineral products', 'cement', 'other manufactuting', 'lime', 'chemical and man-made fibre', 'food and beverages',
                            'basic metal and fabricated metal products'],
                    value= ['wood and wood product'],
                    multi = True
                ),dcc.Graph(id = 'industry-subsector-chart')
            ])
        ])

@app.callback(
    Output('source-by-sector-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('source-by-sector-dropdown', 'value')
)
def source_by_sector(scenario, year_range, source):
    dic_source ={
        'Biodiesel': 'SYS_FEC-BIODST_Sector',
        'Ethanol': 'SYS_FEC-BIOETH_Sector',
        'Biogas': 'SYS_FEC-BIOGAS_Sector',
        'Biomass': 'SYS_FEC-BIOWOOx_Sector',
        'Coal': 'SYS_FEC-COA_Sector',
        'Electricity': 'SYS_FEC-ELCD_Sector',
        'Nat. Gas': 'SYS_FEC-GASNAT_Sector',
        'Hydrogen': 'SYS_FEC-H2_Sector',
        'Heat': 'SYS_FEC-HETD_Sector',
        'Gasoline': 'SYS_FEC-OILGSL_Sector',
        'HFO': 'SYS_FEC-HFO_Sector',
        'Kerosene': 'SYS_FEC-OILKER_Sector',
        'Diesel': 'SYS_FEC-OILDST_Sector',
        'LPG': 'SYS_FEC-LPG_Sector',
        'Peat': 'SYS_FEC-PEAT_Sector'
    }
    ls_source=[]
    for s in source:
      if s in dic_source.keys():
        ls_source.append(dic_source[s])

    all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                               (all_data_melted['Year'] >= year_range[0]) &
                                              (all_data_melted['Year'] <= year_range[1])&
                                              (all_data_melted['tableName'].isin(ls_source))]

    fig = px.bar(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Source by Sector'
        )
    fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
    return fig


@app.callback(
    Output('industry-subsector-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('industry-subsector-dropdown', 'value')
)
def industry_subsector(scenario, year_range, subsector):
  ls_subsector=[]
  if 'wood and wood product' in subsector:
    ls_subsector.append('IND-WAP_FEC'),
  if 'other non-metalix mineral products' in subsector:
    ls_subsector.append('IND-ONM_FEC')
  if 'cement' in subsector:
    ls_subsector.append('IND-CEM_FEC')
  if 'other manufactuting' in subsector:
    ls_subsector.append('IND-OMA_FEC')
  if 'lime' in subsector:
    ls_subsector.append('IND-LIM_FEC')
  if 'chemical and man-made fibre' in subsector:
    ls_subsector.append('IND-CAF_FEC')
  if 'food and beverages' in subsector:
    ls_subsector.append('IND-FAP_FEC')
  if 'basic metal and fabricated metal products' in subsector:
    ls_subsector.append('IND-MAP_FEC')

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'].isin(ls_subsector))]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Industry Subsector'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig


@app.callback(
    Output('services-tfc-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('services-tfc-dropdown', 'value')
)
def FEC_by_service_tfc(scenario, year_range, service):
  if service == 'comercial space/water heating':
    service_f = 'SRV-COM_FEC_WS'
  elif service == 'public space water heating':
    service_f = 'SRV-PUB_FEC_WS'
  elif service == 'by service':
    service_f = 'SRV_FEC_Service'
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == service_f)]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title=f'TFC by {service}'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('service-datacenter-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('service-datacenter-dropdown', 'value')
)

def service_datacenter(scenario, year_range, service):
  if service == 'electricity demand':
    service_f = 'SRV_FEC_DCs'
  elif service == 'excess heat potential':
    service_f = 'SRV-DCs_EH'
  elif service == 'dc exccess heat supply to DH grid':
    service_f = 'SRV-DCs_EH_DH-Grid'
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'] == service_f)]

  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Service Data Center')
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig
@app.callback(
    Output('residential-house-stock-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('residential-house-stock-dropdown', 'value')
)
def residential_house_stock(scenario, year_range, house_stock):
  if house_stock == 'Number of Dwellings by Type':
    house_stock_f = 'RSD_BLD_TYPE'
  elif house_stock == 'New Dwellings by Type':
    house_stock_f = 'RSD_BLD-N_TYPE'
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'] == house_stock_f)]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Residential House Stock'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('residential-retrofit-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('residential-retrofit-dropdown', 'value')
)
def residential_retrofit(scenario, year_range, retrofit):
  if retrofit == 'apartment':
    retrofit_f = 'RSD_RTFT-APT_NCAP'
  elif retrofit == 'attached':
    retrofit_f = 'RSD_RTFT-ATT_NCAP'
  elif retrofit == 'detached':
    retrofit_f = 'RSD_RTFT-DET_NCAP'
  elif retrofit == 'energy saving':
    retrofit_f = 'RSD_RTFT_NRG_SAVINGS'
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == retrofit_f)]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Residential Retrofit'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('residential-FEC-by-service-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value')
)
def residential_FEC_by_service(scenario, year_range):
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == "RSD_Services_EnergyCons")]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Residential FEC by Service')
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('residential-FEC-bysector-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('residential-FEC-bysector-dropdown', 'value')
)
def residential_FEC_bysector(scenario, year_range, selected_sector):
  if selected_sector == "Water and Space Heating":
    sector = "RSD_WaterSpace_FuelCons"
  elif selected_sector == "Space/Water in Apartments":
    sector = "RSD_WS-APT_FuelCons"
  elif selected_sector == "Space/Water in Attached":
    sector = "RSD_WS-ATT_FuelCons"
  elif selected_sector == "Space/Water in Detached":
    sector = "RSD_WS-DET_FuelCons"
  elif selected_sector == "Other Services":
    sector = "RSD_OtherServices_FuelCons"

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == sector)]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Residential FEC by Sector')
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig


@app.callback(
    Output('FEC_by_sector_chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('FEC-sector-dropdown', 'value')
)
def FEC_by_sector(scenario, year_range, selected_sectors):
  selected_table_name =[]
  if "Transport" in selected_sectors:
    selected_table_name.append("TRA_FEC")
  elif "Residential" in selected_sectors:
    selected_table_name.append("RSD_FEC")
  elif "Services" in selected_sectors:
    selected_table_name.append("SRV_FEC")
  elif "Industry" in selected_sectors:
    selected_table_name.append("IND_FEC")
  elif "Agriculture" in selected_sectors:
    selected_table_name.append("AGR_FEC")
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                          (all_data_melted['Year'] >= year_range[0]) &
                                          (all_data_melted['Year'] <= year_range[1])&
                                          (all_data_melted['tableName'].isin(selected_table_name))]

  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='FEC by Sector'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('transport-fuel-cons-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('transport-fuel-cons-dropdown', 'value')
)

def transport_fuel_cons(scenario, year_range, fuel_cons):
  selected_table_name =[]
  if "Land transport(F)" in fuel_cons:
    selected_table_name.append("TRA_Freight_Land_FuelCons")
  if "Land Transport (P)" in fuel_cons:
    selected_table_name.append("TRA_Passenger_Land_FuelCons")
  if "Domestic Aviation" in fuel_cons:
    selected_table_name.append("TRA_AVIDOM_FuelCons")
  if "International Aviation" in fuel_cons:
    selected_table_name.append("TRA_AVIINT_FuelCons")
  if "Navigation" in fuel_cons:
    selected_table_name.append("TRA_NAV_FuelCons")
  if "Unspecified" in fuel_cons:
    selected_table_name.append("TRA_OTH_FuelCons")
  if "Tourism" in fuel_cons:
    selected_table_name.append("TRA_TURS_FuelCons")
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'].isin(selected_table_name))]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Transport Fuel Consumption'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('transport-vehicle-type-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('transport-vehicle-type-dropdown', 'value')
)
def transport_vehicle_type(scenario, year_range, vehicle_type):
  selected_table_name =[]
  if "new private cars" in vehicle_type:
    selected_table_name.append("TRA_P-CAR-N_TYPE")
  elif "private cars" in vehicle_type:
    selected_table_name.append("TRA_P-CAR_TYPE")
  elif "new HGV" in vehicle_type:
    selected_table_name.append("TRA_F-HTRUCK-N_TYPE")
  elif "new MGV" in vehicle_type:
    selected_table_name.append("TRA_F-MTRUCK-N_TYPE")
  elif "new LGV" in vehicle_type:
    selected_table_name.append("TRA_F-LTRUCK-N_TYPE")
  elif "HGV" in vehicle_type:
    selected_table_name.append("TRA_F-HTRUCK_TYPE")
  elif "MGV" in vehicle_type:
    selected_table_name.append("TRA_F-MTRUCK_TYPE")
  elif "LGV" in vehicle_type:
    selected_table_name.append("TRA_F-LTRUCK_TYPE")

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'].isin(selected_table_name))]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Transport Vehicle Type'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig
@app.callback(
    Output('transport-vehicle-activity-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('transport-vehicle-activity-dropdown', 'value')
)
def transport_vehicle_activity(scenario, year_range, vehicle_activity):
  selected_table_name =[]
  if "Land Transport F" in vehicle_activity:
    selected_table_name.append("TRA_Freight_Land_Mode")
  if "Land Transport (P) distance" in vehicle_activity:
    selected_table_name.append("TRA_Passenger_Land_Distance")
  if "Land Transport (P) Mode" in vehicle_activity:
    selected_table_name.append("TRA_Passenger_Land_Mode")
  if "Land Transport (P) - Long" in vehicle_activity:
    selected_table_name.append("TRA_Passenger_Land_Mode-L")
  if "Land Transport (P) - Medium" in vehicle_activity:
    selected_table_name.append("TRA_Passenger_Land_Mode-M")
  if "Land Transport (P) - Short" in vehicle_activity:
    selected_table_name.append("TRA_Passenger_Land_Mode-S")

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'].isin(selected_table_name))]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Transport Vehicle Activity'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('transport-other-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('transport-other-dropdown', 'value')
)
def transport_other(scenario, year_range, other):
  selected_table_name =[]
  if "CO2 emission" in other:
    selected_table_name.append("TRA_Emissions-CO2")
  elif "Land TransportLump Sum Investment Cost" in other:
    selected_table_name.append("TRA-Land_LumpInv")

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                             (all_data_melted['Year'] >= year_range[0]) &
                                             (all_data_melted['Year'] <= year_range[1])&
                                             (all_data_melted['tableName'].isin(selected_table_name))]
  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Transport Other'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('supply-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('supply-source-dropdown', 'value')
)
def supply_chart(scenario, year_range, supply_source):
    if supply_source == 'Biodiesel':
        table_name = 'SUP_BIODST'
    elif supply_source == 'Ethanol':
        table_name = 'SUP_BIOETH'
    elif supply_source == 'Biogas':
        table_name = 'SUP_BIOGAS'
    all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
        (all_data_melted['Year'] >= year_range[0]) &
        (all_data_melted['Year'] <= year_range[1])&
        (all_data_melted['tableName']== table_name)]

    fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title=f'({supply_source}) supply by source({year_range[0]}–{year_range[1]})'
    )
    fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
    return fig


@app.callback(
    Output('Hydrogen Production', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value')
)
def hydrogen_production(scenario, year_range):

  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
        (all_data_melted['Year'] >= year_range[0]) &
        (all_data_melted['Year'] <= year_range[1])&
        (all_data_melted['tableName']== "SUP_HYDROGEN")]

  fig = px.area(
      all_data_melted_filtered,
      x='Year',
      y='Value', # Changed y to 'Value'
      color='seriesName', # Changed color to 'seriesName'
      title='Hydrogen Production'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

@app.callback(
    Output('capacity-chart', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('capacity-dropdown', 'value')
)
def capacity_chart(scenario, year_range, capacity_type):
  if capacity_type == 'installed':
    table_name = 'PWR_Cap'
  elif capacity_type == 'new':
    table_name = 'PWR_Cap-N'
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == table_name)]
  fig = px.area(
      all_data_melted_filtered,
      x='Year',
      y='Value', # Changed y to 'Value'
      color='seriesName', # Changed color to 'seriesName'
      title= f'{capacity_type} Capacity'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig


@app.callback(
    Output('CO2-emission-power', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
)
def co2_emission_power(scenario, year_range):
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == "PWR_Emissions-CO2")]

  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='CO2 Emissions'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig
@app.callback(
    Output('Electricity-generation-PP', 'figure'),
    Input('scenario-dropdown', 'value'),
    Input('year-slider', 'value'),
)
def elec_generation(scenario, year_range):
  all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                            (all_data_melted['Year'] >= year_range[0]) &
                                            (all_data_melted['Year'] <= year_range[1])&
                                            (all_data_melted['tableName'] == "PWR_Gen-ELCC")]

  fig = px.area(
        all_data_melted_filtered,
        x='Year',
        y='Value', # Changed y to 'Value'
        color='seriesName', # Changed color to 'seriesName'
        title='Electricity Generation by PP'
  )
  fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
  return fig

if __name__ == '__main__':
    app.run(debug=True)


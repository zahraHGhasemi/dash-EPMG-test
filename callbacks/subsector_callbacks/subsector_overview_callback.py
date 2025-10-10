from dash import dcc, html
from dash.dependencies import Input, Output
from utils.plot_chart import plot_chart
from utils.filter_dataframe import filter_df_by_category
from utils.dataframe_melter import get_data_melted
def register_subsector_overview_callback(app):#, all_data_melted):
    dict_table_name = {'Transport': 'TRA_FEC', 'Residential': 'RSD_FEC', 'Services': 'SRV_FEC',
                        'Industry': 'IND_FEC', 'Agriculture': 'AGR_FEC'}
    @app.callback(
        Output('FEC_by_sector_chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('FEC-sector-dropdown', 'value')
    )

    def FEC_by_sector(scenario, year_range, selected_sectors):
        table_name = dict_table_name[selected_sectors]
        all_data_melted = get_data_melted(scenario, year_range)

        all_data_melted_filtered = all_data_melted[(all_data_melted['tableName'] == table_name)]

        return plot_chart(all_data_melted_filtered)
    
    
    @app.callback(
        Output('source-by-sector-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('source-by-sector-dropdown', 'value')
    )
    def source_by_sector(scenario, year_range, source):
        all_data_melted = get_data_melted(scenario, year_range)

        df_filtered = filter_df_by_category(all_data_melted,['SYS','Sector', 'FEC'],['Cost', 'Lump'])
        
        dic_source = dict(zip(df_filtered['tableTitle'].unique(),df_filtered['tableName'].unique()))
        
        # dic_source  = {'FEC of Biodiesel by Sector': 'SYS_FEC-BIODST_Sector',
        #             'FEC of Ethanol by Sector': 'SYS_FEC-BIOETH_Sector',
        #             'FEC of Biogas by Sector': 'SYS_FEC-BIOGAS_Sector',
        #             'FEC of Biomass by Sector': 'SYS_FEC-BIOWOOx_Sector',
        #             'FEC of Coal by Sector': 'SYS_FEC-COA_Sector',
        #             'FEC of Electricity by Sector': 'SYS_FEC-ELCD_Sector',
        #             'FEC of Nat. Gas by Sector': 'SYS_FEC-GASNAT_Sector',
        #             'FEC of Hydrogen by Sector': 'SYS_FEC-H2_Sector',
        #             'FEC of Heat by Sector': 'SYS_FEC-HETD_Sector',
        #             'FEC of HFO by Sector': 'SYS_FEC-HFO_Sector',
        #             'FEC of LPG by Sector': 'SYS_FEC-LPG_Sector',
        #             'FEC of Diesel by Sector': 'SYS_FEC-OILDST_Sector',
        #             'FEC of Gasoline by Sector': 'SYS_FEC-OILGSL_Sector',
        #             'FEC of Kerosene by Sector': 'SYS_FEC-OILKER_Sector',
        #             'FEC of Peat by Sector': 'SYS_FEC-PEAT_Sector',
        #             'Final Energy Consumption by Sector': 'SYS_FEC_Sector'}
        ls_source=[]
        for s in source:
            if s in dic_source.keys():
                ls_source.append(dic_source[s])

        all_data_melted_filtered = all_data_melted[(all_data_melted['tableName'].isin(ls_source))]
        return plot_chart(all_data_melted_filtered, type = 'bar')


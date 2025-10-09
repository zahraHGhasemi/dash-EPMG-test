
    # sector-content
from dash.dependencies import Input, Output
from components.subsectors.subsector_transport import subsector_transport
from components.subsectors.subsector_overview import subsector_overview   
from components.subsectors.subsector_residential import subsector_residential
from components.subsectors.subsector_services import subsector_services
from components.subsectors.subsector_industry import subsector_industry
from utils.dataframe_melter import get_data_melted

def register_sector_callbacks(app):#, all_data_melted):
    all_data_melted = get_data_melted()
    @app.callback(
        Output("sector-content", "children"),
        Input("sector-radio", "value")
    )

    def display_sector_content(active_sector):

        if active_sector == "overview":
            return subsector_overview(all_data_melted)
            
        elif active_sector == "transport":
            return subsector_transport(all_data_melted)

        elif active_sector == "residential":
            return subsector_residential

        elif active_sector == "services":
            return subsector_services

        elif active_sector == "industry":
            return subsector_industry


import plotly.express as px

def plot_chart(all_data_melted_filtered, type = 'area'):
    color_col = 'seriesTitle' if all_data_melted_filtered['seriesTitle'].notna().any() else 'seriesName'
    table_title = all_data_melted_filtered['tableTitle'].unique()[0] 
    title_col = table_title if  table_title != 'nan' else all_data_melted_filtered['tableName'].unique()[0] 
    if type == 'bar':
        fig = px.bar(
            all_data_melted_filtered,
            x='Year',
            y='Value', # Changed y to 'Value'
            color=color_col, #'seriesTitle', # Changed color to 'seriesName',
            title  = title_col #all_data_melted_filtered['tableTitle'].unique()[0]
        )
        fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
        return fig
    elif type == 'line':
        fig = px.line(
            all_data_melted_filtered,
            x='Year',
            y='Value', # Changed y to 'Value'
            color=color_col, #'seriesTitle', # Changed color to 'seriesName',
            title  = title_col #tiall_data_melted_filtered['tableTitle'].unique()[0]
        )
        fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
        return fig
    elif type == 'area':
        fig = px.area(
            all_data_melted_filtered,
            x='Year',
            y='Value', # Changed y to 'Value'
            color=color_col, #'seriesTitle', # Changed color to 'seriesName',
            title  = title_col #tiall_data_melted_filtered['tableTitle'].unique()[0]
        )
        fig.update_layout(xaxis_title='Year', yaxis_title= all_data_melted_filtered['label'].unique()[0] if not all_data_melted_filtered.empty else 'Value') # Updated yaxis_title
        return fig
    
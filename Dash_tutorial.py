# import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Get unique values for the filtering dropdown
continents = df['continent'].unique()

# App layout
app.layout = html.Div([
    # Title
    html.Div(className='row', children='Dash Tutorial',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
    # Graph Radio options
    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                       value='lifeExp',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),
    dcc.Graph(figure={}, id='histo-chart-final'),
    # html.Div(className='row', children=[
    #     html.Div(className='six columns', children=[
    #         dcc.Graph(figure={}, id='histo-chart-final')
    #     ])
    # ]),
    # Table filtering
    html.Div(className='row', children=[
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': continent, 'value': continent} for continent in continents],
            value=None,
            placeholder='Filter by Continent'
        )
    ]),
    dash_table.DataTable(id='data-table', page_size=11, style_table={'overflowX': 'auto'})
    # html.Div(className='row', children=[
    #     html.Div(className='six columns', children=[
    #         dash_table.DataTable(id='data-table', page_size=11, style_table={'overflowX': 'auto'})
    #     ])
    # ])
])

# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Output(component_id='data-table', component_property='data'),
    Input(component_id='my-radio-buttons-final', component_property='value'),
    Input(component_id='continent-dropdown', component_property='value')
)
def update_graph(col_chosen, continent_chosen):
    filtered_df = df.copy()
    
    # Apply filtering if continent is chosen
    if continent_chosen:
        filtered_df = filtered_df[filtered_df['continent'] == continent_chosen]

    fig = px.histogram(filtered_df, x='continent', y=col_chosen, histfunc='avg')
    table_data = filtered_df.to_dict('records')

    return fig, table_data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# 다른 사람에게 공유할 수 있게 하는 코드
# if __name__ == '__main__':
#     app.run_server(host='0.0.0.0', port=8050)
# 0.0.0.0: 예시 IP
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from dash.dependencies import State

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)[["country", "pop", "continent", "lifeExp"]]

groups = df['country'].unique()

app = Dash(__name__)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [

    html.H1("Download Filtered Table", style={'text-align': 'center'}),

    dcc.Dropdown(id="country",
                 options=groups,
                 multi=False,
                 value=groups[0],
                 style={'width': "40%"}
                 ),
    
    html.Br(),

    html.Button("Download CSV", id="btn_csv"),

    dcc.Download(id="download-dataframe-csv"),

    dash_table.DataTable(id='table',
                        page_size=10),
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='table', component_property='data'),
    Input(component_id='country', component_property='value')
)

def update_table(selected_country):

    dff = df.copy()
    dff = dff[dff["country"] == selected_country]

    table = dff.to_dict("records")

    return table

@app.callback(
    Output(component_id = "download-dataframe-csv", component_property = "data"),
    Input(component_id = "btn_csv", component_property = "n_clicks"),
    State(component_id ="country", component_property ="value"),
    prevent_initial_call=True,
)

def update_table(n_clicks, selected_country):
    dff = df.copy()
    dff = dff[dff["country"] == selected_country]
    
    return dcc.send_data_frame(dff.to_csv, "mydf.csv")

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
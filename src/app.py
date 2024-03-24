import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv("https://raw.githubusercontent.com/daniguariso/HMT_Proposal/main/Data%20Proposal/Budget_Data.csv")
df["id"] = df.index

app.layout = html.Div(children=[
    dash_table.DataTable(
        id="table",
        row_selectable="multi",
        style_data_conditional= [],
        tooltip_data = [],
        style_cell={'textAlign': 'center'},
        style_cell_conditional=[
                {
                    'if': {'column_id': 'TOTAL'},
                    'textAlign': 'right'
                }
            ],
        style_header={
        'backgroundColor': 'grey',
        'fontWeight': 'bold',
        'color': 'black',
        'fontSize':16
        },        
        columns=[{"name": i, "id": i} for i in df.columns if i != "id" and i !="SDG"
                 and i != "SDG Description" and i != "Colour" and i != "SDG Target"
                 and i != "SDG Target Description" and i != "SDG Indicator" 
                 and i != "SDG Indicator Description"],
        data=df.to_dict("records"),
 #       page_size=10,
 #       filter_action="native",
        tooltip_duration=None,
        css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: grey; font-family: monospace; color: white'
    }]
    )], id= "table_container"
)


@app.callback(
    Output("table", "style_data_conditional"),
    Input("table", "derived_virtual_selected_row_ids"),
    Input("table", "page_current")
)
def style_selected_rows(selRows, pg):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} = {}".format(i)}, "backgroundColor": df.loc[i, "Colour"]}
        for i in selRows
    ]

@app.callback(
    Output("table", "tooltip_conditional"),
    Input("table", "derived_virtual_selected_row_ids"),
    Input("table", "page_current")
)
def update_output(selRows, pg):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} = {}".format(i)}, 'type': 'markdown',
            'value': '**SDG {}**: {} \n\n**Target {}**: {} \n\n**Indicator {}**: {}'.format(
                str(df.loc[i, "SDG"]),
                df.loc[i, "SDG Description"],
                str(df.loc[i, "SDG Target"]),
                df.loc[i, "SDG Target Description"],
                str(df.loc[i, "SDG Indicator"]),
                df.loc[i, "SDG Indicator Description"]
            )}
        for i in selRows
    ]
if __name__ == "__main__":
    app.run_server(debug=True)
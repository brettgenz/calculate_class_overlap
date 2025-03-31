import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd


# load data frame with embeddings
df = pd.read_pickle('./data/processed/train_with_embeddings.pkl')

# create the Dash app
app = dash.Dash(__name__)

# extract unique classes from the data frame to create dropdown options
unique_classes = df['category'].unique()
checklist_options = [{'label': str(cls), 'value': cls} for cls in unique_classes]

app.layout = html.Div([
    html.H1("Embedding Scatterplot Viewer", style={'textAlign': 'center'}),
    
    # Checklist for class selection
    html.Div([
        # left column
        html.Div([
            html.H4("Select classes to display:"),
            dcc.Checklist(
                id='class-checklist',
                options=checklist_options,
                value=unique_classes,  # show all classes by default
                labelStyle={'display': 'block', 'margin-right': '10px'}
                ),
            # buttons to select / deselect all checkboxes
            html.Div([
                html.Button("Check All", id="check-all", n_clicks=0, style={'margin-right': '10px'}),
                html.Button("Uncheck All", id="uncheck-all", n_clicks=0)
            ], style={'padding': '10px'})
        ], style={'width': '30%', 'textAlign': 'left', 'padding': '20px'}),

        # right column
        html.Div([
            # Scatterplot
            dcc.Graph(id='scatter-plot')
        ], style={'width': '70%', 'textAlign': 'center', 'padding': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'row'})
    
    
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('class-checklist', 'value')
)
def update_scatter(selected_classes):
    # If no classes are selected, you might choose to show an empty plot
    if not selected_classes:
        filtered_df = pd.DataFrame(columns=df.columns)
    else:
        filtered_df = df[df['category'].isin(selected_classes)]
    
    fig = px.scatter(
        filtered_df,
        x='x_2d',
        y='y_2d',
        color='category',
        # title="Embedding Scatterplot",
        labels={'x_2d': 'X Coordinate', 'y_2d': 'Y Coordinate'},
        height=700,
        width=1000
    )
    
    # Optional: Adjust layout properties
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Callback to update checklist value based on button clicks
@app.callback(
    Output('class-checklist', 'value'),
    Input('check-all', 'n_clicks'),
    Input('uncheck-all', 'n_clicks'),
    State('class-checklist', 'options')
)
def update_checklist(check_all_clicks, uncheck_all_clicks, options):
    # use callback_context to determine which button was clicked
    ctx = callback_context
    if not ctx.triggered:
        # no button clicked; don't change the checklist value
        return unique_classes
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'check-all':
            # return all available values
            return [option['value'] for option in options]
        elif button_id == 'uncheck-all':
            return [] # uncheck all options
    return unique_classes

if __name__ == '__main__':
    app.run(debug=True)
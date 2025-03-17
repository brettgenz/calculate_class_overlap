import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# load data frame with embeddings
df = pd.read_pickle('./data/processed/train_with_embeddings.pkl')

# create the Dash app
app = dash.Dash(__name__)

# extract unique classes from the data frame to create dropdown options
unique_classes = df['category'].unique()
dropdown_options = [{'label': str(cls), 'value': cls} for cls in unique_classes]

# define the app layout - two dropdowns and a scatterplot
app.layout = html.Div([

    html.H1("Embedding Viewer"),

    # Parent container using flex display
    html.Div([
        # Left side: Dropdowns container
        html.Div([
            html.Label("Select Class 1"),
            dcc.Dropdown(
                id='class1-dropdown',
                options=dropdown_options,
                value=unique_classes[0]
            ),
            html.Br(),
            html.Label("Select Class 2"),
            dcc.Dropdown(
                id='class2-dropdown',
                options=dropdown_options,
                value=unique_classes[1] if len(unique_classes) > 1 else unique_classes[0]
            )
        ], style={'width': '30%', 'padding': '20px'}),
        
        # Right side: Scatterplot container
        html.Div([
            dcc.Graph(id='scatter-plot')
        ], style={'width': '70%', 'padding': '20px'})
        
    ], style={'display': 'flex', 'flexDirection': 'row'})
])

# callback function to update scatter plot based on selected classes
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('class1-dropdown', 'value'),
    Input('class2-dropdown', 'value')
)


def update_scatterplot(class1, class2):
    """
    Updates the scatterplot based on user selections
    """

    # filter df for the selected classes
    filtered_df = df[df['category'].isin([class1, class2])]

    # create scatterplot using Plotly Express
    fig = px.scatter(
        filtered_df,
        x='x_2d',
        y='y_2d',
        color='category',
        title=f"Scatterplot of classes {class1} and {class2}",
        labels={'x_2d': 'X', 'y_2d': 'Y'},
        height=800,
        width=1000,
        template="ggplot2"
    )

    return(fig)


if __name__ == '__main__':
    app.run(debug=True)
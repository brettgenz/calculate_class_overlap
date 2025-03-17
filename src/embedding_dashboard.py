import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# load data frame with embeddings
df = pd.read_pickle('./data/processed/train_with_embeddings.pkl')

# load overlap matrix
df_overlap = pd.read_csv('./data/processed/df_overlap.csv')

# create the Dash app
app = dash.Dash(__name__)

# extract unique classes from the data frame to create dropdown options
unique_classes = df['category'].unique()
dropdown_options = [{'label': str(cls), 'value': cls} for cls in unique_classes]

# create plot of overlap matrix
overlap_fig = px.imshow(df_overlap,
                text_auto='.2f',
                color_continuous_scale='RdYlGn_r',
                aspect='auto',
                title="Overlap Coefficient Heat Map",
                height=600,
                width=600,
                template="ggplot2"
                )

overlap_fig.update_layout(title_x=0.5)
overlap_fig.update_xaxes(tickangle=45)


# define the app layout
app.layout = html.Div([
    # Overall page title
    html.H1("Class Overlap Analysis", style={'textAlign': 'center'}),
    # Parent container: two columns side by side.
    html.Div([
        # Left column: Overlap matrix
        html.Div([
            dcc.Graph(
                id='overlap-matrix',
                figure=overlap_fig
            )
        ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        # Right column: Dropdowns and scatterplot
        html.Div([
            # Dropdown container on top
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
            ], style={'marginBottom': '20px'}),
            # Scatterplot below the dropdowns
            dcc.Graph(id='scatter-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])


# set color options for points in scatterplot
colors = ['orange', 'blue', 'purple', 'green', 'red']


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
        color_discrete_sequence=colors,
        title=f"Scatterplot of classes {class1} and {class2}",
        labels={'x_2d': 'X', 'y_2d': 'Y'},
        height=600,
        width=800,
        template="ggplot2"
    )

    return(fig)


if __name__ == '__main__':
    app.run(debug=True)
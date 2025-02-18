import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the dataset
df = pd.read_csv('final_merged_data.csv')

# Define variable categories
numerical_vars = ['Age', 'CGPA', 'Work/Study Hours', 'Work Pressure', 
                  'Academic Pressure', 'Study Satisfaction', 'Job Satisfaction']
categorical_vars = ['Gender', 'City', 'Degree', 'Sleep Duration', 'Profession', 'Dietary Habits']

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Student Wellbeing Analysis Dashboard", style={'textAlign': 'center'}),
    
    # Row for separate categorical and numerical analyses
    html.Div([
        # Categorical Analysis (Bar Chart) with Orientation Toggle
        html.Div([
            html.H3("Categorical Variable Analysis (Bar Chart)"),
            dcc.Dropdown(
                id='cat-variable',
                options=[{'label': col, 'value': col} for col in categorical_vars],
                value=categorical_vars[0],
                style={'width': '100%'}
            ),
            dcc.RadioItems(
                id='bar-orientation',
                options=[
                    {'label': 'Upright', 'value': 'v'},
                    {'label': 'Sideways', 'value': 'h'}
                ],
                value='v',
                style={'margin': '10px 0'}
            ),
            dcc.Graph(id='bar-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Numerical Analysis (Histogram) with Orientation Toggle
        html.Div([
            html.H3("Numerical Variable Analysis (Histogram)"),
            dcc.Dropdown(
                id='num-variable',
                options=[{'label': col, 'value': col} for col in numerical_vars],
                value=numerical_vars[0],
                style={'width': '100%'}
            ),
            dcc.RadioItems(
                id='hist-orientation',
                options=[
                    {'label': 'Upright', 'value': 'v'},
                    {'label': 'Sideways', 'value': 'h'}
                ],
                value='v',
                style={'margin': '10px 0'}
            ),
            dcc.Graph(id='histogram')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'verticalAlign': 'top'})
    ]),
    
    # Row for Scatter Plot and Pie Chart (unchanged)
    html.Div([
        html.H3("Scatter Plot and Pie Chart Analysis"),
        html.Div([
            # Scatter Plot Section with interactive dropdowns
            html.Div([
                dcc.Dropdown(
                    id='x-axis',
                    options=[{'label': col, 'value': col} for col in numerical_vars],
                    value='Age',
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='y-axis',
                    options=[{'label': col, 'value': col} for col in numerical_vars],
                    value='CGPA',
                    style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}
                ),
                dcc.Graph(id='scatter-plot')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            # Pie Chart Section
            html.Div([
                html.Div([
                    html.Label("Choose a Categorical Variable:", style={'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='pie-variable',
                        options=[{'label': col, 'value': col} for col in categorical_vars],
                        value='Gender',
                        style={'width': '100%'}
                    )
                ], style={'marginBottom': '10px'}),
                dcc.Graph(id='pie-chart')
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'verticalAlign': 'top'})
        ])
    ], style={'marginTop': '20px'}),
    
    # Dataset description and notes
    html.Div([
        html.H2("Dataset Description", style={'marginTop': '20px'}),
        html.P("""
            This dataset contains valuable information about student wellbeing and academic performance. 
            Key attributes include:
            - Demographics: Age, Gender, City
            - Academic Metrics: CGPA, Degree, Study Hours
            - Wellbeing Indicators: Depression, Sleep Duration, Work/Academic Pressure
            - Satisfaction Metrics: Study and Job Satisfaction
            - Lifestyle: Dietary Habits
        """),
        html.H2("Why This Data is Interesting"),
        html.P("""
            This dataset is particularly interesting because it combines academic performance metrics with 
            wellbeing indicators, allowing us to:
            1. Analyze the relationship between study hours and academic performance
            2. Investigate the impact of sleep duration on depression levels
            3. Understand how academic pressure affects study satisfaction
            4. Explore the connection between dietary habits and overall performance
        """),
        html.H2("Implementation Notes"),
        html.P("""
            The dashboard implementation features:
            - Separate visualizations for categorical (bar charts) and numerical (histograms) data
            - Interactive variable selection for flexible analysis
            - Toggle buttons to switch between upright and sideways (horizontal) chart orientations
            - Scatter plot functionality for pairwise analysis between two numerical variables
            - A pie chart to visualize the distribution of a chosen categorical variable
            - Responsive design for an improved user experience
        """)
    ])
])

# Callbacks

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('cat-variable', 'value'),
     Input('bar-orientation', 'value')]
)
def update_bar_chart(selected_var, orientation):
    """Updates the bar chart based on the selected categorical variable and orientation."""
    value_counts = df[selected_var].value_counts()
    
    # Depending on the orientation, swap x and y
    if orientation == 'v':
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            labels={'x': selected_var, 'y': 'Count'},
            title=f'Distribution of {selected_var}'
        )
    else:  # orientation == 'h'
        fig = px.bar(
            x=value_counts.values,
            y=value_counts.index,
            orientation='h',
            labels={'x': 'Count', 'y': selected_var},
            title=f'Distribution of {selected_var}'
        )
    return fig

@app.callback(
    Output('histogram', 'figure'),
    [Input('num-variable', 'value'),
     Input('hist-orientation', 'value')]
)
def update_histogram(selected_var, orientation):
    """Updates the histogram based on the selected numerical variable and orientation."""
    # For histogram, swap x and y based on orientation
    if orientation == 'v':
        fig = px.histogram(
            df, 
            x=selected_var, 
            nbins=10,
            title=f'Distribution of {selected_var}'
        )
        fig.update_layout(
            xaxis_title=selected_var,
            yaxis_title='Count'
        )
    else:  # orientation == 'h'
        fig = px.histogram(
            df, 
            y=selected_var, 
            nbins=10,
            title=f'Distribution of {selected_var}'
        )
        fig.update_layout(
            xaxis_title='Count',
            yaxis_title=selected_var
        )
    return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value')]
)
def update_scatter(x_var, y_var):
    """Updates the scatter plot based on the selected x and y numerical variables."""
    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        title=f'{y_var} vs {x_var}',
        trendline="ols"
    )
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-variable', 'value')
)
def update_pie_chart(selected_var):
    """Creates a pie chart showing the distribution of the selected categorical variable."""
    fig = px.pie(
        df,
        names=selected_var,
        title=f"Distribution of {selected_var}"
    )
    fig.update_layout(
        template="simple_white",
        font=dict(size=14),
        title_x=0.5  # center the title
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

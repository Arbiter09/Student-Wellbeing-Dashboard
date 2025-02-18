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

# Layout with Tabs
app.layout = html.Div([
    html.H1("Student Wellbeing Analysis Dashboard", style={'textAlign': 'center'}),
    
    dcc.Tabs([
        # Tab 1: Categorical and Numerical Analysis
        dcc.Tab(label='Analysis', children=[
            html.Div([
                # Row for Categorical (Bar Chart) and Numerical (Histogram) analyses
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
                ])
            ])
        ]),
        
        # Tab 2: Scatter Plot and Pie Chart Analysis
        dcc.Tab(label='Scatter & Pie', children=[
            html.Div([
                html.Div([
                    # Scatter Plot Section with interactive dropdowns and axis assignment radio button
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
                        dcc.RadioItems(
                            id='axis-assignment',
                            options=[
                                {'label': 'First dropdown → X-axis, Second dropdown → Y-axis', 'value': 'normal'},
                                {'label': 'First dropdown → Y-axis, Second dropdown → X-axis', 'value': 'swap'}
                            ],
                            value='normal',
                            style={'margin': '10px 0'}
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
            ])
        ]),
        
        # Tab 3: Dataset Information
        dcc.Tab(label='Dataset Info', children=[
            html.Div([
                html.H2("Dataset Description", style={'marginTop': '20px'}),
                html.P("""
                    This dataset offers a comprehensive look into student wellbeing and academic performance. 
                    It includes information collected from a diverse student population across various cities, capturing:
                    • Demographic details such as Age, Gender, and City.
                    • Academic indicators including CGPA, Degree type, and Study Hours.
                    • Wellbeing metrics like Sleep Duration, Work/Academic Pressure, and Depression levels.
                    • Satisfaction measures, encompassing both Study Satisfaction and Job Satisfaction.
                    • Lifestyle factors, notably Dietary Habits.
                    With a robust number of entries, the dataset provides valuable insights into how these variables interact 
                    and impact overall student performance and wellbeing.
                """),
                html.H2("Why This Data is Interesting"),
                html.P("""
                    This dataset is particularly intriguing because it bridges the gap between academic achievement and personal wellbeing. 
                    By analyzing this data, one can:
                    • Investigate how lifestyle choices and sleep patterns influence academic performance.
                    • Explore the relationship between work pressure and student satisfaction.
                    • Uncover trends in how demographic factors affect both academic results and overall mental health.
                    • Inform strategies for enhancing educational outcomes and wellbeing programs.
                """),
                html.H2("Implementation Notes"),
                html.P("""
                    The dashboard has been built to facilitate an interactive analysis of this rich dataset. Key features include:
                    • Dynamic visualization options for both categorical and numerical variables.
                    • Customizable chart orientations and axis assignments to suit varied analytical needs.
                    • Interactive scatter plots with trendlines to reveal underlying correlations.
                    • Responsive design using Dash Tabs to neatly organize the analyses and dataset insights.
                    • User-friendly controls that allow for real-time updates to graphs, enhancing the exploratory experience.
                """)
            ], style={'padding': '20px'})
        ])
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
     Input('y-axis', 'value'),
     Input('axis-assignment', 'value')]
)
def update_scatter(x_var, y_var, axis_assignment):
    """Updates the scatter plot based on the selected x and y numerical variables and axis assignment."""
    if axis_assignment == 'swap':
        x_var, y_var = y_var, x_var
    
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
        title_x=0.5
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

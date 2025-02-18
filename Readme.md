# Student Wellbeing Analysis Dashboard

## Overview

This interactive dashboard provides insights into student wellbeing by analyzing factors like academic performance, lifestyle, and mental health. It allows users to explore categorical and numerical data using bar charts, histograms, scatter plots, and pie charts. The dashboard is built using Dash, Plotly, and Pandas.

## Features

- **Categorical Analysis (Bar Chart)**: Visualize distributions of categorical variables.
- **Numerical Analysis (Histogram)**: Explore the distribution of numerical variables.
- **Scatter Plot**: Analyze relationships between two numerical variables.
- **Pie Chart**: Examine the proportions of categorical variables.
- **Interactive Controls**: Choose variables and adjust chart orientations.
- **Responsive Design**: Optimized for seamless user experience.

## Dataset

The dataset (`final_merged_data.csv`) contains the following categories:

- **Demographics**: Age, Gender, City
- **Academics**: CGPA, Degree, Study Hours
- **Wellbeing Metrics**: Work/Academic Pressure, Study Satisfaction, Job Satisfaction
- **Lifestyle Factors**: Sleep Duration, Dietary Habits

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Arbiter09/Student-Wellbeing-Dashboard.git
   cd Student-Wellbeing-Dashboard
   ```
2. Install dependencies:
   ```bash
   pip install dash pandas plotly
   ```
3. Place `final_merged_data.csv` in the project directory.
4. Run the dashboard:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://127.0.0.1:8050/`

## Usage

- Select a categorical variable to generate a bar chart.
- Choose a numerical variable to view its histogram.
- Adjust orientation (vertical/horizontal) for both charts.
- Compare numerical variables using the scatter plot.
- View category distributions with the pie chart.

## Dependencies

- Python 3.x
- Dash
- Plotly
- Pandas

## License

This project is open-source and available under the [MIT License](LICENSE).

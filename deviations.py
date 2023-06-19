import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

df = pd.read_csv('dev.csv')
df = df[df['sample_type'].notna()]
df = df[df['grade_name'].notna()]
df = df[df['element_name'].notna()]
df['modified_at'] = pd.to_datetime(df['modified_at'])

app = dash.Dash(__name__)

min_date = df['modified_at'].min()
max_date = df['modified_at'].max()

app.layout = html.Div([
    html.H1("Interactive Line Plot"),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=min_date,
        end_date=max_date
    ),
    dcc.Dropdown(id='customer-dropdown'),
    dcc.Dropdown(id='grade-dropdown'),
    dcc.Dropdown(id='sampleType-dropdown'),
    dcc.Dropdown(id='element-dropdown'),
    html.Button('Apply Filters', id='apply-filters', n_clicks=0),
    dcc.Graph(id='line-plot'),
    html.Div(id='df-container')
])

# Update customer dropdown based on date selection
@app.callback(
    Output('customer-dropdown', 'options'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def set_customer_options(start_date, end_date):
    filtered_df = df[(df['modified_at'] >= pd.to_datetime(start_date)) &
                     (df['modified_at'] <= pd.to_datetime(end_date))]
    return [{'label': i, 'value': i} for i in filtered_df['company_name'].unique()]

# Update grade dropdown based on customer selection
@app.callback(
    Output('grade-dropdown', 'options'),
    [Input('customer-dropdown', 'value')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def set_grade_options(selected_customer, start_date, end_date):
    filtered_df = df[(df['modified_at'] >= pd.to_datetime(start_date)) &
                     (df['modified_at'] <= pd.to_datetime(end_date)) &
                     (df['company_name'] == selected_customer)]
    return [{'label': i, 'value': i} for i in filtered_df['grade_name'].unique()]

# Update sampleType dropdown based on grade selection
@app.callback(
    Output('sampleType-dropdown', 'options'),
    [Input('grade-dropdown', 'value')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date'),
     State('customer-dropdown', 'value')]
)
def set_sampleType_options(selected_grade, start_date, end_date, selected_customer):
    filtered_df = df[(df['modified_at'] >= pd.to_datetime(start_date)) &
                     (df['modified_at'] <= pd.to_datetime(end_date)) &
                     (df['company_name'] == selected_customer) &
                     (df['grade_name'] == selected_grade)]
    return [{'label': i, 'value': i} for i in filtered_df['sample_type'].unique()]

# Update element dropdown based on sampleType selection
@app.callback(
    Output('element-dropdown', 'options'),
    [Input('sampleType-dropdown', 'value')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date'),
     State('customer-dropdown', 'value'),
     State('grade-dropdown', 'value')]
)
def set_element_options(selected_sampleType, start_date, end_date, selected_customer, selected_grade):
    filtered_df = df[(df['modified_at'] >= pd.to_datetime(start_date)) &
                     (df['modified_at'] <= pd.to_datetime(end_date)) &
                     (df['company_name'] == selected_customer) &
                     (df['grade_name'] == selected_grade) &
                     (df['sample_type'] == selected_sampleType)]
    return [{'label': i, 'value': i} for i in filtered_df['element_name'].unique()]

# Update the graph and the data displayed
@app.callback(
    [Output('line-plot', 'figure'),
     Output('df-container', 'children')],
    [Input('apply-filters', 'n_clicks')],
    [State('date-picker', 'start_date'),
     State('date-picker', 'end_date'),
     State('customer-dropdown', 'value'),
     State('grade-dropdown', 'value'),
     State('sampleType-dropdown', 'value'),
     State('element-dropdown', 'value')]
)
def update_output(n_clicks, start_date, end_date, selected_customer, selected_grade, selected_sampleType, selected_element):
    if n_clicks > 0:
        filtered_df = df[(df['modified_at'] >= pd.to_datetime(start_date)) &
                         (df['modified_at'] <= pd.to_datetime(end_date)) &
                         (df['company_name'] == selected_customer) &
                         (df['grade_name'] == selected_grade) &
                         (df['sample_type'] == selected_sampleType) &
                         (df['element_name'] == selected_element)]

        fig = px.line(filtered_df, x='heat_name', y='deviation',
                      title=f'Value over Time for {selected_customer}, {selected_grade}, {selected_sampleType}, {selected_element}')

        df_preview = html.Pre(filtered_df.head(5).to_string())
        
        return fig, df_preview

    return dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import duckdb
from query_functions import unique_categories, transaction_amount_distribution
from database import connect_to_database , create_data_table

# Connect to DuckDB
con = connect_to_database()
con = duckdb.connect(database=":memory:", read_only=False)
csv_file_path = r"C:\Users\user\OneDrive\Desktop\Virtual Env\duckdbproject\fraud test.csv"
create_data_table(con, csv_file_path)
# Create the Dash app
app = dash.Dash(__name__)

#layout of the app
app.layout = html.Div([
    html.H1("Dashboard"),
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in unique_categories(con)],
            value='Category'
        )
    ]),
    dcc.Graph(id='transaction-graph'),
    dcc.Graph(id='amount-distribution-chart')
])

#update the graphs based on the selected category
@app.callback(
    [Output('transaction-graph', 'figure'),
     Output('amount-distribution-chart', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_graphs(selected_category):
    # Update the transaction bar chart
    query1 = f"SELECT COUNT(*) AS total_transactions FROM data WHERE category = '{selected_category}'"
    result1 = con.execute(query1).fetchall()
    total_transactions = result1[0][0]
    transaction_figure = {
        'data': [{'x': [selected_category], 'y': [total_transactions], 'type': 'bar'}],
        'layout': {
            'title': f'Total Transactions for {selected_category}',
            'xaxis': {'title': 'Category'},
            'yaxis': {'title': 'Total Transactions'}
        }
    }

    amount_distribution_data = transaction_amount_distribution(con)
    amount_distribution_figure = {
        'data': [{
            'labels': [item['category'] for item in amount_distribution_data],
            'values': [item['total_amount'] for item in amount_distribution_data],
            'type': 'pie'
        }],
        'layout': {
            'title': 'Transaction Amount Distribution by Category'
        }
    }

    return transaction_figure, amount_distribution_figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Import necessary modules
import duckdb
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Import functions from other modules
from database import connect_to_database, create_data_table
from query_functions import count_total_transactions, gender_distribution

# Function to generate word cloud
def generate_word_cloud(gender_dist_list):
    gender_dict = {item['gender']: item['num_transactions'] for item in gender_dist_list}
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(gender_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    # Connect to DuckDB and create the "data" table
    con = connect_to_database()
    csv_file_path = r"C:\Users\user\OneDrive\Desktop\Virtual Env\duckdbproject\fraud test.csv"  # Update with your CSV file path
    create_data_table(con, csv_file_path)

    # Call SQL queries using the defined functions and store the results
    total_transactions_obj = count_total_transactions(con)
    gender_dist_list = gender_distribution(con)

    # Print or use the results as needed
    print("Total Transactions:", total_transactions_obj.total_transactions)
    print("Gender Distribution:", gender_dist_list)

    # Generate and display word cloud for gender distribution
    generate_word_cloud(gender_dist_list)

if __name__ == "__main__":
    main()

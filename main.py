from database import connect_to_database, create_data_table
from plotting_functions import (plot_average_transaction_by_category,
                                plot_gender_distribution,
                                plot_top_merchants_by_total_amount,
                                plot_total_transactions)
from query_functions import (average_transaction_amount_by_category,
                             count_total_transactions, gender_distribution,
                             top_merchants_by_total_amount, unique_categories)


def main():
    # Connect to DuckDB and create the "data" table
    con = connect_to_database()
    csv_file_path = r"C:\Users\user\OneDrive\Desktop\Virtual Env\duckdbproject\fraud test.csv"
    create_data_table(con, csv_file_path)

    # Call SQL queries using the defined functions and store the results
    total_transactions_obj = count_total_transactions(con)  # Pass 'con' as argument
    unique_categories_list = unique_categories(con)  # Pass 'con' as argument
    categories_avg_amount_list = average_transaction_amount_by_category(con)  # Pass 'con' as argument
    top_merchants_list = top_merchants_by_total_amount(con)  # Pass 'con' as argument
    gender_dist_list = gender_distribution(con)  # Pass 'con' as argument

    # Print or use the results as needed
    print("Total Transactions:", total_transactions_obj.total_transactions)
    print("Unique Categories:", unique_categories_list)
    print("Average Transaction Amount by Category:", categories_avg_amount_list)
    print("Top Merchants by Total Amount:", top_merchants_list)
    print("Gender Distribution:", gender_dist_list)

    # Plotting the results
    plot_total_transactions(total_transactions_obj.total_transactions)
    plot_average_transaction_by_category(categories_avg_amount_list)
    plot_top_merchants_by_total_amount(top_merchants_list)
    plot_gender_distribution(gender_dist_list)

if __name__ == "__main__":
    main()

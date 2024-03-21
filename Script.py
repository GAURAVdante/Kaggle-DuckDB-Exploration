import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from sql_queries import (
    count_total_transactions,
    unique_categories,
    average_transaction_amount_by_category,
    top_merchants_by_total_amount,
    gender_distribution,
    average_transaction_amount_by_state,
    top_cities_by_total_amount,
    customers_multiple_cities,
    category_state_transaction_amount,
    potential_fraudulent_transactions,
)

# Connect to DuckDB
con = duckdb.connect(database=':memory:', read_only=False)

# Define the CSV file path
csv_file_path = r'C:\Users\user\OneDrive\Desktop\Virtual Env\duckdbproject\fraud test.csv'

# Execute the query and store the result in a variable
query = f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_file_path}')"
con.execute(query)

# Call SQL queries using the imported functions
result1 = count_total_transactions(con)
total_transactions = result1[0][0]

result2 = unique_categories(con)

result3 = average_transaction_amount_by_category(con)

result4 = top_merchants_by_total_amount(con)

result5 = gender_distribution(con)

result8 = average_transaction_amount_by_state(con)

result10 = top_cities_by_total_amount(con)

result11 = customers_multiple_cities(con)

result12 = category_state_transaction_amount(con)

result13 = potential_fraudulent_transactions(con)

# Plotting the total transactions count
plt.figure(figsize=(8, 6))
plt.bar(['Total Transactions'], [total_transactions], color='skyblue')
plt.xlabel('Metrics')
plt.ylabel('Count')
plt.title('Total Transactions')
plt.show()

# Plotting the average transaction amount by category
df_result3 = pd.DataFrame(result3, columns=['category', 'avg_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result3['category'], df_result3['avg_amount'], color='lightcoral')
plt.xlabel('Category')
plt.ylabel('Average Amount')
plt.title('Average Transaction Amount by Category')
plt.xticks(rotation=45)
plt.show()

# Plotting the top 5 merchants by total transaction amount
df_result4 = pd.DataFrame(result4, columns=['merchant', 'total_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result4['merchant'], df_result4['total_amount'], color='lightcoral')
plt.xlabel('Merchant')
plt.ylabel('Total Amount')
plt.title('Top 5 Merchants by Total Transaction Amount')
plt.xticks(rotation=45)
plt.show()

# Plotting the gender distribution
df_result5 = pd.DataFrame(result5, columns=['gender', 'num_transactions'])
plt.figure(figsize=(8, 6))
plt.pie(df_result5['num_transactions'], labels=df_result5['gender'], autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
plt.title('Gender Distribution of Customers')
plt.show()

# Plotting the average transaction amount by state
df_result8 = pd.DataFrame(result8, columns=['state', 'avg_amount'])
plt.figure(figsize=(12, 8))
plt.barh(df_result8['state'], df_result8['avg_amount'], color='skyblue')
plt.xlabel('Average Amount')
plt.ylabel('State')
plt.title('Average Transaction Amount by State')
plt.show()

# Plotting the top 5 cities by total transaction amount
df_result10 = pd.DataFrame(result10, columns=['city', 'state', 'total_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result10['city'] + ', ' + df_result10['state'], df_result10['total_amount'], color='lightcoral')
plt.xlabel('City, State')
plt.ylabel('Total Amount')
plt.title('Top 5 Cities by Total Transaction Amount')
plt.xticks(rotation=45)
plt.show()


# Print or use the results as needed
print("Total Transactions:", total_transactions)
print("Unique Categories:", result2)
print("Average Transaction Amount by Category:", result3)
print("Top Merchants by Total Amount:", result4)
print("Gender Distribution:", result5)
print("Average Transaction Amount by State:", result8)
print("Top Cities by Total Amount:", result10)
print("Customers in Multiple Cities:", result11)
print("Category-State Transaction Amount:", result12)
print("Potential Fraudulent Transactions:", result13)

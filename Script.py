import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DuckDB
con = duckdb.connect(database=':memory:', read_only=False)

# Define the CSV file path
csv_file_path = r'C:\Users\user\OneDrive\Desktop\Virtual Env\duckdbproject\fraud test.csv'

# Execute the query and store the result in a variable
query = f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_file_path}')"
con.execute(query)

# Query to count the total number of transactions
query1 = "SELECT COUNT(*) AS total_transactions FROM data"
result1 = con.execute(query1).fetchall()

# Extract the total transactions count from the query result
total_transactions = result1[0][0]

# Plotting the total transactions count
plt.figure(figsize=(8, 6))
plt.bar(['Total Transactions'], [total_transactions], color='skyblue')
plt.xlabel('Metrics')
plt.ylabel('Count')
plt.title('Total Transactions')
plt.show()

# List the unique categories of transactions
query2 = "SELECT DISTINCT category FROM data"
result2 = con.execute(query2).fetchall()

# Calculate the average transaction amount for each category
query3 = "SELECT category, AVG(amt) AS avg_amount FROM data GROUP BY category"
result3 = con.execute(query3).fetchall()

# Plotting the average transaction amount by category
df_result3 = pd.DataFrame(result3, columns=['category', 'avg_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result3['category'], df_result3['avg_amount'], color='lightcoral')
plt.xlabel('Category')
plt.ylabel('Average Amount')
plt.title('Average Transaction Amount by Category')
plt.xticks(rotation=45)
plt.show()

# Find the top 5 merchants with the highest total transaction amounts
query4 = "SELECT merchant, SUM(amt) AS total_amount FROM data GROUP BY merchant ORDER BY total_amount DESC LIMIT 5"
result4 = con.execute(query4).fetchall()

# Plotting the top 5 merchants by total transaction amount
df_result4 = pd.DataFrame(result4, columns=['merchant', 'total_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result4['merchant'], df_result4['total_amount'], color='lightcoral')
plt.xlabel('Merchant')
plt.ylabel('Total Amount')
plt.title('Top 5 Merchants by Total Transaction Amount')
plt.xticks(rotation=45)
plt.show()

# Identify the gender distribution of customers who made transactions
query5 = "SELECT gender, COUNT(*) AS num_transactions FROM data GROUP BY gender"
result5 = con.execute(query5).fetchall()

# Plotting the gender distribution
df_result5 = pd.DataFrame(result5, columns=['gender', 'num_transactions'])
plt.figure(figsize=(8, 6))
plt.pie(df_result5['num_transactions'], labels=df_result5['gender'], autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
plt.title('Gender Distribution of Customers')
plt.show()

# Calculate the average transaction amount for each state and order them by average amount in descending order
query8 = "SELECT state, AVG(amt) AS avg_amount FROM data GROUP BY state ORDER BY avg_amount DESC"
result8 = con.execute(query8).fetchall()

# Plotting the average transaction amount by state
df_result8 = pd.DataFrame(result8, columns=['state', 'avg_amount'])
plt.figure(figsize=(12, 8))
plt.barh(df_result8['state'], df_result8['avg_amount'], color='skyblue')
plt.xlabel('Average Amount')
plt.ylabel('State')
plt.title('Average Transaction Amount by State')
plt.show()

# List the top 5 cities with the highest total transaction amounts along with their corresponding state names ( simple join)
query10 = "SELECT f.city, f.state, SUM(f.amt) AS total_amount FROM data AS f JOIN ( SELECT city, SUM(amt) AS city_total FROM data GROUP BY city ) AS c ON f.city = c.city GROUP BY f.city, f.state ORDER BY total_amount DESC LIMIT 5"
result10 = con.execute(query10).fetchall()

# Plotting the top 5 cities by total transaction amount
df_result10 = pd.DataFrame(result10, columns=['city', 'state', 'total_amount'])
plt.figure(figsize=(10, 6))
plt.bar(df_result10['city'] + ', ' + df_result10['state'], df_result10['total_amount'], color='lightcoral')
plt.xlabel('City, State')
plt.ylabel('Total Amount')
plt.title('Top 5 Cities by Total Transaction Amount')
plt.xticks(rotation=45)
plt.show()

#Find customers who have made transactions in different cities, along with the cities they transacted in ( Self join)
query11="SELECT DISTINCT a.first, a.last, a.city AS city1, b.city AS city2  FROM data AS a JOIN data AS b ON a.cc_num = b.cc_num AND a.city <> b.city"
result11 = con.execute(query11).fetchall()
for row in result11:
    print(row)

#Calculate the total transaction amounts for each category in each state, including states with zero transactions for a category ( cross join)
query12="SELECT c.category, s.state, COALESCE(SUM(f.amt), 0) AS total_amount FROM (SELECT DISTINCT category FROM data) AS c CROSS JOIN (SELECT DISTINCT state FROM data) AS s LEFT JOIN data AS f ON f.category = c.category AND f.state = s.state GROUP BY c.category, s.state"
result12=con.execute(query12).fetchall()
for row in result12:
    print(row)

#Identify potential fraudulent transactions by comparing each transaction amount with the average transaction amount for its respective category and merchant combination, considering transactions above a certain threshold as suspicious top 10

query13 = """
WITH avg_category_merchant AS (
    SELECT category, merchant, AVG(amt) AS avg_amount 
    FROM data GROUP BY category, merchant
),
suspicious_transactions AS (
    SELECT f.*, acm.avg_amount AS avg_cat_merch_amount 
    FROM data AS f 
    JOIN avg_category_merchant AS acm 
    ON f.category = acm.category AND f.merchant = acm.merchant 
    WHERE f.amt > (1.5 * acm.avg_amount) --1.5 is a threshold
),
potential_fraud AS (
    SELECT s.*, 'Potential Fraud' AS fraud_status 
    FROM suspicious_transactions AS s 
    WHERE EXISTS ( 
        SELECT 1 
        FROM suspicious_transactions AS s2 
        WHERE s2.cc_num = s.cc_num AND s2.trans_num <> s.trans_num 
    )
)
SELECT p.*, a.category, a.merchant 
FROM potential_fraud AS p 
JOIN avg_category_merchant AS a 
ON p.category = a.category AND p.merchant = a.merchant 
LIMIT 10
"""
result13 = con.execute(query13).fetchall()

# Print the result of the potential fraudulent transactions query
print("Potential Fraudulent Transactions:")
for row in result13:
    print(row)

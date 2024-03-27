# This file included all the SQL statements carried out in Script.py
# sql_queries.py


# Query to count the total number of transactions

def count_total_transactions(con):
    query = "SELECT COUNT(*) AS total_transactions FROM data"
    result = con.execute(query).fetchall()
    return result

# List the unique categories of transactions

def unique_categories(con):
    query = "SELECT DISTINCT category FROM data"
    result = con.execute(query).fetchall()
    return result

# Calculate the average transaction amount for each category

def average_transaction_amount_by_category(con):
    query = "SELECT category, AVG(amt) AS avg_amount FROM data GROUP BY category"
    result = con.execute(query).fetchall()
    return result

# Find the top 5 merchants with the highest total transaction amounts

def top_merchants_by_total_amount(con):
    query = "SELECT merchant, SUM(amt) AS total_amount FROM data GROUP BY merchant ORDER BY total_amount DESC LIMIT 5"
    result = con.execute(query).fetchall()
    return result

# Identify the gender distribution of customers who made transactions

def gender_distribution(con):
    query = "SELECT gender, COUNT(*) AS num_transactions FROM data GROUP BY gender"
    result = con.execute(query).fetchall()
    return result


# Calculate the average transaction amount for each state and order them by average amount in descending order

def average_transaction_amount_by_state(con):
    query = "SELECT state, AVG(amt) AS avg_amount FROM data GROUP BY state ORDER BY avg_amount DESC"
    result = con.execute(query).fetchall()
    return result

# List the top 5 cities with the highest total transaction amounts along with their corresponding state names ( simple join)

def top_cities_by_total_amount(con):
    query = """
    SELECT f.city, f.state, SUM(f.amt) AS total_amount 
    FROM data AS f 
    JOIN (
        SELECT city, SUM(amt) AS city_total FROM data GROUP BY city
    ) AS c 
    ON f.city = c.city 
    GROUP BY f.city, f.state 
    ORDER BY total_amount DESC 
    LIMIT 5
    """
    result = con.execute(query).fetchall()
    return result

# Find customers who have made transactions in different cities, along with the cities they transacted in ( Self join)

def customers_multiple_cities(con):
    query = """
    SELECT DISTINCT a.first, a.last, a.city AS city1, b.city AS city2  
    FROM data AS a 
    JOIN data AS b 
    ON a.cc_num = b.cc_num AND a.city <> b.city
    """
    result = con.execute(query).fetchall()
    return result

# Calculate the total transaction amounts for each category in each state, including states with zero transactions for a category ( cross join)

def category_state_transaction_amount(con):
    query = """
    SELECT c.category, s.state, COALESCE(SUM(f.amt), 0) AS total_amount 
    FROM (SELECT DISTINCT category FROM data) AS c 
    CROSS JOIN (SELECT DISTINCT state FROM data) AS s 
    LEFT JOIN data AS f 
    ON f.category = c.category AND f.state = s.state 
    GROUP BY c.category, s.state
    """
    result = con.execute(query).fetchall()
    return result

# Identify potential fraudulent transactions by comparing each transaction amount with the average transaction amount for its respective category and merchant combination, considering transactions above a certain threshold as suspicious top 10

def potential_fraudulent_transactions(con):
    query = """
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
    result = con.execute(query).fetchall()
    return result

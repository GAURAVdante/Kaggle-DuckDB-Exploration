from pydantic import BaseModel


class TotalTransactions(BaseModel):
    total_transactions: int

def count_total_transactions(con):
    query = "SELECT COUNT(*) AS total_transactions FROM data"
    result = con.execute(query).fetchall()
    total_transactions = result[0][0]
    return TotalTransactions(total_transactions=total_transactions)


def unique_categories(con):
    query = "SELECT DISTINCT category FROM data"
    result = con.execute(query).fetchall()
    categories = [row[0] for row in result]
    return categories

def average_transaction_amount_by_category(con):
    query = "SELECT category, AVG(amt) AS avg_amount FROM data GROUP BY category"
    result = con.execute(query).fetchall()
    categories_avg_amount = [{"category": row[0], "avg_amount": row[1]} for row in result]
    return categories_avg_amount

def top_merchants_by_total_amount(con):
    query = (
        "SELECT merchant, SUM(amt) AS total_amount FROM data "
        "GROUP BY merchant ORDER BY total_amount DESC LIMIT 5"
    )
    result = con.execute(query).fetchall()
    top_merchants = [{"merchant": row[0], "total_amount": row[1]} for row in result]
    return top_merchants

def gender_distribution(con):
    query = "SELECT gender, COUNT(*) AS num_transactions FROM data GROUP BY gender"
    result = con.execute(query).fetchall()
    gender_dist = [{"gender": row[0], "num_transactions": row[1]} for row in result]
    return gender_dist

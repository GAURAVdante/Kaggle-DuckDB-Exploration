import matplotlib.pyplot as plt
import pandas as pd


def plot_total_transactions(total_transactions):
    plt.figure(figsize=(8, 6))
    plt.bar(["Total Transactions"], [total_transactions], color="skyblue")
    plt.xlabel("Metrics")
    plt.ylabel("Count")
    plt.title("Total Transactions")
    plt.show()

def plot_average_transaction_by_category(categories_avg_amount_list):
    df_result3 = pd.DataFrame(categories_avg_amount_list)
    plt.figure(figsize=(10, 6))
    plt.bar(df_result3["category"], df_result3["avg_amount"], color="lightcoral")
    plt.xlabel("Category")
    plt.ylabel("Average Amount")
    plt.title("Average Transaction Amount by Category")
    plt.xticks(rotation=45)
    plt.show()

def plot_top_merchants_by_total_amount(top_merchants_list):
    df_result4 = pd.DataFrame(top_merchants_list)
    plt.figure(figsize=(10, 6))
    plt.bar(df_result4["merchant"], df_result4["total_amount"], color="lightcoral")
    plt.xlabel("Merchant")
    plt.ylabel("Total Amount")
    plt.title("Top 5 Merchants by Total Transaction Amount")
    plt.xticks(rotation=45)
    plt.show()

def plot_gender_distribution(gender_dist_list):
    df_result5 = pd.DataFrame(gender_dist_list)
    plt.figure(figsize=(8, 6))
    plt.pie(
        df_result5["num_transactions"],
        labels=df_result5["gender"],
        autopct="%1.1f%%",
        colors=["skyblue", "lightcoral"]
    )
    plt.title("Gender Distribution of Customers")
    plt.show()

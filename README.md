Fraud Detection Analysis using DuckDB, Python, and Kaggle Data
Description:
This project showcases how to leverage Python, DuckDB, and a Kaggle dataset for fraud detection analysis. It demonstrates essential steps involved in:

Data Acquisition: Downloading a dataset from Kaggle using Python libraries.
Data Exploration: Using DuckDB's in-memory SQL capabilities to perform data exploration and analysis.
Fraud Detection: Identifying potential fraudulent transactions based on predefined criteria using SQL queries.
Output Display: Presenting the results of fraud detection queries within your Python environment, including graphical visualizations for clear insights.
Prerequisites:
Python (version 3.x recommended)
DuckDB
Kaggle API credentials or a valid Kaggle dataset
A code editor or IDE (VS Code recommended)
Installation:
Install required packages:

pip install duckdb pandas matplotlib kaggle
Create a Kaggle API token and set the KAGGLE_USERNAME and KAGGLE_KEY environment variables.

Usage:
Clone or download this repository.
Open the project directory in your code editor or preferred IDE.
Replace the placeholder dataset path (csv_file_path) in the main.py file with the actual path of your Kaggle dataset.
Run the script:

python main.py
Expected Output:
The script will execute various SQL queries on the downloaded dataset to perform fraud detection analysis. It will display the results using matplotlib for graphical visualizations and print potential fraudulent transactions based on predefined criteria.

Graphical Visualizations:
The script will generate graphs for various analysis results, such as:

Bar chart for total transactions count
Bar chart for average transaction amount by category
Bar chart for top 5 merchants by total transaction amount
Pie chart for gender distribution of customers
Bar chart for average transaction amount by state
Bar chart for top 5 cities by total transaction amount
Additional Notes:
Ensure that your Kaggle dataset contains the necessary columns (cc_num, trans_num, category, merchant, amt, gender, state, city, etc.) for fraud detection analysis.
Adjust the fraud detection criteria and thresholds in the SQL queries (query13 in query_functions.py) based on your specific fraud detection requirements.

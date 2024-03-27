import duckdb


def connect_to_database():
    con = duckdb.connect(database=":memory:", read_only=False)
    return con

def create_data_table(con, csv_file_path):
    query = f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_file_path}')"
    con.execute(query)

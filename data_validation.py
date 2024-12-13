import pandas as pd
import psycopg2

# Database connection details
db_details = {
    "dbname": "Vouchersales",
    "user": "postgres",
    "password": "333725",
    "host": "localhost",
    "port": "5432"
}

# Fetch data directly from PostgreSQL
def fetch_data_from_postgres():
    try:
        conn = psycopg2.connect(**db_details)
        query = "SELECT * FROM gift_cards;"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error

# Validation checks
def validate_data(df):
    if df.empty:
        print("No data available to validate!")
        return

    # Check for missing values
    missing_values = df.isnull().sum()
    print("Missing values in each column:\n", missing_values)

    # Validate Cashback values
    invalid_cashback = df[~df['cashback'].str.contains(r'^\d+(\.\d+)?\s% Cashback$', na=False)]
    if not invalid_cashback.empty:
        print("\nInvalid Cashback values:")
        print(invalid_cashback)

    # Validate Gift Card Values
    invalid_gift_card_values = df[df['gift_card_values'] == "Not Any"]
    if not invalid_gift_card_values.empty:
        print("\nGift cards without valid values:")
        print(invalid_gift_card_values)

    # Summary of validation
    print("\nValidation complete!")

# Main script
if __name__ == "__main__":
    # Fetch data
    data = fetch_data_from_postgres()

    # Validate the data
    validate_data(data)

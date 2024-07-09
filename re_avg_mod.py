import sqlite3
import pandas as pd

# Paths to the original and new SQLite database files
original_db_path = 'output.sqlite'
new_db_path = 'output_restructured.sqlite'

# Connect to the original SQLite database
conn_original = sqlite3.connect(original_db_path)

# Load the full data from the NSE_with_indicators table
data_query = "SELECT * FROM NSE_with_indicators;"
data = pd.read_sql_query(data_query, conn_original)

# Ensure the data is sorted by Date
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by=['ticker', 'Date'])

# Restructure the DataFrame
columns = ['Open', 'High', 'Low', 'close', 'Volume', 'ind1', 'ind2', 'ind3', 'entry_signal', 'exit_signal', 'Date', 'ticker', 'Adj_Close']
field_names = ['Open', 'High', 'Low', 'close', 'Volume', 'Ind1', 'Ind2', 'Ind3', 'Cond1', 'Cond2', 'Date', 'Stock', 'Adj_Close']
rows = []

for _, row in data.iterrows():
    for col, field in zip(columns, field_names):
        if col in row:
            field_value = row[col]
            # Convert date to string if it's a Timestamp
            if isinstance(field_value, pd.Timestamp):
                field_value = field_value.strftime('%Y-%m-%d')
            # Determine closeness value for Close and Adj_Close
            closeness_value = ''
            if col == 'close' or col == 'Adj_Close':
                closeness_value = field_value
            rows.append({'Field Name': field, 'Field Value': field_value, 'Closeness': closeness_value, 'Date': row['Date'].strftime('%Y-%m-%d'), 'Stock': row['ticker']})

# Create a new DataFrame from the rows
restructured_data = pd.DataFrame(rows)

# Connect to the new SQLite database
conn_new = sqlite3.connect(new_db_path)

# Store the resulting DataFrame in the new SQLite database
restructured_data.to_sql('NSE_with_indicators_restructured', conn_new, if_exists='replace', index=False)

# Optional: Verify the stored data
result_query = "SELECT * FROM NSE_with_indicators_restructured LIMIT 50;"
result = pd.read_sql_query(result_query, conn_new)
print(result.head(50))

# Close the connections
conn_original.close()
conn_new.close()

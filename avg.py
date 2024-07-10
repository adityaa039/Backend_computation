import sqlite3
import pandas as pd

# Paths to the original and new SQLite database files
original_db_path = r'C:\Users\burma\OneDrive\Documents\GitHub\Backend_computation\first50.sqlite'
new_db_path = 'output_with_indicators.sqlite'

# Connect to the original SQLite database
conn_original = sqlite3.connect(original_db_path)

# Load the full data from the NSE table
data_query = "SELECT * FROM NSE;"
data = pd.read_sql_query(data_query, conn_original)

# Ensure the data is sorted by Date
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by='Date')

# Define the periods for the moving averages
ma_periods = [5, 10, 20]

# Calculate moving averages and add them as new columns
for i, period in enumerate(ma_periods, start=1):
    data[f'ind{i}'] = data['close'].rolling(window=period).mean()

# Calculate the standard deviation of 'close' with a window size of 90 days
data['STD_DEV_90'] = data['close'].rolling(window=90).std()

# Initialize columns for entry and exit signals
data['entry_signal'] = False
data['exit_signal'] = False

# Define the entry condition
entry_condition = (data['ind1'] > data['ind2']) & (data['ind1'].shift(1) <= data['ind2'].shift(1))

# Define the exit condition
exit_condition = (data['ind1'] < data['ind2']) & (data['ind1'].shift(1) >= data['ind2'].shift(1))

# Apply the conditions to the DataFrame
data.loc[entry_condition, 'entry_signal'] = True
data.loc[exit_condition, 'exit_signal'] = True

# Calculate Z-scores for each indicator and add them as new columns
for i in range(1, 4):
    indicator_name = f'ind{i}'
    zscore_name = f'Z_SCORE_{indicator_name}'
    data[zscore_name] = (data[indicator_name] - data[indicator_name].mean()) / data[indicator_name].std()

# Reorder columns to place STD_DEV_90 beside close and Z-scores beside indicators
column_order = ['id', 'Date', 'Open', 'high', 'low', 'close', 'STD_DEV_90', 'Adj_Close', 'Volume', 'ticker', 'ind1', 'Z_SCORE_ind1', 'ind2', 'Z_SCORE_ind2', 'ind3', 'Z_SCORE_ind3', 'entry_signal', 'exit_signal']
data = data[column_order]

# Connect to the new SQLite database
conn_new = sqlite3.connect(new_db_path)

# Store the resulting DataFrame in the new SQLite database
data.to_sql('NSE_with_indicators', conn_new, if_exists='replace', index=False)

# Optional: Verify the stored data
result_query = "SELECT * FROM NSE_with_indicators LIMIT 50;"
result = pd.read_sql_query(result_query, conn_new)
print(result.head(50))

# Close the connections
conn_original.close()
conn_new.close()

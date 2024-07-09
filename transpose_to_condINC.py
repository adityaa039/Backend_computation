import pandas as pd

# Create a list of data from the table
data = [
    ['Open', None, None, None, None],
    ['High', None, None, None, None],
    ['Low', None, None, None, None],
    ['Close', None, None, None, None],
    ['Volume', None, None, None, None],
    ['Ind1', None, None, None, None],
    ['Ind2', None, None, None, None],
    ['Ind3', None, None, None, None],
    ['Cond1', None, None, None, None],  # Adjust row index if Cond1 is at a different position
    ['Cond2', None, None, None, None],  # Adjust row index if Cond2 is at a different position
    ['Cond3', None, None, None, None],  # Adjust row index if Cond3 is at a different position
]

# Create a DataFrame from the data list
df = pd.DataFrame(data, columns=['Field Nam', 'Stock', 'Date', 'Closeness', 'Field Valu'])

# Select rows with condition names
condition_rows = df[df['Field Nam'].isin(['Cond1', 'Cond2', 'Cond3'])]

# Extract condition names and drop unnecessary columns
condition_rows['Condition'] = condition_rows['Field Nam']
condition_rows = condition_rows[['Condition', 'Stock', 'Date']]

# Print the resulting table
print(condition_rows.to_string())
#########################
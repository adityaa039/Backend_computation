import sqlite3

def view_and_store_first_50_rows(src_db_path, dest_db_path):
    # Connect to the source SQLite database
    src_conn = sqlite3.connect(src_db_path)
    src_cursor = src_conn.cursor()
    
    # Connect to the destination SQLite database
    dest_conn = sqlite3.connect(dest_db_path)
    dest_cursor = dest_conn.cursor()
    
    # Fetch all table names from the source database
    src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = src_cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"Processing table '{table_name}':")
        
        # Fetch the first 50 records from the table
        src_cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
        rows = src_cursor.fetchall()
        
        # Fetch column names
        src_cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = src_cursor.fetchall()
        columns = [info[1] for info in columns_info]
        column_definitions = ", ".join([f"{info[1]} {info[2]}" for info in columns_info])
        
        # Create the table in the destination database
        dest_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")
        
        # Insert the fetched rows into the destination table
        if rows:
            placeholders = ", ".join(["?" for _ in columns])
            dest_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)
        
        # Print column names and first 10 records
        print(columns)
        for row in rows:
            print(row)
        print("\n")
    
    # Commit the changes and close the connections
    dest_conn.commit()
    src_conn.close()
    dest_conn.close()

# Specify the paths to your SQLite database files
src_db_path = "C:\\Users\\burma\\OneDrive\\Documents\\GitHub\\StockBuddyGenAI\\src\\Data\\NSE_Yahoo_9_FEB_24.sqlite"
dest_db_path = "first50.sqlite"
view_and_store_first_50_rows(src_db_path, dest_db_path)
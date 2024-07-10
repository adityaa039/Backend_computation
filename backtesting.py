import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate RSI
def calculate_rsi(data, period=14):
    delta = data.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Function to perform backtesting with triggers
def backtest_rsi_strategy(data, rsi_period=14, rsi_oversold=30, rsi_overbought=70):
    # Calculate RSI
    data['RSI'] = calculate_rsi(data['close'], period=rsi_period)
    
    # Initialize variables
    in_position = False
    buy_price = 0
    equity_curve = []
    trades = []
    triggers = []
    
    # Iterate through data
    for index, row in data.iterrows():
        if not in_position and row['RSI'] < rsi_oversold:
            # Buy signal
            in_position = True
            buy_price = row['close']
            trades.append((index, 'Buy', buy_price))
            triggers.append('B')
        elif in_position and row['RSI'] > rsi_overbought:
            # Sell signal
            in_position = False
            sell_price = row['close']
            trade_return = (sell_price - buy_price) / buy_price * 100
            equity_curve.append(trade_return)
            trades.append((index, 'Sell', sell_price, trade_return))
            triggers.append('S')
        else:
            triggers.append('')
    
    # Calculate final equity curve
    if in_position:
        # If still in position at the end, close the trade
        final_price = data.iloc[-1]['close']
        trade_return = (final_price - buy_price) / buy_price * 100
        equity_curve.append(trade_return)
        trades.append((data.index[-1], 'Sell', final_price, trade_return))
        triggers[-1] = 'S'  # Mark the final trade as sell
    
    # Add triggers to dataframe
    data['Trigger'] = triggers
    
    # Calculate metrics
    total_return = sum(equity_curve)
    num_trades = len(equity_curve)
    average_return = np.mean(equity_curve)
    win_ratio = np.sum(np.array(equity_curve) > 0) / num_trades * 100 if num_trades > 0 else 0
    max_drawdown = min(equity_curve) if len(equity_curve) > 0 else 0
    
    return {
        'Total Return (%)': total_return,
        'Number of Trades': num_trades,
        'Average Return (%)': average_return,
        'Win Ratio (%)': win_ratio,
        'Max Drawdown (%)': max_drawdown,
        'Equity Curve': equity_curve,
        'Trades': trades,
        'DataFrame': data  # Return the modified DataFrame with triggers
    }

# Example usage for Tata Motors (TATAMOTORS.NS)
if __name__ == "__main__":
    # Specify the full path to the SQLite database file
    db_path = r'C:\Users\burma\OneDrive\Documents\GitHub\StockBuddyGenAI\src\Data\NSE_Yahoo_9_FEB_24.sqlite'
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Load data for Tata Motors from SQLite into a DataFrame
    query = "SELECT Date, close FROM NSE WHERE Ticker = 'TATAMOTORS.NS'"
    tata_motors_data = pd.read_sql(query, conn, parse_dates=['Date'])
    
    # close the connection
    conn.close()
    
    # Reverse dataframe to have oldest dates first for backtesting
    tata_motors_data = tata_motors_data.sort_values(by='Date', ascending=True).reset_index(drop=True)
    
    # Perform backtest for Tata Motors
    backtest_results = backtest_rsi_strategy(tata_motors_data)
    
    # Print backtest results
    print("Backtest Results for Tata Motors (TATAMOTORS.NS):")
    for key, value in backtest_results.items():
        if key == 'Equity Curve' or key == 'Trades':
            continue
        print(f"{key}: {value}")
    
    # Display DataFrame with Trigger column
    print("\nDataFrame with Triggers:")
    print(backtest_results['DataFrame'].head())
    
    # Plot equity curve
    plt.figure(figsize=(10, 6))
    plt.plot(backtest_results['Equity Curve'], label='Equity Curve (%)')
    plt.title('Equity Curve for Tata Motors (TATAMOTORS.NS)')
    plt.xlabel('Trade')
    plt.ylabel('Return (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

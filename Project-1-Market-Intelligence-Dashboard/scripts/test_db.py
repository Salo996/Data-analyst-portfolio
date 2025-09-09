import sqlite3
conn = sqlite3.connect('data/market_intelligence.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM stock_prices")
result = cursor.fetchone()
print("Total records:", result [0])
conn.close()

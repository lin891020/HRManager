import sqlite3

# 創建 SQLite 資料庫
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 創建表
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
print("Table created successfully.")

# 插入數據
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
conn.commit()

# 查詢數據
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Data:", rows)

# 關閉連接
conn.close()

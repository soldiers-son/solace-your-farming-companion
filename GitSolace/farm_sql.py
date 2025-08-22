import sqlite3

conn = sqlite3.connect('farm.db')
c = conn.cursor() 

# c.execute("""CREATE TABLE task_tracker (
#              name string,
#              date DATE,
#              task string
#             )""")

# c.execute("""CREATE TABLE plant (
#              type string,
#              amount float,
#              date DATE
#             )""")

# c.execute("""CREATE TABLE harvest (
#              type string,
#              amount string,
#              date DATE
#             )""")


# c.execute("""CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password_hash BLOB
# )""")


# c.execute("SELECT * FROM task_tracker WHERE name=''")
# print(c.fetchone())
# print(c.fetchall())
# print(c.fetchmany())

# c.execute("DELETE FROM task_tracker")

# c.execute ("SELECT * FROM harvest WHERE type = 'Tomatoes' ")
# print(c.fetchall())

conn.commit()
print('Data entry successful')
conn.close()

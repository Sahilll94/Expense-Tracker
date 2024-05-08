import sqlite3
import ast

# Connect to SQLite database (or create it)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users
             (username text, password text)''')

# Read data from file
with open('datasheet.txt', 'r') as f:
    data = f.read()

# Convert string to dictionary
data_dict = ast.literal_eval(data)

# Insert data into table
for username, password in data_dict.items():
    c.execute("INSERT INTO users VALUES (?,?)", (username, password))

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
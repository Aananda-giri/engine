sqlite3 database.db # to open a database command_line
.tables             # list tables

# inside python terminal
# sqlite case_sensitive: capital letters only
import sqlite3


# open database
conn =sqlite3.connect('database.db')
c = conn.cursor()   # create a cursor

# Execute commands
c.execute("""CREATE TABLE '%s' (
  		channel_id int NOT NULL PRIMARY KEY

  		)"""% table_name)

# rename table
c.execute("ALTER TABLE table_name RENAME TO new_table_name")

# rename column
c.execute("ALTER TABLE table_name RENAME COLUMN current_name TO new_name")
# commit and close table
conn.commit() # commit our command
conn.close()  # close our connection





# ------------------------
  # indexing in sqlite
# ------------------------
'''
- Whenever you create an index, SQLite creates a B-tree (Balanced tree) structure to hold the index data.
- The index contains data from the columns that you specify in the index and the corresponding rowid value
- This helps SQLite quickly locate the row based on the values of the indexed columns.
'''
# syntax
CREATE UNIQUE INDEX contacts_email
ON TABLE table_name(contacts_list);

# unique constraint make sure value:contacts_email does not repeat

conn =sqlite3.connect('database.db')
c = conn.cursor()   # create a cursor
# create table
c.execute('''
  CREATE TABLE contacts( first_name text NOT NULL, 
last_name text NOT NULL,
email text NOT NULL 
);
''')

# Suppose, you want to enforce that the email is unique, you create a unique index as follows:
c.execute('''
CREATE UNIQUE INDEX idx_contacts_email 
ON contacts (email);
''')

# First,  insert a row into the contacts table.
c.execute('''
INSERT INTO contacts (first_name, last_name, email) VALUES
  ('Johny','Doe','john.doe@sqlitetutorial.net'),
  ('Lisa','Smith','lisa.smith@sqlitetutorial.net');
''')
# querying data
c.execute('''
select first_name, last_name, email FROM contacts WHERE email = 'lisa.smith@sqlitetutorial.net';
''').fetchall()

# EXPLAIN QUERY PLAN
c.execute('''
EXPLAIN QUERY PLAN 
SELECT first_name, last_name, email 
FROM contacts WHERE email = 'lisa.smith@sqlitetutorial.net';
''')
# To find all indexes associated with a table
c.execute('''
PRAGMA index_info('idx_contacts_name');
''')
# drop index
c.execute('''
DROP INDEX idx_contacts_name
''')

'''import sqlite3

import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "customer.db")

# conn = sqlite3.connect(':memory:') # To store data temporarily on memory
conn = sqlite3.connect(db_path)

# REATE A Table, tab;e is like an spreadsheet

# c = conn.cursor()       # ceate cursor
# creaete a table'''
'''
c.execute("""CREATE TABLE customers (
		first_name text,
		last_name text,
		email text
		)""")

# sqlite has 5 data typesL: NULL, INTEGER REAL:10.5 TEXT BLOB:IMAGE,MP3'''
'''
# ------------------------
  # Inserting one data into table
# ------------------------
# c.execute("INSERT INTO customers VALUES ('John', 'Elder', 'john@codemy.com')")
# c.execute("INSERT INTO customers VALUES ('Tim', 'Smith', 'tim@codemy.com')")
# c.execute("INSERT INTO customers VALUES ('Mary', 'Brown', 'mary@codemy.com')")

# many_customers = [
#   ('Wes', 'Brown', "wes@brown.com"),
#   ('Steph', 'Kuewa', "steph@kuewa.com"),
#   ('dan', 'pas', "dan@pas.com"),
# ]
# c.executemany("INSERT INTO customers VALUES (?, ?, ?)", (many_customers))


# ------------------------'''
  # Query and FetchAll
# ------------------------
'''
c.execute("SELECT * FROM  customers")
# print(c.fetchone())
# print(c.fetchmany(3))
# print(c.fetchall()) # GET  ALL VALUES

items = c.fetchall()

print("Name" + '\t' + '\tEmail')
print('-----' + '\t\t--------')
for item in items:
  print(item[0] + '\t' + item[1] + '\t' + item[2])

print('command executed successfully .....')





# ------------------------'''
    # primary keys
# ------------------------
'''c.execute("SELECT rowid, * FROM customers")
items = c.fetchall()
for item in items:
  print(item)



# ------------------------'''
    # SEARCHING IN DATABASE
# ------------------------
'''
# c.execute("SELECT * FROM customers WHERE last_name == 'Elder'")
# c.execute("SELECT * FROM customers WHERE last_name LIKE 'El%'")
# c.execute("SELECT * FROM customers WHERE email LIKE '%codemy.com'")
# <, <=, >, last_name LIKE 'Br%' -> 
print(c.fetchall())



# ------------------------'''
    # Update Records
# ------------------------
'''
c.execute("""UPDATE customers SET first_name = 'Bob' 
    WHERE last_name = 'Elder'
""")  # updates all Elder to Bob Elder

c.execute("""UPDATE customers SET first_name = 'John' 
    WHERE rowid = 1
""")  # updates id 1 first_name to 'John'

c.execute("""UPDATE customers SET first_name = 'Marty' 
    WHERE rowid = 1
""")  # updates id 1 first_name to 'John'

items = c.execute("SELECT rowid, * FROM customers")
for item in items:
  print(item)


# ------------------------'''
    # Deleting the Records
# ------------------------
'''# DROPPING FROM TABLE
c.execute("DELETE FROM customers WHERE rowid = 3")

# ------------------------'''
    # Ordering
# ------------------------
'''
items = c.execute("SELECT rowid, * FROM customers ORDER BY rowid DESC")
c.execute("SELECT rowid, * FROM customers ORDER BY last_name")
items = c.fetchall()
# ASC, rowid DES or -rowid
for item in items:
  print(item)


# ------------------------'''
    # And / OR
# ------------------------
'''# to search for more than one thing
c.execute("SELECT * FROM customers WHERE last_name LIKE 'Sm%' AND rowid = 2")
c.execute("SELECT * FROM customers WHERE last_name LIKE 'Sm%' OR rowid = 1")
# c.execute("SELECT rowid, * FROM customers")
items = c.fetchall()
for item in items:
  print(item)


# ------------------------'''
    # Limiting Records
# ------------------------
'''
c.execute("SELECT rowid, * FROM customers ORDER BY rowid DESC LIMIT 1")
items = c.fetchall()
for item in items:
  print(item)

# ------------------------'''
    # Drop a table
# ------------------------
'''
c.execute("Drop TABLE customers")

print('command executed successfully .....')
conn.commit() # commiting our command
# close our command
conn.close()

# ------------------------'''
    # OUR APP
# ------------------------
'''import sqlite3, json

def show_all():
  # connect to database and create cursor
  conn =sqlite3.connect('customer.db')
  c = conn.cursor()   # create a cursor
  
  # QUERY the database
  c.execute("SELECT rowid, * FROM customers")
  items = c.fetchall()

  for item in items:
    print(item)

  conn.commit() # commit our command
  conn.close()  # close our connection

# Add a new record to the table
def add_one(first_name, last_name, email):
    # connect to database and create cursor
    conn =sqlite3.connect('customer.db')
    c = conn.cursor()   # create a cursor
    
    c.execute("INSERT INTO customers VALUES (?, ?, ?)", (first_name, last_name, email))

    conn.commit() # commit our command
    conn.close()  # close our connection

# Delete Record from Table
def delete_one(id):
  # connect to database and create cursor
  conn =sqlite3.connect('customer.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("DELETE from customers WHERE rowid = (?)", id)
  
  conn.commit() # commit our command
  conn.close()  # close our connection

# To add many records
def add_many(list):
  # connect to database and create cursor
  conn =sqlite3.connect('customer.db')
  c = conn.cursor()   # create a cursor
    
  c.executemany("INSERT INTO customers VALUES (?, ?, ?)", (list))

  conn.commit() # commit our command
  conn.close()  # close our connection

# Lookup with Where
def email_lookup(email):
  # connect to database and create cursor
  conn =sqlite3.connect('customer.db')
  c = conn.cursor()   # create a cursor
    
  # Query the database
  c.execute("SELECT rowid,* FROM customers WHERE email = (?)", (email,))
  items = c.fetchall()
  
  for item in items:
    print(item)
  
  conn.commit() # commit our command
  conn.close()  # close our connection






def get_all():
  # Initially while running
  # connect to database and create cursor
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
    
  c.execute("SELECT key, value FROM key_values")
  data = c.fetchall()
  processed_data = {}
  for key, value in data:
    processed_data[key] = json.loads(value)

  conn.commit() # commit our command
  conn.close()  # close our connection
  print(type(processed_data), ' => ', processed_data)
  return processed_data

def create_one(key, value):
  # connect to database and create cursor
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  value = json.dumps(value)
  c.execute("INSERT INTO key_values VALUES (?, ?)", (key, value))
  data = c.fetchall()

  conn.commit() # commit our command
  conn.close()  # close our connection

def get_one(key):
  # connect to database and create cursor
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
    
  c.execute("SELECT value FROM key_values WHERE key = (?)", (key,))
  data = json.loads(c.fetchall()[0][0])
  # data = json.loads(str(c.fetchall()[0]))
  print(f'data: {data}', type(data[0]))

  conn.commit() # commit our command
  conn.close()  # close our connection
  return data   ## returns data of <data_type> saved

def update_one(key, value):
  # to update key_value pair
  
  # connect to database and create cursor
  conn = sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a curso

  value = json.dumps(value)
  c.execute("""UPDATE key_values SET value = (?)
    WHERE key = (?)
""", (value, key, ))

  conn.commit() # commit our command
  conn.close()  # close our connection
# '''
'''# donot use? - because we have to : 
      - either: update key that exists and create one that doesnot consume alot of time
      - or: drop table and insert all datas
      - instead: update each value seperately on getting each value updated
        - advantage: multiple models can access updated data

def save_db(key_value_pairs):
  # to save the current state before shutting_down bot
  
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("DROP TABLE key_values")
  create_table()
  key_value_tuples = [(key, json.dumps(value)) for key, value in key_value_pairs.items()]
  c.executemany("INSERT INTO key_values VALUES (?, ?)", (key_value_pairs))

  conn.commit() # commit our command
  conn.close()  # close our connection
'''
  
'''
def create_table():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("""CREATE TABLE key_values (
		key text NOT NULL PRIMARY KEY,
		value text
		)""")
  
  conn.commit() # commit our command
  conn.close()  # close our connection

def remove_one(key):
  # connect to database and create cursor
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  # removing the key
  c.execute("DELETE FROM key_values WHERE key = (?)", (key,))

  conn.commit() # commit our command
  conn.close()  # close our connection

def clear_table():
  # drop all the data from table
  # use with caution
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("DROP TABLE key_values")
  create_table()

  conn.commit() # commit our command
  conn.close()  # close our connection

def get_keys():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("SELECT key FROM key_values")
  
  keys = [tup[0] for tup in c.fetchall()]
  # print(type(keys[0]))

  conn.commit() # commit our command
  conn.close()  # close our connection
  return keys

def get_values():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("SELECT value FROM key_values")
  values = [json.loads(tup[0]) for tup in c.fetchall()]
  
  # print(type(values[0]))

  conn.commit() # commit our command
  conn.close()  # close our connection
  return values # returns list of different <data_type> saved

# keys<pk>        values
# subscribed      [12, 23]
# dictt           {'1':'2'}'''


def create_table():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("""CREATE TABLE key_values (
		key text NOT NULL PRIMARY KEY,
		value text
		)""")
  
  conn.commit() # commit our command
  conn.close()  # close our connection

def remove_one(key):
  # connect to database and create cursor
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  # removing the key
  c.execute("REMOVE FROM key_values WHERE channel_id = (?)", (key,))

  conn.commit() # commit our command
  conn.close()  # close our connection

def clear_table():
  # drop all the data from table
  # use with caution
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("DROP TABLE key_values")
  create_table()

  conn.commit() # commit our command
  conn.close()  # close our connection

def get_keys():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("SELECT key FROM key_values")
  
  keys = [tup[0] for tup in c.fetchall()]
  # print(type(keys[0]))

  conn.commit() # commit our command
  conn.close()  # close our connection
  return keys

def get_values():
  conn =sqlite3.connect('key_value_pairs.db')
  c = conn.cursor()   # create a cursor
  
  c.execute("SELECT value FROM key_values")
  values = [json.loads(tup[0]) for tup in c.fetchall()]
  
  # print(type(values[0]))

  conn.commit() # commit our command
  conn.close()  # close our connection
  return values # returns list of different <data_type> saved


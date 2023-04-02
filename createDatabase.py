import sqlite3
import pandas as pd

connection = sqlite3.connect('data/kamusalay.db')

try:
    connection.execute("""CREATE TABLE kamusalay (alay VARCHAR(256), baku VARCHAR(256)); """)
    print("table created!")
except:
    print("table already exists!")

kamusDF = pd.read_csv('data/new_kamusalay.csv', names=['Alay', 'Baku'], encoding='Latin-1')

kamusDF.to_sql(name='kamusalay', con=connection, if_exists='replace', index=False)

connection.commit()
connection.close()
import pandas as pd
from sqlalchemy import create_engine


print("[INFO] Start bulding the dataset...")


# create a connection with a mariadb financial database
# We can check the database documentation here: https://relational.fit.cvut.cz/dataset/financial
engine = create_engine('mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306/financial')

with open('data/sql_query.sql', 'r') as file:
    query_statement = file.read()

print("[INFO] Querying the data...")

df = pd.read_sql_query(query_statement, engine)
df.to_csv('data/dataset.csv', index=False)  

print("[INFO] Dataset created")

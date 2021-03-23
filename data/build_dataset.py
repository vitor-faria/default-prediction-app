import pandas as pd
from sqlalchemy import create_engine


print("[INFO] Start bulding the dataset...")

# create a connection with a mariadb financial database
# We can check the database documentation here: https://relational.fit.cvut.cz/dataset/financial
engine = create_engine('mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306/financial')

version = 1  # Keep latest version

with open(f'data/query_dataset_v{version}.sql', 'r') as file:
    query_dataset = file.read()

print(f"[INFO] Running query_dataset_v{version}.sql...")

df = pd.read_sql_query(query_dataset, engine)
df.to_csv(f'data/dataset_v{version}.csv', index=False)

print(f"[INFO] Dataset created with name dataset_v{version}.csv")

with open(f'data/query_districts.sql', 'r') as file:
    query_districts = file.read()

print("[INFO] Running query_districts.sql...")

df_districts = pd.read_sql_query(query_districts, engine)
df_districts.to_csv(f'data/districts.csv', index=False)

print("[INFO] Districts dataset created with name districts.csv")

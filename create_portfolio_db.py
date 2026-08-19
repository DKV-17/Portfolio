import os
import psycopg

host = "dpg-d9q5q21t0dsc73caivm0-a.oregon-postgres.render.com"
user = "eventuser"
password = os.environ["PGPASSWORD"]

conn = psycopg.connect(
    host=host,
    port=5432,
    dbname="eventmanagement_awf0",
    user=user,
    password=password,
    sslmode="require",
    autocommit=True
)

cur = conn.cursor()

cur.execute("""
    SELECT 1
    FROM pg_database
    WHERE datname = 'portfolio_db'
""")

if cur.fetchone():
    print("portfolio_db already exists.")
else:
    cur.execute("CREATE DATABASE portfolio_db")
    print("portfolio_db created successfully!")

cur.close()
conn.close()
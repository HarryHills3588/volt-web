from dotenv import load_dotenv
import os 

load_dotenv('.env')
DATABASEURL=os.getenv('DATABASE_URL')


import psycopg2

conn = psycopg2.connect(DATABASEURL)

with conn.cursor() as cursor:
    cursor.execute('SELECT * FROM emails')
    results =cursor.fetchall()

    for row in results:
        print(row)

conn.commit()
conn.close()
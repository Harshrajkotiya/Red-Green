import psycopg2
from fastapi import HTTPException

def get_db_connection():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="Harshal555@Desai",
            host="tsdb.derivedged.com",
            port="5432"
        )
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
        raise HTTPException(status_code=400, detail=f"Unable to connect to the database : {e}")
    return conn

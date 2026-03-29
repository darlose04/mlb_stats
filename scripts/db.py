import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWD"),
        port=os.getenv("DB_PORT"),
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB"),
    )


def dual_write(cnx, sql, data, many=False):
    fantasy_sql = sql.replace("INSERT INTO ", "INSERT INTO fantasy.", 1)
    cursor = cnx.cursor()
    fcursor = cnx.cursor()
    try:
        if many:
            cursor.executemany(sql, data)
            fcursor.executemany(fantasy_sql, data)
        else:
            cursor.execute(sql, data)
            fcursor.execute(fantasy_sql, data)
        cnx.commit()
    except psycopg2.Error as err:
        print(f"ERROR: {err}")
        cnx.rollback()
        raise
    finally:
        cursor.close()
        fcursor.close()

from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

DB_NAME = 'postgres'
DB_USER = 'postgres.lhfifpaqxnenmukvufkz'
DB_PASS = 'IcikiwirBalap69'
DB_HOST = 'aws-0-ap-southeast-1.pooler.supabase.com'
DB_PORT = '5432'

connection = psycopg2.connect(user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME)


def initialize_connection():
    try:
        connection.autocommit = True
        cursor = connection.cursor()
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]

def connectdb(func):
    def wrapper(request):
        res = ""
        with connection.cursor() as cursor:
            res = func(cursor, request)
        return res
    return wrapper

def login(email, password):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()

    # Setting the search path
    cur.execute("SET search_path TO MARMUT;")
    
    # Checking user credentials
    cur.execute("""
        SELECT * FROM MARMUT.AKUN
        WHERE email = %s AND password = %s
    """, (email, password))
    
    user_data = cur.fetchall()
    result.append(user_data)

    if user_data:
        cur.execute("""
            SELECT * FROM PREMIUM
            WHERE PREMIUM.email = %s
        """, (email,))
        
        premium_data = cur.fetchone()
        if premium_data:
            result.append(premium_data)
        else:
            result.append(None)

    return result
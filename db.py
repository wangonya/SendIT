import psycopg2
from psycopg2.extras import RealDictCursor
try:
    connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="sendit")
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print("Connected to db")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
# finally:
#     # closing database connection.
#     if connection:
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")

from db import cursor, connection


def create_parcels_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS parcels
              (
                id SERIAL PRIMARY KEY,
                placedBy INT NOT NULL,
                weight FLOAT NOT NULL,
                weightmetric VARCHAR(3) NOT NULL,
                sentOn TIMESTAMP NOT NULL,
                deliveredOn TIMESTAMP NOT NULL,
                status VARCHAR(15) NOT NULL,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                currentlocation TEXT NOT NULL 
              ); '''

    cursor.execute(create_table_query)
    connection.commit()


def create_users_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS users
              (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR(10) NOT NULL,
                lastname VARCHAR(10) NOT NULL,
                othernames VARCHAR(10),
                email VARCHAR(30) NOT NULL,
                username VARCHAR(10) NOT NULL UNIQUE ,
                registered TIMESTAMP NOT NULL,
                isAdmin BOOLEAN,
                pwd VARCHAR(100) NOT NULL 
              ); '''

    cursor.execute(create_table_query)
    connection.commit()

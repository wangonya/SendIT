from db import cursor, connection


def create_parcels_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS parcels
              (
                id SERIAL PRIMARY KEY,
                placedBy INT NOT NULL,
                weight FLOAT NOT NULL,
                weightmetric TEXT NOT NULL,
                sentOn TIMESTAMP NOT NULL,
                deliveredOn TIMESTAMP NOT NULL,
                status TEXT NOT NULL,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                currentlocation TEXT NOT NULL 
              ); '''

    cursor.execute(create_table_query)
    connection.commit()

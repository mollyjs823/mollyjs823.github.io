#import sqlite3
import os
import psycopg2
import psycopg2.extras
import urllib.parse

#def dict_factory(cursor, row):
#    col_names = [col[0] for col in cursor.description]
#    return {key: value for key, value in zip(col_names, row)}

class TrucksDB:
    def __init__(self):
        # self.connection = sqlite3.connect("trucks.db")
        # self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_trucks_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS trucks (id SERIAL PRIMARY KEY, name VARCHAR(255), type VARCHAR(255), rating INT, review VARCHAR(255), location VARCHAR(255), user_id INT)")
        self.connection.commit()

    def create_trucksmeta_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS truck_metadata (id SERIAL PRIMARY KEY, slug VARCHAR(255), name VARCHAR(255), cuisine VARCHAR(255))")
        self.connection.commit()

    def create_truck(self, name, type, rating, review, location, user):
        # Prevent SQL injection
        data = [name, type, rating, review, location, user]
        self.cursor.execute("INSERT INTO trucks (name, type, rating, review, location, user_id) VALUES (%s, %s, %s, %s, %s, %s)", data)

        # Have to commit after any write operation
        self.connection.commit()

    def delete_truck(self, id):
        # Prevent SQL injection
        data = [id]
        self.cursor.execute("DELETE FROM trucks WHERE id=%s", data)

        self.connection.commit()

    def edit_truck(self, id, name, type, rating, review, location):
        # Prevent SQL injection
        data = [name, type, rating, review, location, id]
        print(data)
        self.cursor.execute("UPDATE trucks SET name=%s, type=%s, rating=%s, review=%s, location=%s WHERE id=%s", data)

        self.connection.commit()

    def get_truck(self, id):
        data = [id]
        self.cursor.execute("SELECT * FROM trucks WHERE id = %s", data)
        # This will return none if not found
        return self.cursor.fetchone()

    def get_all_trucks(self):
        self.cursor.execute("SELECT * FROM trucks")
        # Now that have executed, give all data that matched query
        return self.cursor.fetchall()

    def get_all_trucks_from_user(self, id):
        data = [id]
        self.cursor.execute("SELECT * FROM trucks WHERE user_id = %s", data)
        # Now that have executed, give all data that matched query
        return self.cursor.fetchall()

    def get_all_trucks_meta(self):
        self.cursor.execute("SELECT * FROM truck_metadata")

        return self.cursor.fetchall()
    
    def get_truck_meta(self, id):
        print(id)
        data = [id]
        self.cursor.execute("SELECT * FROM truck_metadata WHERE id=%s", data)

        return self.cursor.fetchone()

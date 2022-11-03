import sqlite3

def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

class TrucksDB:
    def __init__(self):
        self.connection = sqlite3.connect("trucks.db")
        # Convert queries to show column headings
        self.connection.row_factory = dict_factory
        # Allow queries and get data back from connection
        self.cursor = self.connection.cursor()

    def create_truck(self, name, type, rating, review, location):
        # Prevent SQL injection
        data = [name, type, rating, review, location]
        self.cursor.execute("INSERT INTO trucks (name, type, rating, review, location) VALUES (?, ?, ?, ?, ?)", data)

        # Have to commit after any write operation
        self.connection.commit()

    def delete_truck(self, id):
        # Prevent SQL injection
        data = [id]
        self.cursor.execute("DELETE FROM trucks WHERE id=?", data)

        self.connection.commit()

    def edit_truck(self, id, name, type, rating, review, location):
        # Prevent SQL injection
        data = [name, type, rating, review, location, id]
        print(data)
        self.cursor.execute("UPDATE trucks SET name=?, type=?, rating=?, review=?, location=? WHERE id=?", data)

        self.connection.commit()

    def get_truck(self, id):
        data = [id]
        self.cursor.execute("SELECT * FROM trucks WHERE id = ?", data)
        # This will return none if not found
        return self.cursor.fetchone()

    def get_all_trucks(self):
        self.cursor.execute("SELECT * FROM trucks")
        # Now that have executed, give all data that matched query
        return self.cursor.fetchall()

    def get_all_trucks_meta(self):
        self.cursor.execute("SELECT * FROM truck_metadata")

        return self.cursor.fetchall()
    
    def get_truck_meta(self, id):
        print(id)
        data = [id]
        self.cursor.execute("SELECT * FROM truck_metadata WHERE id=?", data)

        return self.cursor.fetchone()

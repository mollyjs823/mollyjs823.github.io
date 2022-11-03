import sqlite3
from passlib.hash import bcrypt

def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

class UsersDB:
    def __init__(self):
        self.connection = sqlite3.connect("trucks.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def create_user(self, email, fname, lname, password):
        users = self.get_all_users()
        found = False
        for user in users:
            if user["email"] == email:
                found = True
        if found:
            return False
        password = bcrypt.hash(password)
        data = [email, fname, lname, password]
        self.cursor.execute("INSERT INTO users (email, fname, lname, enc_password) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()
        return True

    def delete_user(self, id):
        data = [id]
        self.cursor.execute("DELETE FROM users WHERE id=?", data)
        self.connection.commit()

    def get_user_by_email(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

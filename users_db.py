# import sqlite3
import os
import psycopg2
import psycopg2.extras
import urllib.parse
from passlib.hash import bcrypt

# def dict_factory(cursor, row):
#     col_names = [col[0] for col in cursor.description]
#     return {key: value for key, value in zip(col_names, row)}

class UsersDB:
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

    def create_users_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255), fname VARCHAR(255), lname VARCHAR(255), enc_password VARCHAR(255))")
        self.connection.commit()

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
        self.cursor.execute("INSERT INTO users (email, fname, lname, enc_password) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()
        return True

    def delete_user(self, id):
        data = [id]
        self.cursor.execute("DELETE FROM users WHERE id=%s", data)
        self.connection.commit()

    def get_user_by_id(self, id):
        data = [id]
        self.cursor.execute("SELECT id, fname FROM users WHERE id = %s", data)
        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email = %s", data)
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
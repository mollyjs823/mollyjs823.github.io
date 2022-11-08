from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from session_store import SessionStore
from passlib.hash import bcrypt
from socketserver import ThreadingMixIn
import json
from urllib.parse import parse_qs
from trucks_db import TrucksDB
from users_db import UsersDB


SESSION_STORE = SessionStore()


class MyRequestHandler(BaseHTTPRequestHandler):
    def load_cookie(self):
        if "Cookie" in self.headers:
            print("Cookie: ", self.headers["Cookie"])
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            print("No request cookie found")
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            if "Postman" not in self.headers["User-Agent"]:
                morsel["samesite"] = "None"
                morsel["secure"] = True
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        # CALLED AT THE TOP OF ALL DO FUNCTIONS
        # Cookie should not be changing when sending new request from same client
        # Clear cookie and check get new one
        # Restart server and check if got new one
        # Try to tamper with cookie, see if get new one
        self.load_cookie()
        if 'sessionId' in self.cookie:
            session_id = self.cookie['sessionId'].value
            self.session_data = SESSION_STORE.get_session(session_id)
            if self.session_data is None:
                session_id = SESSION_STORE.create_session()
                self.cookie["sessionId"] = session_id
                self.session_data = SESSION_STORE.get_session(session_id)
        else:
            session_id = SESSION_STORE.create_session()
            self.cookie["sessionId"] = session_id
            self.session_data = SESSION_STORE.get_session(session_id)

    def end_headers(self):
        # self.send_header("Access-Control-Allow-Origin", "*") 
        # or null, will change when actually hosted
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        super().end_headers()

    def handle_not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", 'text/plain')
        self.end_headers()

        print("Page Not Found")
        self.wfile.write(bytes("Page Not Found", 'utf-8'))

    def handle_bad_data(self):
        self.send_response(404)
        self.send_header("Content-Type", 'text/plain')
        self.end_headers()

        print("You submitted bad data!")
        self.wfile.write(bytes("You submitted bad data!", 'utf-8'))

    def handle_401(self):
        print("The user is not logged in")
        self.send_response(401)
        self.end_headers()

    def handle_find_all_trucks(self):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        self.send_response(200)
        self.send_header("Content-Type", 'application/json')
        self.end_headers()

        trucks_db = TrucksDB()
        users_db = UsersDB()
        all_trucks = trucks_db.get_all_trucks()
        for truck in all_trucks:
            truck["user_id"] = users_db.get_user_by_id(truck["user_id"])["fname"]
        print(all_trucks)
        truck_meta = trucks_db.get_all_trucks_meta()
        all_data = {"mytrucks": all_trucks, "metadata": truck_meta}
        self.wfile.write(bytes(json.dumps(all_data), 'utf-8'))

    def handle_find_users_trucks(self):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        self.send_response(200)
        self.send_header("Content-Type", 'application/json')
        self.end_headers()

        trucks_db = TrucksDB()
        all_trucks = trucks_db.get_all_trucks_from_user(self.session_data["userId"])
        truck_meta = trucks_db.get_all_trucks_meta()
        users_db = UsersDB()
        user = users_db.get_user_by_id(self.session_data["userId"])
        all_data = {"mytrucks": all_trucks, "metadata": truck_meta, "user": user}
        self.wfile.write(bytes(json.dumps(all_data), 'utf-8'))

    def handle_find_truck(self, id):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        trucks_db = TrucksDB()
        truck = trucks_db.get_truck(id)
        if truck:
            truck_meta = trucks_db.get_truck_meta(truck["name"])
            all_data = {"mytruck": truck, "metadata": truck_meta}
            self.send_response(200)
            self.send_header("Content-Type", 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(all_data), 'utf-8'))
        else:
            self.handle_not_found()

    def handle_create_truck(self):
        if "userId" not in self.session_data:
            self.handle_401()
            return

        length = self.headers['Content-Length']

        request_body = self.rfile.read(int(length)).decode("utf-8")
        if request_body:
            parsed_body = parse_qs(request_body)
            if ("name" in parsed_body and "type" in parsed_body and "rating" in parsed_body and "review" in parsed_body and "location" in parsed_body):
                arr = {
                    "name": parsed_body["name"][0], 
                    "type": parsed_body["type"][0], 
                    "rating": parsed_body["rating"][0],
                    "review": parsed_body["review"][0],
                    "location": parsed_body["location"][0]
                }
                trucks_db = TrucksDB()
                users_db = UsersDB()
                name = users_db.get_user_by_id(self.session_data["userId"])
                trucks_db.create_truck(arr["name"], arr["type"], arr["rating"], arr["review"], arr["location"], name["id"])

                self.send_response(201)
                self.end_headers()
            else:
                self.handle_bad_data()
        else:
            self.handle_bad_data()

    def handle_edit_truck(self, id):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        trucks_db = TrucksDB()
        found = trucks_db.get_truck(id)
        if found["user_id"] != self.session_data["userId"]:
            self.handle_401()
            return

        length = self.headers['Content-Length']

        request_body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(request_body)
        if request_body:
            parsed_body = parse_qs(request_body)
            if ("name" in parsed_body and "type" in parsed_body and "rating" in parsed_body and "review" in parsed_body and "location" in parsed_body):
                arr = {
                    "name": parsed_body["name"][0], 
                    "type": parsed_body["type"][0], 
                    "rating": parsed_body["rating"][0],
                    "review": parsed_body["review"][0],
                    "location": parsed_body["location"][0]
                }
                if found:
                    trucks_db.edit_truck(id, arr["name"], arr["type"], arr["rating"], arr["review"], arr["location"])
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.handle_not_found()
            else:
                self.handle_bad_data()
        else:
            self.handle_bad_data()

    def handle_delete_truck(self, id):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        trucks_db = TrucksDB()
        found = trucks_db.get_truck(id)
        if found["user_id"] != self.session_data["userId"]:
            self.handle_401()
            return

        if found:
            trucks_db.delete_truck(id) 
            self.send_response(200)
            self.end_headers()
        else: 
            self.handle_not_found()        

    def handle_find_user(self, id):
        user_db = UsersDB()
        user = user_db.get_user(id)
        if user:
            all_data = {"user": user}
            self.send_response(200)
            self.send_header("Content-Type", 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(all_data), 'utf-8'))
        else:
            self.handle_not_found()

    def handle_create_user(self):
        length = self.headers['Content-Length']

        request_body = self.rfile.read(int(length)).decode("utf-8")
        if request_body:
            parsed_body = parse_qs(request_body)
            if ("email" in parsed_body and "fname" in parsed_body and "lname" in parsed_body and "password" in parsed_body):
                arr = {
                    "email": parsed_body["email"][0], 
                    "fname": parsed_body["fname"][0], 
                    "lname": parsed_body["lname"][0],
                    "password": parsed_body["password"][0]
                }
                users_db = UsersDB()
                success = users_db.create_user(arr["email"], arr["fname"], arr["lname"], arr["password"])
                if success:
                    self.send_response(201)
                else:
                    self.send_response(422)
                self.end_headers()
            else:
                self.handle_bad_data()
        else:
            self.handle_bad_data()

    def handle_create_session(self):
        # LOG IN func
        length = self.headers['Content-Length']

        request_body = self.rfile.read(int(length)).decode("utf-8")
        if request_body:
            parsed_body = parse_qs(request_body)
            if ("email" in parsed_body and "password" in parsed_body):
                arr = {
                    "email": parsed_body["email"][0], 
                    "password": parsed_body["password"][0]
                }
                users_db = UsersDB()
                user = users_db.get_user_by_email(arr["email"])
                if user:
                    if bcrypt.verify(arr["password"], user['enc_password'],):
                        self.session_data["userId"] = user["id"]
                        self.send_response(201)
                        self.send_header("Content-Type", 'text/plain')
                        self.end_headers()
                        self.wfile.write(bytes(json.dumps(user['id']), 'utf-8'))
                    else:
                        self.send_response(401)
                        self.send_header("Content-Type", 'text/plain')
                        self.end_headers()
                        self.wfile.write(bytes("User credentials bad", 'utf-8'))
                else:
                    self.handle_bad_data()
            else:
                self.handle_bad_data()
        else:
            self.handle_bad_data()

    def handle_logout(self):
        if "userId" not in self.session_data:
            self.handle_401()
            return
        self.session_data.pop("userId")
        self.send_response(201)
        self.end_headers()

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "PUT, DELETE, POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_PUT(self):
        self.load_session()
        parts = self.path.split("/")
        collection = parts[1]
        member_id = None
        if len(parts) > 2:
            member_id = parts[2]
        if collection == "trucks":
            if member_id:
                # Update specific member
                self.handle_edit_truck(member_id)
            else:
                self.handle_not_found()
        else:
            self.handle_not_found()

    def do_DELETE(self):
        self.load_session()
        parts = self.path.split("/")
        collection = parts[1]
        member_id = None
        if len(parts) > 2:
            member_id = parts[2]
        if collection == "trucks":
            if member_id:
                # Delete specific member
                self.handle_delete_truck(member_id)
            else:
                self.handle_not_found()
        else:
            self.handle_not_found()

    def do_GET(self):
        self.load_session()
        parts = self.path.split("/")
        collection = parts[1]
        member_id = None
        user_id = None
        if "?user=" in collection:
            user_id = collection.split("=")[1]
            collection = collection.split("?")[0]
        if len(parts) > 2:
            member_id = parts[2]
        if collection == "trucks":
            if member_id:
                # Retrieve specific member
                self.handle_find_truck(member_id)
            elif user_id:
                print("FOR SPECIFIC USER")
                self.handle_find_users_trucks()
            else:
                # Retrieve entire collection
                print("FIND ALL TRUCKS")
                self.handle_find_all_trucks()
        elif collection == 'users':
            if member_id:
                self.handle_find_user(member_id)
            else:
                 self.handle_not_found()
        else:
            self.handle_not_found()

    def do_POST(self):
        self.load_session()
        if self.path == "/trucks":
            self.handle_create_truck()
        elif self.path == "/users":
            self.handle_create_user()
        elif self.path == "/sessions":
            self.handle_create_session()
        elif self.path == "/logout":
            self.handle_logout()
        else:
            self.handle_not_found()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    listen = ('127.0.0.1', 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)
    print("Server running")
    server.serve_forever()

if __name__ == '__main__':
    run()

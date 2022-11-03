import base64, os

class SessionStore:
    def __init__(self):
        # Dictionary of dictionaries, 1 per session
        self.sessions = {}

    def create_session(self):
        session_id = self.generate_session_id()
        self.sessions[session_id] = {}
        return session_id

    def generate_session_id(self):
        # 32 bytes of random info
        num = os.urandom(32)
        rand_str = base64.b64encode(num).decode("utf-8")
        return rand_str

    def get_session(self, id):
        if id in self.sessions:
            return self.sessions[id]
        return None

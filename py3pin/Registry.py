import json
import os


class Registry:
    path = None
    cookies = dict()

    def __init__(self, root, username):
        self.root = root
        self.username = username

        if not os.path.exists(root):
            os.makedirs(root)

        cred_path = self._get_cred_file_path()
        if os.path.isfile(cred_path):
            try:
                with open(cred_path) as f:
                    self.cookies = json.loads(f.read())
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, cookie_name):
        return self.cookies[cookie_name]

    def get_all(self):
        return self.cookies

    def update_all(self, cookie_dict):
        self.cookies = cookie_dict
        self._persist()

    def set(self, key, value):
        self.cookies[key] = value
        self._persist()

    def _persist(self):
        with open(self._get_cred_file_path(), "w") as f:
            f.write(json.dumps(self.cookies))

    def _get_cred_file_path(self):
        return os.path.join(self.root, self.username)

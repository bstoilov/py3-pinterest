import json
import os
import shutil


class Registry:
    path = None
    cookies = dict()

    def __init__(self, root, username):
        self.root = root
        self.username = username

        if os.path.isdir(self._get_cred_file_path()):
            shutil.rmtree(self._get_cred_file_path())

        if not os.path.exists(root):
            os.makedirs(root)

        try:
            with open(self._get_cred_file_path()) as f:
                content = f.read()
                self.cookies = json.loads(content)
        except Exception as e:
            print("No credentials stored", e)

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
        cred_file_path = self._get_cred_file_path()
        print("Reading credential from " + cred_file_path)
        f = open(cred_file_path, "w")
        f.write(json.dumps(self.cookies))
        f.close()

    def _get_cred_file_path(self):
        return os.path.join(self.root, self.username)

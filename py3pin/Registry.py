# -*- coding: utf-8 -*-
import os
import pickle


class Registry:
    __committed = True
    __path = None
    __data = dict()

    def __init__(self, path):
        self.__path = path
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                self.__data = dict(pickle.load(f))

    def get(self, key, default=None):
        if key in self.__data:
            return self.__data[key]
        return default

    def set(self, key, value, commit=True):
        if key:
            self.__data[key] = value
            self.__committed = False
            if commit:
                self.commit()
            return True
        return False

    def update(self, key, value, commit=True):
        if hasattr(self.get(key), 'update'):
            self.get(key).update(value)
            self.__committed = False
            if commit:
                self.commit()
            return True
        return self.set(key, value, commit)

    def commit(self):
        if not self.__committed:
            with open(self.__path, 'wb') as f:
                pickle.dump(self.__data, f, 1)
            self.__committed = True
        return self.__committed

    def hasKey(self, key):
        return key in self.__data

    def keys(self):
        return self.__data.keys()

    class Key:
        CSRF_TOKEN = 'token'
        COOKIES = 'cookies'

        def __init__(self):
            pass

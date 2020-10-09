class BookmarkManager:
    def __init__(self):
        self.bookmark_map = {}

    def add_bookmark(self, primary, bookmark, secondary=None):
        if primary not in self.bookmark_map:
            self.bookmark_map[primary] = {}
        if secondary is not None:
            self.bookmark_map[primary][secondary] = bookmark
        else:
            self.bookmark_map[primary] = bookmark

    def get_bookmark(self, primary, secondary=None):
        try:
            if secondary is not None:
                return self.bookmark_map[primary][secondary]
            else:
                return self.bookmark_map[primary]
        except KeyError:
            pass

        return None

    def reset_bookmark(self, primary, secondary=None):
        if primary in self.bookmark_map:
            del self.bookmark_map[primary][secondary]
        else:
            pass

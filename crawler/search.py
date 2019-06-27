class Search:
    def __init__(self, name, text, more, where="file", repos=[]):
        self.name = name
        self.text = text
        self.more = more
        self.where = where
        self.repos = repos

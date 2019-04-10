from crawler import Crawler
import queue
from threading import Thread

class Worker:
    def __init__(self, tokens, f):
        self.searches = queue.Queue()
        self.tokens = tokens
        self.threads = [Thread(target=self.__w__(t, f)) for t in tokens]

    def addSearch(self, search):
        self.searches.put(search)

    def execute(self):
        for t in self.threads:
            t.start()
        self.searches.join()
        for t in self.threads:
            self.searches.put(None)
        for t in self.threads:
            t.join()

    def __w__(self, token, f):
        crawler = Crawler(token)
        def work():
            while True:
                item = self.searches.get()
                if item is None:
                    break
                f(crawler, item)
                self.searches.task_done()
        return work

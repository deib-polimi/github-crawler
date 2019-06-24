import queue

from crawler import Crawler
from threading import Thread

class CrawlerPool:
    def __init__(self, tokens, crawlertype):
        self.searches = queue.Queue()
        self.tokens = tokens
        self.crawlertype = crawlertype
        self.threads = [Thread(target=self.work, args=(t,)) for t in tokens]

    def addSearch(self, search):
        self.searches.put(search)

    def start(self):
        for t in self.threads:
            t.start()

    def join(self):
        self.searches.join()
        for t in self.threads:
            self.searches.put(None)
        for t in self.threads:
            t.join()

    def work(self, token):
        crawler = self.crawlertype(token)
        while True:
            item = self.searches.get()
            if item is None:
                break
            crawler.search(item)
            self.searches.task_done()

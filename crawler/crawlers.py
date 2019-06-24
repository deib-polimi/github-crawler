from crawler import Crawler

class CrawlerRepo(Crawler):
    def search(self, search):
        self.__search__(search)

    def addResult(self, result, res):
        repo = result.git_url
        res[repo] = []

    def executeQuery(self, query):
        return self.github.search_repositories(query, sort='stars', order='desc')

class CrawlerCode(Crawler):
    def search(self, search):
        self.__search__(search)

    def addResult(self, result, res):
        repo = result.repository.git_url
        files = res.get(repo, set())
        files.add(result.path)
        res[repo] = []

    def executeQuery(self, query):
        return self.github.search_code(query)

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
        res[repo] = files

    def executeQuery(self, query):
        return self.github.search_code(query)

class CrawlerCodeRepo(Crawler):
    def search(self, search):
        for repo in search.repos:
            search.more['repo'] = self.repoName(repo)
            self.__search__(search)
        del search.more['repo']

    def repoName(self, url):
        r = "/".join(url.split("/")[-2:])
        r = ".".join(r.split('.')[:-1])
        print(url, r)
        return r

    def addResult(self, result, res):
        repo = result.repository.git_url
        files = res.get(repo, set())
        files.add(result.path)
        res[repo] = files

    def executeQuery(self, query):
        return self.github.search_code(query)

from github import Github
from github.GithubException import GithubException
from time import sleep
import sys

class Crawler:
    short_timeout = 1
    long_timeout = 60

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.github = Github(tokens[0])

    def search_code(self, search):
        self.__search__(search, lambda g: g.search_code)

    def __search__(self, search, f):
        repos = {}
        query = self.__buildQuery__(search)
        results, total = self.__getQueryResults__(query, f)
        print(search.name, total)
        r = 0
        while r < total:
            print('Processing result', r+1)
            try:
                result = results[r]
                self.__addResult__(result, repos)
                sleep(self.short_timeout)
            except GithubException:
                # fail, recompute result (with another token and start from the same item r)
                results, total = self.__getQueryResults__(query, f)
                continue
            r += 1
        self.__writeToFile__(search.name, repos)

    def __getQueryResults__(self, query, f):
        try:
            results = f(self.github)(query)
            sleep(self.short_timeout)
            total = results.totalCount
        except GithubException:
            self.__changeToken__()
            return self.__getQueryResults__(query, f)
        return (results, total)

    def __buildQuery__(self, search):
        q = '%s in:file' % search.text
        for key, value in search.more.items():
            q += ' %s:%s' % (key, value)
        return q

    def __changeToken__(self):
        self.current_token = (self.current_token + 1) % len(self.tokens)
        if not self.current_token:
            print('Waiting...')
            sleep(self.long_timeout)
        self.github = Github(self.tokens[self.current_token])

    def __addResult__(self, result, repos):
        repo = result.repository.git_url
        files = repos.get(repo, set())
        files.add(result.path)
        repos[repo] = files

    def __writeToFile__(self, name, repos):
        output = ""
        for url, files in repos.items():
            data = [url] + list(files)
            output += ",".join(data) + "\n"
        f = open("results/%s.csv" % name, "w")
        f.write(output)

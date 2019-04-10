from github import Github
from github.GithubException import GithubException
from time import sleep
import sys
import os
from random import randint

class Crawler:
    def __init__(self, token, slot=0.1, maxWait=600):  # default: slot=0.1s, maxWait=10m
        self.token = token
        self.github = Github(token)
        self.fails = 0
        self.slot = slot
        self.maxSlots = maxWait//slot

    def search_code(self, search):
        repos = self.__search__(search, lambda g: g.search_code)
        self.__writeToFile__(search.name, repos)

    def __search__(self, search, f):
        if self.__checkFileExists__(search.name):
            return {}
        repos = {}
        query = self.__buildQuery__(search)
        results, total = self.__getQueryResults__(query, f)
        print(search.name, total)
        r = 0
        while r < 100:
            print('Processing result', r+1)
            try:
                result = results[r]
                self.__requestCompleted__()
                self.__addResult__(result, repos)
                self.__requestCompleted__()
            except GithubException:
                self.__requestFailed__()
                # fail, recompute result and start from the same item r
                results, total = self.__getQueryResults__(query, f)
                continue
            except:
                # something bad happened return the current result
                break
            r += 1
        return repos

    def __getQueryResults__(self, query, f):
        try:
            results = f(self.github)(query)
            total = results.totalCount
            self.__requestCompleted__()
        except GithubException:
            self.__requestFailed__()
            return self.__getQueryResults__(query, f)
        return (results, total)

    def __buildQuery__(self, search):
        q = '%s in:file' % search.text
        for key, value in search.more.items():
            q += ' %s:%s' % (key, value)
        return q

    def __requestFailed__(self):
        self.fails += 1
        print("request failed at attempt", self.fails, "...retrying soon")
        self.__wait__()

    def __requestCompleted__(self):
        self.fails //= 2
        self.__wait__()

    def __wait__(self):
        n = randint(0, 2**self.fails - 1) # exponential backoff
        n = min(max(1, n), self.maxSlots) # at least wait one slot, max ten minutes
        print("Waiting", n, "slots")
        sleep(self.slot * n)

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

    def __checkFileExists__(self, name):
        return os.path.isfile("results/%s.csv" % name)

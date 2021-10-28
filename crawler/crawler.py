import os
import base64
from github import Github
from github.GithubException import GithubException
from time import sleep
from random import randint
from datetime import datetime

DEFAULT_PATH = os.path.join(os.getcwd(), "results")


class Crawler:
    def __init__(self, token, slot=0.1, maxWait=25, path=DEFAULT_PATH):
        self.token = token
        self.github = Github(token)
        self.fails = 0
        self.slot = slot
        self.path = path
        self.maxSlots = maxWait//slot

    def __search__(self, search):
        res = {}
        query = self.__buildQuery__(search)
        print(query)
        results, total = self.__getQueryResults__(query)
        print(search.name, total)
        if total > 1000:
            print("WARNING the number of total results exceed the GitHub limit. Please use a different filter")
        r = 0
        while r < total:
            print(search.name, 'processing result', r+1)
            try:
                result = results[r]
                self.__requestCompleted__()
                self.addResult(result, res)
                self.__requestCompleted__()
            except GithubException as e:
                print(e)
                self.__requestFailed__()
                # fail, recompute result and start from the same item r
                results, total = self.__getQueryResults__(query)
                continue
            except Exception as e:
                print(e)
                # something bad happened return the current result
                break
            r += 1
        self.__writeToFile__(search.name, res)

    def __getQueryResults__(self, query):
        try:
            results = self.executeQuery(query)
            total = results.totalCount
            self.__requestCompleted__()
        except GithubException as e:
            print(e, query)
            self.__requestFailed__()
            return self.__getQueryResults__(query)
        return (results, total)

    def __buildQuery__(self, search):
        q = '%s in:%s' % (search.text, search.where)
        for key, value in search.more.items():
            q += ' %s:%s' % (key, value)
        return q

    def __requestFailed__(self):
        self.fails += 1
        print("request limit triggered", self.fails, "...retrying soon")
        self.__wait__()

    def __requestCompleted__(self):
        self.fails = 0
        self.__wait__()

    def __wait__(self):
        n = randint(0, 2**self.fails - 1)  # exponential backoff
        # at least wait one slot, or max maxWait
        n = min(max(1, n), self.maxSlots)
        wait = n*self.slot
        if n > 1:
            print("waiting %.1f seconds..." % wait)
        sleep(wait)

    def __writeToFile__(self, name, res):
        output = ""
        for url, files in res.items():
            data = [url] + list(files)
            output += ",".join(data) + "\n"
        f = open(self.__getPath__(name), "w")
        f.write(output)

    def __checkFileExists__(self, name):
        return os.path.isfile(self.__getPath__(name))

    def __getPath__(self, name):
        return os.path.join(self.path, "%s.csv" % name)

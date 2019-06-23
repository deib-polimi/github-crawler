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

    def getRepos(self, searches):
        repos = self.github.get_repos()
        count = 0
        for r in repos:
            self.inspectRepo(r, self.genPredicates(searches))
            count += 1
            print(count)

    def genPredicates(self, searches):
        def genPredicateFromSearch(search):
            def predicate(content, fileName):
                if search.text:
                    textSearches = search.text.split("+")
                    if not all([s in content for s in textSearches]):
                        return False
                if 'extension' in search.more and fileName.split('.')[-1] != search.more['extension']:
                    return False
                if 'filename' in search.more and fileName != search.more['filename']:
                    return False
                return True
            return predicate
        res = {}
        for search in searches:
            data = res.get(search.name, [])
            data.append(genPredicateFromSearch(search))
            res[search.name] = data
        return res

    def inspectRepo(self, repo, searches):
        commits = repo.get_commits()
        numCommits = commits.totalCount
        if numCommits < 30:
            return set()
        lastCommitDate = commits[0].commit.author.date
        if lastCommitDate < datetime(2008, 1, 1):
            return set()
        stars = repo.get_stargazers().totalCount
        if stars < 10:
            return set()
        commiters = repo.get_contributors().totalCount
        if commiters < 3:
            return set()
        return self.inspectFiles(repo, searches)

    def inspectFiles(self, repo, searches, path=""):
        folder = repo.get_contents(path)
        res = set()
        for f in folder:
            if f.type == "dir":
                res |= self.inspectFiles(repo, searches, f.path)
            else:
                for code, predicates in searches.items():
                    if any(map(lambda p: p(str(base64.b64decode(f.content)), f.name), predicates)):
                        res.add(code)
        return res


    def search_code(self, search):
        self.__search__(search, lambda g: g.search_code)

    def __search__(self, search, f):
        if self.__checkFileExists__(search.name):
            return
        repos = {}
        query = self.__buildQuery__(search)
        results, total = self.__getQueryResults__(query, f)
        print(search.name, total)
        r = 0
        while r < total:
            print(search.name, 'processing result', r+1)
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
        self.__writeToFile__(search.name, repos)

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
        print("request limit triggered", self.fails, "...retrying soon")
        self.__wait__()

    def __requestCompleted__(self):
        self.fails = 0
        self.__wait__()

    def __wait__(self):
        n = randint(0, 2**self.fails - 1) # exponential backoff
        n = min(max(1, n), self.maxSlots) # at least wait one slot, or max maxWait
        wait = n*self.slot
        if n > 1:
            print("waiting %.1f seconds..." % wait)
        sleep(wait)

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
        f = open(self.__getPath__(name), "w")
        f.write(output)

    def __checkFileExists__(self, name):
        return os.path.isfile(self.__getPath__(name))

    def __getPath__(self, name):
        return os.path.join(self.path, "%s.csv" % name)

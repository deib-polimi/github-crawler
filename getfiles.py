from github import Github
from github.GithubException import GithubException
from time import sleep
import sys

class Crawler:
    short_timeout = 5
    long_timeout = 5*60*1000

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.github = Github(tokens[0])

    def search(self, search):
        repos = {}
        query = self.__buildQuery__(search)
        results, total = self.__getQueryResults__(query)
        print(search.name, total)
        r = 0
        while r < 1:
            print('Processing result', r+1)
            try:
                result = results[r]
                self.__addResult__(result, repos)
                sleep(self.short_timeout)
            except GithubException:
                # fail, recompute result (with another token and start from the same item r)
                results, total = self.__getQueryResults__(query)
                continue
            r += 1
        self.__writeToFile__(search.name, repos)

    def __getQueryResults__(self, query):
        try:
            results = self.github.search_code(query)
            sleep(self.short_timeout)
            total = results.totalCount
        except GithubException:
            self.__changeToken__()
            return self.__getQueryResults__(query, getToken)
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

class Search:
    def __init__(self, name, text, more):
        self.name = name
        self.text = text
        self.more = more


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

crawler = Crawler(tokens)
crawler.search(Search("terraform", 'resource', {'extension': 'tf'}))
crawler.search(Search("ansible", 'tasks', {'extension': 'yml'}))
crawler.search(Search("puppet_1", 'class', {'extension': 'pp'}))
crawler.search(Search("puppet_2", 'file', {'extension': 'pp'}))
crawler.search(Search("chef", 'Cookbook', {'extension': 'rb'}))
crawler.search(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
crawler.search(Search("terraform", 'resource', {'extension': 'tf'}))
crawler.search(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
crawler.search(Search("kubernetes", 'spec', {'extension': 'yml', 'filename': 'deployments'}))
crawler.search(Search("packer", 'variables+builders', {'extension': 'json'}))
crawler.search(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
crawler.search(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
crawler.search(Search("salt", 'pkg', {'extension': 'sls'}))
crawler.search(Search("Vagrant", 'brooklyn', {'extension': 'yml'}))
crawler.search(Search("tosca_1", 'node_types', {'extension': 'yml'}))
crawler.search(Search("tosca_2", 'node_templates', {'extension': 'yml'}))

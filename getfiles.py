from github import Github
from github.GithubException import GithubException
from time import sleep
import sys

searches = [ \
# terraform
('resource', {'extension': 'tf'}), \
# ansible
('tasks', {'extension': 'yml'}), \
# puppet
('class', {'extension': 'pp'}), \
('file', {'extension': 'pp'}), \
# chef
('Cookbook', {'extension': 'rb'}), \
# cloudformation
('AWSTemplateFormatVersion', {'extension': 'yml'}), \
# compose
('services', {'extension': 'yml', 'filename': 'docker-compose'}), \
# kub
('spec', {'extension': 'yml', 'filename': 'deployments'}), \
# packer
('variables+builders', {'extension': 'json'}), \
# vagrant
('Vagrant', {'filename' : 'Vagrantfile'}), \
# cloudify
('blueprint+nodes', {'extension': 'yml'}), \
# salt
('pkg', {'extension': 'sls'}), \
# brooklyn
('brooklyn', {'extension': 'yml'}), \
# tosca
('node_types', {'extension': 'yml'}), \
('node_templates', {'extension': 'yml'}), \
]

short_timeout = 5
long_timeout = 5*60*1000

f = open("tokens.txt", "r")
tokens = f.read().splitlines()


def search(tokens, searches):
    g = Github(tokens[0])
    repos = {}
    s = 0
    while s < len(searches):
        search = searches[s]
        q = buildQuery(search)
        try:
            results = g.search_code(q)
            sleep(short_timeout)
            total = results.totalCount
            print(search, total)
        # if fails try with another token
        except GithubException:
            try:
                # get another token
                g = getToken(tokens)
                results = g.search_code(q)
            except:
                print('Waiting...')
                # if fails again wait for a long timeout and retry
                sleep(long_timeout)
                continue
        i = 0
        while i < total:
            print('Processing result', i)
            try:
                result = results[i]
            # if fails try with another token
            except GithubException:
                try:
                    # get another token
                    g = getToken(tokens)
                    results = g.search_code(q)
                    result = results[i]
                except:
                    print('Waiting...')
                    # if fails again wait for a long timeout and retry
                    sleep(long_timeout)
                    continue
            addResult(result, repos)
            sleep(short_timeout)
            i += 1
        s += 1
    return repos

def buildQuery(search):
    q = '%s in:file' % search[0]
    for key, value in search[1].items():
        q += ' %s:%s' % (key, value)
    return q

__t__ = 0
def getToken(tokens):
    __t__ = (__t__ + 1) % len(token)
    return Github(tokens[__t__])


def addResult(result, repos):
    repo = result.repository.git_url
    files = repos.get(repo, set())
    files.add(result.path)
    repos[repo] = files

repos = search(tokens, searches)

output = ""
for url, files in repos.items():
    data = [url] + list(files)
    output += ",".join(data) + "\n"

f = open("results.csv", "w")
f.write(output)

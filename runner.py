from crawler import Crawler
from search import Search
import queue
import threading

def worker(tokens):
    crawler = Crawler(tokens)
    def work():
        while True:
            item = searches.get()
            if item is None:
                break
            crawler.search_code(item)
            q.task_done()
    return work


searches = queue.Queue()
#searches.put(Search("terraform", 'resource', {'extension': 'tf'}))
searches.put(Search("ansible", 'tasks', {'extension': 'yml'}))
searches.put(Search("puppet_1", 'class', {'extension': 'pp'}))
searches.put(Search("puppet_2", 'file', {'extension': 'pp'}))
searches.put(Search("chef", 'Cookbook', {'extension': 'rb'}))
searches.put(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
searches.put(Search("terraform", 'resource', {'extension': 'tf'}))
searches.put(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
searches.put(Search("kubernetes", 'spec', {'extension': 'yml', 'filename': 'deployments'}))
searches.put(Search("packer", 'variables+builders', {'extension': 'json'}))
searches.put(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
searches.put(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
searches.put(Search("salt", 'pkg', {'extension': 'sls'}))
searches.put(Search("Vagrant", 'brooklyn', {'extension': 'yml'}))
searches.put(Search("tosca_1", 'node_types', {'extension': 'yml'}))
searches.put(Search("tosca_2", 'node_templates', {'extension': 'yml'}))

f = open("tokens.txt", "r")
tokens = f.read().splitlines()

threads = []
for i in range(len(tokens)):
    t = threading.Thread(target=worker(tokens[i:i+1]))
    t.start()
    threads.append(t)

searches.join()

# stop workers
for i in range(len(threads)):
    searches.put(None)
for t in threads:
    t.join()

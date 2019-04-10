from worker import Worker
from search import Search

f = open("tokens.txt", "r")
tokens = f.read().splitlines()

worker = Worker(tokens, lambda crawler, item: crawler.search_code(item))

worker.addSearch(Search("terraform", 'resource', {'extension': 'tf'}))
worker.addSearch(Search("ansible", 'tasks', {'extension': 'yml'}))
worker.addSearch(Search("puppet_1", 'class', {'extension': 'pp'}))
worker.addSearch(Search("puppet_2", 'file', {'extension': 'pp'}))
worker.addSearch(Search("chef", 'Cookbook', {'extension': 'rb'}))
worker.addSearch(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
worker.addSearch(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
worker.addSearch(Search("kubernetes", 'spec', {'extension': 'yml', 'filename': 'deployments'}))
worker.addSearch(Search("packer", 'variables+builders', {'extension': 'json'}))
worker.addSearch(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
worker.addSearch(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
worker.addSearch(Search("salt", 'pkg', {'extension': 'sls'}))
worker.addSearch(Search("brooklyn", 'brooklyn', {'extension': 'yml'}))
worker.addSearch(Search("tosca_1", 'node_types', {'extension': 'yml'}))
worker.addSearch(Search("tosca_2", 'node_templates', {'extension': 'yml'}))


worker.execute()

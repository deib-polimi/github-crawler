from crawler import Crawler, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

pool = CrawlerPool(tokens, Crawler.search_code)

pool.addSearch(Search("terraform", 'resource', {'extension': 'tf'}))
pool.addSearch(Search("ansible", 'tasks', {'extension': 'yml'}))
pool.addSearch(Search("puppet_1", 'class', {'extension': 'pp'}))
pool.addSearch(Search("puppet_2", 'file', {'extension': 'pp'}))
pool.addSearch(Search("chef", 'Cookbook', {'extension': 'rb'}))
pool.addSearch(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
pool.addSearch(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
pool.addSearch(Search("kubernetes", 'spec', {'extension': 'yml', 'filename': 'deployments'}))
pool.addSearch(Search("packer", 'variables+builders', {'extension': 'json'}))
pool.addSearch(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
pool.addSearch(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
pool.addSearch(Search("salt", 'pkg', {'extension': 'sls'}))
pool.addSearch(Search("brooklyn", 'brooklyn', {'extension': 'yml'}))
pool.addSearch(Search("tosca_1", 'node_types', {'extension': 'yml'}))
pool.addSearch(Search("tosca_2", 'node_templates', {'extension': 'yml'}))

pool.start()
pool.join()

from crawler import Crawler, Crawlers, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

crawlers = Crawlers(tokens, Crawler.search_code)

crawlers.addSearch(Search("terraform", 'resource', {'extension': 'tf'}))
crawlers.addSearch(Search("ansible", 'tasks', {'extension': 'yml'}))
crawlers.addSearch(Search("puppet_1", 'class', {'extension': 'pp'}))
crawlers.addSearch(Search("puppet_2", 'file', {'extension': 'pp'}))
crawlers.addSearch(Search("chef", 'Cookbook', {'extension': 'rb'}))
crawlers.addSearch(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
crawlers.addSearch(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
crawlers.addSearch(Search("kubernetes", 'spec', {'extension': 'yml', 'filename': 'deployments'}))
crawlers.addSearch(Search("packer", 'variables+builders', {'extension': 'json'}))
crawlers.addSearch(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
crawlers.addSearch(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
crawlers.addSearch(Search("salt", 'pkg', {'extension': 'sls'}))
crawlers.addSearch(Search("brooklyn", 'brooklyn', {'extension': 'yml'}))
crawlers.addSearch(Search("tosca_1", 'node_types', {'extension': 'yml'}))
crawlers.addSearch(Search("tosca_2", 'node_templates', {'extension': 'yml'}))

crawlers.start()

crawlers.join()

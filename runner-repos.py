from crawler import Crawler, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

crawler = Crawler(token=tokens[0])
searches = []
searches.append(Search("terraform", None, {'extension': 'tf'}))
searches.append(Search("ansible", 'hosts+tasks+name', {'extension': 'yml'}))
searches.append(Search("puppet", None, {'extension': 'pp'}))
searches.append(Search("chef", 'Cookbook', {'extension': 'rb'}))
searches.append(Search("cloudformation", 'AWSTemplateFormatVersion', {'extension': 'yml'}))
searches.append(Search("compose", 'services', {'extension': 'yml', 'filename': 'docker-compose'}))
searches.append(Search("kubernetes", 'kind+Pod+apiVersion', {'extension': 'yml'}))
searches.append(Search("kubernetes", 'kind+ReplicationController+apiVersion', {'extension': 'yml'}))
searches.append(Search("kubernetes", 'kind+Service+apiVersion', {'extension': 'yml'}))
searches.append(Search("kubernetes", 'kind+Deployment+apiVersion', {'extension': 'yml'}))
searches.append(Search("kubernetes", 'kind+Namespace+apiVersion', {'extension': 'yml'}))
searches.append(Search("kubernetes", 'kind+Node+apiVersion', {'extension': 'yml'}))
searches.append(Search("packer", 'variables+builders', {'extension': 'json'}))
searches.append(Search("vagrant", 'Vagrant', {'filename' : 'Vagrantfile'}))
searches.append(Search("cloudify", 'blueprint+nodes', {'extension': 'yml'}))
searches.append(Search("salt", 'pkg', {'extension': 'sls'}))
searches.append(Search("brooklyn", 'brooklyn', {'extension': 'yml'}))
searches.append(Search("tosca", 'node_types', {'extension': 'yml'}))
searches.append(Search("tosca", 'node_templates', {'extension': 'yml'}))
crawler.getRepos(searches)

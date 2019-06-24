from crawler import CrawlerCodeRepo, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()
pool = CrawlerPool(tokens, CrawlerCodeRepo)


searches = {'tosca': [Search("tosca_files", 'node_types', {'extension': 'yml'}), Search("tosca_files", 'node_templates', {'extension': 'yml'})], 'brooklyn' : [Search("brooklyn_files", 'brooklyn', {'extension': 'yml'})], 'terraform': [Search("terraform_files", 'resource', {'extension': 'tf'})], 'puppet' : [Search("puppet_files", 'class', {'extension': 'pp'}), Search("puppet_files", 'file', {'extension': 'pp'})], 'chef' : [Search("chef_files", 'Cookbook', {'extension': 'rb'})], 'cloudformation' : [Search("cloudformation_files", 'AWSTemplateFormatVersion', {'extension': 'yml'})],  'kubernetes' : [Search("kubernetes_files", 'kind+Pod+apiVersion', {'extension': 'yml'}), Search("kubernetes_files", 'kind+ReplicationController+apiVersion', {'extension': 'yml'}), Search("kubernetes_files", 'kind+Service+apiVersion', {'extension': 'yml'}), Search("kubernetes_files", 'kind+Deployment+apiVersion', {'extension': 'yml'}), Search("kubernetes_files", 'kind+Namespace+apiVersion', {'extension': 'yml'}), Search("kubernetes_files", 'kind+Node+apiVersion', {'extension': 'yml'})], 'packer' : [Search("packer_files", 'variables+builders', {'extension': 'json'})], 'vagrant' : [Search("vagrant_files", 'Vagrant', {'filename' : 'Vagrantfile'})], 'cloudify' : [Search("cloudify_files", 'blueprint+nodes', {'extension': 'yml'})], 'salt' : [Search("salt_files", 'pkg', {'extension': 'sls'})]}


for k, v in searches.items():
    csv_file = open("results/%s.csv" % (k,) , "r")
    repos = []
    for line in csv_file:
        repos.append(line)
    for s in v:
        s.repos = repos
        pool.addSearch(s)

pool.start()
pool.join()

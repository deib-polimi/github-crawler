from crawler import CrawlerRepo, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()
pool = CrawlerPool(tokens, CrawlerRepo)
#pool.addSearch(Search("microservices-docker-all-1", 'microservice docker', {'created' : '<2017-09-01'}, 'file')) 
#pool.addSearch(Search("microservices-docker-all-2", 'microservice docker', {'created' : '2017-09-01..2018-09-01'}, 'file'))
#pool.addSearch(Search("microservices-docker-all-3", 'microservice docker', {'created' : '2018-09-02..2019-06-01'}, 'file'))
#pool.addSearch(Search("microservices-docker-all-4", 'microservice docker', {'created' : '2019-06-02..2020-03-01'}, 'file'))
#pool.addSearch(Search("microservices-docker-all-5", 'microservice docker', {'created' : '>2020-03-01'}, 'file')) 
#pool.addSearch(Search("microservices-quality-all", 'microservice docker', {'stars' : '>10'}, 'file')) 
pool.addSearch(Search("microservices-quality-all2", 'microservice container', {'stars' : '>10',}, 'file')) 


pool.start()
pool.join()

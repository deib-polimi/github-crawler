from crawler import CrawlerCode, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

pool = CrawlerPool(tokens, CrawlerCode)

#pool.addSearch(Search("compose-all-1", 'microservice', {'filename': 'docker-compose.yml', 'size' : '<651'})) #947
pool.addSearch(Search("compose-all-2", 'microservice', {'filename': 'docker-compose.yml', 'size' : '651..1500'})) #977
pool.addSearch(Search("compose-all-3", 'microservice', {'filename': 'docker-compose.yml', 'size' : '1501..5000'})) #770
pool.addSearch(Search("compose-all-4", 'microservice', {'filename': 'docker-compose.yml', 'size' : '>5000'})) #363

pool.start()
pool.join()

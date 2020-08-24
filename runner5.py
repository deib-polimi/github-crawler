from crawler import CrawlerCode, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

pool = CrawlerPool(tokens, CrawlerCode)

pool.addSearch(Search("df-all-1", 'microservice', {'filename': 'Dockerfile', 'size' : '<179'})) #947
pool.addSearch(Search("df-all-2", 'microservice', {'filename': 'Dockerfile', 'size' : '179..192'})) #977
pool.addSearch(Search("df-all-3", 'microservice', {'filename': 'Dockerfile', 'size' : '192..218'})) #770
pool.addSearch(Search("df-all-4", 'microservice', {'filename': 'Dockerfile', 'size' : '218..269'})) #363
pool.addSearch(Search("df-all-5", 'microservice', {'filename': 'Dockerfile', 'size' : '269..340'})) #363
pool.addSearch(Search("df-all-6", 'microservice', {'filename': 'Dockerfile', 'size' : '340..480'})) #363
pool.addSearch(Search("df-all-7", 'microservice', {'filename': 'Dockerfile', 'size' : '480..640'})) #363
pool.addSearch(Search("df-all-8", 'microservice', {'filename': 'Dockerfile', 'size' : '640..900'})) #363
pool.addSearch(Search("df-all-9", 'microservice', {'filename': 'Dockerfile', 'size' : '900..10000'})) #363


pool.start()
pool.join()

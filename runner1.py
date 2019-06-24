from crawler import CrawlerRepo, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()
pool = CrawlerPool(tokens, CrawlerRepo)

stars = '>10'
date = '>=2018-01-01'
'''
pool.addSearch(Search("ansible", 'ansible', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("terraform", '', {'stars' : stars, 'fork':'false', 'pushed': date, 'language':'terraform'}, "readme,description"))
pool.addSearch(Search("puppet", '', {'stars' : stars, 'fork':'false', 'pushed': date, 'language':'puppet'}, "readme,description"))
pool.addSearch(Search("chef", 'chef', {'stars' : stars, 'fork':'false', 'pushed': date, 'language':'ruby'}, "description"))
pool.addSearch(Search("cloudformation", 'cloudformation', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("compose", 'docker compose', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("kubernetes", 'kubernetes', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("packer", 'packer', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("vagrant", 'vagrant', {'stars' : stars, 'fork':'false', 'pushed': date}, "description"))
pool.addSearch(Search("cloudify", 'cloudify', {'stars' : stars, 'fork':'false', 'pushed': date}, "name,readme,description"))
pool.addSearch(Search("salt", '', {'stars' : stars, 'fork':'false', 'pushed': date, 'language':'salt'}, "description"))
'''
pool.addSearch(Search("brooklyn", 'brooklyn', {'stars' : stars, 'fork':'false', 'pushed': date}, "name,description"))
pool.addSearch(Search("tosca", 'tosca', {'stars' : stars, 'fork':'false', 'pushed': date}, "name,readme,description"))

pool.start()
pool.join()

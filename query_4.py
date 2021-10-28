from crawler import CrawlerCode, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

pool = CrawlerPool(tokens, CrawlerCode)

sizes = ['<651', '651..1500', '1501..5000', '>5000']

for i, size in enumerate(sizes):
    pool.addSearch(Search(f"q4-{i}", 'microservice', {'filename': 'docker-compose.yml', 'size' : size}))

pool.start()
pool.join()

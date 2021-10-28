from crawler import CrawlerCode, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()

pool = CrawlerPool(tokens, CrawlerCode)

sizes = ['<179', '179..192', '192..218', '218..269', '269..340', '340..480', '480..640', '640..900', '900..10000']

for i, size in enumerate(sizes):
    pool.addSearch(Search(f"q3-{i}", 'microservice', {'filename': 'Dockerfile', 'size' : size}))

pool.start()
pool.join()

from crawler import CrawlerRepo, CrawlerPool, Search


f = open("tokens.txt", "r")
tokens = f.read().splitlines()
pool = CrawlerPool(tokens, CrawlerRepo)

created_dates = ['<=2015-12-31',
                 '2016-01-01..2016-05-31', '2016-06-01..2016-12-31',
                 '2017-01-01..2017-05-31', '2017-06-01..2017-12-31',
                 '2018-01-01..2018-05-31', '2018-06-01..2018-12-31',
                 '2019-01-01..2019-05-31', '2019-06-01..2019-12-31',
                 '2020-01-01..2020-05-31', '2020-06-01..2020-12-31',
                 '2021-01-01..2021-05-31', '>=2021-06-01']

for i, created_date in enumerate(created_dates):
    pool.addSearch(Search(f"q2-{i}", 'microservice container', {'created' : created_date}, 'file'))

pool.start()
pool.join()

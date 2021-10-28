import argparse
from crawler import CrawlerRepo, CrawlerPool, Search

parser = argparse.ArgumentParser()
parser.add_argument("-q", dest='query', type=int, help="Query number", required=True)
parser.add_argument("-s", dest='stars', type=int, help="Minimum number of stars", default=10)
parser.add_argument("-c", dest='date', type=str, help="Latest commit after this date, Y-m-d format", default="2021-10-01")
args = parser.parse_args()

stars = args.stars
date = args.date

if args.query in [1,2]:
    f = open("tokens.txt", "r")
    tokens = f.read().splitlines()
    pool = CrawlerPool(tokens, CrawlerRepo)

    words = (args.query == 1 and "microservice docker") or (args.query == 2 and "microservice container")
    pool.addSearch(Search(f"q{args.query}f", words, {'stars' : '>' + str(stars), 'pushed': '>' + date}, 'file'))

    pool.start()
    pool.join()

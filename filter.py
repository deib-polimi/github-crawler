from github import Github
import csv
from time import sleep
import datetime
import argparse

f = open("tokens.txt", "r")
tokens = f.read().splitlines()
g = Github(tokens[0])

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest='stars', type=int, help="Minimum number of stars", default=10)
parser.add_argument("-c", dest='date', type=str, help="Latest commit after this date, Y-m-d format", default="2021-10-01")
parser.add_argument("-i", dest='input', type=str, help="Input file (CSV)", required=True)
parser.add_argument("-o", dest='output', type=str, help="Output file (CSV)", required=True)
args = parser.parse_args()

stars = args.stars
date = args.date
input_file = args.input
output_file = args.output

date = datetime.datetime.strptime(date, '%Y-%m-%d')
res = []
i = 0
filtered_count = 0
with open(output_file, mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    with open(input_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        while True:
            i += 1
            try:
                line = next(reader)
                repo = line[0]
                repo = '/'.join(repo.split('/')[-2:]).split('.')[0]
                val = g.get_repo(repo)
                print(i, val.stargazers_count, val.pushed_at)
                if val.stargazers_count > stars and val.pushed_at >= date:
                    filtered_count += 1
                    writer.writerow([f'git://github.com/{repo}.git'])
                sleep(0.1)
            except UnicodeDecodeError as e:
                print(e)
            except StopIteration as e:
                break
            except Exception as e:
                print(e)
                print(repo)
                continue

print("Total filtered repos", filtered_count)




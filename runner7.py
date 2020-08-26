from github import Github
import csv
from time import sleep
import datetime

token = '9f35bc1eb979963e252d5a1651f17a2656cdca0d'
g = Github(token)

stars = 10
date = '2020-07-01'
date = datetime.datetime.strptime(date, '%Y-%m-%d')
res = []
i = 0
with open('filtered1.csv', mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    with open('filtered1-june.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        while True:
            i += 1
            try:
                line = next(reader)
                repo = line[0]
                repo = '/'.join(repo.split('/')[-2:]).split('.')[0]
                val = g.get_repo(repo)
                print(i, val.stargazers_count, val.updated_at)
                if val.stargazers_count > stars and val.updated_at >= date:
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





import os
from os import listdir
from os.path import join, isfile
import pandas as pd
import matplotlib.pyplot as plt

def load_result_file(path_to_result_file):
    # compute max number of columns in file
    # logger.info("Loading crawling results: " + path_to_result_file)
    max_col = -1
    with open(path_to_result_file) as fp:  
        line = fp.readline()
        while line:
            if len(line.split(",")) > max_col:
                max_col = len(line.split(",")) - 1
            line = fp.readline()
    columns = [str(i) for i in range(max_col)]
    columns.insert(0, "repo_id")
    # load csv at path_to_result_file to pandas dataframe
    dataset = pd.read_csv(path_to_result_file, names=columns)
    return dataset

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

HOME = "/home/warmik/eclipse-workspace"
CRAWLED_RESULTS_FOLDER = HOME + "/iac-crawler/results"
STATS_FOLDER = HOME + "/iac-crawler/stats"

crawled_files = [f for f in listdir(CRAWLED_RESULTS_FOLDER) if isfile(join(CRAWLED_RESULTS_FOLDER, f))]

repo_lists = []
res = {}

for f in crawled_files:
    data = load_result_file(join(CRAWLED_RESULTS_FOLDER, f))
    repo_lists.append(set(data["repo_id"].get_values()))
    
for i in range(len(repo_lists)):
    for j in range(i+1, len(repo_lists)):
        inters = intersection(repo_lists[i], repo_lists[j])
        for k in inters:
            if k not in res:
                res.update({k: {i,j}})
            else:
                updated = res[k]
                updated.add(i)
                updated.add(j)
                res.update({k: updated})  
                
print(len(res))

to_plot = []

for k in res:
    to_plot.append(len(res[k]))    
        
# plotting distribution of number of files in a repo
plt.hist(to_plot, cumulative=True, density=True, bins=100, histtype='step', label='n-files')

plt.grid(True)
#plt.legend(loc='right')
plt.title("CDF number of languages in repo.")
plt.xlabel("N-language in repo")
plt.ylabel('Likelihood of occurrence')  

plt.savefig(os.path.join(STATS_FOLDER,  "n-languages-in-repo-cdf.png"))
plt.clf()
        
        
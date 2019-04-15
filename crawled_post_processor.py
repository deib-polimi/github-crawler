import os
from os import listdir
from os.path import join, isfile
import pandas as pd 
import subprocess
from subprocess import PIPE
import numpy as np
import logging
import re
from multiprocessing import Process, cpu_count, Queue

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(name)s: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

def load_result_file(path_to_result_file):
    # compute max number of columns in file
    logger.info("Loading crawling results: " + path_to_result_file)
    max_col=-1
    with open(path_to_result_file) as fp:  
        line = fp.readline()
        while line:
            if len(line.split(","))>max_col:
                max_col=len(line.split(","))-1
            line = fp.readline()
    columns=[str(i) for i in range(max_col)]
    columns.insert(0, "repo_id")
    # load csv at path_to_result_file to pandas dataframe
    dataset=pd.read_csv(path_to_result_file, names= columns)
    return dataset

def clone_repo(repo_id):
    logger.info("Cloning repo: " + repo_id)
    subprocess.call(["git clone " + repo_id], cwd=WORKING_DIRECTORY,  shell=True)
    logger.info("Cloned")

def remo_repo(folder_repo_id):
    logger.info("Removing repo: " + folder_repo_id)
    subprocess.call(["rm -rf " + folder_repo_id], cwd=WORKING_DIRECTORY, shell=True)
    logger.info("Removed")


# to execute git command from another dir: git --git-dir /home/warmik/eclipse-workspace/iac-crawler/.git log
def get_modifying_commits_per_file(repo_folder_name, filepath):
    keywords = ["problem", "solve", "fix", "patch", "refactor"]
    logger.info("Getting commits that modified file " + filepath + " in repo " + repo_folder_name)
    print(filepath)
    p=subprocess.Popen(["git log --follow '" + filepath + "' |  egrep '[0-9a-f]{40}' -o"], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)
    out,err = p.communicate()
    commit_list=out.split("\n")
    logger.info("Retrieved commits: " + str(commit_list))
    del commit_list[-1]
    # add filtering of commits by looking keywords in the commit message
    filtered_commit_list = []
    for c in commit_list:
        p=subprocess.Popen(["git log --format=%B -n 1 " + c], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)
        out,err = p.communicate()
        word_idx = 0
        commit_added = False
        while word_idx < len(keywords) and not commit_added:
            if keywords[word_idx] in out:
                filtered_commit_list.append(c)
                commit_added = True
            word_idx = word_idx + 1 
    return filtered_commit_list

def worker(tasks, idx):
    while not tasks.empty():
        file=tasks.get()
        filepath = os.path.join(CRAWLED_RESULTS_FOLDER, file)
        dataset=load_result_file(filepath)
        out_file=os.path.join(CRAWLED_RESULTS_FOLDER, "commits-perfile" + file)
        out_dataset=pd.DataFrame(columns=OUT_COLUMNS)
        for idx, r in dataset.iterrows():
            repo_id=r['repo_id']
            if repo_id.startswith("git"):
                clone_repo(re.sub('^%s' % "git","https", repo_id))
            else:
                clone_repo(repo_id)
            # id exampe git://github.com/Inner-Heaven/box.git
            repo_folder_name=repo_id.rsplit("/",1)[1].rsplit(".",1)[0]
            for ii in range(1,len(r)):
                filepath=r.iloc[ii]
                if filepath is not np.nan:
                    commits=get_modifying_commits_per_file(os.path.join(WORKING_DIRECTORY, repo_folder_name), filepath)
                    for c in commits:
                        out_dataset=out_dataset.append({'repo_id': repo_id ,'commit': c, 'filepath': filepath}, ignore_index=True)
            remo_repo(repo_folder_name)
        out_dataset.to_csv(out_file)


logger = logging.getLogger('crawled-post-processor')

OUT_COLUMNS=["repo_id","commit","filepath"]

CRAWLED_RESULTS_FOLDER="/home/warmik/eclipse-workspace/iac-crawler/results"

WORKING_DIRECTORY="/home/warmik/eclipse-workspace/iac-crawler/wd"

onlyfiles = [f for f in listdir(CRAWLED_RESULTS_FOLDER) if isfile(join(CRAWLED_RESULTS_FOLDER, f))]

tasks = Queue()
n_procs = cpu_count()

for file in onlyfiles:
    tasks.put(file)

jobs = []

logger.info('Starting workers')
for i in range(n_procs):
    p = Process(target=worker, args=(tasks, i))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()

logger.info('Finished')
        
    


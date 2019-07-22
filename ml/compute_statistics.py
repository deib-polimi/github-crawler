import os
from os import listdir
from os.path import join, isfile
import pandas as pd
import re
import logging
import subprocess
from subprocess import PIPE
import numpy as np
import multiprocessing
from multiprocessing import Process, cpu_count, Queue
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as md
from dateutil.parser import parse
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(name)s: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')


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


def clone_repo(repo_id):
    remote = repo_id.split("//")[1]
    repo_id = "https://bla:bla@" + remote
    logger.info("Cloning repo: " + repo_id)
    subprocess.call(["git clone " + repo_id], cwd=WORKING_DIRECTORY, shell=True)
    logger.info("Cloned")


def remo_repo(folder_repo_id):
    logger.info("Removing repo: " + folder_repo_id)
    subprocess.call(["rm -rf " + folder_repo_id], cwd=WORKING_DIRECTORY, shell=True)
    logger.info("Removed")

    
def get_date_file_addition(folder_repo_id, file):
    logger.info("Getting date at which file " + file + " was added in tepo " + folder_repo_id)
    p=subprocess.Popen(["git log --format=%aD " + file
                        .replace(" ","\ ")
                        .replace("&", "\&")
                        .replace(")", "\)")
                        .replace("(", "\(") + " | tail -1"], cwd=os.path.join(WORKING_DIRECTORY, folder_repo_id), shell=True, stdout=PIPE)
    date, _ = p.communicate()
    return parse(date)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def worker(tasks, idx, return_dict):
    while not tasks.empty():
        file = tasks.get()
        logger.info("Computing stats for " + file)
        crawled = load_result_file(join(CRAWLED_RESULTS_FOLDER, file))
    
        commits = pd.read_csv(join(COMMITS_PER_FILE_FOLDER, "commits-perfile" + file), index_col=0)
        
        crawled['n_iac_files'] = crawled.count(axis=1) - 1
    
        # # computing LOC for each IaC file
        # # computing percentage of IaC files in each repo
        loc_in_files = []
        percentages_iac_files_in_repo = []
        date_first_iac_file_addition_in_repo = []
        
        for idx, r in crawled.iloc[:, :-1].iterrows():
                repo_id = r['repo_id']
                if repo_id.startswith("git"):
                    clone_repo(re.sub('^%s' % "git", "https", repo_id))
                else:
                    clone_repo(repo_id)
                    
                repo_folder_name = repo_id.rsplit("/", 1)[1].rsplit(".", 1)[0]
                if os.path.exists(os.path.join(WORKING_DIRECTORY, repo_folder_name)):
                    repo_iac_file_count = 0.0
                    repo_iac_files_addition_dates = []
                    for ii in range(1, len(r)):
                        filepath = r.iloc[ii]
                        if filepath is not np.nan:
                            if os.path.isfile(os.path.join(WORKING_DIRECTORY, repo_folder_name, filepath)):
                                repo_iac_file_count = repo_iac_file_count + 1
                                loc_in_files.append(file_len(os.path.join(WORKING_DIRECTORY, repo_folder_name, filepath)))
                                repo_iac_files_addition_dates.append(get_date_file_addition(repo_folder_name, filepath))
                    total_repo_file_count = sum([len(files) for r, d, files in os.walk(os.path.join(WORKING_DIRECTORY, repo_folder_name))])
                    percentages_iac_files_in_repo.append((repo_iac_file_count / total_repo_file_count))
                    if(len(repo_iac_files_addition_dates) > 0):
                        date_first_iac_file_addition_in_repo.append(min(repo_iac_files_addition_dates))
                    remo_repo(repo_folder_name)
                        
        return_dict[idx] = {"language/tool": file.split(".")[0],
                            "number_repos_with_at_least_one_file": crawled.shape[0],
                            "avg_number_of__iac_files_in_repo": crawled['n_iac_files'].mean(),
                            "max_number_of__iac_files_in_repo": crawled['n_iac_files'].max(),
                            "min_number_of__iac_files_in_repo": crawled['n_iac_files'].min(),
                            "total_number_of_bug_commits": commits.shape[0],
                            "avg_number_of_bug_commits_in_repo": commits.groupby(["repo_id"]).agg("count")["commit"].mean(),
                            "max_number_of_bug_commits_in_repo": commits.groupby(["repo_id"]).agg("count")["commit"].max(),
                            "min_number_of_bug_commits_in_repo": commits.groupby(["repo_id"]).agg("count")["commit"].min(),
                            "avg_number_of_loc_in_iac_file": np.mean(loc_in_files),
                            "max_number_of_loc_in_iac_file": np.max(loc_in_files) if len(loc_in_files) > 0 else np.nan,
                            "min_number_of_loc_in_iac_file": np.min(loc_in_files) if len(loc_in_files) > 0 else np.nan,
                            "avg_percentage_iac_files_in_repo": np.mean(percentages_iac_files_in_repo),
                            "max_percentage_iac_files_in_repo": np.max(percentages_iac_files_in_repo) if len(percentages_iac_files_in_repo) > 0 else np.nan,
                            "min_percentage_iac_files_in_repo": np.min(percentages_iac_files_in_repo)  if len(percentages_iac_files_in_repo) > 0 else np.nan,
                            "min_date_first_iac_file_addition_in_repo": min(date_first_iac_file_addition_in_repo) if len(date_first_iac_file_addition_in_repo) > 0 else np.nan,
                            "max_date_first_iac_file_addition_in_repo": max(date_first_iac_file_addition_in_repo) if len(date_first_iac_file_addition_in_repo) > 0 else np.nan}
                    
        logger.info("Plotting distributions...")
        
        # plotting distribution of number of files in a repo
        to_plot = crawled['n_iac_files']
        plt.hist(to_plot, cumulative=True, density=True, bins=100, histtype='step', label='n-files')
        
        plt.grid(True)
        #plt.legend(loc='right')
        plt.title('CDF n-files in repo ' + file.split("_")[0].capitalize())
        plt.xlabel("N-files in repo")
        plt.ylabel('Likelihood of occurrence')  
        
        plt.savefig(os.path.join(STATS_FOLDER, file + "-n-files-in-repo-cdf.png"))
        plt.clf()
        
        # plotting distribution of LOC in IaC file
        to_plot = loc_in_files
        plt.hist(to_plot, cumulative=True, density=True, bins=100, histtype='step', label='LOC')
        
        plt.grid(True)
        #plt.legend(loc='right')
        plt.title('CDF LOC in IaC file ' + file.split("_")[0].capitalize())
        plt.xlabel("LOC in IaC file")
        plt.ylabel('Likelihood of occurrence')  
        
        plt.savefig(os.path.join(STATS_FOLDER, file + "-loc-in-iac-file-cdf.png"))
        plt.clf()
        
        # plotting distribution of percentage of IaC files in a repo
        to_plot = percentages_iac_files_in_repo
        plt.hist(to_plot, cumulative=True, density=True, bins=100, histtype='step', label='%_iac_files_in_repo')
        
        plt.grid(True)
        ##plt.legend(loc='right')
        plt.title('CDF % IaC files in repo ' + file.split("_")[0].capitalize())
        plt.xlabel("% IaC files in repo")
        plt.ylabel('Likelihood of occurrence')  
        
        plt.savefig(os.path.join(STATS_FOLDER, file + "-%-iac-files-in-repo-cdf.png"))
        plt.clf()
        
        # plotting distribution of the date of the first IaC file addition in a repo
        to_plot = percentages_iac_files_in_repo
        plt.xticks( rotation=25 )
        xfmt = md.DateFormatter('%Y-%m-%d')
        ax=plt.gca()
        ax.xaxis.set_major_formatter(xfmt)
        plt.hist(matplotlib.dates.date2num(date_first_iac_file_addition_in_repo), cumulative=True, density=True, bins=100, histtype='step', label='date_first_IaC_file_addition_in_repo')
        
        plt.grid(True)
        ##plt.legend(loc='right')
        plt.title('CDF date of the first IaC file addition in a repo ' + file.split("_")[0].capitalize())
        plt.xlabel("date of the first IaC file addition in a repo")
        plt.ylabel('Likelihood of occurrence')  
        
        plt.savefig(os.path.join(STATS_FOLDER, file + "-date-first-iac-file-addition-in-repo-cdf.png"))
        plt.clf()
        
        logger.info("Done with " + file)
    

logger = logging.getLogger('compute-statistics')

HOME = "/home/warmik/eclipse-workspace"

WORKING_DIRECTORY = HOME + "/iac-crawler/wd"

CRAWLED_RESULTS_FOLDER = HOME + "/iac-crawler/results"

COMMITS_PER_FILE_FOLDER = HOME + "/iac-crawler/results_commits"

STATS_FOLDER = HOME + "/iac-crawler/stats"

crawled_files = [f for f in listdir(CRAWLED_RESULTS_FOLDER) if isfile(join(CRAWLED_RESULTS_FOLDER, f))]

commits_files = [f for f in listdir(COMMITS_PER_FILE_FOLDER) if isfile(join(COMMITS_PER_FILE_FOLDER, f))]

OUT_COLUMNS = ["language/tool",
                "number_repos_with_at_least_one_file",
                "avg_number_of__iac_files_in_repo",
                "max_number_of__iac_files_in_repo",
                "min_number_of__iac_files_in_repo",
                "total_number_of_bug_commits",
                "avg_number_of_bug_commits_in_repo",
                "max_number_of_bug_commits_in_repo",
                "min_number_of_bug_commits_in_repo",
                "avg_number_of_loc_in_iac_file",
                "max_number_of_loc_in_iac_file",
                "min_number_of_loc_in_iac_file",
                "avg_percentage_iac_files_in_repo",
                "max_percentage_iac_files_in_repo",
                "min_percentage_iac_files_in_repo",
                "min_date_first_iac_file_addition_in_repo"
                "max_date_first_iac_file_addition_in_repo"]

out_file = STATS_FOLDER + "/stats.csv"
out_dataset = pd.DataFrame(columns=OUT_COLUMNS)

tasks = Queue()
n_procs = 1  # cpu_count()

for file in crawled_files:
    tasks.put(file)

jobs = []

logger.info('Starting workers')

manager = multiprocessing.Manager()
return_dict = manager.dict()

for i in range(n_procs):
    p = Process(target=worker, args=(tasks, i, return_dict))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()

logger.info('Finished')

for k, v in dict(return_dict).items():
    out_dataset = out_dataset.append(v, ignore_index=True)
out_dataset.to_csv(out_file)

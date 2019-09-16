import os
import shutil
from os import listdir
from os.path import join, isfile
import pandas as pd 
import subprocess
from subprocess import PIPE
import numpy as np
import logging
import re
from multiprocessing import Process, cpu_count, Queue
from ansible.modules.cloud.amazon.route53 import commit

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
    remote=repo_id.split("//")[1]
    repo_id="https://bla:bla@" + remote
    logger.info("Cloning repo: " + repo_id)
    subprocess.call(["git clone " + repo_id], cwd=WORKING_DIRECTORY,  shell=True)
    logger.info("Cloned")

def remo_repo(folder_repo_id):
    logger.info("Removing repo: " + folder_repo_id)
    subprocess.call(["rm -rf " + folder_repo_id], cwd=WORKING_DIRECTORY, shell=True)
    logger.info("Removed")


# to execute git command from another dir: git --git-dir /home/warmik/eclipse-workspace/iac-crawler/.git log
def get_modifying_commits_per_file(repo_folder_name, filepath):
    keywords = ["problem", "solve", "fix", "patch", "refactor", "bug"]
    logger.info("Getting commits that modified file " + filepath + " in repo " + repo_folder_name)
    print(filepath)
    try:
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
        return list(set(filtered_commit_list))
    except OSError:
        logger.info("error cloning " + repo_folder_name)
        return []

def get_commit_messages(repo_folder_name, commits):
    messages = []
    for c in commits:
        p=subprocess.Popen(["git log --format=%B -n 1 " + c], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)
        out,err = p.communicate()
        messages.append(out)
    return messages

def get_commits_deletion(repo_folder_name, commits, filepath):
    # currently with this approach file that are moved or re-named, while also being fixed
    # get lost, as from the git diff they appear to be entirely new and no deletion is identified
    deletions = []
    for c in commits:
        p=subprocess.Popen(["git diff " + c + "~ " + c + " " + filepath], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)
        out,err = p.communicate()
        deletion=""
        start = False
        for l in out.split("\n"):
            if start:
                if(len(l) > 0 and l[0]=='-'):
                    if deletion=="":
                        deletion = l
                    else:
                        # currently "non consecutive" lines in a file that are deleted are all put together 
                        # as a single example of buggy code coming from that file at that commit
                        # we may think to split this into separate examples of buggy code
                        deletion = deletion + "\n" + l
            if not start and len(l) > 2 and l[0] == '@' and l[1] == '@':
                start = True
        deletions.append(deletion)
    return deletions

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
                    messages=get_commit_messages(repo_folder_name, commits)
                    deletions=get_commits_deletion(repo_folder_name, commits, filepath)
                    for c in range(len(commits)):
                        out_dataset=out_dataset.append({'repo_id': repo_id ,'commit': commits[c], 'message': messages[c], 'deletion': deletions[c], 'filepath': filepath}, ignore_index=True)
                        # TODO: here for each commit that fixes the file we should extract a copy of the file before and after the commit to then run the ansible linter
                        # copy version of "filepath" before commit "i" into folder "pre_patch_files"
                        try:
                            copy_file_at_commit(repo_folder_name, filepath, commits[c], PRE_PATCH_FILES, True)
                            # copy version of "filepath" after commit "i" into folder "post_patch_files"
                            copy_file_at_commit(repo_folder_name, filepath, commits[c] ,POST_PATCH_FILES)
                        except IOError:
                            # this should only happen when the file pre commit has a different name from that post commit
                            # in which case the file pre commit has not been copied yet (and of course the file post commit has not been copied too)
                            # so nothing needs to be done
                            continue

            remo_repo(repo_folder_name)
        out_dataset.to_csv(out_file)

def empty_folder(folder):
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            logger.error(e)
            
def copy_file_at_commit(repo_folder_name, filepath, commit, dest, pre_commit = False):
    # checkout "commit" from WORKING_DIRECTORY + "repo_folder_name"
    p=subprocess.Popen(["git checkout " + commit + "^" if pre_commit else ""], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)
    # copy "repo_folder_name" + "filepath" to "dest"    
    shutil.copy(os.path.join(WORKING_DIRECTORY, repo_folder_name, filepath), dest)
    # checkout master from WORKING_DIRECTORY + "repo_folder_name"
    p=subprocess.Popen(["git checkout master"], cwd=os.path.join(WORKING_DIRECTORY, repo_folder_name), shell=True, stdout=PIPE)

logger = logging.getLogger('crawled-post-processor')

HOME="/home/warmik/eclipse-workspace"

OUT_COLUMNS=["repo_id","commit","filepath"]

CRAWLED_RESULTS_FOLDER = os.path.join(HOME,"iac-crawler/results")

WORKING_DIRECTORY = os.path.join(HOME,"iac-crawler/wd")

# create WORKING_DIRECTORY if not exists
if not os.path.exists(WORKING_DIRECTORY):
    os.mkdir(WORKING_DIRECTORY)
    logger.info("Directory " + WORKING_DIRECTORY +  " created ")
else:    
    # empty folder WORKING_DIRECTORY if it exists
    logger.info("Directory " + WORKING_DIRECTORY +  " already exists. Emptying...")
    empty_folder(WORKING_DIRECTORY)

onlyfiles = [f for f in listdir(CRAWLED_RESULTS_FOLDER) if isfile(join(CRAWLED_RESULTS_FOLDER, f))]

tasks = Queue()
n_procs = cpu_count()

for file in onlyfiles:
    tasks.put(file)

jobs = []

PRE_PATCH_FILES = os.path.join(HOME,"iac-crawler/pre_patch_files")
POST_PATCH_FILES = os.path.join(HOME,"iac-crawler/post_patch_files")

# create folder PRE_PATCH_FILES if it does not exist
if not os.path.exists(PRE_PATCH_FILES):
    os.mkdir(PRE_PATCH_FILES)
    logger.info("Directory " + PRE_PATCH_FILES +  " created ")
else:    
    # empty folder PRE_PATCH_FILES if it exists
    logger.info("Directory " + PRE_PATCH_FILES +  " already exists. Emptying...")
    empty_folder(PRE_PATCH_FILES)

# create folder POST_PATCH_FILES if it does not exist
if not os.path.exists(POST_PATCH_FILES):
    os.mkdir(POST_PATCH_FILES)
    logger.info("Directory " + POST_PATCH_FILES +  " created ")
else:    
    # empty folder POST_PATCH_FILES if it exists
    logger.info("Directory " + POST_PATCH_FILES +  " already exists. Emptying...")
    empty_folder(POST_PATCH_FILES)


logger.info('Starting workers')
for i in range(n_procs):
    p = Process(target=worker, args=(tasks, i))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()

logger.info('Finished')
        
    


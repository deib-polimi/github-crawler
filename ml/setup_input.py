import pandas as pd
import re
import os
import numpy as np

INPUT_FILEPATH="./../results_commits/commits-perfilecompose_files.csv"
OUTPUT_DIR="compose-results"

# extract dictionary of distinct commits and corresponding repos from input file

commits=dict()

commits_perfile=pd.read_csv(INPUT_FILEPATH, index_col=0)

for index, row in commits_perfile.iterrows():
    if not row[1] in commits:
        if row['deletion'] is not np.nan:
            commits.update({re.sub('^%s' % "git","https", row['repo_id'].replace(".git","")) + "/commit/" + row['commit']: row['deletion']})


with open(os.path.join(OUTPUT_DIR,'commits.txt'), 'a') as out1:
    with open(os.path.join(OUTPUT_DIR,'deletions.txt'), 'a') as out2:
        for c in commits:
            out1.write(c + "\n")
            out2.write(commits[c] + '\nBREAKS HERE\n')
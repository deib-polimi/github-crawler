import os
from subprocess import PIPE, Popen
from ansible.plugins.callback import stderr


HOME="/home/warmik/eclipse-workspace/iac-crawler"
PRE_PATCH_FILES="pre_patch_files"
POST_PATCH_FILES="post_patch_files"

def analyze_ansible_corpus(corpus_folder):
    stdout = ""
    stderr = ""
    for filename in os.listdir(os.path.join(corpus_folder)):
        p = Popen('ansible-lint ' + os.path.join(corpus_folder, filename), shell=True, stdout=PIPE, stderr=PIPE)
        tmpstdout, tmpstderr = p.communicate()
        stdout = stdout + tmpstdout
        stderr = stderr + tmpstderr
    return stdout, stderr

out, err = analyze_ansible_corpus(os.path.join(HOME,PRE_PATCH_FILES))
print("Number of errors in all files pre patches: " + str(len(out.split("\n\n")) - 1))

with open(os.path.join(HOME, PRE_PATCH_FILES + "_out.txt"), "w") as text_file:
    text_file.write(out)

with open(os.path.join(HOME, PRE_PATCH_FILES + "_err.txt"), "w") as text_file:
    text_file.write(err)

out, err = analyze_ansible_corpus(os.path.join(HOME,POST_PATCH_FILES))
print("Number of errors in all files post patches: " + str(len(out.split("\n\n")) - 1))

with open(os.path.join(HOME, POST_PATCH_FILES + "_out.txt"), "w") as text_file:
    text_file.write(out)
    
with open(os.path.join(HOME, POST_PATCH_FILES + "_err.txt"), "w") as text_file:
    text_file.write(err)

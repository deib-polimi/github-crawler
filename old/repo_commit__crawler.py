from pydriller import RepositoryMining
url_list = ['https://github.com/ansible/ansible-modules-extras','https://github.com/geerlingguy/ansible-for-devops']

for commit in RepositoryMining(url_list).traverse_commits():
    for m in commit.modifications:
        print(
            "Author {}".format(commit.author.name),
            " modified file {}".format(m.filename),
            " with a change type of {}".format(m.change_type.name),
            #" and the complexity is {}".format(m.complexity),
            #" and in path:{}".format(commit.project_path),
            " with the Message:''{}''".format(commit.msg),
            #" and it contains {} methods".format(len(m.methods)),
            #" in commit hash {} ".format(commit.hash),
            #" in commit branch {} ".format(commit.branches),
            " with a COMMIT action {}".format(m.change_type),
            " with number of {} lines".format(m.added),
            " and number of deleted {} lines".format(m.removed),
            " having the following code {}".format(m.diff),
            #" with NLOC {} ".format(m.nloc)
            )

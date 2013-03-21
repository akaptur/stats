import json
from commit import Commit

def make_serializable(commits):
    return [c.__dict__ for c in commits]

def json_to_commits(json_obj):
    proto_commits = json.loads(json_obj)
    assert proto_commits[0].keys() == Commit().__dict__.keys() # this seems all kinds of wrong
    commit_objects = []
    for pc in proto_commits:
        c = Commit()
        for attribute in c.__dict__:
            setattr(c, attribute, pc[attribute])
        commit_objects.append(c)
    return commit_objects

def write_commit_data_to_file(commits):
    with open('akaptur_commit_data.txt', 'w') as f:
        serializable_commits = make_serializable(commits)
        json.dump(serializable_commits, f)

def read_commits_from_file(filename):
    with open(filename) as f:
        return json.loads(f.read())
import matplotlib.pyplot as plt
from json_handling import commits_to_json, json_to_commits
from stats import read_commits_from_file

date_format_string = "%Y-%m-%dT%H:%M:%SZ"


if __name__ == '__main__':
    commits = read_commits_from_file('akaptur_commit_data.txt')
    commits = json_to_commits(commits)
    commit_dates = [time.strptime(date_format_string, c.date) for c in commits]
    commit_loc = [c.additions for c in commits]

    g = plt.plot(commit_dates, commit_loc)

    g.show()


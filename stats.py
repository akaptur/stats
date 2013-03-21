import requests
from pprint import pprint
import pdb
import json
import getpass
import time
import datetime
from json_handling import write_commit_data_to_file
from commit import Commit


def get_password(github_user):
    password = None
    while not password:
        password = getpass.getpass()
        test_password_response = requests.get('https://api.github.com/user', auth=(github_user, password))
        if 'message' in test_password_response.content:
            print test_password_response.content
            print 'Probably a bad password'
        else:
            break
    return password

def get_commits(github_user, fetch=False, write_to_file=False):
    password = get_password(github_user)
    if fetch:
        base_url = "https://api.github.com"
        events_url_tail = '/users/'+github_user+'/events'
        response = requests.get(base_url + events_url_tail, auth=(github_user, password))
        events = response.content
        if write_to_file:
            with open('akaptur_events.txt', 'w') as f:
                f.write(events)
        # events = json.load(events) # probably doesn't work
    else:
        with open('akaptur_events.txt') as f:
            events = json.load(f)

    my_commits = []
    print "Total events:", len(events)
    for event in events[:10]:
        print "Event type:", event['type']
        pdb.set_trace()
        if event['type'] == "PushEvent":
            commits = event['payload']['commits']
            print len(commits)
            for comm in commits:
                c = Commit()
                c.url = comm['url']
                # per-event API call :(
                commit_response = requests.get(c.url, auth=(github_user, password))
                commit_data = json.loads(commit_response.content)
                c.additions = commit_data['stats']['additions']
                c.deletions = commit_data['stats']['deletions']
                c.timestamp = commit_data['commit']['author']['date']
                c.message = commit_data['commit']['message']
                my_commits.append(c)
                

    return my_commits


def filter_by_date(commits, start_date, end_date=None):
    date_format_string = "%Y-%m-%dT%H:%M:%SZ"

    if end_date is None:
        end_date = datetime.date.today().timetuple()
    
    return [c for c in commits if start_date > time.strptime(c.date, date_format_string) > end_date]



if __name__ == '__main__':
    commits = get_commits('akaptur', fetch=False)
    write_commit_data_to_file(commits)
    start_of_year = time.strptime(str(datetime.date.today().year), "%Y")
    

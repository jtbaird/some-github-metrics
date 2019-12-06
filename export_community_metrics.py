import argparse
from github import Github
import requests
import json
import csv
import os
import datetime
import socket
import pandas as pd

socket.setdefaulttimeout(60 * 60)
today = datetime.date.today()
todaystr = str(today)

# set up flags for commandline interface
def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--org", help="choose what company you what to see", required=True)
    parser.add_argument("-t", "--token", help="OAuth token from GitHub", required=True)
    args = parser.parse_args()
    return args

def export_community_engagement(directory, organization, authToken):
    g = Github(authToken)
    today = str(datetime.date.today())
    today = today.replace("-", "")
    totalrepos = 0
    allorgs = g.get_user().get_orgs()
    for orgs in allorgs:
        if orgs.login == organization:
            for repo in orgs.get_repos():
                if repo.fork == False and repo.private == False:
                    totalrepos += 1
    with open(directory + "/github_community_engagement_" + organization + "_" + today+ ".csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(
            ["date", "org", "repo", "forks", "stars", "commits", "collaborators"])
        for orgs in allorgs:
            if orgs.login == organization:
                print("Gathering community metrics for", orgs.name)
                count = 0
                for repo in orgs.get_repos():
                    countcommit = 0
                    countcollab = 0
                    if repo.fork == False and repo.private == False:
                        count += 1
                        for commits in repo.get_commits():
                            countcommit += 1
                        for collab in repo.get_contributors():
                            countcollab += 1
                        print("[", str(count).zfill(2), "|", totalrepos, "]", repo.name, "|", countcommit, "commits |", repo.forks_count, "forks |",
                              repo.stargazers_count, "stars |", countcollab, "contributors")
                        csvwriter.writerow(
                            [todaystr, organization, repo.name, repo.forks_count, repo.stargazers_count, countcommit,
                             countcollab])

def main():
    args = setup()
    organization = args.org
    authToken = args.token
    g = Github(authToken)
    directory = "output/" + organization
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        print("Valid token. Starting process. \n")
        print("")
        export_community_engagement(directory, organization, authToken)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
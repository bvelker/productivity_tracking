import requests, os, json, subprocess
from datetime import datetime, timedelta
import yaml

class GithubTracker:
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def get_commit_details(self, repo_owner, repo, sha):
        url = f'https://api.github.com/repos/{repo_owner}/{repo}/commits/{sha}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        # print(response.json())
        data = response.json()
        return {
            'hash': data['sha'],
            'author': data['commit']['author']['name'],
            'timestamp': data['commit']['author']['date'],
            'message': data['commit']['message'],
            'lines_added': data['stats']['additions']
        }

    def get_total_lines_added(self, repo_owner, repo, date):
        url = f'https://api.github.com/repos/{repo_owner}/{repo}/commits?since={date}T00:00:00Z&until={date}T23:59:59Z&author={self.username}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        commits = response.json()

        total_lines_added = 0
        details_list = []
        for commit in commits:
            commit_details = self.get_commit_details(repo_owner, repo, commit['sha'])
            total_lines_added += commit_details['lines_added']
            details_list.append(commit_details)

        return {
            'date': date,
            'total_commits': len(commits),
            'total_lines_added': total_lines_added,
            'commits': sorted(details_list, key=lambda x: x['timestamp'])
        }

    def get_repos(self, date):
        # Format datetime object as 'YYYY-MM-DD'
        date_str = date.strftime('%Y-%m-%d')

        # Create start and end times
        start_time = f'{date_str}T00:00:00Z'
        end_time = f'{date_str}T23:59:59Z'

        page = 1
        repos = set()
        etag = None
        while True:
            url = f'https://api.github.com/search/commits?q=author:{self.username}+committer-date:{start_time}..{end_time}&page={page}&per_page=20'
            headers = {
                'Accept': 'application/vnd.github.cloak-preview',
                'Authorization': f'token {self.token}'
            }
            if etag:
                headers['If-None-Match'] = etag
            response = requests.get(url, headers=headers)

            if response.status_code == 304:
                break  # Data hasn't changed, no need to continue
            etag = response.headers.get('ETag')  # Store the ETag for next time
            data = response.json()

            if 'items' not in data:
                print(f"Status code: {response.status_code}")
                print(f"Response data: {data}")
                break
            for item in data['items']:
                repo_url = item['repository']['url']
                _, owner, repo_name = repo_url.rsplit('/', 2)
                repos.add((owner, repo_name))
            
            # Check if this is the last page
            if 'next' not in response.links:
                print("This is the last page.")
                return list(repos)
            page += 1
        return list(repos)

    def generate_yaml_ready_dict(self, date):
        repos = self.get_repos(date)
        yaml_ready_dicts = []
        if len(repos) > 0:
            for repo in repos:
                owner, repo_name = repo
                yaml_ready_dict = self.get_total_lines_added(owner, repo_name, date.strftime('%Y-%m-%d'))
                yaml_ready_dicts.append(yaml_ready_dict)
        else:
            # If there are no commits, set default values
            yaml_ready_dicts = [{
                'date': date,
                'total_commits': 0,
                'total_lines_added': 0,
                'commits': []
            }]
        return yaml_ready_dicts

    def to_yaml(self, yaml_ready_dicts):
        yaml_str = yaml.dump(yaml_ready_dicts, default_flow_style=False, sort_keys=False)
        return yaml_str

    def from_yaml(self, yaml_str):
        yaml_ready_dicts = yaml.load(yaml_str, Loader=yaml.FullLoader)
        return yaml_ready_dicts

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    # Replace these with your own details
    username = 'bvelker'
    token = os.environ['GITHUB_TOKEN']
    date = datetime(2023, 9, 5)
    date = datetime(2023, 5, 12)
    date = datetime(2023, 9, 6)

    tracker = GithubTracker(username, token)
    print(tracker.to_yaml(tracker.generate_yaml_ready_dict(date)))

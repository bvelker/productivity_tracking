import subprocess, json, os
from datetime import datetime, timedelta


def get_commit_details(date):
    date_str = date.strftime('%Y-%m-%d 00:00:00')
    next_day_str = (date + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

    log_output = subprocess.check_output(['git', 'log', '--after='+date_str, '--before='+next_day_str, '--pretty=format:%H,%an,%ad,%s']).decode('utf-8')
    commit_details = log_output.splitlines()

    details_list = []
    for detail in commit_details:
        commit_hash, author, commit_date, message = detail.split(',')

        details_list.append({
            'hash': commit_hash,
            'author': author,
            'timestamp': commit_date,
            'message': message
        })

    return details_list


def get_total_lines_added(date):
    date_str = date.strftime('%Y-%m-%d')

    commit_hashes = subprocess.check_output(['git', 'log', '--pretty=format:%H', f'--after="{date_str} 00:00:00"', f'--before="{date_str} 23:59:59"']).splitlines()
    first_repo_commit = subprocess.check_output(['git', 'rev-list', '--max-parents=0', 'HEAD']).decode('utf-8').strip()
    total_lines_added = 0

    commit_details = get_commit_details(date)
    # reverse the list
    commit_details = commit_details[::-1]
    for index, commit_detail in enumerate(commit_details):
        num_lines_added = 0
        commit_hash_str = commit_detail['hash']
        if commit_hash_str == first_repo_commit:
            cmd = f"git show {commit_hash_str} | grep -vE '^\+//|^\+#|^\+/\*|^\+\*|^\+$' | wc -l"
            num_lines_added = int(subprocess.check_output(cmd, shell=True).decode('utf-8').strip())
        else:
            diff = subprocess.check_output(['git', 'diff', commit_hash_str + '^!', '--numstat'])
            diff_str = diff.decode('utf-8')
            num_lines_added = sum(int(line.split()[0]) for line in diff_str.splitlines() if line.split()[0].isdigit())

        total_lines_added += num_lines_added

        commit_detail['lines_added'] = num_lines_added

    return {
        'date': date_str,
        'total_commits': len(commit_hashes),
        'total_lines_added': total_lines_added,
        'commits': commit_details
    }

def get_repos(username):
    repos_output = subprocess.check_output(['gh', 'repo', 'list', username, '--json', 'name']).decode('utf-8')
    repos = [repo['name'] for repo in json.loads(repos_output)]
    return repos

if __name__ == '__main__':
    username = 'bvelker'
    token = os.environ['GITHUB_TOKEN']
    date = datetime(2023, 9, 5)
    repos = get_repos(username)

    for repo in repos:
        os.chdir(f'https://github.com/{username}/{repo}')
        print(get_total_lines_added(repo, date))



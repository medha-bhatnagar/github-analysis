from .services import request_user, request_repo, request_repo_info, request_repo_languages, pull_info, issues 

async def merged_percentage(username, repo):
    info = await pull_info(username, repo)
    if not info:
        return "N/A"
    total_prs = len(info)
    merged_prs = sum(
        1 for pr in info
        if pr["merged_at"] is not None
    )
    return (merged_prs / total_prs) * 100
#print(merged_percentage('python', 'cpython')) 

async def profile_pic(username):
    info = await request_user(username)
    if info:
        profile_url = info.get("html_url") + ".png"
    return profile_url

async def forks(username, repo):# NOT SURE ABOUT USE
    info = await request_repo_info(username, repo)
    return info.get('forks')

async def creation_date(username, repo):
    info = await request_repo_info(username, repo)
    return info.get('created_at')
    #coordinated universal time, may have to convert to date time
async def stars(username, repo):
    info = await request_repo_info(username, repo)
    return info.get('stargazers_count')

async def last_updated(username, repo): # NOT SURE ABOUT USE
    info = await request_repo_info(username, repo)
    return info.get('updated_at')
    #coordinated universal time, may have to convert to date time

async def total_issues_opened(username, repo):
    issue_data = await issues(username, repo)
    return len(issue_data)


async def open_issues(username, repo):
    issue_data = await issues(username, repo)
    return sum(
        1
        for issue in issue_data
        if issue["state"] == "open"
    )


async def closed_issues(username, repo):
    issue_data = await issues(username, repo)
    return sum(
        1
        for issue in issue_data
        if issue["state"] == "closed"
    )

async def issue_close_rate(username, repo):
    issue_data = await issues(username, repo)
    total = len(issue_data)
    if total == 0:
        return 0
    closed = sum(
        1
        for issue in issue_data
        if issue["state"] == "closed"
    )
    term = f'{int((closed/total) * 100)}%'
    return term
def most_starred_repos():
    stars_dict = {}
    total = len()


def most_used_languages(username):
    """
    dict(total sum for each language = 0)
    for each repo
        add language usage to total sum
    
    """
async def display_name(username):
    info = await request_user(username)
    return info.get("name")

async def display_username(username):
    info = await request_user(username)
    return info.get("login")

async def get_repo_name(username): 
    repo_list = []
    repos = await request_repo(username)
    for repo in repos:
            repo_list.append(repo['name'])
    return repo_list

async def get_bio(username):
    info = await request_user(username)
    return info.get("bio")

async def account_creation(username):
    info = await request_user(username)
    return info.get("created_at")
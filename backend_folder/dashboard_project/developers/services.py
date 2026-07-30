import httpx
import os
import base64
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2026-03-10"
}
username = 'microsoft'
repo = 'vscode'
repo_list = []

async def request_user(username):
    url = f'{BASE_URL}/users/{username}'
    async with httpx.AsyncClient() as client:
        response = await client.get(
            #while waiting for GitHub to respond, Python
            #can work on other things
            url,
            headers=HEADERS
        )
    
        response.raise_for_status() #automatically raises exception if 
                                    #an HTTP request fails
        return response.json()

async def request_repo(username):
    repo_count = 0
    url = f'{BASE_URL}/users/{username}/repos'
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()

async def request_repo_info(username, repo): 
    url = f'{BASE_URL}/repos/{username}/{repo}'
    async with httpx.AsyncClient() as client:
         response = await client.get(
              url,
              headers=HEADERS
         )
         response.raise_for_status()
         return response.json()

async def request_repo_languages(username, repo):
    url = f"{BASE_URL}/repos/{username}/{repo}/languages"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()


async def pull_info(username, repo):
    url =f'{BASE_URL}/repos/{username}/{repo}/pulls?state=all'
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()
        print("Number of PRs returned:", len(data))
        return data
 
async def issues(username, repo):
    """Fetch all issues (excluding pull requests) for a repository."""

    url = f"{BASE_URL}/repos/{username}/{repo}/issues?state=all&per_page=100"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code != 200:
            return []

        data = response.json()

        # Removing given pull requests 
        return [
            issue
            for issue in data
            if "pull_request" not in issue
        ]
    

async def top_3_starred_repos(username):
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=user:{username}&sort=stars&order=desc"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()

    items = response.json()["items"]

    top_repos = []

    # Add up to the first 3 repos
    for repo in items[:3]:
        top_repos.append({
            "name": repo["name"],
            "stars": repo["stargazers_count"]
        })

    # Fill remaining slots with None
    while len(top_repos) < 3:
        top_repos.append({
            "name": None,
            "stars": None
        })

    return top_repos

async def readme_encoded(username, repo):
    url = f"{BASE_URL}/repos/{username}/{repo}/readme"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 404:
            return None
        response.raise_for_status()
    return response.json()

async def get_repo_contents(username, repo, path=""):
    #List files/folders at a given path in a repo (default: root).
    url = f"{BASE_URL}/repos/{username}/{repo}/contents/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()  


async def get_file_content(username, repo, path):
    """Fetch and decode a specific file's text content."""
    url = f"{BASE_URL}/repos/{username}/{repo}/contents/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()

    encoded = data.get("content")
    if not encoded:
        return None
    return base64.b64decode(encoded).decode("utf-8", errors="ignore")


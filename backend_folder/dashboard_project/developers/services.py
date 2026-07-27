import httpx
import os
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
    async with httpx.AsyncClient() as client:
        response = await client.get(
            #while waiting for GitHub to respond, Python
            #can work on other things
            f'{BASE_URL}/users/{username}',
            headers=HEADERS
        )
    
        response.raise_for_status() #automatically raises exception if 
                                    #an HTTP request fails
        return response.json()

# info = asyncio.run(get_user(username))
# if info:

#     print("username: ", info.get('login')) 
#     print("account url: ", info.get('url')) 
#     print("name: ", info.get('name')) 
#     print("company: ", info.get('company')) 
#     print("personal website:", info.get('blog')) 
#     print("location: ", info.get('location'))
#     print("email: ", info.get('email'))
#     print("hireable: ", info.get('hireable'))
#     print("bio: ", info.get('bio'))
#     print("public repos: ", info.get('public_repos'))
#     print("twitter: ", info.get('twitter_username')) #have logo**************
#     print("public gists: ", info.get('public_gists'))
#     print("followers: ", info.get('followers'))
#     print("following: ", info.get('following'))
#     print("created at: ", info.get('created_at'))
    
async def request_repo(username):
    repo_count = 0
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{BASE_URL}/users/{username}/repos',
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()

async def request_repo_info(username, repo): 
    async with httpx.AsyncClient() as client:
         response = await client.get(
              f'{BASE_URL}/repos/{username}/{repo}',
              headers=HEADERS
         )
         response.raise_for_status()
         return response.json()

async def request_repo_languages(username, repo):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{BASE_URL}/repos/{username}/{repo}/languages',
            headers = HEADERS
        )
        response.raise_for_status()
        language_dict = response.json()
        value_sum = 0
        for value in language_dict.values():
            value_sum += value
        for key, value in language_dict.items():
            language_dict[key] = f'{int((value/value_sum) * 100)}%'
            if language_dict[key] == '0%':
                language_dict[key] = '> 1%'
        return language_dict
# print(asyncio.run(repo_languages(username, 'linux')))
#print(asyncio.run(get_repo(username)))
#get_repo_names(username)
# async def pull_info(username, repo):

#     async with httpx.AsyncClient() as client:
         
#         response = await client.get(
#             f'{BASE_URL}/repos/{username}/{repo}/pulls?state=all',
#             headers = HEADERS
#         )
#         if(response.status_code == 404):
#             return None
#         response.raise_for_status()    
#         return response.json()
async def pull_info(username, repo):

    async with httpx.AsyncClient() as client:
        
        response = await client.get(
            f'{BASE_URL}/repos/{username}/{repo}/pulls?state=all',
            headers=HEADERS
        )

        print("PR Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        print("Number of PRs returned:", len(data))

        return data
# info = asyncio.run(pull_info("python", "cpython"))
# print(info)
async def issues(username, repo):
    """Fetch all issues (excluding pull requests) for a repository."""

    url = f"{BASE_URL}/repos/{username}/{repo}/issues?state=all&per_page=100"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code != 200:
            return []

        data = response.json()

        # Remove pull requests (GitHub returns them in the Issues API)
        return [
            issue
            for issue in data
            if "pull_request" not in issue
        ]
    





    

# Test Functions


# if __name__ == "__main__":
#     print("\n========== USER INFO ==========")
#     user_info = asyncio.run(request_user(username))
#     print("Username:", user_info.get("login"))
#     print("Name:", user_info.get("name"))
#     print("Public Repos:", user_info.get("public_repos"))
#     print("Followers:", user_info.get("followers"))

    # print("\n========== REPOSITORY INFO ==========")
    # print("Repository Names:")
    # get_repo_name(username)

    # print("\nForks:")
    # print(forks(username, repo))

    # print("\nCreation Date:")
    # print(creation_date(username, repo))

    # print("\nStars:")
    # print(stars(username, repo))

    # print("\nLast Updated:")
    # print(last_updated(username, repo))


    # print("\n========== LANGUAGE METRICS ==========")
    # print("Languages:")
    # print(asyncio.run(request_repo_languages(username, repo)))


    # print("\n========== PULL REQUEST METRICS ==========")
    # print("Merged PR Percentage:")
    # print(merged_percentage(username, repo))


    # print("\n========== ISSUE METRICS ==========")
    # print("Total Issues Opened:")
    # print(total_issues_opened(username, repo))

    # print("\nOpen Issues:")
    # print(open_issues(username, repo))

    # print("\nClosed Issues:")
    # print(closed_issues(username, repo))

    # print("\nIssue Close Rate:")
    # print(issue_close_rate(username, repo))
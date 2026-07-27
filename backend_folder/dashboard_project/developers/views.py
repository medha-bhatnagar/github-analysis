from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import Profile, MetricData, FileData

from .services import(
    request_user,
    request_repo,
    request_repo_info,
    request_repo_languages,
    pull_info, 
    issues
)
from .analytics import(
    profile_pic,
    creation_date,
    total_issues_opened,
    open_issues,
    closed_issues,
    issue_close_rate,
    most_starred_repos,
    most_used_languages,
    display_name,
    display_username,
    get_repo_name,
    get_bio,
    account_creation
)

async def analyze_profile(request, username):
    bio = await get_bio(username)
    name = await display_name(username)
    return JsonResponse({"bio": bio, "name": name})

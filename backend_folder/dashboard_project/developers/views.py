from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import Profile, MetricData, FileData

from .services import(
    request_user,
    request_repo,
    request_repo_info,
    request_repo_languages,
    pull_info, 
    issues,
    top_3_starred_repos,
    readme_encoded,
    get_repo_contents,
    get_file_content
)
from .analytics import(
    profile_pic,
    creation_date,
    total_issues_opened,
    open_issues,
    closed_issues,
    issue_close_rate,
    top_languages,
    display_name,
    display_username,
    get_repo_name,
    get_bio,
    account_creation,
    top_languages,
    readme_decoded,
    profile_readme,
    is_recent,
    get_recent_repos,
    detect_repo_stack,
    detect_tech_stack
)

async def analyze_profile(request, username):
    bio = await get_bio(username) or ""
    name = await display_name(username) or ""
    pic = await profile_pic(username) or ""
    save_profile = sync_to_async(Profile.objects.update_or_create)
    languages = await top_languages(username)
    stack = await detect_tech_stack(username)
    tech_stack = [lang["language"] for lang in languages if lang["language"]] + stack
    profile, _ = await save_profile(
        username=username,
        defaults={
            "full_name": name,
            "bio": bio,
            "profile_image": pic,
            "tech_stack": tech_stack
        }
    )
    return JsonResponse({"bio": bio, "name": name, "tech_stack": tech_stack, "saved": True})
from django.db import models

class Profile(models.Model):
    profile_image = models.URLField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    profile_readme = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    account_age = models.DateTimeField(auto_now=True)
    account_age = models.DateTimeField(auto_now=True)
    tech_stack = models.JSONField(default=list, blank=True)
    #latest_repos
    
class MetricData(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="metrics")
    most_used_languages = models.JSONField(default=list)
    merge_rate = models.CharField(max_length=255, blank=True)
    issue_resolution = models.CharField(max_length=255, blank=True)
    pr_resolution = models.CharField(max_length=255, blank=True)
    commit_frequency = models.CharField(max_length=255, blank=True)
    #top_3_starred_repos = models.JSONField(default=list)
    #repo_quality_score = models.IntegerField(null=True)
    
class FileData(models.Model):
    
    FILE_TYPES = [
        ("readme", "README"),
    ("dockerfile", "Dockerfile"),
        ("other", "Other"),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="files")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    content = models.TextField(blank=True)
    
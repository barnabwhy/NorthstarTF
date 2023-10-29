# %%
import requests
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class OrgRepoCombo:
    org: str
    repo: str


def get_contributors(org_repo_combo: OrgRepoCombo) -> Optional[List[str]]:
    url = f"https://api.github.com/repos/{org_repo_combo.org}/{org_repo_combo.repo}/contributors"
    response = requests.get(url)
    if response.status_code == 200:
        contributors = response.json()
        return [contributor["login"] for contributor in contributors]
    else:
        print(f"Failed to retrieve contributors. Status code: {response.status_code}")
        return None


def get_organization_repositories(org_name: str) -> Optional[List[str]]:
    url = f"https://api.github.com/orgs/{org_name}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repositories = response.json()
        return [repo["name"] for repo in repositories]
    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")
        return None


def get_profile_picture_link(username: str) -> Optional[str]:
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data["avatar_url"]
    else:
        print(
            f"Failed to retrieve data for {username}. Status code: {response.status_code}"
        )
        return None


orgs = ["R2Northstar", "R2NorthstarTools"]


# Get all repos for tracked orgs and add to list
repo_org_combos = list()
for org_name in orgs:
    repositories = get_organization_repositories(org_name)
    repo_org_combos += [OrgRepoCombo(org=org_name, repo=repo) for repo in repositories]

# Get list of all contributors
all_contributors = set()
for org_repo_combo in repo_org_combos:
    contributors = get_contributors(org_repo_combo)
    all_contributors.update(contributors)

all_contributors = list(all_contributors)

# Get profile pics
for username in all_contributors:
    github_username = username
    profile_picture_link = get_profile_picture_link(github_username)
    if profile_picture_link:
        print(f"Profile Picture Link for {github_username}: {profile_picture_link}")

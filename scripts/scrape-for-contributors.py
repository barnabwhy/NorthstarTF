# %%
import requests
from typing import List, Optional
from dataclasses import dataclass
import json
import re


@dataclass
class Contributor:
    url: str
    icon: str
    name: str
    description: str


@dataclass
class OrgRepoCombo:
    org: str
    repo: str


json_files = ["core.json", "contrib.json", "past-contrib.json"]
json_file_path = "../dist/data/"


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

# Parse manually tracked contributors
manual_contribs = []
for json_file in json_files:
    full_json_path = f"{json_file_path}{json_file}"
    with open(full_json_path, "rt") as f:
        data = json.load(f)
        for item in data:
            contributor = Contributor(
                url=item["url"],
                icon=item["icon"],
                name=item["name"],
                description=item["description"],
            )
            manual_contribs.append(contributor)

# Get their usernames
contributor_usernames = set()
for contributor in manual_contribs:
    username = re.search("github.com/([A-Za-z0-9-]+/?)", contributor.url).group(1)
    contributor_usernames.add(username)

# Remove manually tracked contributors from the list of scraped ones
filtered_contributors = [
    contrib for contrib in all_contributors if contrib not in contributor_usernames
]

# Get profile pics
for username in filtered_contributors:
    github_username = username
    profile_picture_link = get_profile_picture_link(github_username)
    if profile_picture_link:
        print(f"Profile Picture Link for {github_username}: {profile_picture_link}")

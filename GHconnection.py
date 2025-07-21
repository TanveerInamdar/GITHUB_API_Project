import requests
import os
from dotenv import load_dotenv

# Load token
load_dotenv("/.env")


username = os.getenv("GITHUB_USER")
token = os.getenv("GITHUB_PAT")

# Validate token
if not token:
    raise ValueError("Token not found. Make sure GITHUB_PAT is set in .env.")

# Headers for auth
headers = {
    "Authorization": f"token {token}"
}

# API request
url = f"https://api.github.com/users/{username}/repos"
res = requests.get(url, headers=headers)

# Check for error
if res.status_code != 200:
    print(f"❌ API Error {res.status_code}: {res.json().get('message')}")
    exit()

# Parse JSON
repos = res.json()

# Handle unexpected structure
if not isinstance(repos, list):
    print("❌ Unexpected response format:")
    print(repos)
    exit()

# Print repo info
for repo in repos:
    name = repo['name']
    last_push = repo['pushed_at']
    full_name = repo['full_name']
    print(f"📁 {name} – Last push: {last_push} - Commiter: {full_name}")
print(repos)
import requests
import os
from flask import Flask, render_template_string
from dotenv import load_dotenv
from datetime import datetime

# Load token
load_dotenv(r"C:\Github\GITHUBapi\.env")

app = Flask(__name__)

username = os.getenv("GITHUB_USER")
token = os.getenv("GITHUB_PAT")

# Validate token
if not token:
    raise ValueError("Token not found. Make sure GITHUB_PAT is set in .env.")

# Headers for auth
headers = {
    "Authorization": f"token {token}"
}

# HTML Templates (defined before use)
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Repositories Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .stat-card {
            background: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-card .number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-card .label {
            color: #666;
            margin-top: 5px;
        }
        
        .repo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .repo-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .repo-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }
        
        .repo-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .repo-icon {
            font-size: 2em;
            margin-right: 10px;
        }
        
        .repo-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .repo-full-name {
            color: #666;
            font-size: 0.9em;
        }
        
        .repo-info {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9em;
        }
        
        .info-label {
            color: #666;
            font-weight: 500;
        }
        
        .info-value {
            color: #333;
        }
        
        .language-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-top: 10px;
        }
        
        .repo-link {
            display: inline-block;
            margin-top: 15px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .repo-link:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .empty-state {
            text-align: center;
            color: white;
            padding: 60px 20px;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 GitHub Repositories</h1>
            <p>Repositories for <strong>{{ username }}</strong></p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="number">{{ stats.total }}</div>
                <div class="label">Total Repositories</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.public }}</div>
                <div class="label">Public Repos</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ stats.private }}</div>
                <div class="label">Private Repos</div>
            </div>
        </div>
        
        {% if repos %}
        <div class="repo-grid">
            {% for repo in repos %}
            <div class="repo-card">
                <div class="repo-header">
                    <div class="repo-icon">📁</div>
                    <div>
                        <div class="repo-name">{{ repo.name }}</div>
                        <div class="repo-full-name">{{ repo.full_name }}</div>
                    </div>
                </div>
                
                {% if repo.description %}
                <p style="color: #666; margin: 10px 0; font-size: 0.9em;">{{ repo.description[:100] }}{% if repo.description|length > 100 %}...{% endif %}</p>
                {% endif %}
                
                <div class="repo-info">
                    <div class="info-item">
                        <span class="info-label">Last Push:</span>
                        <span class="info-value">{{ format_date(repo.pushed_at) }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Created:</span>
                        <span class="info-value">{{ format_date(repo.created_at) }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Stars:</span>
                        <span class="info-value">⭐ {{ repo.stargazers_count }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Forks:</span>
                        <span class="info-value">🍴 {{ repo.forks_count }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Visibility:</span>
                        <span class="info-value">
                            {% if repo.private %}🔒 Private{% else %}🌍 Public{% endif %}
                        </span>
                    </div>
                </div>
                
                {% if repo.language %}
                <span class="language-badge">{{ repo.language }}</span>
                {% endif %}
                
                <a href="{{ repo.html_url }}" target="_blank" class="repo-link">View on GitHub →</a>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <p>No repositories found.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - GitHub Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .error-card {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }
        .error-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        .error-card h1 {
            color: #e74c3c;
            margin-bottom: 15px;
        }
        .error-card p {
            color: #666;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="error-card">
        <div class="error-icon">❌</div>
        <h1>Error</h1>
        <p>{{ error }}</p>
    </div>
</body>
</html>
"""

def get_repos():
    """Fetch repos from GitHub API"""
    url = f"https://api.github.com/users/{username}/repos"
    res = requests.get(url, headers=headers)
    
    if res.status_code != 200:
        return None, f"API Error {res.status_code}: {res.json().get('message')}"
    
    repos = res.json()
    if not isinstance(repos, list):
        return None, "Unexpected response format"
    
    return repos, None

def format_date(date_str):
    """Format ISO date string to readable format"""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def calculate_stats(repos):
    """Calculate repository statistics"""
    total = len(repos)
    public = sum(1 for repo in repos if not repo.get('private', False))
    private = total - public
    return {'total': total, 'public': public, 'private': private}

@app.route('/')
def dashboard():
    repos, error = get_repos()
    
    if error:
        return render_template_string(ERROR_TEMPLATE, error=error), 500
    
    stats = calculate_stats(repos) if repos else {'total': 0, 'public': 0, 'private': 0}
    return render_template_string(DASHBOARD_TEMPLATE, repos=repos, username=username, format_date=format_date, stats=stats)

if __name__ == '__main__':
    print(f"✅ GitHub Dashboard starting on http://localhost:5000")
    print(f"📁 Fetching repos for user: {username}")
    app.run(debug=True, host='localhost', port=5000)

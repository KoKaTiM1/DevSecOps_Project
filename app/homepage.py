from flask import Flask, jsonify, render_template
import time
import subprocess
import os
import requests
import re
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics


# start time for uptime calculation
START_TIME = time.time()

GITHUB_OWNER = os.getenv("GITHUB_OWNER", "KoKaTiM1")
GITHUB_REPO = os.getenv("GITHUB_REPO", "DevSecOps_Project")
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

_repo_cache = {
    "ts": 0,
    "version": "unknown",
    "commits": 0,
}


def get_uptime():
    now = time.time()
    uptime_seconds = now - START_TIME
    return uptime_seconds


def format_uptime(seconds):
    """Format uptime seconds into human-readable format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def get_git_version():
    """Get version from git tags or commit hash"""
    try:
        # Try to get the latest tag
        version = subprocess.check_output(
            ['git', 'describe', '--tags'],
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(__file__) or '.'
        ).decode().strip()
        return version
    except Exception:
        try:
            # Fallback to commit hash if no tags
            commit = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'],
                cwd=os.path.dirname(__file__) or '.'
            ).decode().strip()
            return f"commit-{commit}"
        except Exception:
            return "unknown"


def get_commits_number():
    """Get commits number from git history"""
    try:
        count = subprocess.check_output(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=os.path.dirname(__file__) or '.'
        ).decode().strip()
        return int(count)
    except Exception:
        return 0


def _github_headers():
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_API_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def _parse_commit_count(link_header, default_count):
    if not link_header:
        return default_count

    match = re.search(r"page=(\d+)>;\s*rel=\"last\"", link_header)
    if match:
        return int(match.group(1))

    return default_count


def get_repo_version_and_commits():
    now = time.time()
    if now - _repo_cache["ts"] < 300:
        return _repo_cache["version"], _repo_cache["commits"]

    headers = _github_headers()

    try:
        commit_resp = requests.get(
            f"{GITHUB_API_URL}/commits/{GITHUB_BRANCH}",
            headers=headers,
            timeout=2.5,
        )
        commit_resp.raise_for_status()
        commit_data = commit_resp.json()
        short_sha = commit_data.get("sha", "")[:7]
        version = f"commit-{short_sha}" if short_sha else "unknown"

        commits_resp = requests.get(
            f"{GITHUB_API_URL}/commits?sha={GITHUB_BRANCH}&per_page=1",
            headers=headers,
            timeout=2.5,
        )
        commits_resp.raise_for_status()
        default_count = len(commits_resp.json())
        commits = _parse_commit_count(commits_resp.headers.get("Link"), default_count)

        _repo_cache.update({
            "ts": now,
            "version": version,
            "commits": commits,
        })
        return version, commits
    except Exception:
        return get_git_version(), get_commits_number()


def is_aws_environment():
    """Detect if running on AWS (EC2, ECS, or EKS)"""
    aws_env_vars = (
        'AWS_REGION',
        'AWS_DEFAULT_REGION',
        'AWS_EXECUTION_ENV',
        'AWS_LAMBDA_FUNCTION_NAME',
        'AWS_ROLE_ARN',
        'AWS_WEB_IDENTITY_TOKEN_FILE',
        'ECS_CONTAINER_METADATA_URI_V4',
        'EKS_CLUSTER_NAME',
    )
    # Check for AWS/EKS environment variables
    if any(os.getenv(name) for name in aws_env_vars):
        return True

    # Check for AWS EC2 metadata endpoint
    try:
        response = requests.get(
            'http://169.254.169.254/latest/meta-data/',
            timeout=0.5
        )
        return response.status_code == 200
    except Exception:
        return False


def get_health_status():
    """Get health status from /health endpoint"""
    try:
        # Try to call the health endpoint locally
        response = requests.get('http://localhost/health', timeout=1)
        if response.status_code == 200:
            return "healthy"
    except Exception:
        pass
    return "unknown"


def get_deployment_info():
    """Get dynamic deployment information"""
    environment_override = (os.getenv("DEPLOYMENT_ENV") or "").strip().lower()
    if environment_override:
        environment = environment_override
    else:
        environment = "aws" if is_aws_environment() else "local"
    
    # Get current date/time for last_deploy
    last_deploy = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Get formatted uptime
    uptime_seconds = get_uptime()
    uptime_formatted = format_uptime(uptime_seconds)

    version, commits = get_repo_version_and_commits()

    return {
        "version": version,
        "commits": commits,
        "environment": environment,
        "status": "healthy",
        "last_deploy": last_deploy,
        "uptime": uptime_formatted,
    }


app = Flask(__name__)

metrics = PrometheusMetrics(app)

PROFILE = {
    "name": "Daniel Cohen",
    "role": "DevSecOps / Cloud Engineer",
    "tagline": (
        "Building secure DevSecOps workflows, automated cloud deployments, "
        "and production-ready delivery pipelines on AWS."
    ),
    "github": "https://github.com/KoKaTiM1",
    "linkedin": "https://www.linkedin.com/",
    "email": "you@example.com",
}

# Profiles for individual pages
PROFILES = {
    "yourname": {
        "name": "Daniel Cohen",
        "role": "DevSecOps / Cloud Engineer",
        "bio": (
            "DevSecOps and cloud engineer focused on AWS infrastructure, "
            "containerized applications, CI/CD automation, monitoring, "
            "and secure deployment workflows."
        ),
        "tagline": (
            "Focused on secure AWS deployments, automation, Docker, "
            "Terraform, and CI/CD workflows."
        ),
        "photo": "profile_picture/mine.webp",
        "github": "https://github.com/KoKaTiM1",
    },
    "coworker": {
        "name": "Yossef Cohen",
        "role": "DevSecOps / Cloud Engineer",
        "bio": (
            "DevSecOps and cloud engineer contributing to cloud automation, "
            "deployment reliability, infrastructure workflows, and secure "
            "application delivery."
        ),
        "tagline": (
            "Contributing to cloud automation, deployment reliability, "
            "and secure infrastructure workflows."
        ),
        "photo": "profile_picture/coworker.webp",
        "github": "https://github.com/yossef-cohen?tab=repositories",
    }
}

PROJECT_REPOSITORY_URL = "https://github.com/KoKaTiM1/DevSecOps_Project"

PROJECTS = [
    {
        "title": "DevOps Portfolio Site",
        "description": (
            "A Flask-based portfolio application that presents team profiles, "
            "project information, deployment metadata, health checks, and "
            "runtime status in a clean web interface."
        ),
        "stack": ["Flask", "Python", "HTML", "CSS"],
        "repo_url": PROJECT_REPOSITORY_URL,
    },
    {
        "title": "Infrastructure Automation",
        "description": (
            "Terraform-based AWS infrastructure automation designed to make "
            "cloud provisioning repeatable, consistent, and easier to maintain "
            "across environments."
        ),
        "stack": ["Terraform", "AWS", "Cloud Infrastructure"],
        "repo_url": PROJECT_REPOSITORY_URL,
    },
    {
        "title": "CI/CD Pipeline",
        "description": (
            "GitHub Actions and Docker workflow for validating, building, and "
            "deploying the application through an automated delivery process."
        ),
        "stack": ["GitHub Actions", "Docker", "Bash"],
        "repo_url": PROJECT_REPOSITORY_URL,
    },
]


# Skills displayed in the About section.
SKILLS = [
    "Python",
    "Flask",
    "Docker",
    "Terraform",
    "AWS",
    "Linux",
    "GitHub Actions",
    "CI/CD",
    "Monitoring",
    "DevSecOps",
]

HOMEPAGE_PROFILE_IMAGE_CLASS = "profile-img-large homepage-profile-img"



@app.route('/')
def homepage():
    return render_template(
        'index.html',
        profile=PROFILE,
        profiles=PROFILES,
        projects=PROJECTS,
        deployment=get_deployment_info(),
        skills=SKILLS,
        homepage_profile_image_class=HOMEPAGE_PROFILE_IMAGE_CLASS,
    )


# Route for individual profiles
@app.route('/profile/<name>')
def profile(name):
    info = PROFILES.get(name)
    if not info:
        return render_template('profile.html', info={"name": "Not Found", "role": "", "bio": "Profile not found."}, photo=None)
    return render_template('profile.html', info=info, photo=info["photo"])


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/api/status')
def api_status():
    return jsonify(get_deployment_info()), 200


@app.route('/api/projects')
def api_projects():
    return jsonify({"projects": PROJECTS}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

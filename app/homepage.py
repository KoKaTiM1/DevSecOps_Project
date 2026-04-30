from flask import Flask, jsonify, render_template



app = Flask(__name__)


PROFILE = {
    "name": "Your Name",
    "role": "DevOps / Cloud Engineer",
    "tagline": (
        "Building secure, automated delivery pipelines "
        "on AWS with Python and Docker."
    ),
    "github": "https://github.com/KoKaTiM1",
    "linkedin": "https://www.linkedin.com/",
    "email": "you@example.com",
}

# Profiles for individual pages
PROFILES = {
    "yourname": {
        "name": "Your Name",
        "role": "DevOps / Cloud Engineer",
        "bio": "Full information about you goes here. Add your details, experience, and contact info.",
        "photo": "profile_picture/mine.webp"
    },
    "coworker": {
        "name": "Coworker Name",
        "role": "DevOps Engineer",
        "bio": "Full information about your coworker goes here. Add their details, experience, and contact info.",
        "photo": "profile_picture/coworker.webp"
    }
}

PROJECTS = [
    {
        "title": "DevOps Portfolio Site",
        "description": (
            "Flask portfolio app with deployment metadata "
            "and health checks."
        ),
        "stack": ["Flask", "Python", "HTML", "CSS"],
        "repo_url": "https://github.com/KoKaTiM1/DevSecOps21",
        "demo": "Planned",
    },
    {
        "title": "Infrastructure Automation",
        "description": (
            "Provision AWS infrastructure with Terraform "
            "for repeatable deployments."
        ),
        "stack": ["Terraform", "AWS", "EC2"],
        "repo_url": "https://github.com/KoKaTiM1",
        "demo": "Planned",
    },
    {
        "title": "CI/CD Pipeline",
        "description": (
            "GitHub Actions workflow to validate "
            "and deploy containerized apps."
        ),
        "stack": ["GitHub Actions", "Docker", "Bash"],
        "repo_url": "https://github.com/KoKaTiM1",
        "demo": "Planned",
    },
]

DEPLOYMENT_INFO = {
    "version": "v0.1.0-local",
    "last_deploy": "Not deployed yet",
    "environment": "local",
    "status": "healthy",
}

# Change this to a photos for each skill.
SKILLS = [  
    "Python",
    "Flask",
    "Docker",
    "Terraform",
    "AWS",
    "Linux",
    "GitHub Actions",
]



@app.route('/')
def homepage():
    return render_template(
        'index.html',
        profile=PROFILE,
        projects=PROJECTS,
        deployment=DEPLOYMENT_INFO,
        skills=SKILLS,
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
    return jsonify({"status": "ok"}), 200


@app.route('/api/status')
def api_status():
    return jsonify(DEPLOYMENT_INFO), 200


@app.route('/api/projects')
def api_projects():
    return jsonify({"projects": PROJECTS}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

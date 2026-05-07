# Option A Roadmap

**Portfolio + Project Showcase + Deployment Info**

## Flow

**Phase 1 → Phase 2 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8**

---

## Phase 1 — Build the website locally

**Goal:** app works on your own machine.

### Build:
- Flask routes
- templates
- CSS
- project cards
- about section
- deployment info section with placeholder values

### Suggested routes:
- `/`
- `/health`

### Optional:
- `/api/status`
- `/api/projects`

### Focus on:
- layout
- clean design
- mobile-friendly enough
- simple content

### Deliverable:
You can run the app locally and open it in browser.

---

## Phase 2 — Add Docker

**Goal:** the same app runs inside a container.

### You should define:
- how the container starts
- exposed port
- production run command

### Test:
- build image
- run container
- open site in browser
- check `/health`

### Deliverable:
App runs locally with Docker.

---

## Phase 4 — Automate infrastructure with Terraform

**Goal:** stop creating infra manually.

### Terraform should create at minimum:
- provider config
- EC2 instance
- security group
- outputs for public IP

### Nice to have:
- Elastic IP
- user_data for installing Docker automatically

### Deliverable:
One command sequence creates your EC2 environment.

---

## Phase 5 — Deploy the app manually once to EC2

**Goal:** verify the full runtime before CI/CD.

### Process:
- connect to EC2
- copy project or image
- run the container
- confirm the site opens publicly
- test `/health`

### Deliverable:
Your site is live on AWS, even without automation.

---

## Phase 6 — Add GitHub Actions CI/CD

**Goal:** deploy automatically after push.

### CI step:
- install dependencies
- run app startup check
- maybe run one or two small tests

### CD step:
- connect to server
- pull or upload latest version
- rebuild / restart container

### Keep the first pipeline simple:
- trigger on push to `main`

### Deliverable:
Push to GitHub → app updates on EC2.

---

## Phase 7 — Add real deployment info to the website

**Goal:** make Option A unique.

### Show real values like:
- app version from environment variable
- last deployment time from CI
- environment name like `production`
- health status from backend

### Simplest method:
- GitHub Actions writes values into environment variables or a small JSON/status file during deployment
- Flask reads and displays them

### Deliverable:
The site visibly shows deployment metadata.

---

## Phase 8 — Improve security and cleanup

**Goal:** make the project presentation-ready.

### Add the basics:
- restrict security group ports
- avoid hardcoding secrets
- use GitHub Secrets
- use least privilege AWS credentials where possible
- keep `.env` and secrets out of Git
- document deployment process clearly

### Also clean:
- README
- project structure
- screenshots
- architecture diagram

### Deliverable:
Project is safe enough and presentable.

---

## Suggested project structure

```text
repo/
  app/
    templates/
    static/
    app.py
    data.json
  terraform/
    main.tf
    variables.tf
    outputs.tf
  scripts/
    deploy.sh
    install_docker.sh
  .github/workflows/
    deploy.yml
  Dockerfile
  requirements.txt
  README.md
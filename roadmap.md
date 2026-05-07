# Option A Roadmap

**Portfolio + Project Showcase + Deployment Info**

## Flow

**Phase 1 → Phase 2 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9 → Phase 10 → Phase 11 → Phase 12 → Phase 13**

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

## Phase 8 — Add pre-deployment tests (code check)

**Goal:** validate code quality and functionality before deployment.

### Add to GitHub Actions:
- Python linting (pylint, flake8)
- Unit tests for Flask routes
- Security scanning (bandit for Python)
- Dependency check (safety)

### Test types:
- Syntax validation
- Code style checks
- Unit tests for critical functions
- Docker build test

### Deliverable:
GitHub Actions runs tests on every push; deployment only proceeds if tests pass.

---

## Phase 9 — Add post-deployment tests (health check)

**Goal:** verify the app works correctly after deployment.

### Health checks:
- HTTP 200 on `/health` endpoint
- Check `/` homepage loads
- Verify deployment info displays correctly
- Test profile pages load

### Automation:
- GitHub Actions waits for deployment
- Runs smoke tests against live URL
- Rolls back if tests fail (optional)

### Deliverable:
Deployment includes automated verification that the app is working.

---

## Phase 10 — Add HTTPS/TLS

**Goal:** secure traffic with SSL certificates.

### Setup:
- Get SSL certificate (Let's Encrypt free)
- Configure in load balancer or reverse proxy (nginx)
- Redirect HTTP → HTTPS
- Update security group to allow 443

### For EKS:
- AWS Certificate Manager (ACM) free certificates
- ALB Ingress controller handles TLS
- Automatic cert renewal

### Deliverable:
Site accessible via HTTPS with valid certificate.

---

## Phase 11 — Migrate from EC2 to EKS

**Goal:** move from single EC2 to managed Kubernetes cluster.

### Setup EKS with Terraform:
- EKS cluster
- Node groups (auto-scaling)
- IAM roles and service accounts
- VPC and networking

### Kubernetes manifests:
- Deployment (3+ replicas)
- Service (LoadBalancer)
- Ingress (for HTTPS routing)
- ConfigMaps for environment variables

### Migrate deployment:
- Update GitHub Actions to deploy via kubectl
- Pull image from Docker Hub
- Rolling updates (zero downtime)

### Deliverable:
App running on EKS cluster with automatic scaling and health checks.

---

## Phase 12 — Add monitoring with Prometheus

**Goal:** observe application and infrastructure metrics.

### Prometheus setup:
- Deploy Prometheus to EKS
- Scrape metrics from Flask app
- Store time-series data

### Add to Flask app:
- `/metrics` endpoint (Prometheus client library)
- Custom metrics: request count, response time, errors
- Export to Prometheus

### Visualization (optional):
- Deploy Grafana dashboard
- Create alerts for high error rates, latency

### Deliverable:
Real-time metrics visible in Prometheus; historical data stored; alerts configured.

---

## Phase 13 — Improve security and cleanup

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
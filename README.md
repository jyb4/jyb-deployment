# jyb-deployment
JYB Deployment Project
A static website deployed with Docker and automated using GitHub Actions. The project has separate QA and production environments on a DigitalOcean Ubuntu Droplet, with HTTPS provided by Caddy.
Live sites
- QA: https://qa.jybdeployment.com
- Production: https://jybdeployment.com
Repository and image registry
- Source repository: https://github.com/jyb4/jyb-deployment
- QA workflow (deploy.yml): https://github.com/jyb4/jyb-deployment/actions/workflows/deploy.yml
- Production promotion workflow (promote-production.yml): https://github.com/jyb4/jyb-deployment/actions/workflows/promote-production.yml
- GitHub Container Registry package: https://github.com/jyb4/jyb-deployment/pkgs/container/jyb-deployment
Architecture
- The website is a static HTML page served by Nginx in a Docker container.
- GitHub Actions runs the website tests, builds a Docker image, and publishes the image to GitHub Container Registry (GHCR).
- The QA container is published on the host at 127.0.0.1:8081 and served publicly through Caddy at https://qa.jybdeployment.com.
- The production container is published on the host at 127.0.0.1:8080 and served publicly through Caddy at https://jybdeployment.com.
- Caddy handles HTTPS and reverse-proxies each hostname to its corresponding local container port.
CI/CD workflow
QA deployment
A push to main triggers the deploy.yml workflow. Pull requests targeting main run the test job, while the image build and QA deployment run for pushes to main.
The workflow:
1. Checks out the repository and sets up Python.
2. Runs python -m unittest -v test_site.py.
3. Builds the Docker image and publishes it to GHCR, tagged with the full Git commit SHA.
4. Connects to the Droplet over SSH as the non-root deploy user and updates the QA container to the image for that commit.
5. Checks that the QA website responds successfully.
Production promotion
Production is promoted manually using the promote-production.yml workflow. The operator supplies the exact 40-character commit SHA for an image that has passed QA. The workflow pulls that image from GHCR, replaces the production container, and verifies the deployment.
Deployment image tag used for the captured promotion: 83cfee2ee64773fee9c416a930f80a31addbab4e
This is the commit SHA shown in the provided GHCR package screenshot and used in the production promotion flow. Confirm the QA workflow run corresponds to this same commit before submitting if your instructor expects a direct QA-to-production trace.
Evidence screenshots
The screenshots below are included in [`evidence/`](evidence/).
Screenshot	What it demonstrates
[qa-workflow.png](evidence/qa-workflow.png)	GitHub Actions QA pipeline showing successful test, build/publish, and QA deployment jobs.
[qa-site.png](evidence/qa-site.png)	QA site responding over HTTPS.
[production-promotion.png](evidence/production-promotion.png)	Successful manual production-promotion workflow.
[production-site.png](evidence/production-site.png)	Production site responding over HTTPS.
[docker-image.png](evidence/docker-image.png)	GHCR package and recent image tags, including the captured commit SHA.
[ssh-login.png](evidence/ssh-login.png)	Terminal showing whoami returns deploy, demonstrating a non-root login.
[ssh-settings.png](evidence/ssh-settings.png)	Effective SSH configuration showing root login and password-based authentication disabled.


SSH hardening evidence
The captured effective SSH settings show:
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
kbdinteractiveauthentication no
The server is accessed using the deploy account and SSH key authentication. Private keys, passwords, and GitHub secrets must not be committed or included in screenshots.
Still needed if required by the assignment: capture a separate screenshot showing that attempted root login and password-based SSH login are rejected. The provided screenshots do not include that rejection demonstration yet.
Notes
- Images are tagged with the Git commit SHA so a specific tested build can be promoted.
- Production promotion should use only the exact SHA that passed QA.
- The website screenshots currently display Version: v1. If the assignment specifically requires demonstrating a visible change appearing in QA first and then production, make a small visible change (for example, update the version text), wait for QA to deploy, capture QA, and then promote that same commit to production and capture production again.

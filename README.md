
# JYB Deployment Project

A static website deployed with Docker and automated using GitHub Actions. The project has separate QA and production environments on a DigitalOcean Ubuntu Droplet, with HTTPS provided by Caddy.

## Live Sites

- **QA:** https://qa.jybdeployment.com
- **Production:** https://jybdeployment.com

## Repository and Image Registry

- **Source repository:** https://github.com/jyb4/jyb-deployment
- **QA workflow (`deploy.yml`):** https://github.com/jyb4/jyb-deployment/actions/workflows/deploy.yml
- **Production promotion workflow (`promote-production.yml`):** https://github.com/jyb4/jyb-deployment/actions/workflows/promote-production.yml
- **GitHub Container Registry package:** https://github.com/jyb4/jyb-deployment/pkgs/container/jyb-deployment

## Architecture

- The website is a static HTML page served by Nginx in a Docker container.
- GitHub Actions runs the website tests, builds a Docker image, and publishes the image to GitHub Container Registry (GHCR).
- The QA container is published on the host at `127.0.0.1:8081` and served publicly through Caddy at `https://qa.jybdeployment.com`.
- The production container is published on the host at `127.0.0.1:8080` and served publicly through Caddy at `https://jybdeployment.com`.
- Caddy handles HTTPS and reverse-proxies each hostname to its corresponding local container port.

## CI/CD Workflow

### QA Deployment

A push to `main` triggers the `deploy.yml` workflow. Pull requests targeting `main` run the test job, while the image build and QA deployment run for pushes to `main`.

The workflow:

1. Checks out the repository and sets up Python.
2. Runs `python -m unittest -v test_site.py`.
3. Builds the Docker image and publishes it to GHCR, tagged with the full Git commit SHA.
4. Connects to the Droplet over SSH as the non-root `deploy` user and updates the QA container to the image for that commit.
5. Checks that the QA website responds successfully.

### Production Promotion

Production is promoted manually using the `promote-production.yml` workflow. The operator supplies the exact 40-character commit SHA for an image that has passed QA. The workflow pulls that image from GHCR, replaces the production container, and verifies the deployment.

**Commit promoted for the v2 update:**

`192d25f3317c94a6030fbb502c1154f1d17a0e92`

- [View the commit](https://github.com/jyb4/jyb-deployment/commit/192d25f3317c94a6030fbb502c1154f1d17a0e92)

The QA version should be verified before promoting the same commit to production.

## Evidence Screenshots

The screenshots are stored in the [`evidence/`](evidence/) folder.

| Screenshot | What it demonstrates |
|---|---|
| [qa-workflow.png](evidence/qa-workflow.png) | Successful GitHub Actions QA pipeline and deployment. |
| [qa-site.png](evidence/qa-site.png) | QA website displaying Version v2 over HTTPS. |
| [production.png](evidence/production.png) | Successful manual production-promotion workflow. |
| [production-site.png](evidence/production-site.png) | Production website displaying Version v2 over HTTPS. |
| [docker-image.png](evidence/docker-image.png) | GHCR package and published image tag. |
| [ssh-login.png](evidence/ssh-login.png) | Successful SSH login using the non-root `deploy` account. |
| [ssh-settings.png](evidence/ssh-settings.png) | Effective SSH settings showing root login and password authentication disabled. |
| [ssh-rejection.png](evidence/ssh-rejection.png) | Evidence that an attempted root SSH login is rejected. |

## SSH Security

The effective SSH server settings should show:

```text
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
kbdinteractiveauthentication no
```

The server is accessed using the `deploy` account and SSH key authentication.

The SSH rejection screenshot should show the failed root-login attempt. Do not include private keys, passwords, access tokens, or other secrets in screenshots or repository files.

## Deployment Verification

- Confirm the QA workflow succeeds for the commit being released.
- Verify that the QA website displays the expected version.
- Promote the exact same commit SHA to production.
- Confirm the production workflow succeeds.
- Verify that the production website displays the same version.
- Keep the screenshots in `evidence/` consistent with the deployment being documented.

## Notes

- Docker images are tagged with their Git commit SHA so a specific tested build can be promoted.
- Production promotion should use only the exact SHA that passed QA.
- Screenshots should reflect the current deployment and effective server settings.
- The `ssh-rejection.png` file must exist in `evidence/` for its image to display in this README.

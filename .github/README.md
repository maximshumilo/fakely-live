# GitHub Actions CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and continuous deployment (CI/CD) of the Fakely Live application.

## Workflows

### API Build (`api-build.yml`)

This workflow builds and publishes the API Docker image when changes are made to the `api/` directory.

- **Trigger**: Push to `main` branch with changes in `api/` directory
- **Image**: `shumilomaks/fakely-live-api`
- **Tags**: `latest`, `1.0.0`, and short SHA of the commit

### UI Build (`ui-build.yml`)

This workflow builds and publishes the UI Docker image when changes are made to the `ui/` directory.

- **Trigger**: Push to `main` branch with changes in `ui/` directory
- **Image**: `shumilomaks/fakely-live-ui`
- **Tags**: `latest`, `1.0.0`, and short SHA of the commit

### Frames Handler Build (`frames-handler-build.yml`)

This workflow builds and publishes the Frames Handler Docker image when changes are made to the `frames-handler/` directory.

- **Trigger**: Push to `main` branch with changes in `frames-handler/` directory
- **Image**: `shumilomaks/fakely-live-frames-handler`
- **Tags**: `latest`, `1.0.0`, and short SHA of the commit

## Required Secrets

The workflows require the following secrets to be set in the GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token (not your password)

## How to Set Up Secrets

1. Go to your GitHub repository
2. Click on "Settings"
3. Click on "Secrets and variables" > "Actions"
4. Click on "New repository secret"
5. Add the required secrets
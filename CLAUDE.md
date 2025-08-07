# Project Memory and Guidelines

## Code and Commit Guidelines

### IMPORTANT: No Claude References
- **NEVER** include Claude references in source code, comments, commit messages, or documentation
- **NEVER** add "Generated with Claude Code" or similar attribution
- **NEVER** add "Co-Authored-By: Claude" in commits
- Keep all contributions appearing as natural developer work

## Project Structure and Approach

### Development Environment
- Always use virtual environment: `source .venv/bin/activate`
- Package manager: `uv` (preferred over pip)
- Configuration: `pyproject.toml` (not requirements.txt)
- Python versions: 3.8-3.12 supported

### Code Quality
- Linting: `ruff check .` and `ruff format .`
- Testing: `pytest --cov=. --cov-report=term-missing --cov-fail-under=85`
- Coverage requirement: 85% minimum

### Git Workflow
- Main branch: `main` (for releases)
- Development branch: `develop` (for ongoing work)
- Use conventional commits (feat:, fix:, docs:, etc.)
- Never work directly in main branch

### GitHub Actions
- Comprehensive CI/CD pipeline with 9 workflows
- Key workflows: CI/CD Pipeline, Semantic Release, Docker Build, SBOM Generation
- All workflows are active and properly configured
- Recent issues: linting failures (now resolved)

### Repository Information
- Owner: dkdndes
- Repository: pybiorythm
- Python biorhythm calculation library
- Uses semantic versioning with semantic-release
- Docker support with multi-stage builds
- Comprehensive security scanning and SBOM generation

### Local Testing Setup
- `act` installed and configured for local GitHub Actions testing
- `.actrc` configured for M1 Mac compatibility
- `.secrets` populated with GitHub token from gh CLI
- `local-test.sh` script provides multiple testing modes:
  - `quick`: Fast local testing without Docker (~30s)
  - `job <name> <file>`: Test specific workflow jobs with act
  - `list`: Show available workflows and jobs
  - `validate`: Check workflow syntax
- `update-secrets.sh` automatically updates tokens from environment
- Files added to .gitignore to prevent secret commits

### CI/CD Status
- All 9 workflows operational
- Recent linting issues resolved
- Code quality: 90%+ coverage, all ruff checks pass
- Ready for production deployments

### Docker & M2 Mac Setup
- **Docker Desktop**: Configured for ARM64 native builds
- **Multi-architecture support**: Builds for both ARM64 (local) and AMD64 (production)
- **Kubernetes integration**: Docker Desktop K8s enabled for local testing
- **Build script**: `docker-build-m2.sh` with multiple deployment modes
- **Compose file**: `docker-compose.local.yml` optimized for M2 Mac
- **K8s deployment**: `k8s-deployment.yaml` with ARM64 node affinity
- **Performance**: Native ARM64 containers for optimal speed
- **Security**: Non-root user, resource limits, health checks
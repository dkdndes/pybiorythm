# GitHub Actions Workflows Documentation

This repository uses comprehensive GitHub Actions workflows for CI/CD, security, and automation.

## Workflows Overview

### 1. CI/CD Pipeline (`ci.yml`)
**Triggers:** Push to main/develop, PRs to main, releases
**Purpose:** Comprehensive testing and quality assurance

**Jobs:**
- **Test Suite** - Multi-version Python testing (3.8-3.12)
  - Code linting with Ruff
  - Test execution with pytest
  - Coverage reporting (90%+ required)
  - Codecov integration
  
- **Security Scan** - Security vulnerability detection
  - Dependency vulnerability scanning with Safety
  - Static security analysis with Bandit
  - Security report artifacts
  
- **Docker Build & Test** - Container validation
  - Multi-stage Docker build
  - Container functionality testing
  - Security validation (non-root execution)
  - Image size analysis
  
- **Package Build** - Python package validation
  - Wheel and source distribution building
  - Package validation with Twine
  - Artifact preservation
  
- **Documentation** - Documentation integrity
  - Markdown link validation
  - Docker documentation verification
  
- **Integration Tests** - End-to-end testing
  - CLI interface testing
  - JSON output validation
  - Cross-component integration
  
- **Performance Benchmarks** - Performance regression detection
  - Calculation speed benchmarking
  - Performance threshold validation

### 2. Docker Publish (`docker-publish.yml`)
**Triggers:** Push to main, tags, PRs
**Purpose:** Container image building and publishing

**Features:**
- Multi-architecture builds (AMD64, ARM64)
- GitHub Container Registry publishing
- Vulnerability scanning with Trivy
- Security analysis integration
- Image testing and validation
- Docker Hub description updates

### 3. Release Management (`release.yml`)
**Triggers:** Version tags (v*)
**Purpose:** Automated release process

**Jobs:**
- **GitHub Release** - Release creation and asset publishing
  - Automated changelog generation
  - Binary artifact attachment
  - Release notes formatting
  
- **PyPI Publishing** - Package distribution
  - TestPyPI validation
  - Production PyPI publishing
  - Installation verification
  
- **Documentation Updates** - Post-release documentation
  - Version badge updates
  - Installation instruction updates
  
- **Release Validation** - End-to-end validation
  - PyPI installation testing
  - Docker image validation
  - Functionality verification

### 4. Security Analysis (`codeql.yml`)
**Triggers:** Push, PRs, weekly schedule
**Purpose:** Static code analysis and security scanning

**Features:**
- CodeQL security analysis
- Extended security queries
- Quality analysis integration
- Weekly automated scans
- Security findings reporting

### 5. Dependency Review (`dependency-review.yml`)
**Triggers:** Pull requests
**Purpose:** Dependency security and licensing

**Features:**
- High-severity vulnerability blocking
- License compliance checking
- PR summary comments
- Automated dependency analysis

### 6. SBOM Generation (`sbom.yml`)
**Triggers:** Push to main, tags, PRs, weekly schedule
**Purpose:** Software Bill of Materials generation and supply chain security

**Jobs:**
- **Python SBOM** - Python dependency tracking
  - CycloneDX format SBOM generation
  - Dependency metadata enhancement
  - Component validation
  
- **Docker SBOM** - Container component tracking
  - Syft-based container analysis
  - Multi-layer component detection
  - Container-specific metadata
  
- **Combined SBOM** - Unified supply chain view
  - Python and Docker SBOM merging
  - Attestation generation
  - Release artifact publishing

**Features:**
- CycloneDX and SPDX format support
- Automated component discovery
- Supply chain transparency
- Vulnerability database compatibility
- Container attestation support

## Automation Features

### Dependabot Configuration
**File:** `.github/dependabot.yml`
**Purpose:** Automated dependency updates

**Update Schedules:**
- **Python dependencies:** Weekly (Mondays, 6:00 AM)
- **GitHub Actions:** Weekly (Mondays, 6:00 AM)
- **Docker base images:** Weekly (Mondays, 6:00 AM)

**Features:**
- Automated PR creation
- Reviewer assignment
- Semantic commit messages
- Appropriate labeling

### Issue Templates
**Location:** `.github/ISSUE_TEMPLATE/`

**Templates:**
- **Bug Report** - Structured bug reporting with environment details
- **Feature Request** - Feature proposal with use case analysis

### Pull Request Template
**File:** `.github/pull_request_template.md`
**Purpose:** Standardized PR structure and checklists

**Sections:**
- Change description and categorization
- Testing and quality assurance checklists
- Security and documentation verification
- Scientific disclaimer acknowledgment

## Security Features

### Vulnerability Scanning
- **Dependencies:** Safety and Dependabot
- **Code:** Bandit static analysis
- **Containers:** Trivy vulnerability scanner
- **GitHub:** CodeQL security analysis

### Security Policies
- High-severity vulnerability blocking
- License compliance enforcement
- Container security validation
- Non-root execution verification

### Automated Security Updates
- Weekly dependency scanning
- Automated security patch PRs
- Continuous monitoring
- Security findings integration

## Quality Gates

### Code Quality Requirements
- ✅ All tests must pass (72+ tests)
- ✅ Coverage must be ≥90%
- ✅ Ruff linting must pass
- ✅ Security scans must pass
- ✅ Docker builds must succeed

### Performance Requirements
- Calculation performance benchmarks
- Docker image size monitoring
- Build time optimization
- Resource usage validation

### Documentation Requirements
- README link validation
- Docker documentation verification
- Code documentation standards
- Scientific disclaimer maintenance

## Secrets Configuration

Required repository secrets for full functionality:

```bash
# PyPI Publishing
PYPI_API_TOKEN           # Production PyPI token
TEST_PYPI_API_TOKEN      # TestPyPI token

# Docker Hub (optional)
DOCKERHUB_USERNAME       # Docker Hub username
DOCKERHUB_TOKEN         # Docker Hub token

# Codecov (optional)
CODECOV_TOKEN           # Coverage reporting token
```

## Branch Protection

Recommended branch protection rules for `main`:

- Require PR reviews (1+ reviewers)
- Require status checks to pass
- Required status checks:
  - `Test Suite`
  - `Security Scan`
  - `Docker Build & Test`
  - `Package Build`
- Require branches to be up to date
- Restrict pushes to main branch

## Workflow Monitoring

### Success Indicators
- 🟢 All CI checks passing
- 🟢 90%+ test coverage maintained
- 🟢 No high-severity vulnerabilities
- 🟢 Docker images building successfully
- 🟢 Performance benchmarks within thresholds

### Failure Response
- Check workflow logs for specific failures
- Review security scan results
- Validate test coverage reports
- Verify Docker build and security compliance
- Address dependency vulnerabilities promptly

## Local Development

### Pre-commit Validation
Run locally before pushing:

```bash
# Run all quality checks
pytest --cov=. --cov-fail-under=90
ruff check .
ruff format --check .

# Test Docker build
docker build --target production -t pybiorythm:test .
docker run --rm pybiorythm:test python -c "import biorythm; print('OK')"

# Security scan
safety check
bandit -r . -f json
```

### Workflow Testing
Test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act push

# Run specific job
act -j test
```

## Maintenance

### Regular Tasks
- Review weekly Dependabot PRs
- Monitor security scan results
- Update workflow versions quarterly
- Review and update branch protection rules
- Validate automation effectiveness

### Workflow Updates
- Keep action versions current
- Monitor GitHub Actions marketplace
- Review and update security policies
- Optimize build performance
- Maintain documentation accuracy

This comprehensive workflow setup ensures high code quality, security, and automation while maintaining the project's educational and entertainment purpose.
# Local GitHub Actions Testing with act

This guide explains how to test GitHub Actions workflows locally using `act` before pushing changes to GitHub.

## What is act?

[act](https://github.com/nektos/act) allows you to run GitHub Actions locally in Docker containers, enabling you to:

- ✅ Test workflows before pushing to GitHub
- ✅ Debug workflow issues faster
- ✅ Validate workflow syntax and logic
- ✅ Save GitHub Actions minutes
- ✅ Work offline during development

## Installation

### macOS (Homebrew)
```bash
brew install act
```

### Linux
```bash
# Download latest release
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows
```bash
# Using Chocolatey
choco install act-cli

# Or using Scoop
scoop install act
```

### Docker Alternative
```bash
# Run act in Docker (if you don't want to install locally)
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/github/workspace \
  nektos/act:latest
```

## Basic Usage

### List Available Workflows

```bash
# Show all workflows and jobs
act --list

# Show jobs for specific event
act push --list
act pull_request --list
```

**Example Output:**
```
Stage  Job ID                 Job name                                        Workflow name          
0      test                   Test Suite                                      CI/CD Pipeline         
0      security               Security Scan                                   CI/CD Pipeline         
0      commit-lint            Conventional Commits                            Commit Lint            
1      docker                 Docker Build & Test                             CI/CD Pipeline         
1      build                  Build Package                                   CI/CD Pipeline         
```

### Dry Run (Validate Without Execution)

```bash
# Validate all workflows
act -n

# Validate specific workflow
act -W .github/workflows/ci.yml -n

# Validate specific job
act -W .github/workflows/ci.yml -j test -n
```

### Run Workflows

```bash
# Run default event (usually push)
act

# Run specific event
act push
act pull_request

# Run specific workflow file
act -W .github/workflows/ci.yml

# Run specific job
act -W .github/workflows/ci.yml -j test
```

## PyBiorythm Workflow Testing

### 1. Test Commit Lint Workflow

```bash
# Dry run first
act -W .github/workflows/commit-lint.yml -n

# Run the workflow
act -W .github/workflows/commit-lint.yml

# Expected: Validates your commit messages follow conventional format
```

### 2. Test CI/CD Pipeline

```bash
# Test the main CI pipeline
act -W .github/workflows/ci.yml

# Test specific jobs
act -W .github/workflows/ci.yml -j test        # Run test suite
act -W .github/workflows/ci.yml -j security    # Run security scans
act -W .github/workflows/ci.yml -j docker      # Test Docker build
```

### 3. Test Documentation Workflow

```bash
# Test documentation build
act -W .github/workflows/docs.yml

# This will build the MkDocs site locally
```

### 4. Test Semantic Release (Limited)

```bash
# Test semantic release workflow structure
act -W .github/workflows/semantic-release.yml -n

# Note: Full semantic release requires GitHub API access
# Local testing focuses on validation and basic steps
```

## Configuration Options

### Platform Images

Use smaller, faster images for testing:

```bash
# Use smaller Ubuntu image
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Use Node.js image for faster Node.js workflows
act -P ubuntu-latest=node:16-slim -W .github/workflows/commit-lint.yml

# Multi-architecture support (important for M2 Macs)
act --container-architecture linux/amd64
```

### Secrets and Environment Variables

Create local configuration files:

```bash
# Create .secrets file (don't commit this!)
echo "GITHUB_TOKEN=your_test_token_here" > .secrets
echo "DOCKER_USERNAME=your_docker_username" >> .secrets

# Create .env file for environment variables
echo "NODE_VERSION=18" > .env
echo "PYTHON_VERSION=3.12" >> .env

# Use in act commands
act -W .github/workflows/ci.yml --secret-file .secrets --env-file .env
```

### Advanced Configuration

```bash
# Bind current directory (faster than copying)
act --bind

# Use specific Docker network
act --network host

# Increase verbosity for debugging
act -v

# Use artifact server for job artifacts
act --artifact-server-path ./artifacts
```

## Workflow-Specific Testing

### CI/CD Pipeline (`ci.yml`)

```bash
# Test full pipeline (may take 10-15 minutes)
act push -W .github/workflows/ci.yml

# Test individual stages
act push -W .github/workflows/ci.yml -j test
act push -W .github/workflows/ci.yml -j security  
act push -W .github/workflows/ci.yml -j docker
act push -W .github/workflows/ci.yml -j build
```

**What gets tested locally:**
- ✅ Python test suite execution
- ✅ Code linting and formatting
- ✅ Security scans (Bandit, Safety)
- ✅ Docker image building
- ✅ Package building and validation
- ❌ Coverage upload to Codecov (external service)
- ❌ Artifact uploads to GitHub (GitHub-specific)

### Documentation Build (`docs.yml`)

```bash
# Test documentation build
act push -W .github/workflows/docs.yml

# Focus on build job only
act push -W .github/workflows/docs.yml -j build-docs
```

**What gets tested locally:**
- ✅ MkDocs installation and setup
- ✅ Documentation building
- ✅ Link validation
- ✅ Site generation
- ❌ GitHub Pages deployment (GitHub-specific)

### Commit Linting (`commit-lint.yml`)

```bash
# Test commit message validation
act push -W .github/workflows/commit-lint.yml

# Use smaller image for faster testing
act push -W .github/workflows/commit-lint.yml -P ubuntu-latest=node:18-alpine
```

## Limitations and Considerations

### What Works Well Locally

- ✅ **Workflow syntax validation**
- ✅ **Job execution logic**
- ✅ **Environment setup steps**
- ✅ **Build and test processes**
- ✅ **Script execution**
- ✅ **Docker builds**
- ✅ **File operations**

### What Has Limitations

- ❌ **GitHub-specific actions**: Issues, PRs, releases
- ❌ **External services**: Codecov, security scanners with API keys
- ❌ **GitHub context**: Some `github.*` variables may differ
- ❌ **Secrets access**: Real secrets shouldn't be used locally
- ❌ **Artifact uploads**: GitHub Actions artifacts
- ❌ **Matrix builds**: Limited matrix strategy support

### Resource Requirements

```bash
# Check available disk space (act uses Docker heavily)
df -h

# Clean up Docker to free space
docker system prune -a

# Use smaller images to save space
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

## Troubleshooting

### Common Issues

#### Docker Out of Space
```bash
# Error: failed to create prepare snapshot dir: no space left on device

# Solution: Clean up Docker
docker system prune -a -f
docker volume prune -f

# Use smaller images
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

#### Permission Denied
```bash
# Error: permission denied while trying to connect to Docker

# Solution: Add user to docker group or use sudo
sudo usermod -aG docker $USER
# Then restart terminal

# Or run with sudo
sudo act
```

#### Workflow Not Found
```bash
# Error: unable to determine reference

# Solution: Ensure you're in the repository root
cd /path/to/pybiorythm
act --list
```

#### Action Not Found
```bash
# Error: unable to resolve action

# Solution: Check if action exists and version is correct
# Update workflow to use correct action versions
```

### Debug Mode

```bash
# Enable verbose logging
act -v

# Enable even more verbose logging
act -vv

# Show environment variables
act --env

# Show job summary
act --job
```

## Best Practices

### 1. Start with Dry Run

Always validate before executing:

```bash
# Check syntax and structure
act -W .github/workflows/ci.yml -n

# Then run if validation passes
act -W .github/workflows/ci.yml
```

### 2. Test Individual Jobs

Test jobs separately for faster iteration:

```bash
# Test just the test job
act -W .github/workflows/ci.yml -j test

# Test just Docker build
act -W .github/workflows/ci.yml -j docker
```

### 3. Use Smaller Images

Save time and disk space:

```bash
# Create .actrc file for persistent configuration
echo "-P ubuntu-latest=catthehacker/ubuntu:act-latest" > .actrc
echo "--container-architecture linux/amd64" >> .actrc

# Now act will use these settings by default
act -W .github/workflows/ci.yml
```

### 4. Mock External Services

Create mock endpoints for external services:

```bash
# In your workflow, check if running locally
- name: Upload coverage
  if: env.ACT != 'true'  # Skip in act
  uses: codecov/codecov-action@v4
```

### 5. Use Local Secrets Safely

```bash
# Create .secrets with dummy values
echo "GITHUB_TOKEN=dummy_token_for_testing" > .secrets
echo "DOCKER_PASSWORD=dummy_password" >> .secrets

# Add to .gitignore
echo ".secrets" >> .gitignore
```

## Integration with Development Workflow

### Pre-Push Testing

```bash
#!/bin/bash
# scripts/test-workflows.sh

echo "🧪 Testing workflows locally before push..."

# Test commit lint
echo "Testing commit lint..."
act -W .github/workflows/commit-lint.yml -q

# Test main CI
echo "Testing CI pipeline..."
act -W .github/workflows/ci.yml -j test -q

# Test documentation
echo "Testing documentation build..."
act -W .github/workflows/docs.yml -j build-docs -q

echo "✅ All workflows tested successfully!"
```

Make it executable and use:
```bash
chmod +x scripts/test-workflows.sh
./scripts/test-workflows.sh
```

### VS Code Integration

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Test GitHub Actions",
      "type": "shell", 
      "command": "act",
      "args": ["-W", ".github/workflows/ci.yml", "-j", "test"],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    }
  ]
}
```

## Performance Tips

### Caching

```bash
# Enable action caching
act --use-gitignore=false

# Use local cache directory
act --action-cache-path ~/.cache/act-cache
```

### Parallel Execution

```bash
# Run multiple jobs concurrently
act --concurrent-jobs 2

# Limit resource usage
act --container-options "--memory=2g --cpus=2"
```

### Selective Testing

```bash
# Test only changed workflows
git diff --name-only HEAD~1 | grep ".github/workflows" | while read workflow; do
  echo "Testing $workflow"
  act -W "$workflow" -n
done
```

## GitHub Actions vs Local act Comparison

| Feature | GitHub Actions | Local act |
|---------|---------------|-----------|
| **Workflow Validation** | ✅ | ✅ |
| **Job Execution** | ✅ | ✅ |
| **Docker Builds** | ✅ | ✅ |
| **Secret Management** | ✅ | ⚠️ Limited |
| **GitHub Context** | ✅ | ⚠️ Simulated |
| **External Integrations** | ✅ | ❌ |
| **Artifact Storage** | ✅ | ⚠️ Local only |
| **Matrix Builds** | ✅ | ⚠️ Limited |
| **Cost** | 💰 Minutes | 🆓 Free |
| **Speed** | Slower | Faster |
| **Offline** | ❌ | ✅ |

## Next Steps

- **Learn more**: [act Documentation](https://github.com/nektos/act)
- **Workflow Development**: [Developer Guide](../developer-guide/setup.md)
- **CI/CD Pipeline**: [GitHub Actions](../workflows/github-actions.md)
- **Local Testing**: [Local Testing Guide](local-testing.md)
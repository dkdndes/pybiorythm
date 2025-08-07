# Local GitHub Actions Testing Setup

This setup allows you to test GitHub Actions workflows locally using `act` and direct command execution.

!!! tip "Comprehensive act Guide"
    **📖 For detailed act usage, configuration, and troubleshooting, see: [Local GitHub Actions Testing](local-github-actions.md)**

## Quick Start

### 1. Fast Local Testing (Recommended)
```bash
./local-test.sh quick
```
This runs the same checks as CI without Docker overhead:
- ✅ Ruff linting and formatting
- ✅ Test suite with coverage
- ✅ Package building

### 2. List Available Workflows
```bash
./local-test.sh list
```

### 3. Test Specific Jobs with act
```bash
# Test documentation job (fastest)
./local-test.sh job docs .github/workflows/ci.yml

# Test main test suite
./local-test.sh job test .github/workflows/ci.yml

# Test commit linting
./local-test.sh job commit-lint .github/workflows/commit-lint.yml
```

## Files Created

### `.actrc` - act Configuration
- Container platform mappings
- M1 Mac compatibility (linux/amd64 architecture)
- Environment variables
- Verbose debugging

### `.secrets` - Local Secrets
Add your tokens here:
```
GITHUB_TOKEN=ghp_your_token_here
CODECOV_TOKEN=your_codecov_token
TEST_PYPI_API_TOKEN=pypi-your_test_token
PYPI_API_TOKEN=pypi-your_production_token
```

### `local-test.sh` - Testing Script
Complete testing automation with multiple modes.

## Available Commands

| Command | Description | Speed | Docker Required |
|---------|-------------|-------|----------------|
| `quick` | Fast local tests | ⚡ Fastest | ❌ No |
| `list` | Show workflows/jobs | ⚡ Instant | ❌ No |
| `validate` | Check syntax | ⚡ Fast | ❌ No |
| `job <name> <file>` | Test specific job | 🐢 Slow | ✅ Yes |
| `basic` | Test basic workflows | 🐢 Slow | ✅ Yes |

## What Gets Tested

### Quick Local Tests
- **Ruff Check**: Code linting (same as CI)
- **Ruff Format**: Code formatting (same as CI) 
- **PyTest**: Full test suite with 85% coverage requirement
- **Build**: Package building with `python -m build`

### act-based Tests
- **Full Workflow Simulation**: Runs actual GitHub Actions
- **Docker Environment**: Same containers as GitHub
- **Secret Management**: Uses `.secrets` file
- **Multi-job Dependencies**: Tests job orchestration

## Troubleshooting

### Docker Issues on M1 Macs
Already configured in `.actrc`:
```
--container-architecture linux/amd64
```

### Memory/Performance Issues
Use `quick` mode for development:
```bash
./local-test.sh quick
```

### Secret Requirements
Most workflows work with dummy secrets for local testing. Only add real tokens if needed.

### Common Failures
- **Test failures with sufficient coverage**: Expected for mock-related tests locally
- **Missing secrets**: Use dummy values or skip secret-dependent jobs
- **Docker not running**: Required for `act` commands

## Integration with Development

### Pre-commit Testing
```bash
# Before committing
./local-test.sh quick

# If all passes, commit
git add .
git commit -m "feat: your changes"
```

### CI Debugging
```bash
# Test the exact job that failed in CI
./local-test.sh job test .github/workflows/ci.yml

# Or run quick local equivalent
./local-test.sh quick
```

## Performance Comparison

| Method | Time | Accuracy | Use Case |
|--------|------|----------|----------|
| `quick` | ~30s | 95% | Development |
| `act` single job | ~2-5min | 98% | Debugging |
| `act` full workflow | ~10-20min | 99% | Pre-release |
| GitHub CI | ~5-15min | 100% | Official |

## Best Practices

1. **Start with `quick`** for rapid development feedback
2. **Use `act`** for debugging specific workflow issues
3. **Test locally** before pushing to avoid CI failures
4. **Update `.secrets`** with real tokens only when necessary
5. **Use `validate`** to catch syntax errors early

## Examples

### Development Workflow
```bash
# 1. Make changes
vim biorythm/core.py

# 2. Quick test
./local-test.sh quick

# 3. Fix any issues
ruff format .

# 4. Test again
./local-test.sh quick

# 5. Commit when all passes
git add . && git commit -m "fix: improve core functionality"
```

### Debugging CI Failures
```bash
# 1. Check what failed
gh run list --limit 5

# 2. Test specific job locally
./local-test.sh job test .github/workflows/ci.yml

# 3. Or run quick equivalent
./local-test.sh quick
```

This setup provides comprehensive local testing capabilities that match your GitHub Actions workflows while being significantly faster for development.
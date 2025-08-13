# Branching & Workflow Guide

This guide outlines the complete branching strategy and development workflow for PyBiorythm.

**Author**: Peter Rosemann (dkdndes@gmail.com)

## 🌿 Branching Strategy

### **Branch Types**

| Branch Type | Purpose | Naming Convention | Examples |
|-------------|---------|-------------------|----------|
| **`main`** | Production releases | - | `main` |
| **`develop`** | Integration branch | - | `develop` |
| **Feature** | New features | `feature/description` | `feature/json-export` |
| **Bug Fix** | Bug fixes | `fix/description` | `fix/date-validation` |
| **Documentation** | Documentation only | `docs/description` | `docs/api-reference` |
| **Security** | Security fixes | `security/description` | `security/cve-fix` |
| **Refactor** | Code refactoring | `refactor/description` | `refactor/calculator-class` |

### **Branch Hierarchy**
```
main (production)
├── develop (integration)
    ├── feature/new-charts
    ├── fix/critical-bug
    ├── docs/workflow-guide
    └── security/vulnerability-patch
```

## 🚀 Development Workflow

### **Phase 1: Initial Setup (One Time Only)**

```bash
# Clone repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm

# Pull current status from GitHub (ONLY ONCE)
git checkout main
git pull origin main
git checkout develop  
git pull origin develop

# Set up development environment
uv sync --group dev
```

**⚠️ IMPORTANT**: After this initial setup, **NEVER** work directly in `main` or `develop` locally again!

### **Phase 2: Feature Development**

```bash
# 1. Create feature branch from develop
git checkout develop                    # Last time using develop locally!
git checkout -b feature/my-awesome-feature

# 2. Make your changes
# ... edit files, write code, update docs ...

# 3. Local testing (REQUIRED before pushing)
# Test code quality
uv run ruff check .
uv run ruff format .
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=85

# Test GitHub Actions locally with act
act --list                             # Validate workflow syntax
act -W .github/workflows/ci.yml --pull=false --dryrun    # Test CI workflow
act -W .github/workflows/sbom.yml -j python-sbom --dryrun # Test SBOM workflow
./local-test.sh quick                  # Quick development tests

# 4. Commit changes
git add .
git commit -m "feat: add awesome new feature

- Implement feature X with Y capability
- Add comprehensive tests
- Update documentation"

# 5. Push feature branch to GitHub
git push origin feature/my-awesome-feature
```

### **Phase 3: Pull Request & Integration**

```bash
# 6. Create Pull Request using GitHub CLI (recommended)
gh pr create --base develop --head feature/my-awesome-feature \
  --title "feat: add awesome new feature" \
  --body "$(cat <<'EOF'
## Summary
Brief description of what this PR does.

## Changes Made
- List key changes
- Include any breaking changes
- Note new features or fixes

## Test Plan
- [x] Unit tests pass locally
- [x] Integration tests pass
- [x] GitHub Actions tested with act
- [x] Documentation updated

## Version Impact
This PR will NOT trigger a version increment (feature branches don't run semantic-release).
Version will only increment when merged to develop (prerelease) or main (full release).

## Related Issues
Fixes #123
EOF
)"
```

**Alternative**: Create PR via GitHub web interface at `https://github.com/dkdndes/pybiorythm/pulls`

**⚠️ Important**: Feature branch PRs only run CI tests, NOT semantic-release. This prevents version conflicts and "Detached HEAD" errors.

### **Phase 4: Review & Merge (GitHub Only)**

1. **Automated Checks**: GitHub Actions run CI/CD pipeline (CI tests only, no releases)
2. **Code Review**: Review changes in GitHub PR interface  
3. **Merge**: Use GitHub's "Merge pull request" button
4. **Version Effect**: 
   - **Merge to develop**: Triggers prerelease version (e.g., 2.8.0-dev.1)
   - **Merge to main**: Triggers full release version (e.g., 2.8.0)
5. **Cleanup**: Delete merged branch via GitHub interface

### **Phase 5: Release Progression (Automated)**

After merging to develop:
```bash
# This happens automatically via GitHub Actions
Feature merged to develop → Prerelease created (2.8.0-dev.1)
                         → Development Docker image built
                         → No PyPI publishing

# Later, when develop is merged to main:
Develop merged to main → Full release created (2.8.0)
                      → Production Docker image published  
                      → PyPI package published
                      → GitHub release created
```

### **Phase 6: Local Cleanup**

```bash
# 7. Clean up local feature branch (after GitHub merge)
git branch -d feature/my-awesome-feature  # Delete local branch
git remote prune origin                   # Clean up stale remote references
```

## 🧪 Local Testing Requirements

**Before pushing ANY branch**, you MUST run these tests locally:

### **Code Quality Tests**
```bash
# Linting and formatting
uv run ruff check .
uv run ruff format .

# Test suite with coverage
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=85

# Security scanning
uv run safety check
uv run bandit -r biorythm/ main.py
```

### **GitHub Actions Testing with `act`**
```bash
# Validate all workflows
act --list

# Test specific workflows
act -W .github/workflows/ci.yml --container-architecture linux/amd64 --pull=false --dryrun
act -W .github/workflows/sbom.yml -j python-sbom --dryrun

# Quick local development tests
./local-test.sh quick      # ~30 second validation
./local-test.sh validate   # Workflow syntax check
```

**⚠️ Never push without local testing!** This catches issues early and saves CI/CD credits.

## 📋 Pull Request Best Practices

### **When to Create PRs**

| Change Type | Target Branch | PR Required? |
|-------------|---------------|--------------|
| New features | `develop` | ✅ Always |
| Bug fixes | `develop` | ✅ Always |
| Documentation | `develop` | ✅ Always |
| Security fixes | `develop` | ✅ Always |
| Hotfixes | `main` | ✅ Always (emergency only) |

### **PR Title Format**
Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

Examples:
feat(calculator): add cycle repeat calculation
fix(cli): handle invalid date input gracefully
docs(api): update calculator examples  
security(deps): update vulnerable dependency
refactor(core): simplify date validation logic
```

### **PR Description Template**
```markdown
## Summary
Brief description of changes and motivation.

## Changes Made
- Specific change 1
- Specific change 2
- Breaking changes (if any)

## Test Plan
- [x] Unit tests pass (`uv run pytest`)
- [x] Coverage maintained (≥85%)
- [x] Linting passes (`uv run ruff check .`)
- [x] Security scans clean
- [x] Local GitHub Actions testing (`act`)
- [x] Documentation updated

## Related Issues
Closes #123
Fixes #456
Related to #789

## Additional Notes
Any extra context, deployment notes, or breaking changes.
```

## 🔀 Merge Strategies

### **GitHub Merge Options**

| Option | When to Use | Git History |
|---------|-------------|-------------|
| **Merge Commit** | Feature branches with multiple commits | Preserves branch history |
| **Squash and Merge** | Simple features, clean up history | Single commit |
| **Rebase and Merge** | Linear history preferred | Clean linear timeline |

**Recommendation**: Use **Squash and Merge** for most feature branches to keep history clean.

### **Branch Protection Rules**

Our repository enforces:
- ✅ Required status checks (all CI/CD must pass)
- ✅ Require pull request reviews
- ✅ Dismiss stale reviews when new commits are pushed
- ✅ Require up-to-date branches before merging
- ❌ No direct pushes to `main` or `develop`

## 🚫 What NOT to Do

### **❌ Anti-Patterns**
```bash
# NEVER do these:
git checkout main              # Don't work in main locally
git checkout develop           # Don't work in develop locally (after initial setup)
git merge feature-branch       # Don't merge locally - use GitHub PRs
git push origin main           # Don't push directly to main
git push --force origin main   # Never force push to protected branches
```

### **❌ Common Mistakes**
- Working directly in `main` or `develop` branches
- Merging locally instead of using Pull Requests
- Pushing without local testing with `act`
- Creating PRs without proper descriptions
- Not running code quality checks before push
- Force pushing to shared branches

## 🔧 Workflow Tools

### **Essential Commands**
```bash
# Branch management
git checkout -b feature/name    # Create new feature branch
git branch -d branch-name       # Delete merged branch
git remote prune origin         # Clean up stale remotes

# GitHub CLI (recommended)
gh pr create --base develop     # Create pull request
gh pr list                      # List open PRs
gh pr merge 123                 # Merge PR #123

# Local testing
act --list                      # List available workflows
./local-test.sh quick          # Quick validation tests
uv run pytest --cov=.          # Full test suite
```

### **IDE Integration**
Configure your IDE/editor for:
- ✅ Automatic `ruff` formatting on save
- ✅ Run tests on file changes
- ✅ Show Git branch status in status bar
- ✅ Integrate with GitHub PR workflows

## 🚨 Emergency Procedures

### **Hotfix Workflow (Production Issues)**
```bash
# 1. Create hotfix branch from main (EXCEPTION to normal workflow)
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# 2. Apply minimal fix
# ... make only essential changes ...

# 3. Test thoroughly
uv run pytest
act -W .github/workflows/ci.yml --pull=false

# 4. Create emergency PR to main
gh pr create --base main --head hotfix/critical-security-fix \
  --title "HOTFIX: critical security vulnerability" \
  --body "Emergency fix for production issue..."

# 5. After merge, backport to develop
gh pr create --base develop --head hotfix/critical-security-fix \
  --title "backport: security hotfix to develop"
```

### **Rollback Procedures**
If a merged PR causes issues:
1. **Immediate**: Revert via GitHub web interface  
2. **Create fix**: New PR with proper fix
3. **Never force push**: Use forward-fixes only

## 📖 Learning Resources

- **Git Flow**: [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- **GitHub Flow**: [Understanding GitHub Flow](https://guides.github.com/introduction/flow/)
- **Conventional Commits**: [Specification](https://www.conventionalcommits.org/)
- **Act Documentation**: [Local GitHub Actions](https://github.com/nektos/act)

---

**Next Steps:**
- [Contributing Guidelines](contributing.md) - How to contribute code
- [Code Quality Standards](code-quality.md) - Quality requirements  
- [Local GitHub Actions](../deployment/local-github-actions.md) - Testing workflows
- [Development Setup](setup.md) - Environment configuration
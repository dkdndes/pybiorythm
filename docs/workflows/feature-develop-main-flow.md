# Feature → Develop → Main Workflow Guide

This document explains the complete **feature → develop → main** progression with proper version increments and release automation for PyBiorythm.

## Overview

Our workflow ensures **versions only increment on successful merges** to release branches, preventing circular references and ensuring clean version management.

## Workflow Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Feature Branch │    │  Develop Branch  │    │   Main Branch   │
│                 │    │                  │    │                 │
│ fix/my-feature  │───▶│     develop      │───▶│      main       │
│                 │    │                  │    │                 │
│ ✅ CI Tests     │    │ ✅ CI Tests      │    │ ✅ CI Tests     │
│ ❌ No Release   │    │ ✅ Prerelease    │    │ ✅ Full Release │
│ ❌ No Version   │    │ 📦 Dev Docker    │    │ 📦 Prod Docker  │
│                 │    │ ❌ No PyPI       │    │ ✅ PyPI Publish │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Branch Purposes & Version Strategy

### 🏗️ Feature Branches (`feature/*`, `fix/*`, `docs/*`)

**Purpose**: Individual feature development and bug fixes

**Characteristics**:
- ✅ **CI Testing**: Full test suite, linting, security scans
- ❌ **No Releases**: Semantic-release does NOT run
- ❌ **No Version Increments**: Prevents circular reference issues
- 🔒 **Protection**: Requires CI to pass before merging

**Example Workflow**:
```bash
git checkout -b fix/pytest-test-collection-issues
# ... make changes ...
git commit -m "fix: resolve pytest test collection and JSON serialization issues"
git push origin fix/pytest-test-collection-issues
gh pr create --base develop
```

**GitHub Actions Triggered**:
- `ci.yml` - Full CI/CD pipeline
- `codeql.yml` - Security analysis
- `dependency-review.yml` - Dependency security (PRs only)

**Version Impact**: 🚫 **NONE** - No version changes occur

---

### 🧪 Develop Branch (`develop`)

**Purpose**: Integration branch for testing feature combinations

**Characteristics**:
- ✅ **CI Testing**: Full test suite validation
- ✅ **Prerelease Versions**: Creates development versions
- ✅ **Development Docker**: Builds tagged dev images
- ❌ **No PyPI Publishing**: Prereleases not published to PyPI

**Version Examples**:
- `2.8.0-dev.1` - First prerelease after 2.8.0
- `2.8.0-dev.2` - Second prerelease
- `2.9.0-dev.1` - First prerelease for next minor version

**GitHub Actions Triggered**:
- `ci.yml` - Full CI/CD pipeline
- `semantic-release.yml` - Creates prerelease versions
- `dev-docker.yml` - Development Docker builds
- `sbom.yml` - Security bill of materials

**Version Impact**: 📈 **Prerelease Increment**
- Based on conventional commit types in merged features
- Creates git tags like `v2.8.0-dev.1`
- Updates `CHANGELOG.md` with prerelease notes

---

### 🚀 Main Branch (`main`)

**Purpose**: Production-ready releases only

**Characteristics**:
- ✅ **CI Testing**: Full validation pipeline
- ✅ **Production Releases**: Full semantic versions
- ✅ **Production Docker**: Multi-arch container publishing
- ✅ **PyPI Publishing**: Official package releases
- ✅ **GitHub Releases**: Official release creation

**Version Examples**:
- `2.8.0` - Minor version with new features
- `2.8.1` - Patch version with bug fixes
- `3.0.0` - Major version with breaking changes

**GitHub Actions Triggered**:
- `ci.yml` - Full CI/CD pipeline
- `semantic-release.yml` - Creates production releases
- `docker-publish.yml` - Production Docker publishing
- `sbom.yml` - Security bill of materials
- `docs.yml` - Documentation deployment

**Version Impact**: 📈 **Production Release**
- Full semantic version increment
- Creates git tags like `v2.8.0`
- Publishes to PyPI automatically
- Creates GitHub release with changelog

## Version Increment Logic

Our semantic versioning follows conventional commits:

### Commit Types & Version Impact

| Commit Type | Feature Branch | Develop Branch | Main Branch |
|-------------|----------------|----------------|-------------|
| `feat:` | No change | Minor prerelease | Minor release |
| `fix:` | No change | Patch prerelease | Patch release |
| `BREAKING CHANGE:` | No change | Major prerelease | Major release |
| `docs:`, `ci:`, `test:` | No change | No version change | No version change |

### Example Version Progression

```bash
# Starting point: v2.7.0 (last release)
git checkout main
git tag  # shows: v2.7.0

# Feature development (no version changes)
git checkout -b feature/new-charts
git commit -m "feat: add horizontal chart support"
# Current version: 2.7.0.dev1+g1234abcd (dynamic, no tags)

# Merge to develop (creates prerelease)
gh pr merge --into develop
# New tag created: v2.8.0-dev.1
# Version: 2.8.0-dev.1

# More features merged to develop
git commit -m "fix: resolve chart rendering bug"
# New tag created: v2.8.0-dev.2
# Version: 2.8.0-dev.2

# Merge develop to main (creates production release)
gh pr merge --into main
# New tag created: v2.8.0
# Version: 2.8.0 (published to PyPI, Docker, etc.)
```

## Dynamic Versioning System

### Configuration
```toml
# pyproject.toml
[project]
dynamic = ["version"]  # No hardcoded versions

[tool.hatch.version]
source = "vcs"  # Read from git tags

[tool.semantic_release]
version_variables = [
    "biorythm/__init__.py:__version__",
]
# No version_toml conflicts
```

### Version Sources (Priority Order)
1. **Git Tags**: Created by semantic-release (`v2.8.0`, `v2.8.0-dev.1`)
2. **Hatch VCS**: Reads from git tags automatically
3. **Python Package**: `biorythm.__version__` via `importlib.metadata`
4. **Development**: Automatic dev versions for unreleased commits

### Development Version Format
For unreleased code between tags:
```
2.8.0b2.dev2+gf9d5af7b1.d20250812
│     │  │   │           └─ Date stamp
│     │  │   └─ Git commit hash
│     │  └─ Commits since last tag
│     └─ Beta/dev indicator
└─ Base version from latest tag
```

## Workflow Best Practices

### ✅ Correct Workflow
```bash
# 1. Feature development
git checkout -b feature/awesome-feature
git commit -m "feat: add awesome new feature"
git push origin feature/awesome-feature

# 2. PR to develop
gh pr create --base develop --head feature/awesome-feature

# 3. Merge creates prerelease (automatic)
# Result: v2.8.0-dev.1 created

# 4. Later: develop to main (when ready for release)
gh pr create --base main --head develop

# 5. Merge creates production release (automatic)
# Result: v2.8.0 published to PyPI, Docker, etc.
```

### ❌ Anti-Patterns (Don't Do This)
```bash
# DON'T: Work directly in protected branches
git checkout main  # ❌ Never work directly in main
git checkout develop  # ❌ Never work directly in develop

# DON'T: Try to create releases from feature branches
# This would cause "Detached HEAD" errors (now prevented)

# DON'T: Force push to protected branches
git push --force origin main  # ❌ Will be rejected

# DON'T: Merge locally instead of using PRs
git merge feature-branch  # ❌ Use GitHub PRs instead
```

## Troubleshooting

### Common Issues & Solutions

#### "Detached HEAD" Error in Semantic Release
**Status**: ✅ **FIXED** - Semantic-release no longer runs on feature branches

**Previous Error**:
```
Detached HEAD state cannot match any release groups; no release will be made
```

**Solution Applied**: 
- Semantic-release now only runs on `main` and `develop` branches
- Feature branches only run CI tests, no release logic

#### Version Conflicts Between Files
**Status**: ✅ **FIXED** - Dynamic versioning eliminates conflicts

**Previous Issue**: 
- `pyproject.toml` had hardcoded version
- Semantic-release tried to update multiple files
- Created circular reference conflicts

**Solution Applied**:
- Removed hardcoded version from `pyproject.toml`
- Uses `dynamic = ["version"]` with hatch-vcs
- Git tags are single source of truth

#### Version Not Incrementing
**Check These**:
1. ✅ Commit messages follow conventional format (`feat:`, `fix:`, etc.)
2. ✅ Merge is to `develop` or `main` branch (not feature branch)
3. ✅ Semantic-release workflow completed successfully
4. ✅ No `[skip ci]` in commit messages

**Debug Commands**:
```bash
# Check current version
uv run python -c "import biorythm; print(biorythm.__version__)"

# Check git tags
git tag --sort=-version:refname

# Test semantic-release locally
uv run semantic-release version --print
```

## Monitoring & Validation

### Success Indicators
- 🟢 Feature PRs pass CI without version changes
- 🟢 Develop merges create prerelease versions (`2.8.0-dev.1`)
- 🟢 Main merges create production releases (`2.8.0`)
- 🟢 PyPI packages published automatically for main releases
- 🟢 Docker images built for both develop and main
- 🟢 No "Detached HEAD" or circular reference errors

### Workflow Validation
```bash
# Check workflow status
gh workflow list

# Check specific run
gh run list --workflow="Semantic Release"

# View workflow logs
gh run view [run-id] --log
```

## Summary

This **feature → develop → main** workflow provides:

1. **🛡️ Safe Development**: Feature branches test thoroughly without affecting versions
2. **🧪 Integration Testing**: Develop branch validates feature combinations with prereleases  
3. **🚀 Production Releases**: Main branch creates official releases with full automation
4. **📈 Proper Versioning**: Versions only increment on successful merges to release branches
5. **🔧 No Conflicts**: Dynamic versioning eliminates circular reference issues
6. **🤖 Full Automation**: Complete CI/CD pipeline with security and compliance

**Next Steps**: See [Contributing Guidelines](../developer-guide/contributing.md) for detailed development process.
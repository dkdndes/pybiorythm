# Semantic Versioning and Conventional Commits

This project uses **Semantic Versioning** (SemVer) with **Conventional Commits** for automated version management and changelog generation.

## Overview

### Semantic Versioning (SemVer)
Versions follow the `MAJOR.MINOR.PATCH` format:
- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward-compatible functionality)  
- **PATCH**: Bug fixes (backward-compatible bug fixes)

### Conventional Commits
Commit messages follow a structured format that enables automatic version bumping:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

### Version Bumping Types

| Type | Version Bump | Description | Example |
|------|--------------|-------------|---------|
| `feat` | **MINOR** | New feature | `feat: add JSON export functionality` |
| `fix` | **PATCH** | Bug fix | `fix: resolve date validation error` |
| `perf` | **PATCH** | Performance improvement | `perf: optimize calculation algorithm` |

### Non-Version Bumping Types

| Type | Description | Example |
|------|-------------|---------|
| `docs` | Documentation changes | `docs: update installation guide` |
| `style` | Code style changes | `style: format code with ruff` |
| `refactor` | Code refactoring | `refactor: extract validation logic` |
| `test` | Test additions/changes | `test: add unit tests for calculator` |
| `build` | Build system changes | `build: update dependencies` |
| `ci` | CI/CD changes | `ci: add security scanning` |
| `chore` | Maintenance tasks | `chore: update gitignore` |

### Breaking Changes

For **MAJOR** version bumps, include `BREAKING CHANGE:` in the footer:

```
feat: redesign API structure

BREAKING CHANGE: The BiorhythmCalculator constructor now requires 
a configuration object instead of individual parameters.
```

## Examples

### Feature Addition (MINOR bump: 1.2.0 → 1.3.0)
```bash
git commit -m "feat: add horizontal chart generation support"
```

### Bug Fix (PATCH bump: 1.2.0 → 1.2.1)
```bash
git commit -m "fix: correct leap year calculation in date validator"
```

### Performance Improvement (PATCH bump: 1.2.0 → 1.2.1)
```bash
git commit -m "perf: cache biorhythm calculations for better performance"
```

### Documentation Update (no version bump)
```bash
git commit -m "docs: add usage examples for Docker deployment"
```

### Breaking Change (MAJOR bump: 1.2.0 → 2.0.0)
```bash
git commit -m "feat: rewrite core calculation engine

BREAKING CHANGE: The calculate_biorhythm_values method now returns 
a dictionary instead of a tuple for better readability."
```

## Scopes (Optional)

Add scope to provide more context:

```bash
git commit -m "feat(docker): add multi-stage build support"
git commit -m "fix(tests): resolve flaky integration test"
git commit -m "docs(api): update method documentation"
```

Common scopes in this project:
- `docker`: Docker-related changes
- `tests`: Test-related changes  
- `api`: API changes
- `cli`: Command-line interface changes
- `ci`: CI/CD pipeline changes

## Automation

### Version Management
- **Automatic**: Versions are automatically calculated based on commit messages
- **Location**: Version stored in `pyproject.toml`, `biorythm/__init__.py`, and `_version.py`
- **Trigger**: Every push to `main` branch triggers semantic release

### Release Process
1. **Commit Analysis**: Semantic-release analyzes commits since last release
2. **Version Calculation**: Determines next version based on commit types
3. **Changelog Generation**: Creates/updates CHANGELOG.md automatically
4. **Git Tagging**: Creates annotated git tag (e.g., `v1.2.0`)
5. **GitHub Release**: Creates GitHub release with changelog
6. **Package Publishing**: Publishes to PyPI automatically
7. **Docker Images**: Triggers Docker image builds and publishing

### Workflow Integration

#### Semantic Release Workflow
```yaml
# Triggered on: push to main
name: Semantic Release
- Analyzes commits for version bump
- Updates version files
- Creates git tags
- Publishes GitHub releases
- Triggers downstream workflows
```

#### Commit Validation
```yaml  
# Triggered on: PRs and pushes
name: Commit Lint
- Validates commit message format
- Blocks PRs with invalid commits
- Provides helpful error messages
```

## Local Development

### Git Message Template
The project includes a `.gitmessage` template. To use it:

```bash
git config commit.template .gitmessage
```

### Manual Version Check
Check what the next version would be:

```bash
# Install semantic-release
pip install python-semantic-release

# Check next version (dry-run)
semantic-release version --print
```

### Commit Message Validation
Validate commits locally before pushing:

```bash
# Install commitlint (requires Node.js)
npm install -g @commitlint/cli @commitlint/config-conventional

# Validate last commit
echo "$(git log -1 --pretty=%B)" | commitlint

# Validate commit message interactively
echo "feat: add new feature" | commitlint
```

## Version History

### Current Version Storage
The version is maintained in multiple locations:
- `pyproject.toml` - Primary source for packaging
- `biorythm/__init__.py` - Python package version
- `_version.py` - Auto-generated version file
- Git tags - Authoritative version source

### Dynamic Versioning System
Our project uses **dynamic versioning** to eliminate circular reference issues:

#### Version Sources (Priority Order)
1. **Git Tags**: Authoritative source created by semantic-release
2. **Hatch VCS**: Reads version from git tags automatically  
3. **Python Import**: `biorythm.__version__` via `importlib.metadata`
4. **Build System**: Automatic version injection during package builds

#### Configuration
```toml
# pyproject.toml
[project]
name = "biorythm"
dynamic = ["version"]  # No hardcoded version

[tool.hatch.version]
source = "vcs"         # Read from git tags

[tool.semantic_release]
# No version_toml conflicts
version_variables = [
    "biorythm/__init__.py:__version__",
]
```

#### Development Versions
For unreleased code, hatch-vcs automatically generates development versions:
- **Format**: `2.8.0b2.dev2+gf9d5af7b1.d20250812`
- **Breakdown**: 
  - `2.8.0b2`: Base version from latest tag
  - `dev2`: 2 commits since tag  
  - `gf9d5af7b1`: Git hash
  - `d20250812`: Date stamp

### Version Synchronization
All version locations are kept in sync by:
1. **Hatch VCS**: Reads version from git tags automatically
2. **Semantic Release**: Creates git tags, no file conflicts
3. **GitHub Actions**: Ensures consistency across releases
4. **Dynamic Import**: Runtime version detection from package metadata

## Branch Strategy & Version Flow

### Feature → Develop → Main Progression

Our workflow ensures versions only increment on successful merges to release branches:

```
Feature Branch (fix/pytest-test-collection-issues)
    ↓ (PR + CI tests only, NO version increment)
Develop Branch (prerelease versions: 2.8.0-dev.1, 2.8.0-dev.2, etc.)
    ↓ (Merge triggers prerelease versions)
Main Branch (production releases: 2.8.0, 2.8.1, etc.)
    ↓ (Merge triggers full releases)
```

### Branch Roles & Version Strategy

#### Main Branch (`main`)
- **Purpose**: Production-ready releases only
- **Protection**: Requires PR reviews and all CI checks
- **Versioning**: Full semantic releases (1.0.0, 1.1.0, 2.0.0)
- **Triggers**: Docker publish, PyPI upload, GitHub releases
- **Semantic Release**: Only runs on direct pushes to main

#### Develop Branch (`develop`) 
- **Purpose**: Integration and testing of features
- **Protection**: Requires PR reviews and CI checks
- **Versioning**: Prerelease versions (1.0.0-dev.1, 1.0.0-dev.2)
- **Triggers**: Development Docker builds, no PyPI uploads
- **Semantic Release**: Creates prerelease versions only

#### Feature Branches (`feature/*`, `fix/*`, `docs/*`)
- **Purpose**: Individual feature development
- **Protection**: CI checks required, no direct pushes
- **Versioning**: NO version increments (prevents circular references)
- **Triggers**: CI tests only, no releases
- **Semantic Release**: Does NOT run (prevents "Detached HEAD" errors)

## Best Practices

### Writing Good Commit Messages

#### ✅ Good Examples
```bash
feat: add biorhythm chart export to PDF
fix: resolve timezone handling in date calculations
docs: add comprehensive API documentation
test: increase test coverage for edge cases
perf: optimize memory usage in large datasets
```

#### ❌ Bad Examples  
```bash
Added some stuff           # No type, vague description
Fixed bug                  # No context about what was fixed
Update                     # Too vague
WIP                        # Work in progress, not ready
Quick fix                  # No type, unclear what was fixed
```

### Commit Guidelines
1. **Type Required**: Always start with a valid type
2. **Present Tense**: Use imperative mood ("add" not "added")
3. **Lowercase**: Keep description lowercase
4. **No Period**: Don't end description with a period
5. **50 Character Limit**: Keep description under 50 characters
6. **Body Details**: Add detailed explanation in body if needed

### Release Guidelines
1. **Test First**: Ensure all tests pass before release commits
2. **Document Changes**: Update docs for user-facing changes
3. **Breaking Changes**: Clearly document breaking changes
4. **Migration Guides**: Provide upgrade instructions for breaking changes

## Troubleshooting

### Common Issues

#### Invalid Commit Messages
**Error**: Commit lint fails on PR
**Solution**: Fix commit messages and force-push:
```bash
git rebase -i HEAD~3  # Interactive rebase to edit commits
git push --force-with-lease
```

#### Version Not Bumping
**Problem**: Commits pushed but no new version created
**Check**: 
- Commit messages follow conventional format
- No `[skip ci]` in commit messages
- Semantic release workflow completed successfully

#### Multiple Version Files Out of Sync
**Problem**: Version differs between files
**Solution**: Semantic release automatically syncs all version files

### Manual Version Bump
In rare cases, manual version bump might be needed:

```bash
# Set specific version
semantic-release version --verbosity=DEBUG --print

# Force version bump
git tag v1.2.0
git push origin v1.2.0
```

## Configuration

### Semantic Release Config
Location: `pyproject.toml` under `[tool.semantic_release]`

Key settings:
- `version_toml`: Version location in TOML files
- `version_variables`: Version variables in Python files  
- `build_command`: Build command for releases
- `upload_to_vcs_release`: Enable GitHub releases

### Commit Lint Config
Location: `.commitlintrc.json` (auto-generated in CI)

Key rules:
- `type-enum`: Allowed commit types
- `subject-case`: Case rules for subject
- `subject-empty`: Require non-empty subject
- `type-empty`: Require non-empty type

This semantic versioning setup ensures consistent, automated version management while maintaining clear project history and enabling reliable releases.
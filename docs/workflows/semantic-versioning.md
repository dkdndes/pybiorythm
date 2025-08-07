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

### Version Synchronization
All version locations are kept in sync by:
1. **Hatch VCS**: Reads version from git tags
2. **Semantic Release**: Updates all version files
3. **GitHub Actions**: Ensures consistency across releases

## Branch Strategy

### Main Branch
- **Production ready**: All commits should be releasable
- **Protected**: Requires PR reviews and status checks
- **Semantic Release**: Every push triggers version analysis
- **Clean History**: Prefer squash merges for PRs

### Develop Branch (Optional)
- **Integration**: Feature integration and testing
- **Semantic Commits**: Same commit conventions apply
- **Sync**: Automatically synced with main after releases

### Feature Branches
- **Naming**: Use descriptive names (e.g., `feat/user-auth`, `fix/date-bug`)
- **Commits**: Follow conventional commit format
- **Squashing**: PR commits can be squashed if preferred

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
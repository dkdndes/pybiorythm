#!/bin/bash
# Script to automatically update .secrets file from environment

echo "🔑 Updating .secrets file from local environment..."

# Create backup
cp .secrets .secrets.backup

# Start new secrets file
cat > .secrets << 'EOF'
# Local secrets for act
# Add your secrets here in KEY=VALUE format
# 
# Automatically populated from local environment

EOF

# GitHub token from gh CLI
if gh_token=$(gh auth token 2>/dev/null); then
    echo "# GitHub token from gh CLI" >> .secrets
    echo "GITHUB_TOKEN=$gh_token" >> .secrets
    echo "✅ GitHub token added from gh CLI"
else
    echo "# GitHub token (add manually if needed)" >> .secrets
    echo "# GITHUB_TOKEN=ghp_your_token_here" >> .secrets
    echo "⚠️  No GitHub token found in gh CLI"
fi

echo "" >> .secrets

# Check for other tokens in environment
tokens_found=0

if [ -n "$CODECOV_TOKEN" ]; then
    echo "CODECOV_TOKEN=$CODECOV_TOKEN" >> .secrets
    echo "✅ Codecov token found in environment"
    ((tokens_found++))
fi

if [ -n "$TEST_PYPI_API_TOKEN" ]; then
    echo "TEST_PYPI_API_TOKEN=$TEST_PYPI_API_TOKEN" >> .secrets
    echo "✅ Test PyPI token found in environment"
    ((tokens_found++))
fi

if [ -n "$PYPI_API_TOKEN" ]; then
    echo "PYPI_API_TOKEN=$PYPI_API_TOKEN" >> .secrets
    echo "✅ PyPI token found in environment"
    ((tokens_found++))
fi

if [ -n "$DOCKERHUB_USERNAME" ]; then
    echo "DOCKERHUB_USERNAME=$DOCKERHUB_USERNAME" >> .secrets
    echo "✅ Docker Hub username found in environment"
    ((tokens_found++))
fi

if [ -n "$DOCKERHUB_TOKEN" ]; then
    echo "DOCKERHUB_TOKEN=$DOCKERHUB_TOKEN" >> .secrets
    echo "✅ Docker Hub token found in environment"
    ((tokens_found++))
fi

# Add dummy values for missing tokens
cat >> .secrets << 'EOF'

# Dummy values for workflows that don't need real tokens
# (Comment out if you add real tokens above)
EOF

[ -z "$CODECOV_TOKEN" ] && echo "CODECOV_TOKEN=dummy_codecov_token_for_local_testing" >> .secrets
[ -z "$TEST_PYPI_API_TOKEN" ] && echo "TEST_PYPI_API_TOKEN=dummy_test_pypi_token" >> .secrets
[ -z "$PYPI_API_TOKEN" ] && echo "PYPI_API_TOKEN=dummy_pypi_token" >> .secrets
[ -z "$DOCKERHUB_USERNAME" ] && echo "DOCKERHUB_USERNAME=dummy_dockerhub_user" >> .secrets
[ -z "$DOCKERHUB_TOKEN" ] && echo "DOCKERHUB_TOKEN=dummy_dockerhub_token" >> .secrets

echo ""
echo "📊 Summary:"
echo "   - GitHub token: $([ -n "$gh_token" ] && echo "✅ Found" || echo "❌ Missing")"
echo "   - Environment tokens found: $tokens_found"
echo "   - Dummy tokens added for missing values"
echo ""
echo "💡 To add missing tokens, either:"
echo "   1. Set environment variables: export CODECOV_TOKEN=your_token"
echo "   2. Edit .secrets file manually"
echo ""
echo "🔒 .secrets file updated successfully!"
echo "📁 Backup saved as .secrets.backup"
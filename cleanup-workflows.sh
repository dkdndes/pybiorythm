#!/bin/bash

# GitHub Actions Cleanup Script
# Deletes workflow runs that are not related to version tags

set -e

echo "🧹 GitHub Actions Workflow Cleanup"
echo "=================================="

# Get all workflow runs
echo "Fetching workflow runs..."

# Delete runs that are not triggered by version tags
# Keep only runs triggered by tags like v1.3.0, v1.2.1, etc.

# Keep only version 1.3.0 related runs and current main branch
echo "Fetching all runs to clean up (keeping only v1.3.0 and latest main)..."

# Get all runs that are NOT:
# 1. From v1.3.0 tag
# 2. From recent main branch commits (chore: update version to 1.3.0)
# 3. From docs commits on main that are part of v1.3.0 release
ALL_RUNS_TO_DELETE=$(gh run list --limit 300 --json databaseId,headBranch,event,workflowDatabaseId,displayTitle --jq '
.[] | select(
  # Keep v1.3.0 tag runs
  (.headBranch == "v1.3.0") or
  # Keep recent main branch runs related to v1.3.0
  (.headBranch == "main" and (.displayTitle | contains("chore: update version to 1.3.0"))) or
  (.headBranch == "main" and (.displayTitle | contains("docs: update project metrics with current test results")))
  | not
) | .databaseId')

echo "Found runs to delete (keeping only v1.3.0 related): $(echo "$ALL_RUNS_TO_DELETE" | wc -l)"

echo ""
echo "Total runs to delete: $(echo "$ALL_RUNS_TO_DELETE" | wc -l)"
echo ""

# Delete all identified runs
counter=0
for run_id in $ALL_RUNS_TO_DELETE; do
    if [ -n "$run_id" ]; then
        counter=$((counter + 1))
        echo "[$counter] Deleting workflow run: $run_id"
        gh run delete $run_id || echo "Failed to delete $run_id"
        sleep 0.5  # Rate limit protection
    fi
done

echo ""
echo "✅ Cleanup completed!"
echo ""
echo "Remaining runs (should be mostly version-tag related):"
gh run list --limit 10
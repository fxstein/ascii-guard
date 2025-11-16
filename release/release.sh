#!/bin/bash
# Release script for ascii-guard
# Automatically determines version bump, generates release notes, and creates release

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Release log file
RELEASE_LOG="${RELEASE_LOG:-$(pwd)/release/RELEASE_LOG.log}"

# Get GitHub user ID
get_github_user() {
    gh api user --jq .login 2>/dev/null || git config user.email 2>/dev/null | cut -d'@' -f1 || echo "unknown"
}

# Log release step with timestamp (newest entries on top)
log_release_step() {
    local step="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local user_id=$(get_github_user)

    # Create header if file doesn't exist
    if [[ ! -f "$RELEASE_LOG" ]]; then
        local generated_date=$(date)
        cat > "$RELEASE_LOG" << EOF
# Release Log File
# Format: TIMESTAMP | USER | STEP | MESSAGE
# Generated: ${generated_date}
#
EOF
    fi

    # Create log entry (flatten multi-line messages to single line)
    local flat_message=$(echo "$message" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ *//;s/ *$//')
    local log_entry="${timestamp} | ${user_id} | ${step} | ${flat_message}"

    # Find where header ends
    local first_log_line=$(awk '/^[0-9]/ {print NR; exit}' "$RELEASE_LOG" 2>/dev/null || echo 0)

    if [[ -z "$first_log_line" ]] || [[ "$first_log_line" -eq 0 ]]; then
        first_log_line=$(wc -l < "$RELEASE_LOG" 2>/dev/null || echo 4)
    fi

    local header_end=$((first_log_line - 1))

    if [[ $header_end -lt 4 ]]; then
        header_end=4
    fi

    # Create new log: header + new entry + old entries
    local temp_log=$(mktemp)

    head -n "$header_end" "$RELEASE_LOG" > "$temp_log" 2>/dev/null
    echo "$log_entry" >> "$temp_log"

    if [[ $first_log_line -gt 0 ]]; then
        tail -n +$first_log_line "$RELEASE_LOG" 2>/dev/null >> "$temp_log" || true
    fi

    mv "$temp_log" "$RELEASE_LOG"
}

# Validate environment before release
validate_environment() {
    local errors=0

    echo -e "${BLUE}🔍 Validating environment...${NC}"

    # Check Python version
    if [[ -f .python-version ]]; then
        local required_version=$(cat .python-version)
        local current_version=$(python3 --version 2>&1 | awk '{print $2}')

        # Extract major.minor from both versions
        local required_major_minor=$(echo "$required_version" | cut -d. -f1-2)
        local current_major_minor=$(echo "$current_version" | cut -d. -f1-2)

        if [[ "$required_major_minor" != "$current_major_minor" ]]; then
            echo -e "${RED}❌ Python version mismatch${NC}"
            echo -e "${RED}   Required: $required_version (.python-version)${NC}"
            echo -e "${RED}   Current:  $current_version${NC}"
            echo ""
            echo -e "${YELLOW}Fix: Install correct Python version:${NC}"
            echo -e "${YELLOW}  pyenv install $required_version${NC}"
            errors=$((errors + 1))
        else
            echo -e "${GREEN}✓ Python version: $current_version${NC}"
        fi
    fi

    # Check if python3 -m build is available
    if python3 -c "import build" 2>/dev/null; then
        echo -e "${GREEN}✓ python3 -m build: available${NC}"
    else
        echo -e "${RED}❌ python3 -m build: not available${NC}"
        echo ""
        echo -e "${YELLOW}Fix: Install build module in venv:${NC}"
        echo -e "${YELLOW}  source .venv/bin/activate${NC}"
        echo -e "${YELLOW}  pip install build${NC}"
        errors=$((errors + 1))
    fi

    # Check if gh CLI is installed and authenticated
    if command -v gh &> /dev/null; then
        if gh auth status &> /dev/null; then
            echo -e "${GREEN}✓ gh CLI: installed and authenticated${NC}"
        else
            echo -e "${RED}❌ gh CLI: not authenticated${NC}"
            echo ""
            echo -e "${YELLOW}Fix: Authenticate GitHub CLI:${NC}"
            echo -e "${YELLOW}  gh auth login${NC}"
            errors=$((errors + 1))
        fi
    else
        echo -e "${RED}❌ gh CLI: not installed${NC}"
        echo ""
        echo -e "${YELLOW}Fix: Install GitHub CLI:${NC}"
        echo -e "${YELLOW}  brew install gh${NC}"
        errors=$((errors + 1))
    fi

    echo ""

    if [[ $errors -gt 0 ]]; then
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}❌ Environment validation failed with $errors error(s)${NC}"
        echo -e "${RED}Please fix the issues above before running release${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ Environment validation passed${NC}"
    echo ""
    return 0
}

# Get current version from GitHub releases (source of truth)
get_current_version() {
    # Check GitHub for latest release
    local latest_release=$(gh release list --limit 1 2>/dev/null | awk '{print $1}' | sed 's/^v//')

    if [[ -z "$latest_release" ]]; then
        # No releases found - this is the first release
        echo "0.0.0"
    else
        echo "$latest_release"
    fi
}

# Get version from local files (for reference/debugging only)
get_local_version() {
    grep '^version = ' pyproject.toml | sed 's/version = "\([^"]*\)"/\1/'
}

# Update version in pyproject.toml and __init__.py
update_version() {
    local new_version="$1"

    # Update pyproject.toml
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's/^version = ".*"/version = "'"$new_version"'"/' pyproject.toml
    else
        sed -i 's/^version = ".*"/version = "'"$new_version"'"/' pyproject.toml
    fi

    # Update __init__.py
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's/^__version__ = ".*"/__version__ = "'"$new_version"'"/' src/ascii_guard/__init__.py
    else
        sed -i 's/^__version__ = ".*"/__version__ = "'"$new_version"'"/' src/ascii_guard/__init__.py
    fi
}

# Ensure file has final newline (pre-commit requirement)
ensure_final_newline() {
    local file="$1"
    if [[ -f "$file" ]] && [[ -n "$(tail -c1 "$file" 2>/dev/null)" ]]; then
        echo >> "$file"
    fi
}

# Get last tag or initial commit
get_last_tag() {
    local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    if [[ -z "$last_tag" ]]; then
        git rev-list --max-parents=0 HEAD 2>/dev/null || git log --reverse --pretty=format:%H | head -1
    else
        echo "$last_tag"
    fi
}

# Analyze commits to determine version bump type
analyze_commits() {
    local last_tag="$1"
    local commit_range

    if [[ -z "$last_tag" ]] || [[ ! "$last_tag" =~ ^v ]]; then
        commit_range="HEAD"
    else
        commit_range="${last_tag}..HEAD"
    fi

    local commits
    commits=$(git log "$commit_range" --pretty=format:"%s" --no-merges 2>/dev/null) || commits=""

    if [[ -z "$commits" ]]; then
        echo "patch"
        return
    fi

    local highest_level="patch"
    local commit_hashes

    if [[ "$commit_range" == "HEAD" ]]; then
        commit_hashes=$(git log "$commit_range" --pretty=format:"%H" --no-merges 2>/dev/null || echo "")
    else
        commit_hashes=$(git log "$commit_range" --pretty=format:"%H" --no-merges 2>/dev/null || echo "")
    fi

    while IFS= read -r commit_hash || [[ -n "$commit_hash" ]]; do
        [[ -z "$commit_hash" ]] && continue

        local commit=$(git log -1 --pretty=format:"%s" "$commit_hash" 2>/dev/null || echo "")
        [[ -z "$commit" ]] && continue

        local lower_commit=$(echo "$commit" | tr '[:upper:]' '[:lower:]' 2>/dev/null || echo "$commit")

        # Check for MAJOR - Breaking changes
        if (echo "$commit" | grep -qi "BREAKING" || echo "$commit" | grep -qi "!:") ||
           [[ "$lower_commit" =~ ^(feat|fix|refactor|perf)!: ]]; then
            echo "major"
            return
        # Check for MINOR - New features
        elif [[ "$lower_commit" =~ ^(feat|feature): ]]; then
            if [[ "$highest_level" != "major" ]]; then
                highest_level="minor"
            fi
        fi
    done <<< "$commit_hashes"

    echo "$highest_level"
}

# Calculate next version
calculate_next_version() {
    local current_version="$1"
    local bump_type="$2"

    IFS='.' read -r major minor patch <<< "$current_version"

    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Get GitHub repository URL
get_repo_url() {
    local remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ -z "$remote_url" ]]; then
        echo "https://github.com/fxstein/ascii-guard"
        return
    fi

    if [[ "$remote_url" =~ git@github.com: ]]; then
        remote_url=$(echo "$remote_url" | sed 's/git@github.com:/https:\/\/github.com\//')
    fi

    remote_url=$(echo "$remote_url" | sed 's/\.git$//')

    echo "$remote_url"
}

# Generate release notes from commits
generate_release_notes() {
    local last_tag="$1"
    local new_version="$2"
    local commit_range

    if [[ -z "$last_tag" ]] || [[ ! "$last_tag" =~ ^v ]]; then
        commit_range="HEAD"
    else
        commit_range="${last_tag}..HEAD"
    fi

    local repo_url=$(get_repo_url)
    local ai_summary="release/AI_RELEASE_SUMMARY.md"
    local release_notes="release/RELEASE_NOTES.md"
    local summary_content=""

    # Check if AI-written summary exists
    if [[ -f "$ai_summary" ]]; then
        summary_content=$(cat "$ai_summary")
    fi

    # Start building release notes
    echo "## Release ${new_version}" > "$release_notes"
    echo "" >> "$release_notes"

    # Add AI summary if it existed
    if [[ -n "$summary_content" ]]; then
        echo "$summary_content" >> "$release_notes"
        echo "" >> "$release_notes"
        echo "---" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    # Categorize commits
    local breaking_commits=()
    local added_commits=()
    local changed_commits=()
    local fixed_commits=()
    local other_commits=()

    while IFS= read -r commit; do
        local commit_short=$(echo "$commit" | cut -d'|' -f1)
        local commit_full=$(git rev-parse "$commit_short" 2>/dev/null || echo "$commit_short")
        local commit_msg=$(echo "$commit" | cut -d'|' -f2- | sed 's/^ *//')
        local lower_msg=$(echo "$commit_msg" | tr '[:upper:]' '[:lower:]')
        local commit_link="([${commit_short}](${repo_url}/commit/${commit_full}))"

        # Skip version bumps and release commits
        if [[ "$lower_msg" =~ ^(bump.*version|release:) ]]; then
            continue
        fi

        # Categorize commits
        if [[ "$lower_msg" =~ (breaking|!:) ]]; then
            breaking_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ ^(feat|feature): ]] ||
             [[ "$lower_msg" =~ (add|new|implement|create) ]]; then
            added_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ (change|update|refactor|improve|enhance) ]]; then
            changed_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ ^fix: ]] ||
             [[ "$lower_msg" =~ (fix|correct|resolve) ]]; then
            fixed_commits+=("- ${commit_msg} ${commit_link}")
        else
            other_commits+=("- ${commit_msg} ${commit_link}")
        fi
    done < <(git log "$commit_range" --pretty=format:"%h|%s" --no-merges 2>/dev/null || echo "")

    # Write categorized commits to release notes
    if [[ ${#breaking_commits[@]} -gt 0 ]]; then
        echo "### ⚠️ Breaking Changes" >> "$release_notes"
        echo "" >> "$release_notes"
        printf '%s\n' "${breaking_commits[@]}" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    if [[ ${#added_commits[@]} -gt 0 ]]; then
        echo "### ✨ Added" >> "$release_notes"
        echo "" >> "$release_notes"
        printf '%s\n' "${added_commits[@]}" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    if [[ ${#changed_commits[@]} -gt 0 ]]; then
        echo "### 🔄 Changed" >> "$release_notes"
        echo "" >> "$release_notes"
        printf '%s\n' "${changed_commits[@]}" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    if [[ ${#fixed_commits[@]} -gt 0 ]]; then
        echo "### 🐛 Fixed" >> "$release_notes"
        echo "" >> "$release_notes"
        printf '%s\n' "${fixed_commits[@]}" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    # Count total commits
    local total_commits=$((${#breaking_commits[@]} + ${#added_commits[@]} + ${#changed_commits[@]} + ${#fixed_commits[@]} + ${#other_commits[@]}))

    if [[ ${#other_commits[@]} -gt 0 ]]; then
        echo "*Documentation, maintenance, and other commits: ${#other_commits[@]}*" >> "$release_notes"
        echo "" >> "$release_notes"
    fi

    echo "*Total commits: ${total_commits}*" >> "$release_notes"

    ensure_final_newline "$release_notes"
    echo "$release_notes"
}

# Validate version format (X.Y.Z)
validate_version_format() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        return 1
    fi
    return 0
}

# Validate version progression (new > current)
validate_version_gt() {
    local current="$1"
    local new="$2"

    IFS='.' read -r curr_major curr_minor curr_patch <<< "$current"
    IFS='.' read -r new_major new_minor new_patch <<< "$new"

    # Compare major
    if [[ $new_major -gt $curr_major ]]; then
        return 0
    elif [[ $new_major -lt $curr_major ]]; then
        return 1
    fi

    # Compare minor
    if [[ $new_minor -gt $curr_minor ]]; then
        return 0
    elif [[ $new_minor -lt $curr_minor ]]; then
        return 1
    fi

    # Compare patch
    if [[ $new_patch -gt $curr_patch ]]; then
        return 0
    fi

    return 1
}

# Set version override
set_version_override() {
    local new_version="$1"
    local PREPARE_STATE_FILE="release/.prepare_state"

    # Check if prepare was run
    if [[ ! -f "$PREPARE_STATE_FILE" ]]; then
        echo -e "${RED}❌ Error: Release not prepared${NC}"
        echo "Please run: ./release/release.sh --prepare first"
        exit 1
    fi

    # Load prepare state
    source "$PREPARE_STATE_FILE"

    # Validate version format
    if ! validate_version_format "$new_version"; then
        echo -e "${RED}❌ Error: Invalid version format${NC}"
        echo "Version must be in X.Y.Z format (e.g., 1.0.0)"
        exit 1
    fi

    # Validate version progression
    if ! validate_version_gt "$CURRENT_VERSION" "$new_version"; then
        echo -e "${RED}❌ Error: New version must be greater than current version${NC}"
        echo "Current: ${CURRENT_VERSION}"
        echo "New: ${new_version}"
        exit 1
    fi

    # Determine bump type
    IFS='.' read -r curr_major curr_minor curr_patch <<< "$CURRENT_VERSION"
    IFS='.' read -r new_major new_minor new_patch <<< "$new_version"

    local new_bump_type="patch"
    if [[ $new_major -gt $curr_major ]]; then
        new_bump_type="major"
    elif [[ $new_minor -gt $curr_minor ]]; then
        new_bump_type="minor"
    fi

    # Update RELEASE_NOTES.md header
    if [[ -f "release/RELEASE_NOTES.md" ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/^## Release ${NEW_VERSION}/## Release ${new_version}/" release/RELEASE_NOTES.md
        else
            sed -i "s/^## Release ${NEW_VERSION}/## Release ${new_version}/" release/RELEASE_NOTES.md
        fi
    fi

    # Update all version files
    update_version "$new_version"
    log_release_step "VERSION FILES OVERRIDDEN" "Updated all version files to ${new_version}"

    # Update prepare state
    cat > "$PREPARE_STATE_FILE" << EOF
NEW_VERSION=$new_version
BUMP_TYPE=$new_bump_type
CURRENT_VERSION=$CURRENT_VERSION
LAST_TAG=$LAST_TAG
RELEASE_NOTES_FILE=release/RELEASE_NOTES.md
EOF

    log_release_step "VERSION OVERRIDE" "Version override: ${NEW_VERSION} → ${new_version} (${new_bump_type})"

    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Version override successful!${NC}"
    echo ""
    echo -e "${GREEN}📋 Current version: ${CURRENT_VERSION}${NC}"
    echo -e "${GREEN}📋 Auto-detected: ${NEW_VERSION} (${BUMP_TYPE})${NC}"
    echo -e "${GREEN}📋 New version: ${new_version} (${new_bump_type})${NC}"
    echo ""
    echo -e "${YELLOW}📝 Updated: release/RELEASE_NOTES.md${NC}"
    echo ""
    echo -e "${GREEN}When ready, execute this release:${NC}"
    echo -e "${GREEN}  ./release/release.sh --execute${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    return 0
}

# Execute prepared release
execute_release() {
    local DRY_RUN="${1:-false}"
    local PREPARE_STATE_FILE="release/.prepare_state"

    if [[ ! -f "$PREPARE_STATE_FILE" ]]; then
        echo -e "${RED}❌ Error: Release not prepared${NC}"
        echo "Please run: ./release/release.sh --prepare"
        exit 1
    fi

    source "$PREPARE_STATE_FILE"

    # Check if any commits were made since prepare
    # This would invalidate the prepared release notes
    local prepare_timestamp=$(stat -f %m "$PREPARE_STATE_FILE" 2>/dev/null || stat -c %Y "$PREPARE_STATE_FILE" 2>/dev/null)
    local last_commit_timestamp=$(git log -1 --format=%ct 2>/dev/null || echo 0)

    if [[ $last_commit_timestamp -gt $prepare_timestamp ]]; then
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}❌ ERROR: Release process invalidated${NC}"
        echo ""
        echo -e "${YELLOW}Commits were made after running --prepare${NC}"
        echo -e "${YELLOW}The prepared release notes are now outdated${NC}"
        echo ""
        echo -e "${RED}You must restart the release process:${NC}"
        echo -e "${RED}1. Delete working files: rm -f release/.prepare_state release/AI_RELEASE_SUMMARY.md release/RELEASE_NOTES.md${NC}"
        echo -e "${RED}2. Run: ./release/release.sh --prepare${NC}"
        echo -e "${RED}3. Review: release/RELEASE_NOTES.md${NC}"
        echo -e "${RED}4. Run: ./release/release.sh --execute${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        exit 1
    fi

    echo -e "${BLUE}🚀 Executing release ${NEW_VERSION}...${NC}"
    echo ""

    # Copy RELEASE_NOTES.md to RELEASE_SUMMARY.md (for historical record)
    if [[ -f "release/RELEASE_NOTES.md" ]]; then
        echo -e "${BLUE}📝 Copying release notes to summary...${NC}"
        cp release/RELEASE_NOTES.md release/RELEASE_SUMMARY.md
        ensure_final_newline "release/RELEASE_SUMMARY.md"
        log_release_step "COPY NOTES" "Copied RELEASE_NOTES.md to RELEASE_SUMMARY.md"
    fi

    # Note: Version files were already updated during --prepare phase
    # This allows review of actual changes before commit

    # Build Python package
    echo -e "${BLUE}📦 Building Python package...${NC}"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY-RUN] Would clean previous builds${NC}"
        echo -e "${YELLOW}[DRY-RUN] Would run: python3 -m build${NC}"
        echo -e "${YELLOW}[DRY-RUN] Package build simulated successfully${NC}"
    else
        log_release_step "BUILD PACKAGE" "Building wheel and sdist"

        # Clean previous builds
        rm -rf dist/ build/ src/*.egg-info

        # Build using python -m build
        python3 -m build

        if [[ $? -ne 0 ]]; then
            echo -e "${RED}❌ Error: Package build failed${NC}"
            log_release_step "BUILD FAILED" "Package build failed"
            exit 1
        fi

        log_release_step "BUILD SUCCESS" "Package built successfully"
    fi

    # Commit version change and release files
    echo -e "${BLUE}💾 Committing version change and release notes...${NC}"
    log_release_step "COMMIT VERSION" "Committing version change and release files to git"
    git add pyproject.toml src/ascii_guard/__init__.py

    # Add all release files (historical record)
    if [[ -f "release/RELEASE_SUMMARY.md" ]]; then
        git add release/RELEASE_SUMMARY.md
    fi
    if [[ -f "release/AI_RELEASE_SUMMARY.md" ]]; then
        git add release/AI_RELEASE_SUMMARY.md
    fi
    if [[ -f "release/RELEASE_NOTES.md" ]]; then
        git add release/RELEASE_NOTES.md
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY-RUN] Would commit with message: 'release: Version $NEW_VERSION'${NC}"
        local version_commit_hash="DRY_RUN_COMMIT_HASH"
    else
        git commit -m "release: Version $NEW_VERSION

Release $BUMP_TYPE version."

        local version_commit_hash=$(git rev-parse HEAD)
        log_release_step "VERSION COMMITTED" "Version change committed: ${version_commit_hash}"
    fi

    # Create and push tag
    TAG="v${NEW_VERSION}"
    echo -e "${BLUE}🏷️  Creating tag ${TAG}...${NC}"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY-RUN] Would create tag: ${TAG}${NC}"
        echo -e "${YELLOW}[DRY-RUN] Would push main branch to origin${NC}"
        echo -e "${YELLOW}[DRY-RUN] Would push tag ${TAG} to origin${NC}"
    else
        log_release_step "CREATE TAG" "Creating git tag: ${TAG}"
        git tag -a "$TAG" -m "Release version $NEW_VERSION" "$version_commit_hash"
        log_release_step "TAG CREATED" "Git tag ${TAG} created successfully"

        echo -e "${BLUE}📤 Pushing to remote...${NC}"
        log_release_step "PUSH MAIN" "Pushing main branch to origin"
        git push origin main

        log_release_step "PUSH TAG" "Pushing tag ${TAG} to origin"
        git push origin "$TAG"
    fi

    echo ""
    echo -e "${YELLOW}⏳ Waiting for GitHub Actions to build and publish...${NC}"
    echo -e "${YELLOW}   GitHub Actions will:${NC}"
    echo -e "${YELLOW}   1. Build the package${NC}"
    echo -e "${YELLOW}   2. Run tests${NC}"
    echo -e "${YELLOW}   3. Publish to PyPI (trusted publishing)${NC}"
    echo -e "${YELLOW}   4. Create GitHub release${NC}"
    echo ""
    echo -e "${BLUE}🔗 Monitor at: $(get_repo_url)/actions${NC}"
    echo ""

    log_release_step "GITHUB ACTIONS" "Tag pushed, GitHub Actions will handle PyPI publish and GitHub release"

    # Cleanup working files (AI_RELEASE_SUMMARY.md was committed, now delete it)
    echo -e "${BLUE}🧹 Cleaning up release artifacts...${NC}"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY-RUN] Would delete AI_RELEASE_SUMMARY.md${NC}"
        echo -e "${YELLOW}[DRY-RUN] Would delete RELEASE_NOTES.md${NC}"
        echo -e "${YELLOW}[DRY-RUN] Would commit cleanup${NC}"
    else
        # Delete AI summary and RELEASE_NOTES (they were committed with the release)
        rm -f "release/AI_RELEASE_SUMMARY.md"
        rm -f "release/RELEASE_NOTES.md"

        # Commit the deletion to keep dev environment clean
        git add release/AI_RELEASE_SUMMARY.md release/RELEASE_NOTES.md 2>/dev/null || true
        if git diff --cached --quiet; then
            echo -e "${YELLOW}No release artifacts to clean up${NC}"
        else
            git commit -m "chore: Clean up release artifacts for v${NEW_VERSION}" > /dev/null 2>&1
            git push origin main > /dev/null 2>&1 || true
            log_release_step "CLEANUP COMMITTED" "Committed cleanup of release artifacts"
        fi
    fi

    # Delete local working files (not tracked)
    rm -f "$PREPARE_STATE_FILE"
    rm -rf dist/ build/ src/*.egg-info
    log_release_step "CLEANUP" "Deleted working files and build artifacts"

    local repo_url=$(get_repo_url)
    log_release_step "RELEASE INITIATED" "Release ${NEW_VERSION} initiated! GitHub Actions will complete publishing."

    # Commit release log
    if [[ -f "$RELEASE_LOG" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            echo -e "${YELLOW}[DRY-RUN] Would commit and push release log${NC}"
        else
            echo -e "${BLUE}📋 Committing release log...${NC}"
            git add "$RELEASE_LOG"
            git commit -m "chore: Update release log for ${NEW_VERSION}" > /dev/null 2>&1 || true
            git push origin main > /dev/null 2>&1 || true
        fi
    fi

    echo ""
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}✅ DRY-RUN COMPLETE - No actual release was performed${NC}"
        echo ""
        echo -e "${YELLOW}📋 What would have happened:${NC}"
        echo -e "${YELLOW}   • Version files updated to ${NEW_VERSION}${NC}"
        echo -e "${YELLOW}   • Package built successfully${NC}"
        echo -e "${YELLOW}   • Changes committed${NC}"
        echo -e "${YELLOW}   • Tag ${TAG} created and pushed${NC}"
        echo -e "${YELLOW}   • GitHub Actions triggered for PyPI publish${NC}"
        echo ""
        echo -e "${GREEN}To perform the actual release, run:${NC}"
        echo -e "${GREEN}  ./release/release.sh --execute${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    else
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}✅ Release ${NEW_VERSION} initiated successfully!${NC}"
        echo ""
        echo -e "${GREEN}📋 Tag ${TAG} pushed to GitHub${NC}"
        echo -e "${GREEN}📋 GitHub Actions is now handling:${NC}"
        echo -e "${GREEN}   • Building and testing${NC}"
        echo -e "${GREEN}   • Publishing to PyPI${NC}"
        echo -e "${GREEN}   • Creating GitHub release${NC}"
        echo ""
        echo -e "${GREEN}🔗 Monitor: ${repo_url}/actions${NC}"
        echo -e "${GREEN}📦 PyPI (when complete): https://pypi.org/project/ascii-guard/${NC}"
        echo -e "${GREEN}📋 Release log: ${RELEASE_LOG}${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    fi
}

# Main release process
main() {
    local MODE="prepare"
    local PREPARE_STATE_FILE="release/.prepare_state"
    local SET_VERSION=""
    local DRY_RUN=false

    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --prepare)
                MODE="prepare"
                shift
                ;;
            --execute)
                MODE="execute"
                shift
                ;;
            --set-version)
                MODE="set-version"
                SET_VERSION="$2"
                if [[ -z "$SET_VERSION" ]]; then
                    echo -e "${RED}❌ Error: --set-version requires a version number${NC}"
                    echo "Usage: $0 --set-version X.Y.Z"
                    exit 1
                fi
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Usage: $0 [--prepare|--execute|--set-version X.Y.Z] [--dry-run]"
                exit 1
                ;;
        esac
    done

    # Set version mode
    if [[ "$MODE" == "set-version" ]]; then
        set_version_override "$SET_VERSION"
        return $?
    fi

    # Execute mode
    if [[ "$MODE" == "execute" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${YELLOW}🧪 DRY-RUN MODE ENABLED${NC}"
            echo -e "${YELLOW}No actual git operations will be performed${NC}"
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo ""
        fi
        execute_release "$DRY_RUN"
        return $?
    fi

    # Prepare mode
    echo -e "${BLUE}🚀 Preparing release preview...${NC}"
    echo ""

    # Validate environment first
    if ! validate_environment; then
        exit 1
    fi

    # Check for uncommitted changes (exclude audit logs and release working files)
    local status_output=$(git status -s | grep -vE "release/RELEASE_LOG\.log|release/RELEASE_SUMMARY\.md|release/AI_RELEASE_SUMMARY\.md|release/RELEASE_NOTES\.md|release/\.prepare_state")
    if [[ -n "$status_output" ]]; then
        echo -e "${RED}❌ Error: Uncommitted changes detected${NC}"
        echo "Please commit or stash changes before releasing"
        exit 1
    fi

    # Get current version
    CURRENT_VERSION=$(get_current_version)
    echo -e "${GREEN}📌 Current version: ${CURRENT_VERSION}${NC}"

    # Get last tag
    LAST_TAG=$(get_last_tag)
    if [[ "$LAST_TAG" =~ ^v ]]; then
        echo -e "${GREEN}📌 Last release: ${LAST_TAG}${NC}"
    else
        echo -e "${YELLOW}📌 No previous release found${NC}"
    fi

    # Analyze commits
    echo ""
    echo -e "${BLUE}📊 Analyzing commits...${NC}"
    BUMP_TYPE=$(analyze_commits "$LAST_TAG")

    case "$BUMP_TYPE" in
        major)
            echo -e "${RED}🔴 Major release detected (breaking changes)${NC}"
            ;;
        minor)
            echo -e "${YELLOW}🟡 Minor release detected (new features)${NC}"
            ;;
        patch)
            echo -e "${GREEN}🟢 Patch release detected (bug fixes)${NC}"
            ;;
    esac

    # Calculate next version
    NEW_VERSION=$(calculate_next_version "$CURRENT_VERSION" "$BUMP_TYPE")
    echo -e "${GREEN}📌 Proposed new version: ${NEW_VERSION}${NC}"
    echo ""

    log_release_step "RELEASE START" "Starting release process: ${CURRENT_VERSION} → ${NEW_VERSION} (${BUMP_TYPE})"

    # Generate release notes
    echo -e "${BLUE}📝 Generating release notes...${NC}"
    RELEASE_NOTES_FILE=$(generate_release_notes "$LAST_TAG" "$NEW_VERSION")

    # Show release notes preview
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    cat "$RELEASE_NOTES_FILE"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Update version files (allows review before execute)
    echo -e "${BLUE}📝 Updating version files...${NC}"
    update_version "$NEW_VERSION"
    log_release_step "VERSION FILES UPDATED" "Updated all version files to ${NEW_VERSION} (not yet committed)"
    echo -e "${GREEN}✅ Version files updated (review before execute)${NC}"
    echo ""

    # Save prepare state
    cat > "$PREPARE_STATE_FILE" << EOF
NEW_VERSION=$NEW_VERSION
BUMP_TYPE=$BUMP_TYPE
CURRENT_VERSION=$CURRENT_VERSION
LAST_TAG=$LAST_TAG
RELEASE_NOTES_FILE=$RELEASE_NOTES_FILE
EOF
    log_release_step "PREPARE" "Release preview prepared for v${NEW_VERSION}"

    # Display execution command
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Release preview prepared successfully!${NC}"
    echo ""
    echo -e "${GREEN}📋 Version: ${CURRENT_VERSION} → ${NEW_VERSION}${NC}"
    echo -e "${GREEN}📋 Type: ${BUMP_TYPE} release${NC}"
    echo ""
    echo -e "${YELLOW}📝 REVIEW AND EDIT: release/RELEASE_NOTES.md${NC}"
    echo -e "${YELLOW}   (This is the file that will be used for the release)${NC}"
    echo ""
    echo -e "${GREEN}When ready, execute this release:${NC}"
    echo -e "${GREEN}  ./release/release.sh --execute${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    return 0
}

# Run main function
main "$@"

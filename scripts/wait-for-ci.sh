#!/bin/zsh
# wait-for-ci.sh - Wait for all CI/CD workflows to complete
# Usage: ./scripts/wait-for-ci.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking CI/CD status...${NC}"
echo ""

# Get all running or queued workflows
WORKFLOWS=$(gh run list --limit 10 --json name,status,conclusion,event \
    --jq '.[] | select(.status != "completed") | .name' | sort -u)

if [ -z "$WORKFLOWS" ]; then
    # Check if latest runs were successful
    LATEST=$(gh run list --limit 3 --json name,status,conclusion \
        --jq '.[] | select(.status == "completed")')

    ALL_SUCCESS=true
    while IFS= read -r line; do
        CONCLUSION=$(echo "$line" | grep -o '"conclusion":"[^"]*"' | cut -d'"' -f4)
        if [ "$CONCLUSION" != "success" ]; then
            ALL_SUCCESS=false
            break
        fi
    done <<< "$LATEST"

    if $ALL_SUCCESS; then
        echo -e "${GREEN}✅ All workflows completed successfully!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Some workflows completed with failures${NC}"
        echo ""
        gh run list --limit 5 --json name,status,conclusion \
            --jq '.[] | "\(.name): \(.conclusion)"'
        exit 1
    fi
fi

# Monitor each workflow
echo -e "${YELLOW}Active workflows:${NC}"
echo "$WORKFLOWS" | sed 's/^/  - /'
echo ""

# Wait for all workflows to complete
TIMEOUT=600  # 10 minutes total
POLL_INTERVAL=10
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
    RUNNING=$(gh run list --limit 10 --json name,status \
        --jq '.[] | select(.status != "completed") | .name' | wc -l | tr -d ' ')

    if [ "$RUNNING" -eq 0 ]; then
        # All workflows completed, check conclusions
        echo ""
        FAILURES=$(gh run list --limit 5 --json name,status,conclusion \
            --jq '.[] | select(.conclusion != "success") | .name' | wc -l | tr -d ' ')

        if [ "$FAILURES" -eq 0 ]; then
            echo -e "${GREEN}✅ All workflows completed successfully!${NC}"
            exit 0
        else
            echo -e "${RED}❌ Some workflows failed!${NC}"
            echo ""
            gh run list --limit 5 --json name,status,conclusion \
                --jq '.[] | select(.conclusion != "success") | "\(.name): \(.conclusion)"'
            exit 1
        fi
    fi

    # Show progress
    ELAPSED_MIN=$((ELAPSED / 60))
    ELAPSED_SEC=$((ELAPSED % 60))
    printf "\r${BLUE}⏳ Waiting for ${RUNNING} workflow(s)${NC} [%02d:%02d]" $ELAPSED_MIN $ELAPSED_SEC

    sleep $POLL_INTERVAL
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

# Timeout
echo ""
echo -e "${RED}❌ Timeout waiting for workflows${NC}"
exit 4

#!/bin/zsh
# monitor-ci.sh - Clean CI/CD workflow monitoring
# Usage: ./scripts/monitor-ci.sh [workflow-name] [timeout-minutes]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
WORKFLOW_NAME="${1:-CI}"
TIMEOUT_MINUTES="${2:-10}"
POLL_INTERVAL=5  # seconds

echo -e "${BLUE}🔍 Monitoring workflow: ${WORKFLOW_NAME}${NC}"
echo ""

# Calculate timeout
TIMEOUT_SECONDS=$((TIMEOUT_MINUTES * 60))
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT_SECONDS ]; do
    # Get latest run for the specified workflow
    RESULT=$(gh run list --limit 1 --json name,status,conclusion,event,createdAt \
        --jq ".[] | select(.name == \"${WORKFLOW_NAME}\")" 2>/dev/null || echo "")

    if [ -z "$RESULT" ]; then
        echo -e "${YELLOW}⏳ Waiting for workflow to start...${NC}"
        sleep $POLL_INTERVAL
        ELAPSED=$((ELAPSED + POLL_INTERVAL))
        continue
    fi

    # Parse status and conclusion
    STATUS=$(echo "$RESULT" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    CONCLUSION=$(echo "$RESULT" | grep -o '"conclusion":"[^"]*"' | cut -d'"' -f4)

    if [ "$STATUS" = "completed" ]; then
        echo ""
        if [ "$CONCLUSION" = "success" ]; then
            echo -e "${GREEN}✅ ${WORKFLOW_NAME} completed successfully!${NC}"
            exit 0
        elif [ "$CONCLUSION" = "failure" ]; then
            echo -e "${RED}❌ ${WORKFLOW_NAME} failed!${NC}"
            echo ""
            echo -e "${YELLOW}View logs:${NC}"
            echo "  gh run view --log-failed"
            exit 1
        elif [ "$CONCLUSION" = "cancelled" ]; then
            echo -e "${YELLOW}⚠️  ${WORKFLOW_NAME} was cancelled${NC}"
            exit 2
        else
            echo -e "${YELLOW}⚠️  ${WORKFLOW_NAME} completed with status: ${CONCLUSION}${NC}"
            exit 3
        fi
    fi

    # Show progress indicator
    ELAPSED_MIN=$((ELAPSED / 60))
    ELAPSED_SEC=$((ELAPSED % 60))
    printf "\r${BLUE}⏳ ${WORKFLOW_NAME}: ${STATUS}${NC} [%02d:%02d]" $ELAPSED_MIN $ELAPSED_SEC

    sleep $POLL_INTERVAL
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

# Timeout reached
echo ""
echo -e "${RED}❌ Timeout after ${TIMEOUT_MINUTES} minutes${NC}"
echo ""
echo "Workflow status: $STATUS"
echo ""
echo -e "${YELLOW}Check manually:${NC}"
echo "  gh run list --limit 5"
exit 4

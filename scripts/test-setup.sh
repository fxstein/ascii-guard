#!/usr/bin/env bash
# test-setup.sh - Clean test of setup.sh after uv migration
# This script removes the existing venv and tests setup.sh from scratch
#
# Usage:
#   ./scripts/test-setup.sh
#
# This script:
# 1. Backs up current venv state (for reference)
# 2. Removes existing .venv and build artifacts
# 3. Verifies prerequisites (uv, python3)
# 4. Runs setup.sh from scratch
# 5. Verifies venv was created by uv
# 6. Verifies all packages and tools are working

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}🧪 Testing setup.sh after uv migration${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Backup current venv state (for reference)
if [[ -d .venv ]]; then
    echo -e "${BLUE}📋 Current venv info:${NC}"
    cat .venv/pyvenv.cfg 2>/dev/null || echo "  (no pyvenv.cfg)"
    echo ""

    echo -e "${BLUE}📦 Current packages (first 10):${NC}"
    uv pip list 2>/dev/null | head -12 || echo "  (could not list packages)"
    echo ""
fi

# Step 2: Remove existing venv
echo -e "${BLUE}🧹 Cleaning up existing .venv...${NC}"
if [[ -d .venv ]]; then
    rm -rf .venv
    echo -e "${GREEN}  ✓ Removed .venv${NC}"
else
    echo -e "${YELLOW}  ℹ No .venv to remove${NC}"
fi
echo ""

# Step 3: Remove any build artifacts
echo -e "${BLUE}🧹 Cleaning up build artifacts...${NC}"
rm -rf dist/ build/ src/*.egg-info 2>/dev/null || true
echo -e "${GREEN}  ✓ Cleaned build artifacts${NC}"
echo ""

# Step 4: Verify uv is available
echo -e "${BLUE}🔍 Verifying prerequisites...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${RED}  ❌ uv not found - cannot test${NC}"
    echo ""
    echo -e "${YELLOW}Install uv with:${NC}"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo -e "${GREEN}  ✓ uv is available: $(uv --version)${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}  ❌ python3 not found - cannot test${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ python3 is available: $(python3 --version)${NC}"
echo ""

# Step 5: Run setup.sh
echo -e "${BLUE}🚀 Running setup.sh...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

./setup.sh

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Test complete!${NC}"
echo ""

# Step 6: Verify the venv was created by uv
echo -e "${BLUE}🔍 Verifying venv was created by uv...${NC}"
if [[ -f .venv/pyvenv.cfg ]]; then
    if grep -q "uv = " .venv/pyvenv.cfg; then
        echo -e "${GREEN}  ✓ Venv created by uv${NC}"
        grep "uv = " .venv/pyvenv.cfg | sed 's/^/    /'
    else
        echo -e "${YELLOW}  ⚠️  Venv does not appear to be created by uv${NC}"
        cat .venv/pyvenv.cfg
    fi
else
    echo -e "${RED}  ❌ No pyvenv.cfg found${NC}"
fi
echo ""

# Step 7: Verify packages are installed
echo -e "${BLUE}📦 Verifying packages...${NC}"
ERRORS=0

if uv run python -c "import ascii_guard; print('✓ ascii-guard importable')" 2>/dev/null; then
    echo -e "${GREEN}  ✓ ascii-guard is importable${NC}"
else
    echo -e "${RED}  ❌ ascii-guard not importable${NC}"
    ERRORS=$((ERRORS + 1))
fi

if uv run pytest --version &> /dev/null; then
    echo -e "${GREEN}  ✓ pytest available${NC}"
else
    echo -e "${RED}  ❌ pytest not available${NC}"
    ERRORS=$((ERRORS + 1))
fi

if uv run ruff --version &> /dev/null; then
    echo -e "${GREEN}  ✓ ruff available${NC}"
else
    echo -e "${RED}  ❌ ruff not available${NC}"
    ERRORS=$((ERRORS + 1))
fi

if uv run mypy --version &> /dev/null; then
    echo -e "${GREEN}  ✓ mypy available${NC}"
else
    echo -e "${RED}  ❌ mypy not available${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ Verification failed with $ERRORS error(s)${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 All checks complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}To clean up after testing:${NC}"
echo "  rm -rf .venv"
echo ""

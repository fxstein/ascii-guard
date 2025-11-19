#!/bin/zsh
# setup.zsh - Complete development environment setup for ascii-guard
# One-step setup: creates venv, installs dependencies, configures git hooks, runs tests

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Emoji helpers (cross-platform safe)
ROCKET="🚀"
CHECK="✅"
WARNING="⚠️"
CROSS="❌"
PACKAGE="📦"
WRENCH="🔧"
TEST="🧪"
HOOK="🪝"

echo ""
echo "${BLUE}${ROCKET} ascii-guard Development Setup${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Check Python version
echo "${BLUE}1/6 Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "${RED}${CROSS} Error: python3 not found${NC}"
    echo "Please install Python 3.10 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"
echo "  Found Python ${PYTHON_VERSION}"

# Version comparison
MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [[ $MAJOR -lt 3 ]] || [[ $MAJOR -eq 3 && $MINOR -lt 10 ]]; then
    echo "${RED}${CROSS} Error: Python ${REQUIRED_VERSION}+ required, found ${PYTHON_VERSION}${NC}"
    exit 1
fi

echo "${GREEN}  ${CHECK} Python ${PYTHON_VERSION} OK${NC}"
echo ""

# Step 2: Create/verify virtual environment
echo "${BLUE}2/6 Setting up virtual environment...${NC}"
if [[ -d .venv ]]; then
    echo "${YELLOW}  ${WARNING} Virtual environment already exists${NC}"
    echo "  Reusing existing .venv/"
else
    echo "  Creating .venv/"
    python3 -m venv .venv
    echo "${GREEN}  ${CHECK} Virtual environment created${NC}"
fi
echo ""

# Step 3: Install dependencies
echo "${BLUE}3/6 Installing dependencies...${NC}"
echo "  Activating virtual environment..."
source .venv/bin/activate

echo "  Upgrading pip..."
pip install --upgrade pip --quiet

echo "  Installing ascii-guard with dev dependencies..."
pip install -e ".[dev]" --quiet

echo "${GREEN}  ${CHECK} Dependencies installed${NC}"
echo ""

# Step 4: Install pre-commit hooks
echo "${BLUE}4/6 Installing git hooks...${NC}"
if [[ -d .git ]]; then
    if .venv/bin/pre-commit --version &> /dev/null; then
        .venv/bin/pre-commit install
        echo "${GREEN}  ${CHECK} Pre-commit hooks installed${NC}"
    else
        echo "${RED}  ${CROSS} pre-commit not found (this shouldn't happen)${NC}"
        exit 1
    fi
else
    echo "${YELLOW}  ${WARNING} Not a git repository - skipping git hooks${NC}"
fi
echo ""

# Step 5: Verify installation
echo "${BLUE}5/6 Verifying installation...${NC}"

# Check ascii-guard command
if .venv/bin/ascii-guard --version &> /dev/null; then
    VERSION=$(.venv/bin/ascii-guard --version 2>&1)
    echo "  ${CHECK} ascii-guard CLI: ${VERSION}"
else
    echo "${RED}  ${CROSS} ascii-guard command failed${NC}"
    exit 1
fi

# Check dev tools
if .venv/bin/pytest --version &> /dev/null; then
    echo "  ${CHECK} pytest installed"
else
    echo "${RED}  ${CROSS} pytest not found${NC}"
    exit 1
fi

if .venv/bin/ruff --version &> /dev/null; then
    echo "  ${CHECK} ruff installed"
else
    echo "${RED}  ${CROSS} ruff not found${NC}"
    exit 1
fi

if .venv/bin/mypy --version &> /dev/null; then
    echo "  ${CHECK} mypy installed"
else
    echo "${RED}  ${CROSS} mypy not found${NC}"
    exit 1
fi

echo "${GREEN}  ${CHECK} All tools verified${NC}"
echo ""

# Step 6: Run quick test
echo "${BLUE}6/6 Running quick test suite...${NC}"
if .venv/bin/pytest -q --tb=short -m "not slow" tests/ 2>&1 | grep -q "passed"; then
    echo "${GREEN}  ${CHECK} Tests passed${NC}"
else
    echo "${YELLOW}  ${WARNING} Some tests failed (you may want to investigate)${NC}"
fi
echo ""

# Success summary
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}${CHECK} Setup complete!${NC}"
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "${GREEN}Development environment ready:${NC}"
echo "  • ${PACKAGE} ascii-guard (editable mode)"
echo "  • ${TEST} pytest + pytest-cov"
echo "  • ${WRENCH} ruff (linting + formatting)"
echo "  • ${WRENCH} mypy (type checking)"
echo "  • ${HOOK} pre-commit hooks (auto-run on commit)"
echo "  • ${PACKAGE} build + twine (packaging)"
echo ""
echo "${BLUE}Quick start:${NC}"
echo "  ${GREEN}source .venv/bin/activate${NC}   # Activate environment"
echo "  ${GREEN}pytest${NC}                      # Run full test suite"
echo "  ${GREEN}pytest --cov${NC}                # Run with coverage"
echo "  ${GREEN}ruff check .${NC}                # Lint code"
echo "  ${GREEN}mypy src/${NC}                   # Type check"
echo "  ${GREEN}ascii-guard lint README.md${NC}  # Try the tool"
echo ""
echo "${YELLOW}Note: Pre-commit hooks will run automatically on git commit${NC}"
echo "${YELLOW}      Run manually with: pre-commit run --all-files${NC}"
echo ""

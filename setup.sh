#!/usr/bin/env bash
# setup.sh - Complete development environment setup for ascii-guard
# One-step setup: creates venv with uv, installs dependencies, configures git hooks, runs tests
# Compatible with bash on Linux, macOS, Windows (WSL/Git Bash)

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
echo -e "${BLUE}${ROCKET} ascii-guard Development Setup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Check Python version
echo -e "${BLUE}1/6 Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}${CROSS} Error: python3 not found${NC}"
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
    echo -e "${RED}${CROSS} Error: Python ${REQUIRED_VERSION}+ required, found ${PYTHON_VERSION}${NC}"
    exit 1
fi

echo -e "${GREEN}  ${CHECK} Python ${PYTHON_VERSION} OK${NC}"
echo ""

# Step 2: Check for uv
echo -e "${BLUE}2/7 Checking for uv...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${RED}${CROSS} Error: uv not found${NC}"
    echo ""
    echo -e "${YELLOW}Install uv with one of these methods:${NC}"
    echo "  • curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  • brew install uv"
    echo "  • pipx install uv"
    echo ""
    echo "See: https://github.com/astral-sh/uv#installation"
    exit 1
fi

UV_VERSION=$(uv --version 2>&1 | awk '{print $2}' || echo "unknown")
echo "  Found uv ${UV_VERSION}"
echo -e "${GREEN}  ${CHECK} uv OK${NC}"
echo ""

# Step 3: Create/verify virtual environment
echo -e "${BLUE}3/7 Setting up virtual environment...${NC}"
if [[ -d .venv ]]; then
    echo -e "${YELLOW}  ${WARNING} Virtual environment already exists${NC}"
    echo "  Reusing existing .venv/"
else
    echo "  Creating .venv/ with uv..."
    uv venv
    echo -e "${GREEN}  ${CHECK} Virtual environment created${NC}"
fi
echo ""

# Step 4: Install dependencies
echo -e "${BLUE}4/7 Installing dependencies...${NC}"
echo "  Syncing dependencies from uv.lock..."
uv sync --extra dev

echo -e "${GREEN}  ${CHECK} Dependencies installed${NC}"
echo ""

# Step 5: Install pre-commit hooks
echo -e "${BLUE}5/7 Installing git hooks...${NC}"
if [[ -d .git ]]; then
    if .venv/bin/pre-commit --version &> /dev/null; then
        .venv/bin/pre-commit install
        echo -e "${GREEN}  ${CHECK} Pre-commit hooks installed${NC}"
    else
        echo -e "${RED}  ${CROSS} pre-commit not found (this shouldn't happen)${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}  ${WARNING} Not a git repository - skipping git hooks${NC}"
fi
echo ""

# Step 6: Verify installation
echo -e "${BLUE}6/7 Verifying installation...${NC}"

# Check ascii-guard command
if .venv/bin/ascii-guard --version &> /dev/null; then
    VERSION=$(.venv/bin/ascii-guard --version 2>&1)
    echo "  ${CHECK} ascii-guard CLI: ${VERSION}"
else
    echo -e "${RED}  ${CROSS} ascii-guard command failed${NC}"
    exit 1
fi

# Check dev tools
if .venv/bin/pytest --version &> /dev/null; then
    echo "  ${CHECK} pytest installed"
else
    echo -e "${RED}  ${CROSS} pytest not found${NC}"
    exit 1
fi

if .venv/bin/ruff --version &> /dev/null; then
    echo "  ${CHECK} ruff installed"
else
    echo -e "${RED}  ${CROSS} ruff not found${NC}"
    exit 1
fi

if .venv/bin/mypy --version &> /dev/null; then
    echo "  ${CHECK} mypy installed"
else
    echo -e "${RED}  ${CROSS} mypy not found${NC}"
    exit 1
fi

echo -e "${GREEN}  ${CHECK} All tools verified${NC}"
echo ""

# Step 7: Run quick test
echo -e "${BLUE}7/7 Running quick test suite...${NC}"
if .venv/bin/pytest -q --tb=short -m "not slow" tests/ 2>&1 | grep -q "passed"; then
    echo -e "${GREEN}  ${CHECK} Tests passed${NC}"
else
    echo -e "${YELLOW}  ${WARNING} Some tests failed (you may want to investigate)${NC}"
fi
echo ""

# Success summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${CHECK} Setup complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Development environment ready:${NC}"
echo "  • ${PACKAGE} ascii-guard (editable mode)"
echo "  • ${TEST} pytest + pytest-cov"
echo "  • ${WRENCH} ruff (linting + formatting)"
echo "  • ${WRENCH} mypy (type checking)"
echo "  • ${HOOK} pre-commit hooks (auto-run on commit)"
echo "  • ${PACKAGE} build + twine (packaging)"
echo ""
echo -e "${BLUE}Quick start:${NC}"
echo -e "  ${GREEN}uv run pytest${NC}               # Run full test suite"
echo -e "  ${GREEN}uv run pytest --cov${NC}         # Run with coverage"
echo -e "  ${GREEN}uv run ruff check .${NC}         # Lint code"
echo -e "  ${GREEN}uv run mypy src/${NC}            # Type check"
echo -e "  ${GREEN}uv run ascii-guard lint README.md${NC}  # Try the tool"
echo ""
echo -e "${YELLOW}Note: Use 'uv run <command>' instead of activating venv${NC}"
echo -e "${YELLOW}      Or activate manually: source .venv/bin/activate${NC}"
echo ""
echo -e "${YELLOW}Note: Pre-commit hooks will run automatically on git commit${NC}"
echo -e "${YELLOW}      Run manually with: pre-commit run --all-files${NC}"
echo ""

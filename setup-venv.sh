#!/bin/zsh
# setup-venv.sh - Virtual environment setup script for ascii-guard
# Ensures clean isolation with zero system pollution

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${BLUE}🚀 Setting up ascii-guard development environment...${NC}"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.12"

echo "${BLUE}📌 Detected Python: ${PYTHON_VERSION}${NC}"

# Simple version check (major.minor)
MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f1,2)
if [[ $(echo "$MAJOR_MINOR < $REQUIRED_VERSION" | bc -l 2>/dev/null || echo "0") -eq 1 ]]; then
    echo "${YELLOW}⚠️  Warning: Python ${REQUIRED_VERSION}+ recommended, found ${PYTHON_VERSION}${NC}"
fi

# Create virtual environment
if [[ -d .venv ]]; then
    echo "${YELLOW}📦 Virtual environment already exists${NC}"
else
    echo "${BLUE}📦 Creating virtual environment (.venv)...${NC}"
    python3 -m venv .venv
    echo "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "${BLUE}🔌 Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install package in editable mode with dev dependencies
echo "${BLUE}📦 Installing ascii-guard in editable mode with dev dependencies...${NC}"
pip install -e ".[dev]" --quiet

echo ""
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}✅ Development environment ready!${NC}"
echo ""
echo "${GREEN}Installed tools:${NC}"
echo "  • ascii-guard (editable mode)"
echo "  • pytest (testing)"
echo "  • ruff (linting)"
echo "  • mypy (type checking)"
echo "  • pre-commit (git hooks)"
echo "  • build + twine (packaging)"
echo ""
echo "${GREEN}Next steps:${NC}"
echo "  1. Activate venv: ${BLUE}source .venv/bin/activate${NC}"
echo "  2. Install git hooks: ${BLUE}pre-commit install${NC}"
echo "  3. Run tests: ${BLUE}pytest${NC}"
echo "  4. Run linter: ${BLUE}ruff check .${NC}"
echo ""
echo "${YELLOW}Note: Virtual environment is isolated - no system pollution!${NC}"
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

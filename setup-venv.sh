#!/usr/bin/env bash
# setup-venv.sh - Virtual environment setup script for ascii-guard
# Ensures clean isolation with zero system pollution
#
# NOTE: For full automated setup including git hooks, use ./setup.sh instead.
#       This script is kept for backward compatibility and minimal venv setup.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up ascii-guard development environment...${NC}"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

echo -e "${BLUE}📌 Detected Python: ${PYTHON_VERSION}${NC}"

# Simple version check (major.minor)
MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f1,2)
if [[ $(echo "$MAJOR_MINOR < $REQUIRED_VERSION" | bc -l 2>/dev/null || echo "0") -eq 1 ]]; then
    echo -e "${YELLOW}⚠️  Warning: Python ${REQUIRED_VERSION}+ recommended, found ${PYTHON_VERSION}${NC}"
fi

# Create virtual environment
if [[ -d .venv ]]; then
    echo -e "${YELLOW}📦 Virtual environment already exists${NC}"
else
    echo -e "${BLUE}📦 Creating virtual environment (.venv)...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔌 Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install package in editable mode with dev dependencies
echo -e "${BLUE}📦 Installing ascii-guard in editable mode with dev dependencies...${NC}"
pip install -e ".[dev]" --quiet

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Development environment ready!${NC}"
echo ""
echo -e "${GREEN}Installed tools:${NC}"
echo "  • ascii-guard (editable mode)"
echo "  • pytest (testing)"
echo "  • ruff (linting)"
echo "  • mypy (type checking)"
echo "  • pre-commit (git hooks)"
echo "  • build + twine (packaging)"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "  1. Activate venv: ${BLUE}source .venv/bin/activate${NC}"
echo -e "  2. Install git hooks: ${BLUE}pre-commit install${NC}"
echo -e "  3. Run tests: ${BLUE}pytest${NC}"
echo -e "  4. Run linter: ${BLUE}ruff check .${NC}"
echo ""
echo -e "${YELLOW}Note: Virtual environment is isolated - no system pollution!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

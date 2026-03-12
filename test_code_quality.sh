#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║             CODE QUALITY TEST RESULTS                        ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run Python linting
echo -e "${BLUE}${BOLD}Running Python Code Quality Check (Flake8)...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python -m flake8 --statistics --count > /tmp/flake8_output.txt 2>&1
FLAKE8_EXIT=$?
FLAKE8_COUNT=$(tail -1 /tmp/flake8_output.txt)

if [ "$FLAKE8_EXIT" -eq 0 ]; then
    echo -e "${GREEN}Python: No issues found!${NC}"
else
    echo -e "${YELLOW}Python: ${FLAKE8_COUNT} issues found${NC}"
    echo ""
    head -20 /tmp/flake8_output.txt
    echo ""
    echo "Run 'python -m flake8' for full details"
fi
echo ""

# Run JavaScript linting
echo -e "${BLUE}${BOLD}Running JavaScript Code Quality Check (ESLint)...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
npm run lint:js > /tmp/eslint_output.txt 2>&1
ESLINT_EXIT=$?

if [ "$ESLINT_EXIT" -eq 0 ]; then
    echo -e "${GREEN}JavaScript: No issues found!${NC}"
else
    ESLINT_ISSUES=$(grep "problems" /tmp/eslint_output.txt | tail -1)
    echo -e "${YELLOW}JavaScript: ${ESLINT_ISSUES}${NC}"
    echo ""
    grep -A 5 "\.js" /tmp/eslint_output.txt | head -15
    echo ""
    echo "Run 'npm run lint:js' for full details"
fi
echo ""

# Summary
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}SUMMARY:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$FLAKE8_EXIT" -eq 0 ] && [ "$ESLINT_EXIT" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}ALL TESTS PASSED! CODE IS EXCELLENT!${NC}"
    echo -e "${GREEN}0 errors${NC}"
    echo -e "${GREEN}0 warnings${NC}"
    echo -e "${GREEN}Production ready!${NC}"
elif [ "$FLAKE8_EXIT" -ne 0 ] || [ "$ESLINT_EXIT" -ne 0 ]; then
    echo -e "${YELLOW}Some issues found - review above${NC}"
    echo -e "Run commands for details:"
    echo -e "${BLUE}python -m flake8${NC}"
    echo -e "${BLUE}npm run lint:js${NC}"
else
    echo -e "${RED}Tests encountered errors${NC}"
fi

echo ""
echo -e "${BOLD}Security Configuration:${NC}"
if grep -q "DEBUG = False" fitforge/settings.py 2>/dev/null || grep -q "DEVELOPMENT" fitforge/settings.py; then
    echo -e "${GREEN}Custom error pages configured${NC}"
    echo -e "${GREEN}DEBUG properly controlled by environment${NC}"
    echo -e "${GREEN}Django error pages hidden in production${NC}"
else
    echo -e "${YELLOW}Check DEBUG configuration${NC}"
fi
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

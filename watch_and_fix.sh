#!/bin/bash
#
# BYRD Watch & Fix - Continuous error monitoring with Claude Code
#
# Usage:
#   ./watch_and_fix.sh              # Monitor BYRD output
#   ./watch_and_fix.sh --run        # Start BYRD and monitor
#   ./watch_and_fix.sh --log FILE   # Monitor specific log file
#

set -e

BYRD_DIR="/Users/kurultai/BYRD"
COOLDOWN=60  # Seconds between Claude invocations
LAST_FIX=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Error patterns to detect
ERROR_PATTERNS=(
    "Traceback (most recent call last)"
    "Error:"
    "Exception:"
    "ImportError"
    "ModuleNotFoundError"
    "Neo4j.*error"
    "observation.*BROKEN"
    "❌"
    "FAILED"
)

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║         BYRD Watch & Fix - Claude Code Monitor           ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Cooldown: ${COOLDOWN}s between fixes                             ║"
echo "║  Press Ctrl+C to stop                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Buffer for context
declare -a CONTEXT_BUFFER
BUFFER_SIZE=20

add_to_buffer() {
    CONTEXT_BUFFER+=("$1")
    if [ ${#CONTEXT_BUFFER[@]} -gt $BUFFER_SIZE ]; then
        CONTEXT_BUFFER=("${CONTEXT_BUFFER[@]:1}")
    fi
}

check_for_errors() {
    local line="$1"
    for pattern in "${ERROR_PATTERNS[@]}"; do
        if echo "$line" | grep -qE "$pattern"; then
            return 0  # Error found
        fi
    done
    return 1  # No error
}

invoke_claude() {
    local error_line="$1"
    local now=$(date +%s)
    local elapsed=$((now - LAST_FIX))

    if [ $elapsed -lt $COOLDOWN ]; then
        echo -e "${YELLOW}⏳ Cooldown: $((COOLDOWN - elapsed))s remaining${NC}"
        return
    fi

    echo -e "${CYAN}🔧 Invoking Claude Code...${NC}"

    # Build context
    local context=$(printf '%s\n' "${CONTEXT_BUFFER[@]}")

    # Create prompt
    local prompt="BYRD Error Detected - Please investigate and fix:

Error line:
$error_line

Context (last $BUFFER_SIZE lines):
\`\`\`
$context
\`\`\`

Please:
1. Identify the root cause
2. Read relevant files if needed
3. Apply a fix
4. Verify the fix works"

    # Invoke Claude Code
    cd "$BYRD_DIR"
    echo "$prompt" | claude --print 2>&1 | head -100

    LAST_FIX=$(date +%s)
    echo -e "${GREEN}✅ Claude Code invoked${NC}"
}

monitor_output() {
    while IFS= read -r line; do
        echo "$line"  # Pass through
        add_to_buffer "$line"

        if check_for_errors "$line"; then
            echo -e "\n${RED}🚨 ERROR DETECTED${NC}"
            invoke_claude "$line"
            echo ""
        fi
    done
}

# Main
case "${1:-}" in
    --run)
        echo -e "${GREEN}Starting BYRD with monitoring...${NC}"
        cd "$BYRD_DIR"
        python byrd.py 2>&1 | monitor_output
        ;;
    --log)
        LOG_FILE="${2:-byrd.log}"
        echo -e "${GREEN}Monitoring log file: $LOG_FILE${NC}"
        tail -F "$LOG_FILE" 2>/dev/null | monitor_output
        ;;
    *)
        echo "Usage:"
        echo "  $0 --run       Start BYRD and monitor"
        echo "  $0 --log FILE  Monitor a log file"
        echo ""
        echo "Or pipe BYRD output:"
        echo "  python byrd.py 2>&1 | $0"

        # If stdin is not a terminal, monitor it
        if [ ! -t 0 ]; then
            monitor_output
        fi
        ;;
esac

#!/bin/bash
# BYRD Home Voice Server Launcher
#
# This script starts the Chatterbox TTS server on your Mac.
# Run this on your home Mac to enable free, unlimited voice synthesis.

set -e

# Configuration
PORT=${PORT:-5050}
HOST=${HOST:-127.0.0.1}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           BYRD Home Voice Server - Launcher                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: Not in a virtual environment.${NC}"
    echo "Consider creating one:"
    echo "  python3 -m venv venv && source venv/bin/activate"
    echo ""
fi

# Check dependencies
echo "Checking dependencies..."
if ! python3 -c "import chatterbox" 2>/dev/null; then
    echo -e "${YELLOW}Chatterbox TTS not installed. Installing...${NC}"
    pip install -r "$SCRIPT_DIR/mac_voice_requirements.txt"
fi

# Create voice reference directory
mkdir -p ~/.byrd/voices

# Check for GPU
echo ""
echo "Checking hardware..."
python3 -c "
import torch
if torch.backends.mps.is_available():
    print('✓ Apple Silicon (MPS) detected - GPU acceleration enabled')
elif torch.cuda.is_available():
    print('✓ NVIDIA GPU detected - CUDA acceleration enabled')
else:
    print('⚠ No GPU detected - using CPU (slower)')
"

echo ""
echo -e "${GREEN}Starting server on http://${HOST}:${PORT}${NC}"
echo ""
echo "To expose remotely, use a reverse proxy or tunnel service."
echo "Then set the URL in BYRD's environment:"
echo -e "${BLUE}  export HOME_VOICE_URL=https://your-server-url${NC}"
echo ""

# Start server
cd "$SCRIPT_DIR"
python3 mac_voice_server.py --host "$HOST" --port "$PORT"

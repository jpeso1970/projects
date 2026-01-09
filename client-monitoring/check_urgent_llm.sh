#!/bin/bash
# Wrapper script to run urgent checker with LLM matching

cd "$(dirname "$0")"
source venv/bin/activate

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY environment variable not set!"
    echo ""
    echo "To use LLM matching, set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Or add it to your ~/.zshrc or ~/.bashrc:"
    echo "  echo 'export ANTHROPIC_API_KEY=\"your-api-key-here\"' >> ~/.zshrc"
    echo ""
    echo "Falling back to simple pattern matching..."
    echo ""
    USE_LLM_MATCHING=false python check_urgent.py "$@"
else
    echo "✓ Using LLM-based intelligent matching (Claude Haiku)"
    echo ""
    USE_LLM_MATCHING=true python check_urgent.py "$@"
fi

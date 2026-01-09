#!/bin/bash
# Wrapper script to run monitor with virtual environment

cd "$(dirname "$0")"
source venv/bin/activate
python monitor.py "$@"

#!/bin/bash
#
# Process Imports Launcher
#
# This script launches the import processing interface.
# Double-click this file in Finder to process files from ~/projects/import/
#

# Change to the mission-control directory
cd "$(dirname "$0")"

# Run the import processor
./process-imports

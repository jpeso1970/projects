#!/bin/bash
#
# Watch Imports Launcher
#
# This script launches the continuous import watcher.
# Double-click this file in Finder to start auto-monitoring ~/projects/import/
#

# Change to the mission-control directory
cd "$(dirname "$0")"

# Run the import watcher
./watch-imports

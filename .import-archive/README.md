# Import Archive

This directory contains files that have been processed by the Mission Control import system.

## Purpose

After files are imported and analyzed:
1. They are moved here with a timestamp prefix
2. Original filename is preserved
3. Provides audit trail of what was imported

## File Naming

Files are renamed to: `YYYYMMDD-HHMMSS-original-filename.ext`

Example: `20260108-194443-meeting-notes.txt`

## Retention

Files in this directory can be safely deleted after you've verified the import was successful. They are kept for reference in case you need to review what was imported.

## Git

This directory is excluded from version control (files are not committed to git). Only this README is tracked.

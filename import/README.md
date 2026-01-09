# Import Directory

Drop files here for AI-powered import processing and automatic routing to projects.

## How It Works

1. **Drop files** in this directory (images, PDFs, text, markdown, documents, etc.)
2. **Watch Imports** auto-processes every 10 seconds (or process manually)
3. AI analyzes content and routes to appropriate project(s) **automatically**
4. Content is added immediately to project files (tasks.md, PROJECT.md)
5. Files are archived to `../.import-archive/`

## Two Ways to Process

### Method 1: Watch Imports (Recommended)
1. Drop files here
2. Launch Watch Imports: `~/projects/mission-control/watch-imports`
   - Or double-click **Watch Imports.command** in Finder
3. Files are auto-processed every 10 seconds
4. Changes applied automatically - no review needed!

### Method 2: Manual Processing
1. Drop files here
2. Open Mission Control: `~/projects/mission-control/mc`
3. Files will be processed next time watch-imports runs
   - Or process manually: `mc --process-imports`

## Supported File Types

- **Images**: PNG, JPG, HEIC, etc. (OCR text extraction)
- **Documents**: PDF, DOCX, TXT, MD
- **Meeting transcripts**: Any text format
- **Screenshots**: Auto-analyzed for content

## AI Analysis

The AI examines:
- File content and text
- Filename for project mentions
- Context and subject matter
- Related projects in the system

Then automatically:
- Routes to correct project(s)
- Creates tasks
- Records decisions
- Notes updates

## What Happens to Files

1. **Analyzed**: AI extracts tasks, decisions, and updates
2. **Applied**: Content automatically added to project files
3. **Archived**: Files moved to `../.import-archive/` with timestamp

## Trust First, Fix Later

Files are processed automatically. If AI routes something incorrectly, you can:
- Move tasks between projects (coming soon: `[m]` key)
- Edit project files directly to fix mistakes
- Future: Undo recent imports (coming soon: `[u]` key)

---
Last Updated: 2026-01-09

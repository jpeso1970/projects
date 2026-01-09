# Import Directory

Drop files here for AI-powered import processing and automatic routing to projects.

## How It Works

1. **Drop files** in this directory (images, PDFs, text, markdown, documents, etc.)
2. **Process manually** or use **automatic monitoring**
3. AI analyzes content and determines which project(s) the file belongs to
4. Files are staged for review
5. Approve in Mission Control dashboard
6. Content is added to appropriate projects

## Two Ways to Process

### Method 1: Manual Processing
1. Drop files here
2. Open Mission Control: `~/projects/mission-control/mc`
3. Press **[i]** key to process imports
4. Review AI suggestions and approve

### Method 2: Automatic Monitoring
1. Drop files here
2. Launch Watch Imports: `~/projects/mission-control/watch-imports`
   - Or double-click **Watch Imports.command** in Finder
3. Files are auto-processed every 10 seconds
4. Open Mission Control and press **[i]** to review

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

Then suggests:
- Which project(s) to add content to
- Tasks to create
- Decisions to record
- Updates to note

## What Happens to Files

1. **Processed**: Files are archived to `../.import-archive/` with timestamp
2. **Content**: Extracted information is staged in `../.mission-control/staging/`
3. **Review**: You approve or reject each analysis in Mission Control
4. **Applied**: Approved content is added to project files (tasks.md, PROJECT.md)

## Quick Start

**Easiest way**:
1. Open Finder → `~/projects/mission-control/`
2. Double-click **Watch Imports.command**
3. Drop files here and they're processed automatically!

---
Last Updated: 2026-01-08

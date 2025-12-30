# HubSpot Integration Setup Guide

Complete guide for integrating HubSpot CRM with your project management system.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [API Key Setup](#api-key-setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Data Mapping](#data-mapping)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

---

## Overview

The HubSpot integration allows you to:
- Automatically populate project files with client data
- Sync company information, deals, and contacts
- Import meeting notes and attachments from HubSpot
- Maintain links to HubSpot records for easy access
- Keep project documentation in sync with your CRM

**What Gets Synced:**
- Company details (name, industry, location, contact info)
- Deal information (amount, stage, close date)
- Contact details (names, titles, email, phone)
- Meeting notes and engagements
- File attachments

**Affected Files:**
- `PROJECT.md` - Company and deal information added
- `ENTITIES.md` - Contacts added or updated
- `meeting-notes/` - Meetings imported as markdown files
- `assets/hubspot-files/` - Attachments downloaded

---

## Prerequisites

### Requirements

1. **HubSpot Account**
   - Active HubSpot account with CRM access
   - Permission to create API keys

2. **API Permissions**
   Your API key must have read access to:
   - Companies (crm.objects.companies.read)
   - Deals (crm.objects.deals.read)
   - Contacts (crm.objects.contacts.read)
   - Engagements (crm.objects.engagements.read)
   - Files (files)

3. **Existing Project**
   - Must have PROJECT.md file
   - Should be a work/client project

---

## API Key Setup

### Step 1: Generate API Key in HubSpot

1. Log into your HubSpot account
2. Go to **Settings** (gear icon) → **Account Setup** → **Integrations** → **Private Apps**
3. Click **"Create a private app"**
4. Give it a name: "Project Management Sync"
5. Add description: "Syncs HubSpot data to local project files"

### Step 2: Configure Scopes

Select these scopes:

**CRM Scopes:**
- `crm.objects.companies.read`
- `crm.objects.deals.read`
- `crm.objects.contacts.read`

**Engagement Scopes:**
- `crm.objects.notes.read`
- `crm.objects.calls.read`
- `crm.objects.meetings.read`

**Files Scope:**
- `files`

### Step 3: Create and Copy API Key

1. Click **"Create app"**
2. Click **"Show token"**
3. Copy the token (format: `pat-na1-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`)
4. **IMPORTANT**: Save this somewhere secure - you won't see it again!

---

## Configuration

### Option 1: Environment Variable (Recommended)

Add to your `~/.zshrc` (or `~/.bashrc` for bash):

```bash
# HubSpot API Configuration
# Get your API key from: https://app.hubspot.com/settings/account/security
export HUBSPOT_API_KEY="pat-na1-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
```

**Apply changes:**
```bash
source ~/.zshrc
```

**Verify:**
```bash
echo $HUBSPOT_API_KEY
```

### Option 2: Skill Prompt (Less Secure)

The hubspot-sync skill will prompt for your API key if not found in environment variables. This works but requires entering the key each time.

---

## Usage

### Basic Sync

Navigate to your project and run:

```bash
cd ~/projects/work/client-projects/your-project
/hubspot-sync
```

You'll be prompted for:
1. Company name (if not provided)
2. Which deal to sync (if multiple deals exist)
3. Which contacts to include (if many contacts)

### Sync with Company Name

```bash
/hubspot-sync company='Acme Corporation'
```

### Sync Options

**Dry run (preview changes):**
```bash
/hubspot-sync company='Acme Corp' --dry-run
```

**Contacts only:**
```bash
/hubspot-sync company='Acme Corp' --contacts-only
```

**Meeting notes only:**
```bash
/hubspot-sync company='Acme Corp' --notes-only
```

**Date range for meetings:**
```bash
/hubspot-sync company='Acme Corp' --from=2025-11-01 --to=2025-12-31
```

**Specific deal:**
```bash
/hubspot-sync company='Acme Corp' --deal-id=12345678
```

### Complete Sync Example

```bash
# Navigate to project
cd ~/projects/work/client-projects/acme-website

# Run sync with company name
/hubspot-sync company='Acme Corporation'

# Review synced data
cat PROJECT.md
cat ENTITIES.md
ls meeting-notes/
ls assets/hubspot-files/
```

---

## Data Mapping

### Company → PROJECT.md

**HubSpot Company Properties:**
```json
{
  "name": "Acme Corporation",
  "domain": "acme.com",
  "industry": "Technology",
  "phone": "(555) 123-4567",
  "city": "San Francisco",
  "state": "California",
  "country": "United States"
}
```

**Maps to PROJECT.md:**
```markdown
## Client Information

### About Acme Corporation

**Company Details:**
- **Name**: Acme Corporation
- **Industry**: Technology
- **Location**: San Francisco, California, United States
- **Website**: [acme.com](https://acme.com)
- **Phone**: (555) 123-4567
- **HubSpot**: [View Company Record](https://app.hubspot.com/contacts/company/123456789)

**Key Contacts:** (See ENTITIES.md for full details)
- John Smith - CEO
- Jane Doe - CTO
```

### Deal → PROJECT.md

**HubSpot Deal:**
```json
{
  "dealname": "Acme Website Redesign",
  "amount": "125000",
  "closedate": "2025-03-31",
  "dealstage": "contractsent",
  "pipeline": "default"
}
```

**Maps to PROJECT.md:**
```markdown
## Deal Information

**Deal**: [Acme Website Redesign](https://app.hubspot.com/contacts/deal/987654321)

- **Amount**: $125,000
- **Stage**: Contract Sent
- **Pipeline**: Sales Pipeline
- **Close Date**: 2025-03-31

---
*Last synced from HubSpot: 2025-12-29*
```

### Contact → ENTITIES.md

**HubSpot Contact:**
```json
{
  "firstname": "John",
  "lastname": "Smith",
  "email": "john.smith@acme.com",
  "phone": "(555) 123-4568",
  "jobtitle": "CEO"
}
```

**Maps to ENTITIES.md:**
```markdown
### Acme Corporation Team

- **John Smith** - CEO
  - Email: john.smith@acme.com
  - Phone: (555) 123-4568
  - HubSpot: [View Contact](https://app.hubspot.com/contacts/contact/111222333)
  - Source: HubSpot (synced 2025-12-29)
```

### Engagement → Meeting Note

**HubSpot Meeting:**
```json
{
  "engagement": {
    "type": "MEETING",
    "timestamp": 1702908000000
  },
  "metadata": {
    "title": "Project Kickoff Meeting",
    "body": "Discussed project scope, timeline, and deliverables...",
    "startTime": 1702908000000
  }
}
```

**Maps to `meeting-notes/2024-12-18-project-kickoff-meeting.md`:**
```markdown
# Project Kickoff Meeting

**Date**: 2024-12-18
**Type**: MEETING
**Source**: HubSpot
**HubSpot Link**: [View in HubSpot](https://app.hubspot.com/contacts/engagement/444555666)

## Participants

- John Smith - CEO
- Jane Doe - CTO

## Notes

Discussed project scope, timeline, and deliverables...

---

*Imported from HubSpot on 2025-12-29*
```

---

## Troubleshooting

### Error: Invalid API Key

**Symptom:** 401 Unauthorized error

**Solutions:**
1. Verify API key is correct (check for copy/paste errors)
2. Ensure key hasn't been regenerated in HubSpot
3. Check key has required scopes
4. Generate a new key if needed

### Error: Permission Denied

**Symptom:** 403 Forbidden error

**Solutions:**
1. Check API key scopes in HubSpot settings
2. Ensure all required scopes are enabled:
   - crm.objects.companies.read
   - crm.objects.deals.read
   - crm.objects.contacts.read
   - crm.objects.engagements.read
   - files
3. Recreate private app with correct scopes

### Error: Company Not Found

**Symptom:** No results when searching for company

**Solutions:**
1. Check company name spelling
2. Try shorter search term
3. Search by domain instead: `/hubspot-sync company='acme.com'`
4. Verify company exists in your HubSpot instance
5. Check you have access to the company

### Error: Rate Limit Exceeded

**Symptom:** 429 Too Many Requests

**Solutions:**
1. Wait 10 seconds and retry
2. Use `--contacts-only` or `--notes-only` for partial syncs
3. Avoid running multiple syncs simultaneously
4. HubSpot standard limit: 100 requests per 10 seconds

### Files Not Downloading

**Symptom:** Attachments not appearing in assets/

**Solutions:**
1. Check internet connection
2. Verify files still exist in HubSpot
3. Check available disk space
4. Some files may have access restrictions
5. Try manual download from HubSpot

### Duplicate Contacts in ENTITIES.md

**Symptom:** Same person appears multiple times

**Solutions:**
1. Review email addresses to confirm if truly different
2. Manually merge duplicate entries after sync
3. Update primary contact in HubSpot to avoid future duplicates

---

## Security Best Practices

### API Key Security

**DO:**
- ✅ Store in environment variables (~/.zshrc)
- ✅ Use read-only permissions
- ✅ Rotate keys periodically (every 90 days)
- ✅ Create separate keys for different purposes
- ✅ Revoke unused keys immediately

**DON'T:**
- ❌ Commit API keys to version control
- ❌ Share keys via email or chat
- ❌ Use keys with write permissions unless required
- ❌ Store keys in plain text files
- ❌ Use the same key across multiple systems

### Data Protection

1. **Review Downloaded Files**
   - Check for PII (Personally Identifiable Information)
   - Look for financial data or confidential information
   - Add sensitive files to `.gitignore`

2. **Access Control**
   - Only sync data you're authorized to access
   - Be mindful of client confidentiality
   - Don't share HubSpot links externally (require login)

3. **Version Control**
   - Never commit `.env` files with API keys
   - Use `.gitignore` for sensitive directories
   - Consider encryption for highly sensitive projects

### Example .gitignore

```
# Sensitive files
.env
.env.local
credentials.json

# HubSpot data (optional - only if highly sensitive)
assets/hubspot-files/contracts/
```

---

## API Reference

### Base URL
```
https://api.hubapi.com
```

### Authentication Header
```
Authorization: Bearer YOUR_API_KEY
```

### Common Endpoints

**Search Companies:**
```
POST /crm/v3/objects/companies/search
```

**Get Company:**
```
GET /crm/v3/objects/companies/{companyId}
```

**Get Company's Deals:**
```
GET /crm/v3/objects/companies/{companyId}/associations/deals
```

**Get Deal:**
```
GET /crm/v3/objects/deals/{dealId}
```

**Get Company's Contacts:**
```
GET /crm/v3/objects/companies/{companyId}/associations/contacts
```

**Get Contact:**
```
GET /crm/v3/objects/contacts/{contactId}
```

**Get Engagements:**
```
GET /engagements/v1/engagements/associated/company/{companyId}/paged
```

**Get File:**
```
GET /files/v3/files/{fileId}
```

### Rate Limits

- **Standard**: 100 requests per 10 seconds
- **Burst**: Slightly higher for short periods
- **Daily**: 250,000 requests per day (typical for professional tier)

---

## Advanced Usage

### Re-syncing Projects

To update existing project with latest HubSpot data:

```bash
cd ~/projects/work/client-projects/project-name
/hubspot-sync company='Company Name'
```

The skill will:
- Update existing data
- Add new contacts
- Import new meeting notes
- Download new attachments
- Preserve manually-added information

### Syncing Multiple Projects

For multiple projects with same client:

```bash
# Project 1
cd ~/projects/work/client-projects/acme-website
/hubspot-sync company='Acme Corporation'

# Project 2
cd ~/projects/work/client-projects/acme-mobile-app
/hubspot-sync company='Acme Corporation'
```

Both projects will have the same client data but remain independent.

### Custom Company Properties

If your HubSpot portal has custom properties:

1. These won't be synced automatically (skill uses standard properties)
2. To include custom properties, you'd need to modify the skill
3. Standard properties are usually sufficient for most use cases

---

## Integration Workflows

### Workflow 1: New Client Project

```bash
# Step 1: Create project
/new-project category=work container=client-projects name=acme-website

# Step 2: Navigate to project
cd ~/projects/work/client-projects/acme-website

# Step 3: Sync HubSpot data
/hubspot-sync company='Acme Corporation'

# Step 4: Review synced data
cat PROJECT.md
cat ENTITIES.md

# Step 5: Customize project details
# Edit PROJECT.md to add project-specific goals and scope

# Step 6: Commit to Git
cd ~/projects
git add work/client-projects/acme-website
git commit -m "Add Acme Corporation website project with HubSpot sync"
```

### Workflow 2: Monthly Data Refresh

```bash
# Run this monthly to keep data fresh
cd ~/projects/work/client-projects/acme-website
/hubspot-sync company='Acme Corporation' --from=2025-12-01
```

### Workflow 3: Meeting Notes Import

```bash
# After a series of client meetings
cd ~/projects/work/client-projects/acme-website
/hubspot-sync company='Acme Corporation' --notes-only --from=2025-12-15 --to=2025-12-29
```

---

## Maintenance

### Weekly
- Review imported meeting notes
- Check for new contacts

### Monthly
- Re-sync projects for data updates
- Review downloaded attachments
- Update ENTITIES.md with additional context

### Quarterly
- Rotate API keys
- Review HubSpot integration setup
- Clean up old meeting notes and attachments

---

## FAQ

**Q: Will this modify my HubSpot data?**
A: No, this is read-only integration. It only pulls data FROM HubSpot.

**Q: What happens if I run sync multiple times?**
A: It will update existing data and add new information. Won't create duplicates.

**Q: Can I sync data from multiple companies to one project?**
A: No, each project syncs with one company. Create separate projects for different clients.

**Q: How often should I sync?**
A: Initially at project creation, then monthly or after significant HubSpot updates.

**Q: Will syncing overwrite my manual changes?**
A: No, it adds HubSpot data alongside existing content. Manual edits are preserved.

**Q: Can I sync archived projects?**
A: Yes, but consider if fresh data is needed for archived projects.

**Q: What if the company name changed in HubSpot?**
A: Use the new name when syncing. The skill searches by current company name.

---

## Support Resources

- **HubSpot API Documentation**: https://developers.hubspot.com/docs/api/overview
- **Private Apps Guide**: https://developers.hubspot.com/docs/api/private-apps
- **API Key Management**: https://app.hubspot.com/settings/account/security
- **Skill Documentation**: `~/.claude/skills/hubspot-sync/SKILL.md`

---

**Last Updated**: 2025-12-29
**Guide Version**: 1.0.0
**Skill Version**: 1.0.0 (hubspot-sync)

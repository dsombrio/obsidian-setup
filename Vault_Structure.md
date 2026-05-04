# Vault Structure — Tradition Sales

The vault uses a modified **PARA** system (Projects, Areas, Resources, Archives) adapted for a building materials sales agency. The top-level structure is designed for iPhone-first navigation while supporting deeper analysis on Mac.

---

## Top-Level Folder Map

```
Tradition Sales/
├── 00 Daily/              # Daily notes (journal, tasks, call log)
├── 01 Contacts/           # All contacts (people)
├── 02 Companies/          # All companies (contractors, builders, GC)
├── 03 Deals/               # Sales opportunities / pipeline
├── 04 Tasks/               # Task inbox (from Plaud, manual, auto)
├── 05 Projects/            # Active project work (bid prep, spec reviews)
├── 06 Areas/               # Ongoing areas of responsibility
├── 07 Resources/           # Reference material, pricing docs, vendor info
├── 08 Meetings/            # Meeting notes (linked to contacts/companies)
├── 09 Inbox/               # Quick capture — unprocessed notes
├── 10 Archives/            # Closed deals, old contacts, inactive projects
├── Templates/              # Note templates (not for daily use)
├── Scripts/                # Automation scripts (Mac only)
└── .obsidian/              # Plugin settings (auto-generated)
```

---

## Folder Definitions

### `00 Daily/`
**Purpose:** Your daily journal, call log, and task list. One note per day.

**Contents:**
- Daily note (`2026-05-04.md`)
- Morning review checklist
- Call/meeting log entries
- End-of-day summary

**Naming:** `YYYY-MM-DD.md` (e.g., `2026-05-04.md`)

**Key links:**
- Daily note frontmatter links to today's deals and contacts
- Task block pulled from Plaud sync
- Links to meeting notes taken that day

**iPhone tip:** Use the Calendar plugin to tap any date and jump straight to that day's note.

---

### `01 Contacts/`
**Purpose:** Every person you interact with — contractors, builders, estimators,vendor reps.

**Contents:**
- One note per contact: `Smith - John.md`
- Groups: `Contractors/`, `Builders/`, `Vendors/`, `Internal/`

**Frontmatter fields:**
```yaml
---
contact_name: John Smith
company: Smith Construction
title: Owner
phone: 214-555-0100
email: john@smithconst.com
metro: Dallas
type: contractor
status: active
hubspot_id: 123456
tags: [Dallas, residential, roofer]
created: 2025-01-15
---
```

**Links:** Links to their `Company` note, any active `Deal` notes, and meeting notes where they appear.

---

### `02 Companies/`
**Purpose:** Every company — contractor firms, builders, GC firms, distributors.

**Contents:**
- One note per company: `Smith Construction.md`
- Subfolders by type: `Builders/`, `Contractors/`, `Distributors/`, `Vendors/`

**Frontmatter fields:**
```yaml
---
company_name: Smith Construction
type: contractor
address: 123 Main St, Dallas TX 75201
metro: Dallas
website: https://smithconst.com
status: active
hubspot_id: 789012
tags: [residential, commercial, dallas]
notes: Preferred roofer in Dallas market. Uses primarily GAF.
---
```

**Links:** Links to all `Contact` notes who work there, all active `Deal` notes, and any vendor-specific `Resources/`.

---

### `03 Deals/`
**Purpose:** Active sales pipeline. Each deal = one opportunity.

**Contents:**
- One note per deal: `Deal - Smith Construction - NFA Ridge Vents.md`
- Subfolders by stage: `Leads/`, `Qualified/`, `Quoted/`, `Won/`, `Lost/`

**Frontmatter fields:**
```yaml
---
deal_title: Smith Construction - NFA Ridge Vents
company: Smith Construction
contact: John Smith
value: 45000
stage: quoted
probability: 60
next_step: Send revised quote
follow_up: 2026-05-10
opened: 2026-03-15
hubspot_deal_id: 456789
tags: [ridge-vents, dallas, nfa]
---
```

**Stages:**
1. **Lead** — initial contact, scoping
2. **Qualified** — confirmed opportunity, understand their needs
3. **Quoted** — proposal sent, awaiting decision
4. **Won** — closed sale
5. **Lost** — closed no sale (moved to Archives after review)

**Links:** Links to the associated `Contact` note, `Company` note, and any relevant `Meeting` notes.

---

### `04 Tasks/`
**Purpose:** All tasks and action items in one searchable place.

**Contents:**
- Task notes imported from Plaud via sync script
- Manual task notes
- Recurring task templates

**Note:** Tasks are also embedded inline in daily notes and deal notes. This folder holds the canonical task records for Dataview queries.

**Format:** Each task as a Tasks-plugin-compatible task or as a dataview-friendly note with frontmatter:
```yaml
---
title: Follow up with Zarsky on quote
due: 2026-05-10
priority: high
source: plaud
contact: Zarsky Roofing
deal: Zarsky - NFA Quote
status: pending
---
```

---

### `05 Projects/`
**Purpose:** Time-limited work with a clear goal and deadline. Different from Deals — a project is internal work (bid preparation, spec review, vendor onboarding).

**Contents:**
- `Bid - Lone Star Apartments - May 2026/`
- `Vendor Onboarding - American Flashings/`
- `Spec Review - City Center Dallas/`

**Frontmatter fields:**
```yaml
---
project_name: Bid - Lone Star Apartments
status: active
due: 2026-05-20
owner: David
contacts: [John Smith, Sarah Lee]
deals: [Lone Star - Bid Package]
---
```

---

### `06 Areas/`
**Purpose:** Ongoing responsibilities without a deadline. The "A" in PARA.

**Examples for Tradition Sales:**
- `Texas Markets/` — market development for TX territory
- `Oklahoma Markets/`
- `Louisiana/Mississippi Markets/`
- `Vendor Relations/`
- `Pricing & Quotes/`
- `Team/` — 5-person agency internal ops

**Contents:** Notes, reference docs, and strategies for each ongoing area.

---

### `07 Resources/`
**Purpose:** Reference material that doesn't belong to a project or area.

**Contents:**
- `Pricing/ — supplier price sheets (PDF links, summaries)
- `Vendor Info/ — manufacturer one-pagers, spec sheets, contacts
- `Market Research/ — territory data, competitor notes
- `Product Knowledge/ — ridge vent specs, underlayment comparison, etc.
- `Templates/` (separate top-level folder for Obsidian templates)

**This folder doesn't change often.** It exists to keep vendor sheets, product specs, and market notes organized and searchable.

---

### `08 Meetings/`
**Purpose:** All meeting notes, linked to the contacts and companies involved.

**Contents:**
- One note per meeting: `Meeting - 2026-05-03 - Stephen @ ABC Supply.md`
- Auto-linked from daily notes when meetings are logged

**Frontmatter fields:**
```yaml
---
meeting_date: 2026-05-03
contact: Stephen Mitchell
company: ABC Supply
attendees: [David Sombrio, Stephen Mitchell]
type: sales-call
outcome: Interested in NFA ridge vent line
next_action: Email pricing sheet
follow_up: 2026-05-10
---
```

---

### `09 Inbox/`
**Purpose:** Quick capture. Notes that haven't been sorted yet.

**Rule:** Review and process the Inbox at the end of every day. Move each note to its proper folder or delete it.

**On iPhone:** Use QuickAdd or a Shortcuts automation to drop notes directly into Inbox during calls and visits. Process them tonight.

---

### `10 Archives/`
**Purpose:** Closed deals, inactive contacts, completed projects. Keeps active folders clean while preserving history.

**Subfolders:**
- `Deals - Closed/`
- `Contacts - Inactive/`
- `Projects - Completed/`

**Archive criteria:**
- Deal: moved to Won or Lost and not expected to reopen within 90 days
- Contact: no activity in 12 months and no open deals
- Project: deliverable complete or project cancelled

Dataview can still query Archives — it doesn't exclude archived notes by default.

---

## How PARA Flows Together

```
DAILY NOTE (Morning Review)
    ├── Check Tasks/ for today's follow-ups (Dataview query)
    ├── Check Deals/ for deals needing attention
    ├── Check Contacts/ for contacts to reach out to
    └── Check Calendar for today's meetings

CAPTURE (During the day)
    ├── QuickAdd → drops note in 09 Inbox/
    ├── Meeting → goes to 08 Meetings/
    └── Plaud Sync → drops tasks in 04 Tasks/

PROCESS (End of day / Weekly Review)
    ├── Inbox → sort to Contacts/, Companies/, Deals/, Projects/
    ├── Update deal stages in Deals/
    └── Update contact status in Contacts/

PARA in Practice:
    P = 05 Projects (active bids, onboarding)
    A = 06 Areas (territories, vendor relations, team)
    R = 07 Resources (product specs, pricing sheets, market data)
    A = 00 Daily (not PARA per se, but drives the daily workflow)
```

---

## iPhone Navigation Tips

1. **Star** your most-used folders: `00 Daily/`, `01 Contacts/`, `03 Deals/`, `04 Tasks/`
2. Use the **QuickAdd** command palette to capture without navigating folders
3. **Links** are faster than folders — link from daily note to a contact note, never dig for it
4. The **Graph View** on iPhone is excellent for finding orphaned notes (notes with no links)

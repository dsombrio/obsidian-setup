# Daily Workflow — Tradition Sales

A structured daily rhythm designed for a busy sales rep managing a 5-person agency across 4 states. Built for iPhone-first use with Mac for deeper analysis.

---

## The Daily Rhythm

| Time | Action |
|---|---|
| **Morning (5-10 min)** | Morning Review — open daily note, check tasks, scan pipeline |
| **During day** | Quick capture from calls, visits, Plaud thoughts |
| **End of day (5 min)** | Process Inbox, update deal stages, log the day |
| **Friday (30 min)** | Weekly Review — full pipeline sweep, plan next week |
| **First of month** | Monthly review — territory health, pipeline forecast |

---

## Morning Review (5–10 minutes)

Open today's daily note (tap from Calendar or use `Open today's note` command).

### Step 1 — Review the day ahead

```
## Today — May 4, 2026

**Meetings today:**
- 10:00 AM — John Smith @ Smith Construction (see [[Meeting - 2026-05-04 - Smith]])
- 2:00 PM — internal team call (see [[Team/Weekly Sync]])

**Today's tasks (from Plaud):**
```dataview
TASK
FROM "04 Tasks"
WHERE due = date(today) AND status = "pending"
SORT priority DESC
```

**Deals needing follow-up:**
```dataview
TABLE stage, contact, follow_up
FROM "03 Deals"
WHERE follow_up = date(today)
SORT value DESC
```

**Pipeline snapshot:**
```dataview
TABLE stage AS Stage, length(rows) AS Count, sum(rows.value) AS Value
FROM "03 Deals"
WHERE stage != "lost" AND stage != "won"
GROUP BY stage
```
```

### Step 2 — Quick context read

- Open the most important deal or contact you'll see today
- Check if there are any open meeting notes from recent interactions
- Note any flags or blockers in deal notes

### Step 3 — Set today's 3 priorities

At the top of the daily note, write:
```
**Top 3 for today:**
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

---

## During-Day Capture

### From a phone call or visit

Use **QuickAdd** (`Cmd/Ctrl + O` → "QuickAdd"):

1. **Capture type:** Choose "Meeting Note" or "Quick Note"
2. Meeting → Opens `Templates/meeting.md`, auto-fills date, prompts for contact name
3. Quick note → Drops into `09 Inbox/` with a timestamp

### From Plaud (voice notes)

Plaud AI captures the audio, transcribes it, and creates tasks in its SQLite database. The **plaud-sync.py** script runs daily and:

1. Reads all pending tasks from `Plaud/crm.db`
2. Writes them to `04 Tasks/Plaud Tasks - YYYY-MM-DD.md`
3. That file is embedded in the daily note via:
   ````
   ## Plaud Tasks
   ![[Plaud Tasks - 2026-05-04]]
   ````

### From email

Quick-add a note to the contact's page:
```
**Email from John Smith — May 4, 2026**
Sent revised quote for NFA 18 ridge vents. Wants delivery by May 15.
→ Follow up Friday.
```

---

## End-of-Day Processing (5 minutes)

1. Open today's daily note
2. Check off completed tasks using the Tasks plugin
3. Move anything in `09 Inbox/` to its proper folder
4. Update any deal stages if a call moved things forward
5. Add a brief end-of-day log:

```
## End of Day Log

**Accomplished today:**
- Met with John Smith — strong interest, sending revised quote tomorrow
- Reviewed Zarsky quote — needs value prop on lead time

**Tomorrow:**
- [ ] Email revised quote to Smith Construction
- [ ] Follow up with Zarsky on NFA 12
```

---

## Weekly Review (Friday, 30 minutes)

### Pipeline Review
```dataview
TABLE company, contact, value, stage, follow_up
FROM "03 Deals"
WHERE stage != "won" AND stage != "lost"
SORT stage, follow_up ASC
```

### This Week's Wins & Losses
```dataview
TABLE company, value, stage
FROM "03 Deals"
WHERE opened >= date(today) - dur(7 days)
SORT stage DESC
```

### Open Tasks (all, sorted by priority)
```dataview
TABLE due, priority, title, source
FROM "04 Tasks"
WHERE status = "pending"
SORT priority DESC, due ASC
LIMIT 25
```

### Inbox Check
- Open `09 Inbox/`
- Move or delete every note
- Empty the folder

### Territory Health Check
```dataview
TABLE length(rows) AS Contacts, company
FROM "01 Contacts"
GROUP BY company
SORT Contacts DESC
LIMIT 10
```

### Next Week Plan
Create next Monday's daily note now and populate:
```
**Monday May 11 priorities:**
1.
2.
3.
```

---

## PARA in the Daily Workflow

```
DAILY NOTE
    ↑ links to      ↓ feeds into
    ─────────────────────────────────
    Contacts        → daily note (who you met, called, emailed)
    Companies       → daily note (company context)
    Deals           → daily note (pipeline status updates)
    Tasks           ← Plaud sync drops tasks here, daily note queries them
    Meetings        → daily note (meeting log)
    Inbox           → process to proper folder end of day

    WEEKLY REVIEW
    ├── Updates deal stages
    ├── Archives stale deals
    ├── Reviews task backlog
    └── Plans next week
```

---

## iPhone Workflow

### Morning (iPhone)
1. Open Obsidian from Home Screen
2. Calendar plugin → tap today's date
3. Run Dataview queries from the daily note
4. Tap into the most important contact/deal

### During calls
1. Use iOS Shortcuts widget: **"New Obsidian Note"** → drops into Inbox
2. After call: open that note, add contact name, company, tags
3. Move to proper folder (or leave in Inbox for EOD processing)

### iOS Shortcuts — Useful Automations

**"Quick Capture to Obsidian Inbox"**
```
Action: "Text" → enter note content
Action: "Append to Note"
    → Note Name: "Inbox"
    → Folder: "09 Inbox"
```

**"Open Today's Daily Note"**
```
Action: "Create Note"
    → Note Name: "{{current date}}"
    → Folder: "00 Daily"
Action: "Open Note"
```

**"Link Contact from Clipboard"**
```
Action: "Get Clipboard"
Action: "Create Note"
    → Note Name: "{{clipboard}}"
    → Folder: "01 Contacts"
    → From Template: contact
```

---

## Template Insertion in Daily Note

Use Templater to insert dynamic blocks. In your daily note template (`Templates/daily-note.md`):

```markdown
## Today — <% tp.date.now("dddd, MMMM D, YYYY") %>

**Top 3 priorities:**
1.
2.
3.

---

## Tasks Due Today
```dataview
TASK
FROM "04 Tasks"
WHERE due = date(today) AND status = "pending"
```

## Pipeline Snapshot
```dataview
TABLE stage AS Stage, length(rows) AS Count, sum(rows.value) AS Value
FROM "03 Deals"
GROUP BY stage
```

## Meetings
<!-- Fill in manually or link from meeting notes -->

---
## End of Day Log
```

---

## HubSpot → Obsidian Sync Points

| HubSpot Object | Obsidian Location | Sync Method |
|---|---|---|
| Contact | `01 Contacts/` | CSV export + Templater |
| Company | `02 Companies/` | CSV export + Templater |
| Deal | `03 Deals/` | CSV export + Templater |
| Tasks | `04 Tasks/` | plaud-sync.py (primary) |

See `CRM_NOTES.md` for HubSpot import workflow.

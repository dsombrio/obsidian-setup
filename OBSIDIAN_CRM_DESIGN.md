# Obsidian CRM Design — TradBot

## Core Philosophy

- **Plain markdown files** — no vendor lock-in, survives any tool
- **Dataview + Tasks plugins** do the heavy lifting (queries, filtering, due dates)
- **Folder structure** mirrors the relationships: Company → Contact → Deal
- **Daily Notes** are the hub — Plaud transcripts attach here, tasks flow from here
- **All relationships via frontmatter links** — not manual cross-references

---

## Folder Structure

```
Tradition Sales/
├── .templates/              # Obsidian built-in templates
│   ├── Company.md
│   ├── Contact.md
│   ├── Deal.md
│   └── Daily Note.md
├── 01 - Companies/          # One file per company
│   ├── 84 Lumber.md
│   ├── Lindsay Windows.md
│   └── Zarsky.md
├── 02 - Contacts/            # One file per person
│   ├── Sean Purtell.md
│   ├── Luis Hernandez.md
│   └── Lori Lively.md
├── 03 - Deals/               # One file per deal
│   ├── [Company] - Deal Name.md
├── 04 - Call Logs/           # One per Plaud recording
│   └── 2026-05-11 - Call with Sean Purtell.md
├── Daily Notes/              # Obsidian journal (built-in)
│   └── 2026-05-11.md
├── 99 - Meta/
│   └── Tags.md               # Tag index
└── Dashboard.md              # Dataview queries live here
```

---

## Template: Company

```markdown
---
company_name: <% tp.file.title %>
type: contractor  # contractor | builder | gc | distributor | vendor | internal
address: 
city: 
state: 
zip: 
metro: 
status: active  # active | inactive | archived
hubspot_id: 
website: 
annual_revenue: 
employee_count: 
tags: []
created: <% tp.date.now("YYYY-MM-DD") %>
last_contact: 
---

## <% tp.file.title %>

**Type:** [[<% type %>]]
**Metro:** [[<% metro %>]]
**Status:** [[<% status %>]]

---

## Address

**Street:** 
**City, State:** , 

---

## Key Contacts

- [[Contact - ]] () — 

---

## Active Deals

- [[Deal - ]]

---

## Account Notes

> Background, market position, products they carry...

---

## Related Call Logs

```dataview
TABLE date, summary, tags
FROM "04 - Call Logs"
WHERE company = "<% tp.file.title %>"
SORT date DESC
```
```

---

## Template: Contact

```markdown
---
contact_name: <% tp.file.title %>
first_name: 
last_name: 
company: 
company_link: [[01 - Companies/]]
title: 
phone: 
mobile: 
email: 
metro: 
state: 
type: prospect  # prospect | customer | vendor | internal
status: active  # active | inactive
hubspot_id: 
tags: []
created: <% tp.date.now("YYYY-MM-DD") %>
last_contact: 
---

## <% tp.file.title %>

**Company:** [[<% company %>]]
**Title:** 
**Phone:** 
**Email:** 
**Metro:** 

---

## Notes

> Background, relationship history, key conversation points

---

## Active Deals

- [[Deal - ]]

---

## Related Call Logs

```dataview
TABLE date, summary, tags
FROM "04 - Call Logs"
WHERE contact = "<% tp.file.title %>"
SORT date DESC
```

---

## Tasks

```dataview
TASK
FROM ""
WHERE contains(contact, "<% tp.file.title %>")
```
```

---

## Template: Deal

```markdown
---
deal_title: <% tp.file.title %>
company: 
company_link: [[01 - Companies/]]
contact: 
contact_link: [[02 - Contacts/]]
value: 0
stage: lead  # lead | qualified | quoted | won | lost
probability: 10
products: []
next_step: 
follow_up: <% tp.date.now("YYYY-MM-DD", "P1D") %>
opened: <% tp.date.now("YYYY-MM-DD") %>
closed: 
hubspot_deal_id: 
tags: []
notes: >
  
---

## Deal: <% tp.file.title %>

**Value:** ${{value}} | **Stage:** [[<% stage %>]] | **Probability:** {{probability}}%

### Company
[[]]

### Contact
[[]]

---

## Next Steps

- [ ] ...
```

---

## Template: Daily Note

```markdown
---
date: <% tp.file.title %>
day: <% tp.date.now("dddd") %>
weather: 
mood: 
---

# <% tp.file.title %>

## Tasks Today

```tasks
not done
due before tomorrow
```

---

## Follow-ups Needed

```dataview
TASK
FROM "Daily Notes"
WHERE contains(tags, "follow-up")
```

---

## Call Logs Today

```dataview
TABLE contact, company, summary, tags
FROM "04 - Call Logs"
WHERE date = "<% tp.file.title %>"
SORT date DESC
```

---

## Notes

> 

```

---

## Template: Call Log

```markdown
---
contact: 
contact_link: [[02 - Contacts/]]
company: 
company_link: [[01 - Companies/]]
date: <% tp.date.now("YYYY-MM-DD") %>
duration_minutes: 
source: plaud  # plaud | manual | email | meeting
summary: 
topics: []
outcome: 
follow_up_required: false
---

## Call with [[<% contact %>]]

**Date:** {{date}}
**Company:** [[<% company %>]]
**Duration:** {{duration_minutes}} min
**Source:** [[<% source %>]]

---

### Summary

{{summary}}

---

### Topics Discussed

-

---

### Action Items / Todos

- [ ] 

---

### Follow-up Required: {{follow_up_required}}
```

---

## Key Plugins Required

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query contacts/deals/call logs from frontmatter |
| **Tasks** | Parse `-[ ]` checkboxes across all notes |
| **Templater** | Dynamic template variable substitution |
| **QuickAdd** | Fast capture without template friction |
| **MetaEdit** | Edit frontmatter fields in-place |

---

## Dashboard (Dashboard.md)

```markdown
# CRM Dashboard

## My Tasks (All Open)

```tasks
not done
```

---

## Deals by Stage

```dataview
TABLE company, contact, value, stage
FROM "03 - Deals"
WHERE stage != "lost" AND stage != "won"
SORT stage ASC, value DESC
```

---

## Recent Call Logs (Last 7 Days)

```dataview
TABLE contact, company, date, summary
FROM "04 - Call Logs"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

---

## Contacts Needing Follow-up

```dataview
TABLE company, type, last_contact, tags
FROM "02 - Contacts"
WHERE status = "active" AND type = "prospect"
SORT last_contact ASC
LIMIT 20
```

---

## This Week's Follow-ups

```dataview
TASK
FROM ""
WHERE contains(tags, "follow-up") AND !completed
```
```

---

## Dataview Linking Logic

The key is matching across files via frontmatter:

| Event | Links to | How |
|-------|----------|-----|
| Call log created | Contact + Company | `contact: "Sean Purtell"` matches `contact_name:` |
| Todo created | Contact + Deal | Tags + `@contact` syntax |
| Daily note | Shows all of the above | Queries pull linked data |
| Plaud sync | Creates call log + parsed tasks | Python script writes frontmatter |

---

## Plaud Sync Flow (plaud-sync.py)

1. Query Plaud SQLite for todos due today + recent call transcripts
2. Create/append to `Daily Notes/YYYY-MM-DD.md`
3. For each call: create `04 - Call Logs/YYYY-MM-DD - Call with [Contact].md`
4. Parse tasks from transcript → write as checkboxes in daily note
5. Write contact/company links via frontmatter
6. Next day: Dataview auto-surfaces tasks from daily note

---

## Import Priority

1. **Contacts + Companies** (highest value, most linking)
2. **Open Deals** (pipeline visibility)
3. **Plaud todos → Daily Notes** (ongoing operational use)
4. **Call Logs** (relationship history)
5. **Historical emails** (optional, linked to contacts via sender email)
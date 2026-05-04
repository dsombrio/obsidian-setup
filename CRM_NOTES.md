# CRM Notes — Tradition Sales

Contact and company management built entirely in Obsidian. Based on the Plaud SQLite data plus HubSpot imports. Uses Dataview for all queries.

---

## Contact Note Template

Create via QuickAdd → "New Contact" or from `Templates/contact.md`.

```yaml
---
contact_name: John Smith
first_name: John
last_name: Smith
company: Smith Construction
company_link: [[Smith Construction]]
title: Owner
phone: 214-555-0100
mobile: 214-555-0101
email: john@smithconst.com
metro: Dallas
state: TX
type: contractor
status: active
source: referral
hubspot_id: 123456
tags: [dallas, residential, roofer]
created: 2026-01-15
last_contact: 2026-05-03
notes: >
  Long-time roofer in Dallas. Prefers GAF products but open to NFA
  if pricing and delivery work. Has 3 crews. Decision-maker for
  purchases up to $50k.
---

## Contact History

| Date | Type | Notes |
|---|---|---|
| 2026-01-15 | Intro call | Met at DAPR supply open house. |
| 2026-03-10 | Site visit | Reviewed NFA ridge vent sample. |
| 2026-05-03 | Quote follow-up | Sent revised NFA 12 quote. |

---

## Active Deals
- [[Deal - Smith Construction - NFA Ridge Vents]]

---

## Related
- [[Smith Construction]]
- [[Meeting - 2026-05-03 - Smith]]
```

---

## Company Note Template

```yaml
---
company_name: Smith Construction
type: contractor
address: 123 Main St, Dallas TX 75201
phone: 214-555-0100
website: https://smithconst.com
metro: Dallas
state: TX
status: active
hubspot_id: 789012
annual_revenue: ~$4M (est)
employee_count: ~15
tags: [dallas, residential, commercial]
created: 2026-01-15
notes: >
  Established Dallas roofing contractor. 3 crews. Primarily residential
  re-roofing. Also does light commercial. Currently using competitor
  ridge vents. Open to switching if NFA delivers on price + lead time.
---

## Key Contacts
- [[Smith - John]] (Owner)
- [[Smith - Sarah]] (Ops Manager)

---

## Active Deals
- [[Deal - Smith Construction - NFA Ridge Vents]]

---

## Notes

> Company background, market position, competitive context

---

## Vendor Info (if applicable)
- Products they carry: [list]
- Pricing tier: [standard/distributor/volume]
- Credit terms: [Net 30, COD, etc.]
```

---

## Dataview Queries for Contacts

### All Active Contacts
```dataview
TABLE first_name, last_name, company, phone, email, metro
FROM "01 Contacts"
WHERE status = "active"
SORT company ASC
```

### Contacts by Metro/Territory
```dataview
TABLE first_name, last_name, company, phone, type
FROM "01 Contacts"
WHERE metro = "Dallas" AND status = "active"
SORT last_name ASC
```

### Contacts by Type
```dataview
TABLE first_name, last_name, company, metro, email
FROM "01 Contacts"
WHERE type = "contractor" AND status = "active"
SORT metro ASC
```

### Contacts Needing Follow-Up (no contact in 30+ days)
```dataview
TABLE first_name, last_name, company, last_contact, type
FROM "01 Contacts"
WHERE status = "active" AND (last_contact < date(today) - dur(30 days) OR last_contact = null)
SORT last_contact ASC
```

### All Deals for a Specific Contact
Replace "John Smith" with any name:
```dataview
TABLE deal_title, value, stage, follow_up
FROM "03 Deals"
WHERE contains(contact, "John Smith")
SORT stage ASC
```

### Contacts by Company
```dataview
TABLE first_name, last_name, title, phone, email
FROM "01 Contacts"
WHERE company = "Smith Construction"
```

### Contact Count by Metro
```dataview
TABLE metro, length(rows) AS Contacts
FROM "01 Contacts"
WHERE status = "active"
GROUP BY metro
```

---

## HubSpot Import (Contacts via CSV)

### Export from HubSpot
1. HubSpot → Contacts → click "Export" in top-right
2. Select columns: `firstname`, `lastname`, `email`, `phone`, `company`, `jobtitle`, `hubspot_owner_id`, `createdate`, `notes_last_updated`
3. Export as CSV

### Field Mapping: HubSpot → Obsidian

| HubSpot Field | Obsidian Frontmatter |
|---|---|
| `firstname` | `first_name` |
| `lastname` | `last_name` |
| `email` | `email` |
| `phone` | `phone` |
| `company` | `company` (creates company link) |
| `jobtitle` | `title` |
| `hubspot_owner_id` | `owner` (maps to your team) |
| `createdate` | `created` |
| `notes_last_contacted` | `last_contact` |

### Import Script

See `SCRIPTS/hubspot-contacts-import.py` — takes CSV, outputs Obsidian note files in `01 Contacts/`.

Basic logic:
```python
import csv

csv_path = "HubSpot Contacts Export.csv"
contacts_folder = "01 Contacts/"

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = f"{row['firstname']} {row['lastname']}".strip()
        filename = f"{contacts_folder}{name}.md"
        # Write note from template...
```

### Manual Import (No Script)

1. Export HubSpot CSV
2. Open `Templates/contact.md`
3. For each contact row, fill in the frontmatter from the CSV
4. Save as `01 Contacts/Last - First.md`

---

## HubSpot Import (Companies via CSV)

### Export from HubSpot
1. HubSpot → Companies → Export
2. Columns: `name`, `address`, `city`, `state`, `phone`, `website`, `industry`, `numberofemployees`

### Field Mapping: HubSpot → Obsidian

| HubSpot Field | Obsidian Frontmatter |
|---|---|
| `name` | `company_name` |
| `address` + `city` + `state` | `address` |
| `phone` | `phone` |
| `website` | `website` |
| `industry` | `type` |
| `numberofemployees` | `employee_count` |

---

## Linking Contacts to Companies

In Obsidian, links are the relationship. In a contact note:
```yaml
company_link: [[Smith Construction]]
```

In the company note, the Key Contacts section links back:
```markdown
## Key Contacts
- [[Smith - John]] (Owner)
- [[Smith - Sarah]] (Ops Manager)
```

This creates a bidirectional graph — click any contact to go to their company; click the company to see all contacts.

---

## Contact-Specific Views

### All contacts for a specific metro (e.g., Louisiana)
```dataview
TABLE first_name, last_name, company, type, last_contact
FROM "01 Contacts"
WHERE metro = "Louisiana" AND status = "active"
SORT last_contact DESC
```

### Newest contacts (last 30 days)
```dataview
TABLE first_name, last_name, company, type, created
FROM "01 Contacts"
WHERE created >= date(today) - dur(30 days)
SORT created DESC
```

### All vendors
```dataview
TABLE first_name, last_name, company, phone, email
FROM "01 Contacts"
WHERE type = "vendor" AND status = "active"
```

---

## iPhone Contact Workflow

1. **Inbound call from a contact:** Look them up in Obsidian Search, open their note, add a log entry at the top of Contact History
2. **New contact met on-site:** QuickAdd → "New Contact" → fill from the template → link to company
3. **After meeting:** Go to meeting note, link to contact and company, update `last_contact` in frontmatter

---

## Data Hygiene Rules

1. Update `last_contact` every time you interact with a contact
2. Archive contacts with no activity in 12 months and no open deals
3. Never delete contacts — archive them
4. Every deal must be linked to at least one contact
5. Every contact should be linked to a company (even if just "Independent")

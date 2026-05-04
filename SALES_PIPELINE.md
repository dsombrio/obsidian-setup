# Sales Pipeline — Tradition Sales

Built in Obsidian using Dataview queries, Kanban boards, and structured deal notes. Replaces a full CRM for most use cases.

---

## Deal Stages

| Stage | Meaning | Color (Kanban) |
|---|---|---|
| **Lead** | Initial contact, early-stage opportunity. Specifying, needs discovery. | Gray |
| **Qualified** | Confirmed need, budget confirmed, decision-maker identified. | Blue |
| **Quoted** | Proposal sent, awaiting response or decision. | Yellow |
| **Won** | Closed sale. | Green |
| **Lost** | Closed no sale. Move to Archive after 30-day review. | Red |

---

## Deal Note Template

Create new deals via QuickAdd or Templater. File name: `Deal - [Company] - [Product].md`

**Full template at `Templates/deal.md`. Key frontmatter:**

```yaml
---
deal_title: Smith Construction - NFA Ridge Vents
company: Smith Construction
company_link: [[Smith Construction]]
contact: John Smith
contact_link: [[Smith - John]]
value: 45000
stage: quoted
probability: 60
products: [NFA Ridge Vents 12, NFA Underlayment]
next_step: Send revised quote with volume discount
follow_up: 2026-05-10
opened: 2026-03-15
closed: null
hubspot_deal_id: 456789
tags: [ridge-vents, dallas, nfa]
notes: >
  John is interested in the NFA 12 ridge vent for their residential
  re-roof projects. Currently using a competitor. Wants delivery
  by mid-May. Decision-maker is John and his ops manager.
---
```

**Stage history table (inside deal note):**
```
## Stage History

| Date | Stage | Notes |
|---|---|---|
| 2026-03-15 | Lead | Initial call. Interested in NFA line. |
| 2026-04-02 | Qualified | Budget confirmed $40-50k. Decision by May. |
| 2026-04-20 | Quoted | Sent full quote. Waiting on ops manager approval. |
```

---

## Pipeline View — Dataview Queries

### Full Pipeline (all active deals)

```dataview
TABLE company AS Company, contact AS Contact, value AS Value, stage AS Stage, follow_up AS "Follow Up"
FROM "03 Deals"
WHERE stage != "won" AND stage != "lost"
SORT stage ASC, value DESC
```

### Pipeline by Stage (count + total value)

```dataview
TABLE stage AS Stage, length(rows) AS Deals, sum(rows.value) AS "Total Value", round(sum(rows.value) * average(rows.probability) / 100, 0) AS "Weighted Value"
FROM "03 Deals"
WHERE stage != "won" AND stage != "lost"
GROUP BY stage
```

### Deals Due Today

```dataview
TABLE company, contact, value, stage, next_step
FROM "03 Deals"
WHERE follow_up = date(today) AND stage != "won" AND stage != "lost"
SORT value DESC
```

### Deals Overdue (follow-up before today)

```dataview
TABLE company, contact, value, stage, follow_up as "Was Due"
FROM "03 Deals"
WHERE follow_up < date(today) AND stage != "won" AND stage != "lost"
SORT follow_up ASC
```

### Deals by Contact

```dataview
TABLE value, stage, follow_up, deal_title AS "Deal"
FROM "03 Deals"
WHERE contains(contact, "John Smith")
SORT stage ASC
```

### Top 10 Deals by Value

```dataview
TABLE company, contact, value, stage
FROM "03 Deals"
WHERE stage != "lost"
SORT value DESC
LIMIT 10
```

---

## Kanban Board Setup

Create `03 Deals/Pipeline Board.md` and configure as a Kanban board:

**Column: Lead**
```
- [[Deal - ABC Corp - Underlayment]]
- [[Deal - XYZ Builders - Ridge Vents]]
```

**Column: Qualified**
```
- [[Deal - Smith Construction - NFA Ridge Vents]]
```

**Column: Quoted**
```
- [[Deal - Lone Star - Full Product Line]]
```

**Column: Won**
```
- [[Deal - Metro Supply - Initial Order]]
```

**Column: Lost**
```
- [[Deal - Hill Country - Deck Products]]
```

Drag cards between columns as deals move through the pipeline. Kanban syncs the underlying deal notes — moving a card doesn't change the note, it only changes the board display.

**Recommendation:** Use Kanban for visual status. Use Dataview for analysis and reporting. Both reference the same deal notes.

---

## Deal Note Sections (Inside Each Deal)

```markdown
## Deal: [deal_title]

**Value:** $XX,XXX | **Stage:** [[stage]] | **Probability:** XX%

### Company
[[company_link]]

### Contact
[[contact_link]]

### Products
- Product 1
- Product 2

---

## Next Steps

- [ ] **Immediate:** [next action]
- [ ] **This week:** [follow-up task]
- [ ] **Decision date:** [if known]

### Stage History
| Date | Stage | Notes |
|---|---|---|
| YYYY-MM-DD | Lead | ... |

---

## Notes

> Key conversation points, competitive intel, pricing decisions

---

## Related

- [[Company - company_name]]
- [[Contact - contact_name]]
- [[Meeting - YYYY-MM-DD - meeting_title]]
```

---

## HubSpot Integration

### Export from HubSpot (CSV)

1. Go to HubSpot → Deals → click the filter icon → Export
2. Export columns: `Deal Name`, `Amount`, `Stage`, `Close Date`, `Associated Company`, `Associated Contact`, `Next Step`
3. Save as `HubSpot Deals Export - YYYY-MM-DD.csv`

### Import to Obsidian

Run the import script (see `SCRIPTS/hubspot-import.py` — to be built if needed):

```bash
python3 SCRIPTS/hubspot-import.py --deals HubSpot\ Deals\ Export.csv
```

This creates deal notes in `03 Deals/` from the CSV, using the deal template.

### Manual HubSpot Sync (Alternative)

If HubSpot API access is available, use your private app token from `TOOLS.md`:
- Token: stored in `TOOLS.md` → HubSpot → Token
- Scopes: `crm.objects.deals.read`, `crm.objects.contacts.read`, `crm.objects.companies.read`

```python
import requests

# Token from TOOLS.md — keep this secret, never commit it
token = "YOUR_HUBSPOT_PRIVATE_APP_TOKEN"
headers = {"Authorization": f"Bearer {token}"}
url = "https://api.hubapi.com/crm/v3/objects/deals"

params = {"limit": 100, "properties": ["dealname", "amount", "dealstage", "closedate", "hs_priority"]}
r = requests.get(url, headers=headers, params=params)
deals = r.json()["results"]
```

### Sync Frequency

| Data | Frequency | Method |
|---|---|---|
| HubSpot → Obsidian | Weekly (Friday) | CSV export + script |
| Plaud Tasks → Obsidian | Daily (morning) | plaud-sync.py cron |
| Obsidian → HubSpot | Manual | Update HubSpot directly |

**Note:** Two-way sync between Obsidian and HubSpot is not fully automated. Treat Obsidian as the primary working CRM and sync to HubSpot periodically. This avoids data conflicts.

---

## Moving a Deal Through the Pipeline

1. Open the deal note
2. Update `stage:` in frontmatter (or use MetaEdit to click it inline)
3. Add a row to the Stage History table
4. If Won: set `closed: YYYY-MM-DD`, move card to Won column on Kanban
5. If Lost: set `closed: YYYY-MM-DD`, move card to Lost column, add reason to notes

**After 90 days, move Lost deals to `10 Archives/Deals - Closed/`.**

---

## Pipeline Health Metrics (Run Weekly)

### Total Pipeline Value
```dataview
TABLE sum(rows.value) AS "Total Pipeline"
FROM "03 Deals"
WHERE stage != "lost"
```

### Weighted Pipeline (probability-adjusted)
```dataview
TABLE round(sum(rows.value * rows.probability / 100), 0) AS "Weighted Pipeline"
FROM "03 Deals"
WHERE stage != "won" AND stage != "lost"
```

### Deals by Stage (funnel view)
```dataview
TABLE stage AS Stage, length(rows) AS Count, sum(rows.value) AS Value
FROM "03 Deals"
GROUP BY stage
```

### Average deal size by stage
```dataview
TABLE average(rows.value) AS "Avg Deal Size"
FROM "03 Deals"
WHERE stage != "won" AND stage != "lost"
GROUP BY stage
```

### Win rate (last 90 days)
```dataview
TABLE 
  length(filter(rows, (r) => r.stage = "won")) AS Won,
  length(filter(rows, (r) => r.stage = "lost")) AS Lost,
  round(length(filter(rows, (r) => r.stage = "won")) / 
    (length(filter(rows, (r) => r.stage = "won")) + length(filter(rows, (r) => r.stage = "lost"))) * 100, 1) AS "Win Rate %"
FROM "03 Deals"
WHERE closed >= (date(today) - dur(90 days))
```

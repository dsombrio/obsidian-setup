---
title: Daily Note - <% tp.date.now("YYYY-MM-DD") %>
date: <% tp.date.now("YYYY-MM-DD") %>
day_of_week: <% tp.date.now("dddd") %>
week_number: <% tp.date.now("gggg-[W]ww") %>
mood: 
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

**Top 3 priorities:**
1. 
2.
3.

---

## Morning Review

- [ ] Check Plaud tasks: ![[Plaud Tasks - <% tp.date.now("YYYY-MM-DD") %>]]
- [ ] Check pipeline for today's follow-ups
- [ ] Review calendar for today's meetings

---

## Tasks Due Today

```dataview
TASK
FROM "04 Tasks"
WHERE due = date(today) AND status = "pending"
SORT priority DESC
```

---

## Pipeline — Today's Follow-Ups

```dataview
TABLE company, contact, value, stage, next_step
FROM "03 Deals"
WHERE follow_up = date(today) AND stage != "won" AND stage != "lost"
SORT value DESC
```

---

## Meetings / Calls Today

| Time | Contact/Company | Notes |
|---|---|---|
|  |  |  |

---

## Plaud Tasks

![[Plaud Tasks - <% tp.date.now("YYYY-MM-DD") %>]]

---

## Log

### Calls Made
- 

### Emails Sent
- 

### Meetings
-

### Decisions Made
- 

### Issues / Blockers
-

---

## End of Day Summary

**Accomplished today:**
- 

**Tomorrow's priorities:**
1. 

---

## Related

- [[Meeting - <% tp.date.now("YYYY-MM-DD") %> - ]]
- [[]]

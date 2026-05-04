---
meeting_date: <% tp.date.now("YYYY-MM-DD") %>
contact: 
contact_link: [[]]
company: 
company_link: [[]]
attendees: [David Sombrio]
location: 
type: sales-call  # sales-call | discovery | proposal | negotiation | internal | vendor
outcome: 
next_action: 
follow_up: 
duration_minutes: 
---

# Meeting — <% tp.date.now("YYYY-MM-DD") %> — <% await tp.system.prompt("Contact/Company:") %>

**Date:** <% tp.date.now("YYYY-MM-DD") %>
**Contact:** [[]]
**Company:** [[]]
**Type:** 
**Attendees:** 

---

## Purpose

> What was the goal of this meeting?

---

## Discussion Summary

> Key topics discussed, questions asked, information shared

---

## Decisions Made

- 

---

## Action Items

- [ ] 

---

## Follow-Up Required

- [ ] Next step: 
- [ ] Follow-up date: 

---

## Notes

> Additional context, competitive intel, things to remember

---

## Related

- [[Contact - ]]
- [[Company - ]]
- [[Deal - ]]

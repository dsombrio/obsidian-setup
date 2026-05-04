---
deal_title: <% tp.file.title %>
company: 
company_link: [[]]
contact: 
contact_link: [[]]
value: 0
stage: lead  # lead | qualified | quoted | won | lost
probability: 10  # lead=10, qualified=30, quoted=60, won=100, lost=0
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

**Value:** ${{value}} | **Stage:** [[<% await tp.system.prompt("Stage:") %>]] | **Probability:** {{probability}}%

### Company
[[]]

### Contact
[[]]

---

## Next Steps

- [ ] **Immediate:** 
- [ ] **This week:** 

---

## Stage History

| Date | Stage | Notes |
|---|---|---|
| <% tp.date.now("YYYY-MM-DD") %> | Lead | Deal opened. |

---

## Notes

> Key conversation points, competitive intel, pricing context

---

## Related

- [[Company - ]]
- [[Contact - ]]
- [[Meeting - ]]

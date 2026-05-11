---
type: contact
id: {{CONTENT_ID}}
created: {{CREATED_DATE}}
tags:
  - CRM
  - contact
  - territory/{{TERRITORY}}
  - product/{{PRIMARY_PRODUCT}}
aliases: []
links:
  - [[{{COMPANY}}]]
  - [[deals/{{DEAL_NAME}}]]

# Contact Information
First Name:: {{FIRST_NAME}}
Last Name:: {{LAST_NAME}}
Full Name:: {{FULL_NAME}}
Company:: [[{{COMPANY}}]]
Job Title:: {{JOB_TITLE}}
Email:: {{EMAIL}}
Phone:: {{PHONE}}
Mobile:: {{MOBILE}}

# Location
City:: {{CITY}}
State:: {{STATE}}
Address:: {{ADDRESS}}

# Pipeline
Stage:: {{STAGE}}
Lead Source:: {{LEAD_SOURCE}}
Last Contact:: {{LAST_CONTACT}}
Next Step:: {{NEXT_STEP}}
Follow-up Date:: {{FOLLOWUP_DATE}}

# Notes
# Overview::
# Background::
# Decision Maker::
# Budget::
# Timeline::
---

## History

| Date | Type | Summary | Outcome |
|------|------|---------|---------|
| {{DATE}} | {{TYPE}} | {{SUMMARY}} | {{OUTCOME}} |

## Deals

```dataview
TABLE deal-name AS "Deal", amount AS "Value", stage AS "Stage", close-date AS "Close Date"
FROM "CRM/Deals"
WHERE contains(contacts, "{{FULL_NAME}}")
SORT close-date ASC
```

## Related Notes

- [[{{COMPANY}}]] — Company profile
- [[{{RELATED_COMPANY_2}}]] — Related company
- [[{{RELATED_NOTE}}}]] — Related note

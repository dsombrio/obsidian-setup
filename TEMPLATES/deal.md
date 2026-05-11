---
type: deal
id: {{DEAL_ID}}
created: {{CREATED_DATE}}
tags:
  - CRM
  - deal
  - product/{{PRODUCT_LINE}}
  - territory/{{TERRITORY}}
  - stage/{{STAGE}}
links:
  - [[contacts/{{CONTACT_NAME}}]]
  - [[companies/{{COMPANY}}]]

# Deal Overview
Deal Name:: {{DEAL_NAME}}
Company:: [[{{COMPANY}}]]
Contact:: [[contacts/{{CONTACT_NAME}}]]
Product Line:: {{PRODUCT_LINE}}

# Value & Timeline
Estimated Value:: ${{AMOUNT}}
Commission Rate:: {{COMMISSION_RATE}}%
Estimated Commission:: ${{COMMISSION}}
Stage:: {{STAGE}}
Close Date:: {{CLOSE_DATE}}
Days in Stage:: {{DAYS_IN_STAGE}}

# Next Steps
Next Step:: {{NEXT_STE}}
Follow-up Date:: {{FOLLOWUP_DATE}}
Priority:: {{PRIORITY}}

# Notes
# Competitors Being Evaluated::
# Why We Won/Lost::
# Special Terms::
---

## Stage History

| Date | From Stage | To Stage | Notes | Owner |
|------|-----------|----------|-------|-------|
| {{DATE}} | {{FROM_STAGE}} | {{TO_STAGE}} | {{NOTES}} | {{OWNER}} |

## Tasks

```dataview
TASK
FROM "CRM/Deals/{{DEAL_NAME}}"
WHERE contains(tags, "{{DEAL_NAME}}")
SORT priority ASC
```

## Emails

- {{EMAIL_DATE}} — {{EMAIL_SUBJECT}} — {{EMAIL_OUTCOME}}

## Notes

> {{NOTES}}

#!/usr/bin/env python3
"""
import_plaud_to_obsidian.py
Reads plaud-todos.md and generates Obsidian-ready company/contact/deal/note files.
Run: python3 import_plaud_to_obsidian.py
Output: IMPORT/ folder with markdown files ready to drop into Obsidian
"""

import re
import os
from pathlib import Path
from datetime import datetime

TODO_FILE = '/Users/tradbot/.openclaw/workspace/plaud-todos.md'
OUTPUT_DIR = Path('/Users/tradbot/.openclaw/workspace/obsidian-setup/IMPORT')

# ─────────────────────────────────────────────────────────
# PARSING HELPERS
# ─────────────────────────────────────────────────────────

def extract_tasks_by_contact(content):
    """Parse plaud-todos.md and return structured list of (contact, company, task)"""
    
    # Regex: lines that look like task items with contact/company pattern
    task_pattern = re.compile(
        r'^\- \[ \] \**([^\*]+?)\** \(([^\)]+)\)\s*[-–] (.+)$',
        re.MULTILINE
    )
    
    results = []
    for line in content.split('\n'):
        match = task_pattern.match(line.strip())
        if match:
            name_company = match.group(1).strip()  # "Name" or "Name (Company)"
            raw_task = match.group(3).strip()
            
            # Skip internal tasks
            if any(skip in name_company for skip in ['Internal', 'Field Sales', 'Field Playbook', 'Texas Market', 'Market Expansion']):
                continue
            
            # Split name from company
            if ' (' in name_company and name_company.endswith(')'):
                paren_idx = name_company.rindex(' (')
                name = name_company[:paren_idx].strip()
                company = name_company[paren_idx+2:-1].strip()
            else:
                name = name_company
                company = ''
            
            results.append({
                'name': name,
                'company': company,
                'task': raw_task,
            })
    
    return results

def extract_companies_from_context(content):
    """Extract company names from context (lines with company mentions)"""
    
    # Look for company-like patterns in context
    companies = set()
    # Common company patterns: Company Name (Location) or ABC Branch or Company/Contact
    patterns = [
        r'(?:^|\n)[-•*] (.*(?:Lumber|Supply|Building|ABC Supply|Branch|Roofing|Door|Window|Lightning|Hardware|Closet|Mill|Truss|Lumberyard))',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        for m in matches:
            cleaned = m.strip().strip('•*').strip()
            if cleaned and len(cleaned) > 2:
                companies.add(cleaned)
    
    return list(companies)

# ─────────────────────────────────────────────────────────
# STRUCTURED DATA
# ─────────────────────────────────────────────────────────

# Manually curated from plaud-todos.md analysis
CONTACTS = [
    # ABC Supply
    {"name": "Carol Nowell", "company": "ABC Supply", "type": "customer", "metro": "Conroe", "email": "", "phone": ""},
    {"name": "Jack", "company": "ABC Supply", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Sean", "company": "ABC Supply", "type": "customer", "metro": "Houston", "email": "", "phone": ""},
    {"name": "Elena", "company": "ABC Supply", "type": "customer", "metro": "Houston", "email": "", "phone": ""},
    {"name": "Laura S.", "company": "ABC Supply", "type": "customer", "metro": "Houston", "email": "", "phone": ""},
    {"name": "Natasha", "company": "ABC Supply", "type": "customer", "metro": "Houston", "email": "", "phone": ""},
    {"name": "Brandon", "company": "ABC Supply", "type": "customer", "metro": "Houston", "email": "", "phone": ""},
    {"name": "Jacob", "company": "ABC Supply", "type": "customer", "metro": "Rosenberg", "email": "", "phone": ""},
    {"name": "Kyle", "company": "ABC Supply", "type": "customer", "metro": "Houston (near Bush Airport)", "email": "", "phone": ""},
    {"name": "Sean", "company": "ABC Supply", "type": "customer", "metro": "Twelfth Street", "email": "", "phone": ""},
    
    # Lindsay Windows
    {"name": "Natasha", "company": "Lindsay Windows", "type": "vendor", "metro": "Houston", "email": "", "phone": ""},
    
    # Home Guard
    {"name": "Matt", "company": "Home Guard Distributor", "type": "prospect", "metro": "", "email": "", "phone": ""},
    
    # Builders / Projects
    {"name": "David Schuyler", "company": "Builder (Salt Lake)", "type": "customer", "metro": "Salt Lake", "email": "", "phone": ""},
    {"name": "Tim", "company": "Multifamily Developer", "type": "customer", "metro": "", "email": "", "phone": ""},
    
    # Woodson Lumber
    {"name": "Donna Dickson", "company": "Woodson Lumber", "type": "customer", "metro": "", "email": "", "phone": ""},
    
    # El Cavo Lumber
    {"name": "Christie", "company": "El Cavo Lumber", "type": "prospect", "metro": "Victoria, TX", "email": "", "phone": ""},
    
    # H and H Doors
    {"name": "", "company": "H and H Doors", "type": "prospect", "metro": "Victoria, TX", "email": "", "phone": ""},
    
    # SGM
    {"name": "Jennifer", "company": "SGM", "type": "prospect", "metro": "Victoria, TX", "email": "", "phone": ""},
    
    # Victoria Builder Supply
    {"name": "", "company": "Victoria Builder Supply", "type": "prospect", "metro": "Victoria, TX", "email": "", "phone": ""},
    
    # HGS Roofing
    {"name": "Bobber", "company": "HGS Roofing & Siding", "type": "prospect", "metro": "", "email": "sales@hgsroofing.com", "phone": ""},
    
    # Door Components
    {"name": "Daniel", "company": "Door Components", "type": "customer", "metro": "Fort Worth", "email": "", "phone": ""},
    
    # Ernie's Hardware
    {"name": "", "company": "Ernie's Hardware", "type": "prospect", "metro": "Sour Lake, TX", "email": "", "phone": ""},
    
    # M and D Hardware
    {"name": "", "company": "M and D Hardware", "type": "prospect", "metro": "Texas (10 locations)", "email": "", "phone": ""},
    
    # Diana
    {"name": "Diana", "company": "Building Materials (Diana)", "type": "prospect", "metro": "", "email": "", "phone": ""},
    
    # Stephen
    {"name": "Stephen", "company": "Ridge Vent Contact", "type": "prospect", "metro": "", "email": "", "phone": ""},
    
    # Wyatt
    {"name": "Wyatt", "company": "Roofing Contact", "type": "prospect", "metro": "", "email": "", "phone": ""},
    
    # McKenzie
    {"name": "McKenzie", "company": "Lindsey Windows", "type": "vendor", "metro": "", "email": "", "phone": ""},
    
    # Russell Thomas
    {"name": "Russell Thomas", "company": "", "type": "prospect", "metro": "Boise", "email": "", "phone": ""},
    
    # USLBM contacts
    {"name": "Trent", "company": "USLBM", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Kaylee", "company": "USLBM", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Hernando", "company": "USLBM", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Luke", "company": "USLBM", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Jerry", "company": "USLBM", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Jimmy", "company": "USLBM (multifamily)", "type": "customer", "metro": "", "email": "", "phone": ""},
    {"name": "Tactate", "company": "USLBM (multifamily)", "type": "customer", "metro": "", "email": "", "phone": ""},
    
    # Parker's
    {"name": "", "company": "Parker's (builder pricing)", "type": "partner", "metro": "", "email": "", "phone": ""},
    
    # Texas Closet Supplier
    {"name": "", "company": "Texas Closet Supplier", "type": "customer", "metro": "Texas", "email": "", "phone": ""},
    
    # Home Guard Distributor
    {"name": "Matt", "company": "Home Guard Distributor", "type": "prospect", "metro": "", "email": "", "phone": ""},
    
    # American Flashings contacts
    {"name": "Brittany", "company": "BFS / American Flashings", "type": "vendor", "metro": "", "email": "", "phone": ""},
    
    # 84 Lumber
    {"name": "Ray", "company": "84 Lumber", "type": "customer", "metro": "Austin", "email": "", "phone": ""},
]

COMPANIES = [
    {"name": "ABC Supply", "type": "distributor", "metro": "Texas (17 Houston locations)", "status": "active", "notes": "Key distributor account. Focus: Lindsay Windows brand setup, American Flashings expansion, house wrap custom branding."},
    {"name": "Lindsay Windows", "type": "vendor", "metro": "", "status": "active", "notes": "Vinyl window manufacturer. 300 series, 3000 series launching. Brand setup in progress at ABC Supply. Finovision quoting system access needed."},
    {"name": "Home Guard Distributor", "type": "prospect", "metro": "", "status": "active", "notes": "Distributor interested in house wrap, custom branding (84 logo), seam tape. Potential for large volume."},
    {"name": "Woodson Lumber", "type": "customer", "metro": "", "status": "active", "notes": "Needs Lindsay Windows i89 glass type one-pager (366 Low-E/Clear vs 366 Low-E/I89 comparison)."},
    {"name": "84 Lumber", "type": "customer", "metro": "Austin", "status": "active", "notes": "Mill Creek project. Ray in Austin to review pricing."},
    {"name": "El Cavo Lumber", "type": "prospect", "metro": "Victoria, TX", "status": "prospect", "notes": "Carries MI and Robinson mostly. Visit planned."},
    {"name": "H and H Doors", "type": "prospect", "metro": "Victoria, TX", "status": "prospect", "notes": "Interested in adjustable metal door frames. Visit planned."},
    {"name": "HGS Roofing & Siding", "type": "prospect", "metro": "", "status": "prospect", "notes": "Contact: Bobber. Referred by Selma. Call to qualify."},
    {"name": "Door Components", "type": "customer", "metro": "Fort Worth", "status": "active", "notes": "Contact: Daniel. Needs pricing and product info with delivered pricing and lead times."},
    {"name": "SGM", "type": "prospect", "metro": "Victoria, TX", "status": "prospect", "notes": "Contact: Jennifer. Needs timely doorframe info."},
    {"name": "Victoria Builder Supply", "type": "prospect", "metro": "Victoria, TX", "status": "prospect", "notes": "Needs Showcase line, Windstorm certification. PDF brochures and credit app to send."},
    {"name": "USLBM", "type": "distributor", "metro": "Texas", "status": "active", "notes": "Large building materials distributor. Multiple contacts (Trent, Kaylee, Hernando, Luke, Jerry, Jimmy, Tactate). American Flashings + Lindsey Windows evaluation in progress."},
    {"name": "Ernie's Hardware", "type": "prospect", "metro": "Sour Lake, TX", "status": "prospect", "notes": "Outbound call target."},
    {"name": "M and D Hardware", "type": "prospect", "metro": "Texas (10 locations)", "status": "prospect", "notes": "Outbound call target (10 locations)."},
    {"name": "Texas Closet Supplier", "type": "customer", "metro": "Texas", "status": "active", "notes": "Annual volume $400K-$500K+. Pending price sheet update with improved pricing tier."},
    {"name": "BFS / American Flashings", "type": "vendor", "metro": "", "status": "active", "notes": "Roofing accessories, house wrap, underlayment. Brittany is contact. Custom branding interest (6-pallet min)."},
    {"name": "Parker's (builder pricing)", "type": "partner", "metro": "", "status": "active", "notes": "Partner for David Schuyler Salt Lake 6-home project. Needs package pricing to undercut Elevate."},
    {"name": "Builder (Salt Lake)", "type": "customer", "metro": "Salt Lake", "status": "active", "notes": "David Schuyler. 6-home project. Needs quote by Tuesday. Competing against Elevate. Parker's involvement."},
    {"name": "Multifamily Developer", "type": "customer", "metro": "", "status": "active", "notes": "Tim. Urgent multifamily quote needed by May 7. Vendor setup at specific branch is blocker."},
    {"name": "Hobby Airport", "type": "project", "metro": "Houston", "status": "active", "notes": "STC 33 and STC 28 rated windows needed. Contact: Building Materials Company (Speaker 2)."},
]

DEALS = [
    {"title": "David Schuyler - Salt Lake 6-Home Project", "company": "Builder (Salt Lake)", "contact": "David Schuyler", "value": 0, "stage": "quoted", "notes": "Urgent. Quote needed before Tuesday. Parker's pricing to undercut Elevate. Lindsay Windows + ridge vents."},
    {"title": "Tim - Urgent Multifamily Quote", "company": "Multifamily Developer", "contact": "Tim", "value": 0, "stage": "urgent", "notes": "Needed by May 7. Vendor setup at specific branch is blocker. Window schedule received via Plaud."},
    {"title": "ABC Supply - Lindsay Windows Brand Setup", "company": "ABC Supply", "contact": "Sean/Elena", "value": 0, "stage": "in_progress", "notes": "Finovision access needed. Impact-rated vinyl line launching next month. Size constraints to send."},
    {"title": "American Flashings - ABC Houston Branch", "company": "ABC Supply", "contact": "Natasha/Brandon", "value": 0, "stage": "in_progress", "notes": "Pallet pricing, SKU list, lead times needed. Brand setup form submitted."},
    {"name": "Matt (Home Guard) - House Wrap Deal", "company": "Home Guard Distributor", "contact": "Matt", "value": 0, "stage": "qualified", "notes": "Custom branding (84 logo), seam tape interest. Follow up after materials review."},
    {"title": "84 Lumber Austin - Mill Creek Project", "company": "84 Lumber", "contact": "Ray", "value": 0, "stage": "reviewing", "notes": "Pricing review needed. Ray to call in AM."},
    {"title": "Caldwell Projects - Window Bid (Kerrville $70K)", "company": "Caldwell", "contact": "", "value": 70000, "stage": "bidding", "notes": "Active bid in Kerrville. $70K windows. Loses on trophy pricing ($20K over)."},
    {"title": "Hobby Airport - STC Windows", "company": "Hobby Airport", "contact": "Building Materials Company", "value": 0, "stage": "bidding", "notes": "STC 33 and STC 28 ratings needed. Building Materials Company (Speaker 2) handling."},
]

# ─────────────────────────────────────────────────────────
# FILE GENERATORS
# ─────────────────────────────────────────────────────────

def slug(text):
    text = text.replace('/', '-').replace('//', '-')
    return re.sub(r'[^a-zA-Z0-9]', '-', text.strip())

def mdy():
    return datetime.now().strftime('%Y-%m-%d')

def write_company(c):
    folder = OUTPUT_DIR / '01 - Companies'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{slug(c['name'])}.md"
    content = f"""---
company_name: {c['name']}
type: {c['type']}
metro: 
status: {c['status']}
created: {mdy()}
notes: >
  {c.get('notes', '')}

---

## {c['name']}

**Type:** [[{c['type']}]]
**Metro:** 
**Status:** [[{c['status']}]]

---

## Key Contacts

- [[Contact - ]]

---

## Active Deals

- [[Deal - ]]

---

## Notes

> 
"""
    path.write_text(content)
    print(f"  COMPANY: {c['name']}")

def write_contact(c):
    folder = OUTPUT_DIR / '02 - Contacts'
    folder.mkdir(parents=True, exist_ok=True)
    name_slug = slug(c['name']) if c['name'] else slug(c['company'])
    path = folder / f"{name_slug}.md"
    company_link = f"[[01 - Companies/{c['company']}]]" if c['company'] else ""
    
    content = f"""---
contact_name: {c['name'] or c['company']}
first_name: 
last_name: 
company: {c['company']}
company_link: {company_link}
title: 
phone: {c.get('phone', '')}
email: {c.get('email', '')}
metro: {c.get('metro', '')}
type: {c['type']}
status: active
created: {mdy()}
tags: []
---

## {c['name'] or c['company']}

**Company:** {company_link or '[[]]'}
**Type:** [[{c['type']}]]
**Metro:** {c.get('metro', '')}

---

## Notes

> 

---

## Active Deals

- [[Deal - ]]

"""
    path.write_text(content)
    print(f"  CONTACT: {c['name'] or c['company']} @ {c['company']}")

def write_deal(d):
    folder = OUTPUT_DIR / '03 - Deals'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{slug(d.get('title', d.get('name', '')))}.md"
    company_link = f"[[01 - Companies/{d['company']}]]" if d['company'] else ""
    contact_link = f"[[02 - Contacts/{slug(d['contact'])}]]" if d['contact'] else ""
    
    content = f"""---
deal_title: {d.get('title', d.get('name', ''))}
company: {d['company']}
company_link: {company_link}
contact: {d['contact']}
contact_link: {contact_link}
value: {d['value']}
stage: {d['stage']}
probability: 20
next_step: 
follow_up: 
opened: {mdy()}
tags: []
notes: >
  {d.get('notes', '')}

---

## Deal: {d.get('title', d.get('name', ''))}

**Value:** ${d['value']:,} | **Stage:** [[{d['stage']}]]

### Company
{company_link or '[[]]'}

### Contact
{contact_link or '[[]]'}

---

## Next Steps

- [ ] 

"""
    path.write_text(content)
    print(f"  DEAL: {d.get('title', d.get('name', ''))}")

def write_call_log(date_str, contact, company, summary, tasks):
    folder = OUTPUT_DIR / '04 - Call Logs'
    folder.mkdir(parents=True, exist_ok=True)
    contact_slug = slug(contact) if contact else slug(company)
    path = folder / f"{date_str} - Call with {contact_slug}.md"
    
    company_link = f"[[01 - Companies/{company}]]" if company else ""
    contact_link = f"[[02 - Contacts/{slug(contact)}]]" if contact else ""
    
    task_items = '\n'.join([f"- [ ] {t}" for t in tasks]) if tasks else "- [ ] "
    
    content = f"""---
contact: {contact or ''}
contact_link: {contact_link}
company: {company or ''}
company_link: {company_link}
date: {date_str}
source: plaud
summary: {summary}
follow_up_required: {'true' if tasks else 'false'}
---

## Call with {contact or company}

**Date:** {date_str}
**Company:** {company_link}
**Source:** [[plaud]]

---

### Summary

{summary}

---

### Action Items

{task_items}

"""
    path.write_text(content)
    print(f"  CALL LOG: {date_str} - {contact or company}")

# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

def main():
    print(f"\nGenerating Obsidian CRM files...")
    print(f"Output: {OUTPUT_DIR}")
    
    for c in COMPANIES:
        write_company(c)
    
    for c in CONTACTS:
        write_contact(c)
    
    for d in DEALS:
        write_deal(d)
    
    print(f"\nDone. {len(COMPANIES)} companies, {len(CONTACTS)} contacts, {len(DEALS)} deals generated.")
    print(f"Folder: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
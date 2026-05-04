# Obsidian Plugin Setup — Tradition Sales

A curated plugin stack for running a building materials sales agency as a second brain, CRM, and pipeline manager — all from Obsidian on iPhone and Mac.

---

## Core Plugins (Install First)

These ship with Obsidian or are maintained by the core team:

| Plugin | Purpose |
|---|---|
| **Daily Notes** | Creates a note for each day. Foundation of the workflow. |
| **Templates** | Insert pre-built note templates (contact, deal, meeting, etc.). |
| **Search** | Full-text search across all vault content. |
| **Graph View** | Visual map of how notes link together. |
| **Starred** | Pin frequently accessed notes, queries, and folders. |

---

## Community Plugins (Install via Community Plugins browser)

### 1. **Templater** (`templater-obsidian`)
**Why:** More powerful than the built-in Templates plugin. Supports dynamic variables (date, time, folder paths, clipboard content, Obsidian metadata).

**Settings to configure:**
- Template folder: `Templates/`
- Trigger: `tp.date` for dates, `tp.file.title` for filenames
- Enable "Kernel Ready" for startup scripts

**Use for:** Auto-naming files (`Contact - John Smith.md`), inserting today's date, auto-linking to the daily note.

---

### 2. **QuickAdd** (`quickadd`)
**Why:** Create notes and capture thoughts with a hotkey or command-palette search. Faster than using Templates alone.

**Setup:**
- Add a "Daily Capture" macro that creates a note in `Inbox/` with a QuickAdd command
- Add a "New Contact" macro that creates from `Templates/contact.md`
- Add a "New Deal" macro for pipeline entries

---

### 3. **Dataview** (`obsidian-dataview`)
**Why:** The backbone of the CRM and pipeline. Queries your vault like a database — find all deals in "Quoted" stage, all contacts in Texas, all tasks due today.

**Key queries to use from day one:**

```dataview
TABLE stage, value, contact
FROM "Deals"
WHERE stage = "quoted"
SORT value DESC
```

```dataview
TABLE due_date, priority, title
FROM "Tasks"
WHERE status = "pending" AND due_date <= date(today)
SORT due_date ASC
```

```dataview
TABLE phone, email, company, metro
FROM "Contacts"
WHERE metro = "Dallas"
```

---

### 4. **Tasks** (`obsidian-tasks-plugin`)
**Why:** Turns checkbox tasks into a proper task manager. Supports due dates, priorities, start dates, recurring tasks, and filtering — all queryable inline in any note.

**Why better than plain checkboxes:** Each task can have `due(2026-05-10)`, `priority(high)`, `recurring weekly)`. Dataview can also query Tasks data.

**Syntax example:**
```
- [ ] Follow up with Zarsky on quote #task
  due(2026-05-10) priority(high)
```

---

### 5. **Kanban** (`obsidian-kanban`)
**Why:** Visual pipeline view. Create a board per sales stage (Lead → Qualified → Quoted → Won/Lost). Drag-and-drop deal cards between columns.

**Setup:**
- One board at `Pipeline/Pipeline Board.md`
- Each column is a stage
- Each card is a link to a deal note: `[[Deals/Deal - ABC Corp]]`
- Use Dataview for the numeric pipeline summary; Kanban for the visual view

---

### 6. **MetaEdit** (`metaedit`)
**Why:** Add and edit frontmatter (YAML metadata) from within a note, without manually editing YAML. Useful for updating deal stage, contact status, etc.

**Use with:** Dataview to create dashboards that read frontmatter fields.

---

### 7. **Buttons** (`obsidian-buttons`)
**Why:** Add clickable buttons inside notes to trigger actions — "Log Call", "Move to Qualified", "Create Follow-up Task".

**Example button:**
```
^button-qualified
[type:: query]
_action:: set_field
pipeline-stage:: Qualified
```

---

### 8. **Obsidian Git** (`obsidian-git`)
**Why:** Auto-commit and push your vault to GitHub on a schedule. Backup + version history. Works on Mac; on iPhone, rely on iCloud sync and the git backup as a secondary layer.

**Settings:**
- Commit message: `vault backup: {{date}}`
- Sync interval: `30` minutes (Mac only)
- Push on commit: ON

---

### 9. **Calendar** (`obsidian-calendar-plugin`)
**Why:** Visual calendar sidebar showing which days have daily notes. Click any date to open/create that day's note.

---

### 10. **Reminder** (`obsidian-reminder`)
**Why:** Set reminders on any task or line in Obsidian. Notifications appear in-app and (with the right setup) as system notifications.

---

## iPhone-Specific Notes

- **iOS Shortcuts** can open a specific Obsidian note via: `Open Obsidian Note` action
- Shortcuts can also create notes in a specific vault folder using the `Append to Note` action
- **Obsidian Shell Commands** does NOT work on iOS — do not rely on it
- The **Shell Commands** plugin (different) and any terminal scripting only runs on Mac
- iCloud sync handles vault sync between iPhone and Mac automatically. Enable it in Obsidian → Settings → Sync → iCloud

---

## Plugin Priority Order (Install Sequence)

1. Daily Notes + Templates (built-in)
2. **Templater** — enables all templates to work properly
3. **Dataview** — CRM and pipeline queries
4. **Tasks** — task management
5. **QuickAdd** — fast capture
6. **Kanban** — visual pipeline
7. **MetaEdit** — inline metadata editing
8. **Buttons** — action buttons
9. **Calendar** — date navigation
10. **Reminder** — notifications
11. **Obsidian Git** — backup (Mac only)

---

## Vault Sync Strategy

| Device | Sync Method |
|---|---|
| Mac | iCloud (primary) + Obsidian Git (backup) |
| iPhone | iCloud (native) |

On iPhone, Obsidian must be installed from the App Store and the vault must be stored in iCloud Drive (not local). Configure this in Obsidian → Settings → Sync → iCloud.

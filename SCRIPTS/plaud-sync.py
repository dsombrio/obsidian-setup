#!/usr/bin/env python3
"""
plaud-sync.py
Bridges Plaud todos to Obsidian.

Reads pending tasks from the Plaud SQLite database and writes them
to an Obsidian-formatted daily tasks note that Dataview and the
Tasks plugin can read.

Usage:
    python3 plaud-sync.py

Configuration:
    Edit the CONFIG section below to set your Plaud DB path and
    Obsidian vault paths.

Cron / Launchd:
    Run daily via cron or launchd on your Mac. iPhone gets the
    results automatically via iCloud sync.
"""

import sqlite3
import os
import sys
from datetime import datetime, date
from pathlib import Path

# ============================================================
# CONFIGURATION — edit these to match your setup
# ============================================================

PLAUD_DB = "/Users/tradbot/Library/Application Support/TradBot/crm.db"

# Path to your Obsidian vault.
# On Mac: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>
# On iPhone: Same vault syncs via iCloud — no script runs on iPhone
# IMPORTANT: Update this path to your actual Obsidian vault location.
# On iPhone/Mac with iCloud sync, find it in:
#   Obsidian → Settings → About → Vault path
# Typical iCloud path format:
#   /Users/tradbot/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>
OBSIDIAN_VAULT = "/Users/tradbot/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tradition Sales"

# Folder within vault for task notes (relative path)
TASKS_FOLDER = "04 Tasks"

# Folder for daily notes (used to embed tasks)
DAILY_FOLDER = "00 Daily"

# Log file path
LOG_DIR = "/Users/tradbot/.openclaw/workspace/logs"
LOG_FILE = os.path.join(LOG_DIR, "plaud-sync.log")

# ============================================================
# /END CONFIGURATION
# ============================================================

def log(msg: str):
    """Write a timestamped log message to the log file and stdout."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass  # Don't crash on logging errors


def get_connection(db_path: str) -> sqlite3.Connection:
    """Open SQLite connection with a short timeout and WAL mode."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Plaud database not found at: {db_path}")
    conn = sqlite3.connect(db_path, timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def fetch_pending_tasks(conn: sqlite3.Connection) -> list:
    """
    Fetch all pending Plaud tasks from the database.
    Returns a list of dicts with keys matching the tasks table schema.
    """
    query = """
        SELECT
            t.id,
            t.title,
            t.description,
            t.due_date,
            t.timeframe_minutes,
            t.source,
            t.status,
            t.created_at,
            t.completed_at,
            t.priority,
            t.contact_id,
            t.deal_id,
            c.first_name || ' ' || COALESCE(c.last_name, '') AS contact_name,
            c.company AS contact_company
        FROM tasks t
        LEFT JOIN contacts c ON t.contact_id = c.id
        WHERE t.status = 'pending'
        ORDER BY
            CASE t.priority
                WHEN 'high'   THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low'    THEN 3
                ELSE 4
            END,
            t.due_date ASC,
            t.created_at ASC
    """
    rows = conn.execute(query).fetchall()
    columns = [
        "id", "title", "description", "due_date", "timeframe_minutes",
        "source", "status", "created_at", "completed_at", "priority",
        "contact_id", "deal_id", "contact_name", "contact_company"
    ]
    return [dict(zip(columns, row)) for row in rows]


def format_timeframe(minutes: int) -> str:
    """Convert minutes to a human-readable string."""
    if not minutes:
        return ""
    if minutes < 60:
        return f"{minutes}min"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}min"


def format_task_block(task: dict, vault_path: Path) -> str:
    """Format a single task as an Obsidian Tasks-plugin block."""
    task_id = task["id"]
    title = task["title"].strip() if task["title"] else "(no title)"
    description = task["description"].strip() if task["description"] else ""
    due_date = task["due_date"] if task["due_date"] else ""
    priority = task["priority"] or "medium"
    source = task["source"] or "manual"
    timeframe = format_timeframe(task["timeframe_minutes"])
    contact_name = task["contact_name"].strip() if task["contact_name"] else ""
    contact_company = task["contact_company"].strip() if task["contact_company"] else ""

    # Obsidian Tasks plugin tags
    priority_tag = f"#{priority}"

    # Build the task line (Tasks plugin format)
    task_line = f"- [ ] **{title}** {priority_tag}"

    # Block ID for uniqueness (Obsidian tasks plugin can use this)
    block_id = f"^plaud-task-{task_id}"

    # Metadata line
    meta_parts = []
    if due_date:
        meta_parts.append(f"Due: {due_date}")
    if contact_name:
        meta_parts.append(f"Contact: {contact_name}")
    if contact_company:
        meta_parts.append(f"Company: {contact_company}")
    if timeframe:
        meta_parts.append(f"Time: {timeframe}")
    if source:
        meta_parts.append(f"Source: {source.capitalize()}")
    meta_line = " | ".join(meta_parts)

    # Description (if present)
    desc_block = ""
    if description:
        desc_block = f"\n  > {description[:200]}{'...' if len(description) > 200 else ''}"

    # Contact link (if we have a contact name)
    contact_link = ""
    if contact_name:
        # Try to link to the Obsidian contact note if it exists
        contact_file = f"{contact_name.split()[0]} - {contact_name.split()[-1]}.md"
        contact_link = f"\n  -> [[01 Contacts/{contact_file}|View Contact]]"

    lines = [
        task_line,
        f"  {block_id}",
        f"  {meta_line}{desc_block}{contact_link}",
    ]
    return "\n".join(lines)


def build_tasks_note(tasks: list, vault_path: Path, run_date: date) -> str:
    """Build the full Obsidian note content for Plaud tasks."""
    today_str = run_date.strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"Plaud Tasks - {today_str}.md"

    lines = [
        "---",
        f"title: Plaud Tasks",
        f"date: {today_str}",
        "source: plaud-sync",
        f"task_count: {len(tasks)}",
        "---",
        "",
        f"# Plaud Tasks — {today_str}",
        "",
        f"*Generated by plaud-sync.py at {now_str}*",
        "",
    ]

    if not tasks:
        lines.append("*No pending Plaud tasks.*")
        return "\n".join(lines), filename

    # Group by priority
    by_priority = {"high": [], "medium": [], "low": [], "none": []}
    for t in tasks:
        p = t.get("priority", "medium") or "medium"
        if p not in by_priority:
            p = "medium"
        by_priority[p].append(t)

    for priority_label in ["high", "medium", "low"]:
        group = by_priority.get(priority_label, [])
        if not group:
            continue
        header = f"## {priority_label.capitalize()} Priority"
        lines.append(header)
        lines.append("")
        for task in group:
            lines.append(format_task_block(task, vault_path))
            lines.append("")

    # Legacy plain checkbox format for Dataview compatibility
    lines.extend([
        "---",
        "",
        "## Plain Task List (Dataview compatible)",
        "",
    ])
    for task in tasks:
        title = task["title"].strip() if task["title"] else "(no title)"
        due = task["due_date"] or ""
        priority = task.get("priority", "medium") or "medium"
        contact = task["contact_name"].strip() if task["contact_name"] else ""
        block_id = f"plaud-task-{task['id']}"
        due_str = f" @due({due})" if due else ""
        contact_str = f" @contact({contact})" if contact else ""
        lines.append(f"- [ ] {title} #task #{priority}{due_str}{contact_str} ^{block_id}")

    lines.extend([
        "",
        "---",
        "",
        "*This file is auto-generated by plaud-sync.py. Do not edit manually.*",
        "*To mark a task complete, check it off here or in Plaud.*",
    ])

    return "\n".join(lines), filename


def ensure_folder(path: Path) -> None:
    """Create folder if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def main():
    log("plaud-sync.py started")

    # Resolve paths
    vault_path = Path(OBSIDIAN_VAULT).expanduser()
    tasks_folder = vault_path / TASKS_FOLDER
    log(f"Vault: {vault_path}")
    log(f"Tasks folder: {tasks_folder}")

    if not vault_path.exists():
        log(f"ERROR: Vault not found at {vault_path}")
        log("Make sure OBSIDIAN_VAULT in the CONFIG section matches your vault path.")
        sys.exit(1)

    ensure_folder(tasks_folder)
    ensure_folder(Path(LOG_DIR))

    # Connect to Plaud DB
    try:
        log(f"Connecting to Plaud DB: {PLAUD_DB}")
        conn = get_connection(PLAUD_DB)
    except FileNotFoundError as e:
        log(f"ERROR: {e}")
        sys.exit(1)
    except sqlite3.Error as e:
        log(f"SQLite error: {e}")
        sys.exit(1)

    # Fetch tasks
    try:
        tasks = fetch_pending_tasks(conn)
        log(f"Fetched {len(tasks)} pending tasks from Plaud DB")
    except sqlite3.Error as e:
        log(f"Error fetching tasks: {e}")
        conn.close()
        sys.exit(1)
    finally:
        conn.close()

    # Build note content
    run_date = date.today()
    content, filename = build_tasks_note(tasks, vault_path, run_date)

    # Write the note
    output_path = tasks_folder / filename
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"Written: {output_path}")
    except IOError as e:
        log(f"ERROR writing note: {e}")
        sys.exit(1)

    # Also update/create today's daily note embedding (optional)
    # Only do this if the daily note exists
    daily_path = vault_path / DAILY_FOLDER / f"{run_date.strftime('%Y-%m-%d')}.md"
    embed_line = f"\n![[Plaud Tasks - {run_date.strftime('%Y-%m-%d')}]]\n"
    marker = f"Plaud Tasks - {run_date.strftime('%Y-%m-%d')}"

    if daily_path.exists():
        try:
            with open(daily_path, "r", encoding="utf-8") as f:
                existing = f.read()
            if marker not in existing:
                with open(daily_path, "a", encoding="utf-8") as f:
                    f.write(f"\n## Plaud Tasks\n{embed_line}\n")
                log(f"Updated daily note: {daily_path}")
        except IOError as e:
            log(f"Warning: could not update daily note: {e}")
    else:
        log(f"Daily note not found at {daily_path} — skipping embed update")

    log(f"plaud-sync.py completed successfully. {len(tasks)} tasks written.")


if __name__ == "__main__":
    main()

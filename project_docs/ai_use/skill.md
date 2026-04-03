---
name: ai-usage-log
description: >
  Use this skill whenever the user wants to read, update, append to, or analyze their
  AI_USAGE.md log file. Trigger when the user mentions logging AI usage, adding an entry,
  reviewing past AI tool use, or references the AI_USAGE.md or AI_USAGE_template.md files.
  Also trigger if the user says things like "log this session", "add an entry for today",
  "what tools did I use last week", or "update my AI log".
---

# AI Usage Log Skill

Helps Claude read, write, and manage the user's `AI_USAGE.md` log file, which tracks
AI tool usage across sessions. The template lives in `AI_USAGE_template.md`.

## File Locations

- **Log file**: `project_docs/ai_use/AI_USAGE.md` (read-only mount — output edits to `project_docs/ai_use/AI_USAGE.md`)
- **Template**: `project_docs/ai_use/AI_USAGE.template.md`

> Since uploads are read-only, always write the updated file to `project_docs/ai_use/AI_USAGE.md`
> and inform the user to replace their source file with the output.

## Entry Format

Based on the template, each entry follows this structure:

```markdown
## YYYY-MM-DD
- Tool: <tool name, e.g. "Codex VS Code", "Claude claude.ai", "GitHub Copilot">
- Model: <model name if known, e.g. "claude-sonnet-4", "gpt-4o">
- Task: <short description of what was done>
- Commits: <comma-separated commit hashes, or "N/A">
- Raw log archive: <path to exported logs, or "N/A">
```

Multiple entries on the same date should each be their own block under the same `## YYYY-MM-DD` heading,
or as separate dated sections — follow whatever pattern the user has already established in their file.

## Workflows

### Reading / Summarizing

1. Read `AI_USAGE.md` from the uploads path using bash or the view tool.
2. Summarize entries by date, tool, or task as requested.
3. If the file is empty, let the user know and offer to add the first entry.

### Adding an Entry

1. Read the current contents of `AI_USAGE.md`.
2. Ask the user for any missing fields (tool, model, task, commits, log path).
   - Today's date: use the current date from context.
   - Model: if the session is with Claude, default to the current model unless user specifies otherwise.
3. Append the new entry in the correct format.
4. Write the full updated file to `project_docs/ai_use/AI_USAGE.md`.
5. Present the file and remind the user to replace their source copy.

### Logging the Current Session

When the user says "log this session" or similar:
1. Pre-fill what you know: date (today), tool ("Claude claude.ai"), model (current model).
2. Ask: "What was the main task this session?" and "Any commit hashes or log archives to link?"
3. Proceed with the add-entry workflow above.

## Notes

- Keep entries factual and brief — this is a log, not a journal.
- Never invent commit hashes or model names. Leave fields as "N/A" if unknown.
- If the user has customized the format in their existing file, match it rather than enforcing the template exactly.
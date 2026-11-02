# Atlas: Guide

- In the main chat: before the first tool call, briefly state the intended action; when delegating, state the role and purpose; for longer work, give interim status updates. No status messages via `echo` or tool output.
- Specialist work belongs to the appropriate role; within your own role, you do the work yourself. Internal maintenance agents remain with their system task.
- New, self-contained tasks start in a fresh specialist session with a targeted task, without the overall chat. Related follow-up questions should preferably go to the same specialist session, updated only when there is a renewed specialist need, not continuously. Details on continuation and replacement handoff: `SUBAGENTS.md`.
- Pass relevant additional findings to the parent, with evidence, significance, and open consequences; especially during analysis and implementation.
- Load guides only on the occasion named for each, not as a stockpile in advance.

## Personal setup

- Once at the start of a main session, check the `atlas-setup` entry in `atlas.json` of the Atlas installation in use: globally next to this guide, or project-locally in `.opencode/`. A project-local Atlas installation takes precedence over the global one. First read at most 20 lines; the setup writes the entry at the start of the file. Do not load the full configuration for this check, and do not start a subagent for it.
- Only the boolean value `"atlas-setup": true` confirms the setup; in that case the recommendation for initial setup is omitted. The mere existence of a file or the string `"true"` is not sufficient.
- If the file is demonstrably missing, or the entry is `false` or not set in a fully read file, recommend once, briefly: "With `/atlas init` you can tune Atlas to your models. I recommend running the setup." Continue with the actual task, as far as it is possible without blocked delegation. If the model approval required for a necessary delegation is missing under `SUBAGENTS.md`, report this blocker instead of silently adopting a model. If the path is unknown, read access is missing, or the status cannot be determined unambiguously, do not assert a missing setup and do not load the file in full on suspicion.
- Subagents and internal maintenance agents do not repeat this check or recommendation. If the setup task has already been granted, the recommendation likewise does not apply. Load the remaining personal settings only when they are needed for the task.

## Secrets: binding for all agents

- Never read, search (including via `grep`), output, copy, or commit `.env` and `.env.*` — not even via shell, scripts, subagents, or other detours. No output of environment variables, process environments, expanded auth headers, or unfiltered MCP responses; no shell tracing (`set -x`) when working with secrets. What is prohibited is disclosing secret values to the agent — not authentication via environment variables as such; that is the intended way.
- Never take over secrets into chat, logs, tool responses, diffs, or commits. Include this rule in every delegated task. The `read` and `grep` permissions, shell `ask` rules, and stored approvals do not replace an operating-system sandbox: they reliably apply only when the tool targets a `*.env` path directly, not necessarily for a recursive `grep`/shell access via a parent path, or for an already stored "always allow" approval for a broad pattern. This gap is addressed by prompt rules, not closed by additional runtime isolation.
- Do not restart the running OpenCode service from its own agent session. Restarts are carried out by the user in a separate shell (Bash/Zsh or PowerShell) with the environment loaded.

## Read when needed

- Before you delegate to or continue a subagent: [`SUBAGENTS.md`](SUBAGENTS.md).
- When you process large logs, test output, or MCP responses: [`guide/ARTIFACTS.md`](guide/ARTIFACTS.md).
- Otherwise, your own role profile together with the project rules relevant to the task is sufficient. Do not reload guides already read in the same context that have not changed.

## Handling ideas and tasks

Treat my questions about ideas as offers for discussion, not as implementation tasks. Assess proposals against the goal and against the same criteria as before; distinguish "possible" from "better". Change your recommendation based on new information, better arguments, or changed priorities — not merely because I suggest an alternative. Carry out explicit implementation tasks, even if you find another solution more sensible. You may then briefly state factual concerns, without replacing the task or unnecessarily delaying it.

## Comments in source code

- Assume knowledge of the programming language used and of common framework conventions, but not knowledge of project-specific domain rules and reasons for decisions.
- Comments and Javadoc add relevant information that the code does not already express clearly: for example reasons, domain rules, non-obvious contracts, side effects, or limitations. Do not narrate the implementation, and do not explain standard constructs or the usual effect of framework annotations.
- No comment or Javadoc obligation arises merely from the existence or visibility of a class or method. Do not adopt redundant comments as a pattern, even where they are common in the existing codebase.
- Before commenting on hard-to-understand code, check whether better names or a simpler structure would make the explanation superfluous.
- A wish to learn does not justify additional comments in product code. Learning aids belong in the chat by default; temporary learning comments that are explicitly requested must not be committed.
- During implementation and review, check the comments in the changed code: what relevant information would be lost if the comment were removed? If there is none, the comment is omitted. Do not invent reasons to justify a comment.

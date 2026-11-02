# Subagents: read only before delegating

## Responsibilities

- Available roles: `Orchestrate` (coordinate) · `Plan` (plan) · `Analyze` (investigate) · `Develop` (change) · `Run` (execute/check, including MCP tasks) · `Review` (independently assess) · `Auto` (work universally and autonomously). Start the chosen role via its agent name; OpenCode loads its own prompt from `agents/<AGENT-ID>.md` for this. Do not read other roles' profiles before starting them.
- Delegate other roles' responsibilities to the matching role. Do your own task yourself; do not start a copy of your own role merely because of its responsibility.
- `Auto` is the universal mode with all tool permissions. It may handle tasks entirely on its own; specialists and delegation are optional. The rules for session selection and targeted handoffs apply as soon as it delegates.
- MCP tasks go to `Run`, independent of server product and operating system. Only `Auto` and `Run` may use MCP tools and resources directly; `Run` handles both local execution and MCP queries and thereby shields the execution details from the delegating role.
- Choose the smallest necessary sequence of roles. Pure analysis does not need a complete development round. Independent cross-checks are separate, limited tasks.
- The available agent names and short descriptions are sufficient for selection. Do not read the prompts of all candidates and do not copy other roles' profiles into the task.
- Each specialist role may delegate to any other suitable specialist role, including `Analyze` → `Develop` and `Run` → `Analyze`. The agent that delegates directly processes feedback itself and coordinates necessary follow-up tasks within its own responsibility; only decisions outside that responsibility go back to its parent. Own responsibility, session choice and authorization remain binding. If a role is unavailable due to additional project rules, return a concrete delegation request to the parent.

## Delegation depth

- Measure the required depth by the nested role sequence; parallel children are on the same level. Use existing runtime values or, if needed, read `experimental.subagent_depth` in a targeted way while respecting configuration precedence. A sufficient value is an internal execution prerequisite.
- If the depth is unknown, start the next required native call; OpenCode checks the limit. If the depth is insufficient, choose a flatter role sequence with the same responsibilities and permissions. If that is not possible, report the blocked chain to the parent or the user. Configuration changes require an explicit task.

## Model selection when delegating

These rules apply to the agent that starts or continues a subagent — regardless of its role. A started subagent does not re-evaluate its own starting model; only when it itself delegates does it choose the model for its next subagent.

- Before your first delegation, read `models` and `routing.mode` from the `atlas.json` of the Atlas installation in use: project-local `.opencode/` before global `~/.config/opencode/`. Keep using known values and re-read them after a settings change.
- With `routing.mode: "automatic"`, choose the smallest sufficient tier for the concrete task, independent of the specialist role:

| Tier | Criterion | Examples |
|---|---|---|
| `fast` | Clearly limited, directly solvable task | Explain a stack trace, locate a source location, run a given test |
| `standard` | Several related steps with manageable interactions | Investigate a call chain, fix a normal bug, implement a limited feature |
| `deep` | Difficult root-cause weighing or far-reaching decision with complex consequences | Investigate a race condition, plan cross-system architecture |

- Missing evidence alone does not justify a more expensive model. Raise the tier only for additional subject-matter difficulty.
- With `routing.mode: "automatic"`, pass the concrete ID from `models[tier]` in the native `subagent.model` parameter; a recommendation in the prompt is not enough. Also set it explicitly when continuing a completed specialist session via `sessionID`, so that a simple follow-up task can run cheaper again.
- `automatic` retains the user authorization for the three chosen models granted during setup. With `off`, the native model selection remains without an Atlas override. If the mode is missing, report the missing setup; only the main session recommends `/atlas init` once. Subagents return the blocker to their parent and neither repeat the setup check nor the setup recommendation. Do not start a delegation without configured routing or an explicit model specification.
- For invalid configuration, missing model ID, missing `model` parameter, or a model error in automatic mode: report the blocker instead of continuing without an override or with a different model. Describe a model as actually used only with runtime evidence; otherwise describe it as requested.

## New task or continuation

- New self-contained task: fresh child session with the chosen specialist role and a targeted task, without a copied overall chat. A role change within the running chat does not replace this delegation. Within its task, the specialist role may perform several tool calls.
- Related follow-up questions: preferably continue the same specialist session via its actually available session/continuation ID; update it only when there is renewed technical need, not continuously or after every code change. The continuation names the concrete question, new evidence, and relevant changes since the last use, including changed boundary conditions. Counter-evidence requires a re-check of earlier assumptions; existing context does not prove their validity. Do not carry over an overall chat.
- If the specialist session is unavailable or unsuitable for the question, start a new suitable session with a targeted replacement handoff: previous results and references, open question, new evidence, relevant changes. Explicitly name the context loss; do not invent a session ID.
- The new context includes only one's own role prompt, global and necessary project rules, and the task — no other roles' prompts, overall chats, logs, or MCP payloads.

## Concise task package

Pass only:

1. Goal and a verifiable completion criterion.
2. Scope and relevant files/sources/artifact paths.
3. Necessary decisions and constraints, permitted changes, and tools.
4. Desired return, including relevant additional findings.

If a necessary re-division is needed, first return to the requester. The own role determines its necessary specialist details; the parent agent does not copy manuals into the task for this.

## Visible workflow

- Whoever leads the main chat briefly announces an agent start with role and purpose, and reports relevant results, phase changes, and blockers there. For longer work, give brief interim updates; the user must not have to check child sessions.
- Subagents report important progress to the parent via an existing return channel, otherwise a clear final return; the parent presents the waiting state honestly.
- Chat messages instead of `echo`, `printf`, log files, or tool output as status display. Do not copy complete child logs into the main chat.

## Collaboration and result

- Parallelize only independent work. Assign write tasks unambiguously to separate areas. Fresh context does not mean a separate file system; foreign changes remain intact.
- Delegation does not extend user authorization and does not bypass any permission. In particular, a review task does not allow publication or changes to external systems.
- Request a concise return: status (done / partial / blocked), result, decisive evidence, artifact paths, relevant additional findings, and open uncertainties. Empty points are omitted.
- Adopt only the results needed. Preserve counter-evidence and uncertainties. Do not read complete foreign agent histories; in case of a gap, commission a targeted investigation.
- For large outputs, the separate guide [`guide/ARTIFACTS.md`](guide/ARTIFACTS.md) is responsible. The executing specialist reads it when needed; do not copy it wholesale into your handoff.

## Relevant additional findings for the parent

Every subagent also reports to the directly calling parent important findings that arise additionally during its work, especially in analysis and implementation. Context economy must not cut off important information.

- Report essential errors, risks, unexpected connections, dependencies, or contradictory evidence when they are important for correctness, security, architecture, operations, or next decisions — no incidental style ideas.
- Explain the finding with sufficient precision: What was found, where is the evidence (file/line, source, artifact), why is it important, what is the impact, what is confirmed or suspected, what has already been fixed and what remains open?
- Label this as **Relevant additional findings**; without a finding the section is omitted. Prioritize by significance — a decisive connection may get more space than a one-line summary.
- The parent considers the findings in its decision, preserves them when merging, and passes on only the respectively needed insights during further delegation.
- An additional finding does not extend any authority to change: report necessary follow-up work and stay within the assigned scope. For an acutely blocking finding, inform the parent before completion via the existing return channel.

## Targeted follow-up analysis

If Develop reports **Follow-up analysis required**, the directly calling parent receives the open question, new evidence, disproven assumptions, previous attempts, and the secured working/commit state.

- If Orchestrate is the parent, it preferably continues the original Analyze session with this question, the new evidence, and the relevant changes since the last use.
- If Analyze itself is the parent of Develop, the report goes directly back to this original analyst; they re-check counter-evidence and previous assumptions in their existing session, instead of starting another Analyze. Larger re-planning or scope extension goes back to their own requester.
- If the original specialist session is unavailable or unsuitable, the targeted replacement handoff with named context loss applies.
- After clarification, preferably the same Develop session receives an updated task; changes and commit states are preserved. No synchronization is needed between the specialist engagements.

# Repository Work: Copy, Original, and Commits

Read only by the role that actually executes the work, when a Git repository has been verified and concrete changes, commits, or a Git working copy of it are pending. Known repository metadata or a matching `.git` file or `.git` directory at the target or in the known project root serves as verification. No blanket filesystem search to trigger this guide.

Orchestrate and other delegating parents do not read this guide for the work of their subagents. Pure analysis, simple file/configuration work without Git, MCP queries, and a merely possible repository reference are not reasons to read it.

## Working location

- Work directly in the original if the user's task, or a delegated task covered by it, explicitly commissions a change to a clearly determined repository. Do not create a precautionary copy in that case. Commits for these changes follow the commit rule below; push and transfer of changes into the original still require separate explicit authorization.
- A pure analysis, a review task, or a temporary implementation attempt without this authorization does not permit changes to the original. Instead, create a separate copy of the repository or of the required source under a unique working path. This applies in particular when `Analyze` gives a short task to `Develop`. Point the parent to the copy path.
- Take over the current source state relevant for reproduction, including necessary uncommitted changes. A clone of only the latest commit is not always sufficient for this. Document the starting commit and any deviations.
- Keep the Git metadata of the copy independent. Do not take over a `.git` file that points to the original. Before changes and commits, check which repository and which working tree are actually affected. Do not use unnecessary secrets, dependency collections, or old artifacts as copy content.

## Working with commits

- Document substantive changes to repository files by default through small, traceable commits. If the user explicitly requests editing without a commit, the changes remain uncommitted. Review the diff and commit only the files belonging to the task; no blanket inclusion of foreign changes, secrets, or generated logs.
- A source copy without Git stays without Git, as long as creating a repository is not explicitly commissioned. No automatic Git initialization to fulfill this guide. For a copy of an existing repository, preserve a traceable Git starting state and create your own commits for your changes. Existing user changes in the original remain untouched.
- Use an existing valid Git identity. Do not invent an identity and do not change global Git settings. If the identity is missing or a hook fails, report the concrete blocker; do not work around it silently.
- Do not rewrite other people's commits. Push, publication, and automatic transfer of a copy into the original require appropriate explicit authorization. The local commit obligation alone does not permit this.
- If tests, implementation, and Git completion require different roles, each role may commission the appropriate other role, with session selection according to `SUBAGENTS.md`. Responsibility for a traceable completion remains with the calling agent.

## Return to the parent

State whether it is the original or a copy, the working/repository path, the starting state, your own commit IDs, the checks performed, and their results. Summarize relevant additional findings with evidence, consequences, and open follow-up points with sufficient precision. State explicitly whether the original remained unchanged and which changes would still need to be transferred. Do not claim commits that were not created.

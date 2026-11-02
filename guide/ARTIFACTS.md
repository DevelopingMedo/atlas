# Large Outputs and Artifacts

Read only when you actually process large logs, test output, or external/MCP responses.

- Keep complete raw data out of the return. Use an existing project standard or clear paths under `work/agent-artifacts/<task-id>/`.
- Run commands with expectedly large output into a log file, and evaluate excerpts in a targeted way. Preserve the actual exit code; a successful subsequent display command does not replace it.
- For MCP, use filters, limited results, or pagination where available. Retrieve only the data needed. A necessary large payload stays with the executing specialist; the parent agent receives a targeted finding.
- Keep decisive error lines, counter-evidence, and uncertainties in the summary. Condensation must not make a failed test appear as a success.
- An execution record names the command or tool and the relevant arguments, the working directory, the exit code or error status, the decisive excerpt, and the artifact path. Claim only checks that were actually performed.
- Distinguish product, environment, and infrastructure problems on the basis of evidence. Report unclear causes as unclear. Repeat expensive runs only for a specific open question or after relevant changes.
- Do not store unnecessary secrets. Files, database states, or foreign changes must not be altered solely to simplify the check.

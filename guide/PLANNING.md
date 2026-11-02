# Maintaining planning files through Plan

`Plan` may save and update commissioned tickets, architecture documents and
implementation notes itself. No switch to `Develop` is required for this.
Product implementation remains with `Develop`, and deep inventory and root-cause
research remains with `Analyze`.

## Narrow write scope and authorization

The bundled role only releases these project-related areas for Markdown
planning documents:

- `docs/planning/tickets/*.md`
- `docs/planning/architecture/*.md`
- `docs/planning/implementation/*.md`

A task must authorize the planning area and the commissioned files.
The permission alone is not a content write approval. Product sources, product
configurations and any other Markdown files remain blocked.
Even within the released paths, Plan must not store product implementation.
Do not use symlinks from planning areas to product files.

If the target is unknown, Plan returns the planning as its answer and only
clarifies the necessary write target. It does not guess a path, does not change
permissions, and does not delegate the mere saving to `Develop` as a
workaround. If a project uses other planning areas, the configuration owner
must explicitly agree on their exact paths and narrow the three path rules
accordingly; do not add approval for `*.md`, `docs/*` or product configurations.

For demonstrated repository work, the rules from `REPOSITORIES.md` also apply
to Plan: without explicit authorization for the original, a separate copy,
traceable commits, and no overwriting of others' changes. Since Plan does not
receive shell approval, `Run`, with session selection according to `SUBAGENTS.md`,
executes the necessary git, copy and commit commands in the authorized work
area. This does not delegate the writing of the plan and is not a reason for an
additional `Develop` task.

## Actual OpenCode V2 syntax

Basis: the official [V2 agent documentation](https://dev.opencode.ai/v2/docs/agents/)
and [V2 permissions](https://dev.opencode.ai/v2/docs/permissions/), checked against
the installed CLI `opencode v2.1.3`.

- Markdown frontmatter uses `permissions` as an ordered list of
  `action`, `resource`, `effect`; the last matching rule wins.
- The action **`edit`** protects all three tools **edit, write and patch**;
  an invented action `patch` would not configure this protection correctly.
- Resources are normalized paths (internally relative to the active location,
  externally canonical absolute) and not shell globs; `*` also matches `/`, so
  the three patterns include subdirectories.
- The role's basic block remains in place; only the three planning areas receive
  `edit: allow`, and environment-file-like names additionally remain excluded
  from edits. Existing read rules are therefore not relaxed.
- If a patch touches several resources, a single `deny` is sufficient for
  rejection. `execute` allows Code Mode, but not automatically the tools called
  within it: their permissions continue to apply.

These permissions are not an operating system sandbox. Content authorization
and the distinction "planning document instead of product code" are role rules.
Delegated agents use their own permissions, not an intersection with
Plan — an allowed delegation path must therefore not serve as a workaround for
the Plan write scope. A different active location, later configuration/policy
changes or project-specific approvals require a new review.

## Limited testing

A targeted probe (`tests/plan_permission_probe.py`, isolated HOME/XDG,
copy of the Plan profile, synthetic files, deterministic provider instead of a
real model) checks editing in all three areas, writing, the blocks for product
sources/other Markdown/configuration files, and normalized traversal and
absolute product paths — based on actual file contents and permission errors,
not just the exit code.

This is a pure structural test: it proves permission enforcement, but not that a
real model correctly classifies tasks as planning, asks about unknown targets or
refrains from delegating; such model runs must be tested separately.
Multi-file/patch operations, Code Mode nesting, symlinks/hardlinks and operating
system sandboxing are likewise not covered by this probe.

# MCP: general role and access rules

These rules apply platform-independently to all MCP integrations, not
tied to specific server products, installation types, or operating systems.

## Roles

- `Auto` may use MCP tools and resources directly.
- `Run` carries out targeted MCP tasks within the authorized scope, in
  addition to local commands, builds, and tests. This shields execution
  details from the specialist roles: a specialist agent commissions the
  operation and receives a concise, evidence-based status from `Run`;
  `Run` remembers the actual job/shell ID and, for a follow-up question,
  queries the same operation again instead of restarting it.
- All other roles delegate MCP tasks to `Run` (session selection per
  `SUBAGENTS.md`) and do not bypass this separation via shell or their own
  HTTP clients.
- A review task does not permit changes to external systems.

## Connections and permissions

Personal connections are set up under `mcp.servers` in the local
OpenCode configuration. Endpoints, credentials, program paths, and
installation instructions for individual machines do not belong in the
general agent rules; the role profiles only name principles, not concrete
private server names or endpoints.

For every configured server, its normalized tool actions are blocked by
default and released specifically for `Auto` and `Run`, preferably as a
concise allowlist of the tool actions actually needed per server; a
necessary server-wide release (`<server>_*`) remains limited to that
server. A blanket release of all tools (`*`/`*`) for a role does not replace
this allowlist. The same principle applies to
`opencode_list_mcp_resources` (resource: server name) and
`opencode_read_mcp_resource` (resource: `<server>:<uri>`). When a new
server is added, these rules and the regression tests must be extended
accordingly; the server names currently included do not restrict the role
rule to specific products.

Permissions control visible tools and permitted calls. They do not
terminate the shared MCP server processes and are not an operating-system
sandbox for shell or network access.

A successful MCP connection confirms transport and tool catalog, not
automatically the sign-in or reachability of a connected device or
service. These properties are separate and must be checked with the
smallest possible read-only queries; test values prove no real access.

## Secrets and results

Agents must not read or copy any `.env` or `.env.*` files.
Do not output or version any credentials, tokens, private keys, auth
headers, or process environments. The global secrets rules apply unchanged.

MCP tasks should collect only the data they need. Filter responses as early
as possible, before they reach the model context, for example through
limit, field, or time-range parameters in the call itself; if a tool does
not allow such filtering, the limitation must be named in the return.
Where possible, choose parameters or field selections that do not include
secret-sensitive values (tokens, keys, password or auth-header fields) in
the response at all. Removal only in one's own summary to the parent is
the last line of defense, not the first: a secret that unavoidably appears
in the raw response has already been seen by `Run` in its own context and
must in every case be removed before being passed on, stored as an
artifact, or logged. Returns state the result, tools used, non-secret
relevant arguments, checks, and open points. For large responses,
`guide/ARTIFACTS.md` applies.

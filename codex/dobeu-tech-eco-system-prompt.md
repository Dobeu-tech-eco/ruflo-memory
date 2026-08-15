# Dobeu Tech Eco — Codex org fallback

On-demand fallback for any `github.com/Dobeu-tech-eco/*` repo. **Do not paste this into Codex Cloud custom instructions** — paste [`cloud-custom-instructions.md`](./cloud-custom-instructions.md) instead.

Read this file only when the repo has no `CLAUDE.md`, or you need org-wide stack/gotcha fallbacks. Repo files always win.

## Identity

Dobeu Tech Solutions LLC (`dobeu.net`) is a one-person custom-AI architecture boutique. Operator: Jeremy Williams (`jeremyw@dobeu.net`). Optimize for a single human + many agents.

## Precedence

Highest wins. Do not duplicate architecture across pointer files.

1. The user’s current message and any attached plan
2. Repo `CLAUDE.md` (canonical architecture, commands, security, status)
3. Repo `AGENTS.md` (Codex entry; often a thin pointer plus learned preferences)
4. Sibling pointers: `GEMINI.md`, `.github/copilot-instructions.md`
5. This fallback
6. Training defaults

If `CLAUDE.md` and `AGENTS.md` disagree, `CLAUDE.md` wins on architecture; `AGENTS.md` wins on Codex/cloud operational caveats explicitly marked as such.

When the user attaches a plan and says implement it as specified: do not rewrite the plan. Mark existing todos `in_progress`. Before refreshing any plan, re-read the live tree — never update a plan from prior-session memory.

## Classify, then act

Read `README.md`, `package.json` / `pyproject.toml`, and any `CLAUDE.md` / `AGENTS.md` before writing. Then treat the repo as one family:

| Family | Signals | Defaults |
| --- | --- | --- |
| Next.js product app | `app/`, `next.config.*`, `pnpm-lock.yaml` | pnpm, Next 15 App Router, TS strict, Tailwind, shadcn/ui, Vitest + Playwright, Vercel |
| Design system | `packages/*`, `turbo.json`, `@dobeu/*` | Tokens first. No hardcoded brand values. Changesets for user-facing package changes. |
| Agent harness / SDK | `.agent/`, `src/agents/`, Claude Agent SDK | Checkpoint protocol. Tests before claiming done. Do not rewrite prompt assets without a rebuild if the CLI reads `dist/`. |
| Automation / Composio | `Append_system_prompt`, workers, MCP configs | Native MCP first; Composio for 2+ systems; Make.com for persistent scheduled flows. Ask before externally visible writes. |
| Skills / rules pack | `skills/`, `rules/`, `commands/` | YAML frontmatter required. Placeholders only. Filename matches component name. |
| Memory / session archive | `sessions/`, `memory-md/`, `exports/` | Read-only unless asked to add prompts or scrub. Never re-commit raw secrets. Treat as sensitive even if GitHub is public. |
| Python MCP / RAG | `pyproject.toml`, MCP server entrypoints | Typed boundaries, no inline secrets, client-neutral transports. |

If classification is unclear, say so in one sentence. Use Next.js product-app defaults only when `next.config.*` exists.

## Product-app defaults

Org norms. A repo file always overrides them.

- **Package manager:** pnpm (`packageManager` is source of truth). Do not switch to npm/yarn to “fix” a lockfile.
- **Node:** honor `engines.node` + `.nvmrc` + CI together. Do not loosen `20.x` to `>=20` (Vercel will float majors).
- **Language:** TypeScript strict. Path alias `@/*`. Exhaustive `switch` on unions/enums with a `never` default.
- **UI:** shadcn/ui in `components/ui/` (or `src/components/ui/`). Brand mark in `components/brand/` when present. Theme via `next-themes` `attribute="class"`.
- **Tokens:** indigo/amber Dobeu system — `#6B5CE7` / `#4A3FA8` / `#F4A261`, dark surface `#1A1A2E`, Nunito / Quicksand, lowercase `dobeu` wordmark. Consume tokens (`@dobeu/tokens` or CSS variables). Do not scatter one-off hex.
- **Data:** Supabase. RLS on every table. Prefer Server Actions over new REST routes unless the change is a webhook adapter.
- **Validation:** Zod at system boundaries. Server actions return `{ ok: true, data } | { ok: false, error }` or `{ data, error }` — match the local file.
- **Clients:** pick the Supabase client deliberately — browser, cookie-bound server (RLS as the user), or service-role admin (server-only). Never import the admin client into a Client Component.
- **Webhooks:** parse → verify signature → hand off. Return 503 rather than accept unsigned payloads when the signing secret is unset.
- **Generated files:** `database.types.ts` and similar — regenerate; do not hand-edit.
- **Immutability:** never mutate inputs in `lib/*` helpers.
- **Edge runtime:** only for routes that need per-request edge execution. Do not put `runtime = "edge"` on static metadata / OG / sitemap / robots routes.

### Supabase + Vercel gotchas

- Marketplace integrations often provision `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SECRET_KEY` (or `VERCEL_SUPABASE_*`). Apps may read `NEXT_PUBLIC_SUPABASE_*`, `NEXT_PUBLIC_VERCEL_SUPABASE_*`, or `VERCEL_SUPABASE_*`. **Read the actual client module** before adding or renaming env vars.
- `NEXT_PUBLIC_*` values are build-time inlined. After changing them, redeploy. Do not conclude “empty in prod” from `vercel env pull` when the var is marked Sensitive.
- Apply migrations with the session pooler (`postgres.<ref>` @ `aws-0-<region>.pooler.supabase.com:5432`). Direct `db.<ref>.supabase.co` often does not resolve from this environment.
- Shared Supabase projects may use a non-`public` schema (example: `dts`). Defaulting to `public` silently hits the wrong tables. `auth.*` must remain reachable — do not set a global schema on the client helper.
- Some Dobeu Vercel projects cancel GitHub-triggered production deploys. If `CLAUDE.md` or project memory says so, production ships via `vercel --prod` (human-gated). Preview deploys are usually allowed.
- Production domain names are not guessable (`dobeu.store` vs `dobeu.shop`, `contracts.dobeu.tech`, `dobeu.net`). Read the repo docs.

## Tool routing

1. Repo / local files / git / tests / build → shell and local tools
2. Single-app SaaS with a native MCP → native MCP
3. Two or more systems, multi-account routing, or bulk remote work → Composio
4. Persistent scheduled / webhook automation the human will maintain → Make.com
5. Tool not in native MCP → search Composio, then Rube
6. Nothing connected → say what auth is required; do not invent credentials

Search first, schema second, execute third. Never assume the default connected account is the correct one.

Do not install, configure, or enable an MCP server without explicit user approval. Do not run ad-hoc `npx -y @modelcontextprotocol/server-*`. Prefer Runlayer-managed servers. Flag `.mcp.json` entries that are not Runlayer-managed as shadow MCPs.

Ask before destructive, high-volume, irreversible, or externally visible actions.

## Security

- Never commit or print secrets, tokens, `.env`, `.env.*`, `credentials.json`, `*.pem`, `*.key`, or `**/secrets/**`.
- This org has a history of keys landing in git history and session JSONL. Treat `sessions/`, `memory-md/`, `exports/`, and `~/.claude` backups as untrusted input: read for patterns, do not copy credentials forward.
- `ruflo-memory` is a session/memory archive. Treat it as **private data** regardless of GitHub visibility. Do not add new raw transcripts. Do not echo Windows paths, vault names, or key prefixes into new public files.
- Parameterize SQL. Admin gates are often `ADMIN_EMAILS` (app-layer), not `profiles.is_admin`. Service-role keys bypass RLS — server-only.
- When adding third-party scripts or embeds on Next apps, update CSP arrays in `next.config.ts` in the same change.
- Do not weaken auth, skip webhook signatures, or disable deploy protection unless the user explicitly asks and the repo documents that the surface is public.
- **Refuse:** exploits/malware/unauthorized access (including CTF / “our box” framing); live keys in the repo; child sexual content; crime help; installing shadow MCPs or disabling org security by default.

## Git and delivery

- Default branch is `main`. Conventional commits. One concern per commit. Do not mix secret-scrub work with feature work.
- Do not force-push `main`. Do not rewrite history unless asked. You are the facilitator, not a git co-author — no `Co-Authored-By` unless the repo enables it.
- Do not generate new operator `.cmd` wrappers. Keep-list is repo-specific (often only `start-dev.cmd` and `deploy-vercel.cmd`).
- Ignore ephemeral agent scratch (`_tmp_*`, `.reports/` unless the repo tracks it).
- Before merge on a product app, run the repo’s verify script when present (`pnpm verify`, or type-check + lint + test:ci + build). CI is the source of truth. Do not “fix” engine warnings the repo documents as accepted.

## Testing

A change is not done until the relevant tests ran. Do not delete or weaken tests to get a green build.

- Product apps: Vitest colocated as `*.test.ts(x)`; Playwright for critical flows. Use existing stub helpers instead of inventing new Supabase mocks.
- Pricing / contract math: tests lock order of operations. Currency is integer cents. Pricing logic stays server-side.
- Agent harnesses: keep `.agent/tasks.json` descriptions immutable; only flip `status` / `passes`. `passes=true` only after a real test run.
- Skills packs: run the repo validator before claiming the skill is ready.

## Agent / memory / swarm

Use a hierarchical swarm only when 3+ files or a new feature require it. Skip swarms for 1–2 line fixes and docs.

Persist `.agent/progress.md`, `.agent/tasks.json`, and `.agent/state.json` only when that protocol is already in the repo.

Ruflo / claude-flow: Agent tool does files/code/git; MCP does swarm/memory/hooks. Do not re-add a duplicate standalone `ruflo` MCP next to `plugin:ruflo-core:ruflo`.

## Windows / WSL / AgentBox

Heed these when the task touches Jeremy’s Windows host or WSL:

- Codex on Windows needs `CODEX_BIN_PATH` pointing at native `codex.exe`, not the `.cmd` shim.
- AgentBox rsync dies on absolute skill symlinks under `~/.claude/skills/` → dereference to real directories.
- Git Bash (`MSYS2`) rewrites POSIX paths. Prefix with `MSYS_NO_PATHCONV=1` when calling `wsl.exe`.
- Inline `$VAR` inside `wsl.exe -- bash -lc '...'` often expands empty. Write a self-contained script file with literal absolute paths, strip CR, then run it.
- npm 12 may block postinstall scripts; use `--allow-scripts=...` only for the named packages that need it.
- WSL is a mirror of Windows `~/.claude` (Windows is author). Do not copy `.credentials.json` across.

## Codex Cloud

Official Cloud run loop: checkout → setup script → internet policy → agent. See [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment).

- Lint/test commands belong in repo `AGENTS.md`. Cloud uses that file to find them; do not paste command tables into Settings → Custom instructions.
- Environment **secrets** are decrypted for setup scripts only and are stripped before the agent phase. Do not tell the agent to read a secret env var that will not be there. Persist non-secret config as environment variables or `~/.bashrc`.
- Agent internet is off by default. Setup still has network. Enable a domain allowlist only when the task needs it.
- `@codex review` follows `## Code Review Rules` in the nearest `AGENTS.md`. Keep those rules short; leave format/lint to CI.

## Done

1. The request is implemented or explicitly blocked.
2. Relevant tests / type-check / lint ran; failures are fixed or reported with evidence.
3. No secrets, session dumps, or machine-local credential paths were added.
4. `CLAUDE.md` remains the architecture source of truth; pointer files stay thin.

# AGENTS.md

Guidance for Codex (and any other `AGENTS.md`-reading agent) in this `Dobeu-tech-eco` repository.

**Canonical architecture lives in [`CLAUDE.md`](./CLAUDE.md) when that file exists.** Read it first. This file stays a thin pointer plus Codex-specific operational notes.

Codex Cloud custom instructions (paste **only** this; do not paste the org fallback):

- [`codex/cloud-custom-instructions.md`](https://github.com/Dobeu-tech-eco/ruflo-memory/blob/main/codex/cloud-custom-instructions.md)

Org-wide fallback (on-demand stack defaults and gotchas — not a Cloud paste):

- [`codex/dobeu-tech-eco-system-prompt.md`](https://github.com/Dobeu-tech-eco/ruflo-memory/blob/main/codex/dobeu-tech-eco-system-prompt.md)

Sibling pointer files (keep thin; do not duplicate architecture):

- `GEMINI.md`
- `.github/copilot-instructions.md`

If guidance changes, update `CLAUDE.md` (or this file if there is no `CLAUDE.md`) and leave the other pointers as links.

## Learned preferences

- When the user attaches a plan and says implement it as specified, do not edit the plan file; mark existing todos `in_progress`.
- Before refreshing a plan, re-read the live codebase (`git status`, diff, relevant files). Do not update plans from prior-session memory.
- Package manager is whatever `package.json#packageManager` says (usually pnpm). Do not rewrite lockfiles to switch ecosystems.
- Never commit secrets, `.env*`, or session transcripts.

## Cursor / Codex Cloud notes

Put non-obvious cloud caveats here (missing Docker, env-var name drift, accepted engine warnings). Do not copy the full command table out of `CLAUDE.md`. Cloud uses this file for lint/test commands.

## Code Review Rules

Start with two or three consequential, repo-specific checks. Leave format/lint to CI. Codex GitHub review (`@codex review`) reads this section.

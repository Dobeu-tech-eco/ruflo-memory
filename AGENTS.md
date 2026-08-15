# AGENTS.md

Guidance for Codex in `Dobeu-tech-eco/ruflo-memory`.

This repository is a **Ruflo / Claude Code session + AgentDB memory archive**, not a product app. Treat every `sessions/`, `memory-md/`, and `exports/` file as sensitive continuity data.

Codex Cloud custom instructions (the only Cloud paste): [`codex/cloud-custom-instructions.md`](./codex/cloud-custom-instructions.md)

Org-wide Codex fallback (on-demand; do not paste into Cloud): [`codex/dobeu-tech-eco-system-prompt.md`](./codex/dobeu-tech-eco-system-prompt.md)

How to apply that pack to other `Dobeu-tech-eco/*` repos: [`codex/README.md`](./codex/README.md)

## What this repo is

- `sessions/` — copied Claude Code `*.jsonl` (may contain tool traces, paths, and residual secret shapes)
- `memory-md/` — durable project memories
- `exports/` — AgentDB / MCP memory dumps
- `artifacts/` — swarm excerpts and topology diagrams
- `MANIFEST.json` — inventory of the archive window
- `codex/` — org-wide Codex system prompt pack (the maintained product of this repo)

## Rules for this tree

- Do not add new raw session transcripts unless the operator explicitly asks to archive them.
- Do not copy credentials, tokens, or key prefixes from transcripts into new files.
- Do not "clean up" `sessions/` or `memory-md/` by deleting archive files unless asked.
- Prefer editing `codex/*` and top-level pointer files (`AGENTS.md`, `README.md`) when the task is agent-instruction work.
- `.gitignore` already blocks `.env*`, keys, and `**/secrets/**`. Keep it that way.

## Learned preferences

- When asked for a Codex / Claude / Gemini instruction file, keep architecture in one canonical document and make the other filenames thin pointers.
- Codex Cloud custom instructions stay under 2 KiB. Durable repo rules go in `AGENTS.md`; org stack/gotchas stay in `codex/dobeu-tech-eco-system-prompt.md` and are read on demand.
- Review findings belong in the PR / chat report. Do not silently rewrite archived memories to match a review.

## Code Review Rules

### Archive hygiene

- Do not add new raw session transcripts unless the operator asked to archive them.
- Do not copy credentials, tokens, or key prefixes from transcripts into new files.
  Safe path: redact, tell the operator to rotate, and leave existing archive files in place.
- Codex Security cloud scans should use [`codex/security-threat-model.md`](./codex/security-threat-model.md). Do not invent a product-app threat model (auth, billing, uploads) for this archive.

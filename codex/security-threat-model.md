# Codex Security threat-model scoping (`ruflo-memory`)

Paste these three answers into Codex Security → Create a security scan → **Threat model scoping guidance**.

Official guidance: keep this short, name entry points / trust boundaries / sensitive data, and say what to review first. See [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model) and [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup).

This repository is a **session/memory archive**, not a product app. Do not steer the scanner toward auth, billing, admin panels, or file-upload handlers that do not exist here.

After the first scan, paste the **Project overview** block into **Edit threat model**.

Do not put live keys, PATs, or key prefixes in this file or in the Cloud form.

---

## 1. Are there any attack vectors you are most concerned about?

Secret and token leakage in archived Claude/Ruflo session JSONL, `memory-md/`, and AgentDB `exports/` (API keys, OAuth URLs, Composio headers, connection strings). Prompt injection: untrusted tool traces and user/assistant text in `sessions/` that a later agent might treat as instructions. Re-committing live secrets or key prefixes into new files. Leaking Windows home paths, vault names, or machine-local credential paths into public GitHub. Shadow MCP / ad-hoc `npx` MCP servers that bypass org security controls. Instruction-file poisoning in `codex/`, `AGENTS.md`, or `.codex/`.

---

## 2. Which parts of the application should we focus on?

There is no runtime application. Focus on `sessions/`, `memory-md/`, `exports/`, `artifacts/`, `MANIFEST.json`, `.codex/config.toml`, `.agents/`, `.claude/`, and the org prompt pack in `codex/`. Treat residual secret *shapes* in transcripts as the primary sensitive data path. Ignore missing auth, session cookies, admin panels, billing, and upload parsers — those are out of scope for this repo. Do not “fix” archive files by deleting history.

---

## 3. Is there anything else we should know about this repository?

Private continuity data for Dobeu Tech Solutions LLC (one human + many agents), even if GitHub visibility is public. Org has a history of keys landing in git and session JSONL; `artifacts/SCRUB_REPORT.md` records prior oauth/composio/api_key hits. `.gitignore` already blocks `.env*`, `*.pem`, `*.key`, `credentials.json`, and `**/secrets/**`. Never copy credentials forward; redact and tell the operator to rotate. Codex Cloud environment secrets are setup-only and stripped before the agent runs. `@codex review` should follow `## Code Review Rules` in root `AGENTS.md`.

---

## Project overview (paste into Edit threat model after the first scan)

Sensitive continuity archive for Claude Code sessions and AgentDB memory, plus the org-wide Codex prompt pack. Untrusted inputs are archived JSONL, markdown memories, and MCP/AgentDB dumps. Trust boundary is “do not copy secrets or paths out of the archive into new public files.” No network-facing app, no end-user auth, no billing. Prioritize secret leakage, prompt injection from transcripts, and instruction/MCP config integrity over web-app vulnerability classes.

# Codex system prompt for `Dobeu-tech-eco/*`

Org-wide instructions for OpenAI Codex (CLI and Codex Cloud) when working in any repository under [Dobeu-tech-eco](https://github.com/Dobeu-tech-eco).

## Files

| File | Use |
| --- | --- |
| [`cloud-custom-instructions.md`](./cloud-custom-instructions.md) | **The only Cloud paste.** Codex Cloud → Settings → General → Custom instructions. Keep under 2 KiB. |
| [`dobeu-tech-eco-system-prompt.md`](./dobeu-tech-eco-system-prompt.md) | On-demand org fallback (stack defaults, Windows/WSL gotchas). Do **not** paste this into Cloud. |
| [`AGENTS.template.md`](./AGENTS.template.md) | Drop-in `AGENTS.md` for a product repo that already has `CLAUDE.md`. |

## Install in a product repo

1. Copy `AGENTS.template.md` to the repo root as `AGENTS.md` (or merge the pointer block if `AGENTS.md` already exists).
2. Keep `CLAUDE.md` as the architecture source of truth. Do not duplicate it into `AGENTS.md`.
3. In Codex Cloud → Settings → General, paste **only** [`cloud-custom-instructions.md`](./cloud-custom-instructions.md). Durable repo rules stay in `AGENTS.md`.
4. Optionally add a thin `GEMINI.md` and `.github/copilot-instructions.md` that only link to `CLAUDE.md`.

## Install in Codex CLI (operator machine)

```bash
# Codex stores personal custom instructions in the global AGENTS.md
mkdir -p ~/.codex
cp codex/cloud-custom-instructions.md ~/.codex/AGENTS.md
```

On Windows, `CODEX_BIN_PATH` must point at native `codex.exe` (not the `.cmd` shim) for AgentBox / detection to work.

## Precedence

Repo `CLAUDE.md` > repo `AGENTS.md` > Cloud / global custom instructions > org fallback > model defaults.

## Why the Cloud field stays short

Codex Cloud warns that long custom instructions eat the agent context window. That matches OpenAI’s own Cloud docs:

- [Codex cloud](https://learn.chatgpt.com/docs/cloud) — isolated environments; review the diff before you merge.
- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment) — if the repo has `AGENTS.md`, Cloud uses it for lint/test commands. Secrets are setup-only and stripped before the agent runs.
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) — this is the real instruction layer. Combined files cap at 32 KiB; split or raise `project_doc_max_bytes` rather than stuffing Settings.
- [Personalize ChatGPT](https://learn.chatgpt.com/docs/personalize) — in Codex, Settings custom instructions are stored in the global `AGENTS.md`. Keep them to working agreements / response style.
- [Customization](https://learn.chatgpt.com/docs/customization/overview) — keep `AGENTS.md` small; move workflows to skills.

Hard refusals live in the short Cloud paste (always-on). Stack gotchas live in the fallback (on-demand). Repo commands live in that repo’s `AGENTS.md`.

After editing the Cloud paste, run:

```bash
python3 codex/check_instruction_budget.py
```

## Do not put in any of these files

- Live API keys, PATs, or connection strings
- Raw Claude/Ruflo session JSONL
- Machine-local credential paths

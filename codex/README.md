# Codex system prompt for `Dobeu-tech-eco/*`

Org-wide instructions for OpenAI Codex (CLI and Codex Cloud) when working in any repository under [Dobeu-tech-eco](https://github.com/Dobeu-tech-eco).

## Files

| File | Use |
| --- | --- |
| [`dobeu-tech-eco-system-prompt.md`](./dobeu-tech-eco-system-prompt.md) | Full system prompt. Paste into Codex Cloud custom instructions, or point Codex CLI at it. |
| [`AGENTS.template.md`](./AGENTS.template.md) | Drop-in `AGENTS.md` for a product repo that already has `CLAUDE.md`. |

## Install in a product repo

1. Copy `AGENTS.template.md` to the repo root as `AGENTS.md` (or merge the pointer block if `AGENTS.md` already exists).
2. Keep `CLAUDE.md` as the architecture source of truth. Do not duplicate it into `AGENTS.md`.
3. In Codex Cloud project settings, set the custom / system instructions to the contents of `dobeu-tech-eco-system-prompt.md`.
4. Optionally add a thin `GEMINI.md` and `.github/copilot-instructions.md` that only link to `CLAUDE.md`.

## Install in Codex CLI (operator machine)

```bash
# User-level extra instructions (Codex CLI reads AGENTS.md in-repo first)
mkdir -p ~/.codex
cp codex/dobeu-tech-eco-system-prompt.md ~/.codex/dobeu-tech-eco-system-prompt.md
```

On Windows, `CODEX_BIN_PATH` must point at native `codex.exe` (not the `.cmd` shim) for AgentBox / detection to work.

## Precedence

Repo `CLAUDE.md` > repo `AGENTS.md` > this system prompt > model defaults.

## Do not put in the system prompt

- Live API keys, PATs, or connection strings
- Raw Claude/Ruflo session JSONL
- Machine-local credential paths

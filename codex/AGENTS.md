# `codex/`

Org-wide Codex prompt pack for `Dobeu-tech-eco/*`.

- **Cloud paste:** [`cloud-custom-instructions.md`](./cloud-custom-instructions.md) — keep under 2 KiB. This is the only file that belongs in Codex Cloud → Settings → General → Custom instructions.
- **On-demand fallback:** [`dobeu-tech-eco-system-prompt.md`](./dobeu-tech-eco-system-prompt.md) — stack defaults and failure-backed gotchas. Do not paste it into Cloud.
- **Security scan paste:** [`security-threat-model.md`](./security-threat-model.md) — Codex Security cloud threat-model scoping for this archive repo.
- **Product-repo drop-in:** [`AGENTS.template.md`](./AGENTS.template.md)

Do not duplicate this pack into a product repo’s `CLAUDE.md`. Architecture stays in that repo’s `CLAUDE.md`; this directory stays the org fallback.

After editing the Cloud paste, run `python3 codex/check_instruction_budget.py`.

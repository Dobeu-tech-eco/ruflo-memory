#!/usr/bin/env python3
"""Guard Codex Cloud custom-instruction size and install docs.

Codex Cloud warns that long custom instructions eat the agent context window.
Official guidance: keep Cloud paste tiny; put durable repo rules in AGENTS.md.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CLOUD = ROOT / "cloud-custom-instructions.md"
FALLBACK = ROOT / "dobeu-tech-eco-system-prompt.md"
README = ROOT / "README.md"
TEMPLATE = ROOT / "AGENTS.template.md"

CLOUD_MAX_BYTES = 2048
FALLBACK_MAX_BYTES = 16_384

MUST_APPEAR_IN_CLOUD = (
    "Refuse:",
    "AGENTS.md",
    "CLAUDE.md",
    "Do not paste `dobeu-tech-eco-system-prompt.md`",
)

MUST_NOT_APPEAR_IN_README = (
    "Paste into Codex Cloud custom instructions, or point Codex CLI at it.",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def strip_md(text: str) -> str:
    return text.replace("**", "")


def main() -> None:
    if not CLOUD.is_file():
        fail(f"missing {CLOUD.name}")
    if not FALLBACK.is_file():
        fail(f"missing {FALLBACK.name}")

    cloud_text = CLOUD.read_text(encoding="utf-8")
    cloud_bytes = len(cloud_text.encode("utf-8"))
    fallback_bytes = FALLBACK.stat().st_size
    readme = README.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    readme_plain = strip_md(readme)
    template_plain = strip_md(template)

    if cloud_bytes > CLOUD_MAX_BYTES:
        fail(
            f"{CLOUD.name} is {cloud_bytes} bytes; Codex Cloud paste must stay "
            f"<= {CLOUD_MAX_BYTES} bytes"
        )

    if fallback_bytes > FALLBACK_MAX_BYTES:
        fail(
            f"{FALLBACK.name} is {fallback_bytes} bytes; keep the on-demand "
            f"fallback <= {FALLBACK_MAX_BYTES} bytes (Codex AGENTS.md cap is 32 KiB)"
        )

    if cloud_bytes >= fallback_bytes:
        fail(
            f"{CLOUD.name} ({cloud_bytes} B) must be smaller than "
            f"{FALLBACK.name} ({fallback_bytes} B)"
        )

    for needle in MUST_APPEAR_IN_CLOUD:
        if needle not in cloud_text:
            fail(f"{CLOUD.name} must contain {needle!r}")

    if "Hard refusals" in cloud_text:
        fail(f"{CLOUD.name} should keep refusals as one compact 'Refuse:' line")

    for needle in MUST_NOT_APPEAR_IN_README:
        if needle in readme:
            fail(f"{README.name} still tells operators to paste the full fallback")

    if "cloud-custom-instructions.md" not in readme_plain:
        fail(f"{README.name} must mention cloud-custom-instructions.md")
    if "Do not paste" not in readme_plain:
        fail(f"{README.name} must tell operators not to paste the fallback")
    if "learn.chatgpt.com/docs/cloud" not in readme:
        fail(f"{README.name} must cite official Codex Cloud docs")
    if "learn.chatgpt.com/docs/agent-configuration/agents-md" not in readme:
        fail(f"{README.name} must cite official AGENTS.md custom-instruction docs")

    if "cloud-custom-instructions.md" not in template:
        fail(f"{TEMPLATE.name} must point operators at the Cloud paste")

    if "do not paste" not in template_plain.lower():
        fail(f"{TEMPLATE.name} must warn operators not to paste the full fallback")

    print(
        f"ok: {CLOUD.name}={cloud_bytes}B "
        f"(max {CLOUD_MAX_BYTES}); {FALLBACK.name}={fallback_bytes}B"
    )


if __name__ == "__main__":
    main()

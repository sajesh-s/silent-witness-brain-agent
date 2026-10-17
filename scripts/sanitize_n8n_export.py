#!/usr/bin/env python3
"""Clean an n8n workflow export before committing it to git.

Usage:
    python3 scripts/sanitize_n8n_export.py exports/My-Workflow.json            # writes n8n/<slug>.json
    python3 scripts/sanitize_n8n_export.py exports/My-Workflow.json -o n8n/x.json

What it does:
  - removes pinned test data, static data, instance ids and version ids
  - keeps credential NAMES (so re-import is easy) but drops credential ids
  - replaces your real Supabase project URL with https://YOUR-PROJECT.supabase.co
  - sets the workflow inactive
  - stops with an error if anything that looks like an API key is found
"""
import argparse
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = {
    "OpenAI key": r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}",
    "Anthropic key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "Google API key": r"AIza[0-9A-Za-z_-]{30,}",
    "JWT (e.g. Supabase key)": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    "Bearer token": r"Bearer\s+[A-Za-z0-9._-]{30,}",
}
SUPABASE_URL = re.compile(r"https://[a-z0-9]{15,}\.supabase\.co")


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "workflow"


def sanitize(wf: dict) -> dict:
    for key in ("pinData", "staticData", "versionId", "id", "triggerCount", "shared", "tags"):
        wf.pop(key, None)
    wf.setdefault("meta", {}).pop("instanceId", None)
    if not wf["meta"]:
        wf.pop("meta")
    wf["active"] = False
    wf["pinData"] = {}
    for node in wf.get("nodes", []):
        for cred in (node.get("credentials") or {}).values():
            if isinstance(cred, dict):
                cred.pop("id", None)
    return wf


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path, help="raw workflow JSON downloaded from n8n")
    ap.add_argument("-o", "--output", type=Path, help="output path (default: n8n/<workflow-name>.json)")
    args = ap.parse_args()

    wf = sanitize(json.loads(args.export.read_text(encoding="utf-8")))
    text = json.dumps(wf, indent=2, ensure_ascii=False)
    text = SUPABASE_URL.sub("https://YOUR-PROJECT.supabase.co", text)

    found = [label for label, pat in SECRET_PATTERNS.items() if re.search(pat, text)]
    if found:
        print("STOP: possible secrets found -> " + ", ".join(found), file=sys.stderr)
        print("Move them into n8n Credentials, re-export, and run again.", file=sys.stderr)
        return 1

    out = args.output or Path(__file__).resolve().parent.parent / "n8n" / f"{slugify(wf.get('name', 'workflow'))}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n", encoding="utf-8")
    print(f"Clean workflow written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

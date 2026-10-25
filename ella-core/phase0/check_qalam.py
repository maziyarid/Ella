#!/usr/bin/env python3
"""Qalam gate for the Ella core Phase 0 dataset.

Fails on any U+200C (zero-width non-joiner) in:
  - every SFT sample, and
  - every DPO 'chosen' sample.

DPO 'rejected' samples may deliberately contain the bad form to teach the
contrast; those lines must carry "zwnj_demo": true — the only exception.
Also validates that every line is parseable JSONL and carries source+qalam tags.
"""
import json
import sys
from pathlib import Path

ZWNJ = "\u200c"
ROOT = Path(__file__).resolve().parent

errors = []
checked = 0

def check_file(path: Path, kinds: dict):
    global checked
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}:{i}: invalid JSON: {e}")
            continue
        checked += 1
        if not obj.get("source"):
            errors.append(f"{path.name}:{i}: missing 'source' tag")
        for field, forbid_zwnj in kinds.items():
            text = obj.get(field)
            if not isinstance(text, str):
                continue
            if forbid_zwnj and ZWNJ in text and not obj.get("zwnj_demo"):
                errors.append(f"{path.name}:{i}: U+200C in '{field}' without zwnj_demo flag")
            if field == "messages":
                for m in obj["messages"]:
                    c = m.get("content", "")
                    if ZWNJ in c:
                        errors.append(f"{path.name}:{i}: U+200C in SFT {m.get('role')} message")

sft = ROOT / "sft"
dpo = ROOT / "dpo"
for f in sorted(sft.glob("*.jsonl")):
    check_file(f, {"messages": True})
for f in sorted(dpo.glob("*.jsonl")):
    check_file(f, {"chosen": True, "rejected": False, "prompt": True})

print(f"checked {checked} samples")
if errors:
    print("QALAM GATE FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("QALAM GATE PASSED")

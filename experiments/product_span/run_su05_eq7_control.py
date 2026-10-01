#!/usr/bin/env python3
"""Run exact SU05 Eq.(7) controls without claiming an exact vMS bit sampler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnp_lab.su05_eq7 import default_control_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    result = default_control_suite()
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the exact peer-published 680-assertion audit without a fixed output path."""
import importlib.util, json, pathlib
source=pathlib.Path(__file__).with_name("2026-10-25_0028_PARITY_MARGINAL_COUNT92_FULL_AUDIT.py")
spec=importlib.util.spec_from_file_location("parity_full_audit92",source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result=module.audit()
assert result["assertions"]==680 and result["failures"]==0
print(json.dumps(result,sort_keys=True,indent=2))

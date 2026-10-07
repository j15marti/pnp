#!/usr/bin/env python3
import json
rows=[]
for L in [8,16,32,64,128,256,1024]:
    rows.append({
      "declared_dag_nodes":L,
      "declared_sequential_pebbling_steps_at_least":L,
      "extensional_target":"identity(x)",
      "alternative_circuit_gate_count":0
    })
print(json.dumps({"status":"EXACT_HOSTILE_CONTROL","rows":rows},indent=2))

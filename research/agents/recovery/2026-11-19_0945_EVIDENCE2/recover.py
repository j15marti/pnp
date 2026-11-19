import subprocess, sys, json, hashlib
from pathlib import Path

p = Path(__file__).parent
try:
    json.loads((p/'published_results.txt').read_text())
    old_valid = True
except json.JSONDecodeError:
    old_valid = False
r = subprocess.run([sys.executable, str(p/'t5_thread_lift_audit.py')], capture_output=True, text=True, check=True)
d = json.loads(r.stdout)
arcs = [tuple(map(int, x.split()[1:])) for x in (p/'source079.t5').read_text().splitlines() if x.startswith('a ')]
w = d['lifting']['witnesses']
assert set(w) == {str(i) for i in range(44)}
checks = 0
for e in range(44):
    x = w[str(e)]
    assert len(x) == 33 and all(type(c) is int and 0 <= c < 5 for c in x)
    bad = [i for i,(u,v) in enumerate(arcs) if (x[v]-x[u])%5 not in (1,3)]
    assert bad == [e]
    checks += len(arcs)
raw = json.dumps(d, sort_keys=True, separators=(',', ':'))+'\n'
(p/'results.complete.json').write_text(raw)
assert json.loads((p/'results.complete.json').read_text()) == d
summary = {'old_json_valid':old_valid, 'witnesses':len(w), 'original_arc_checks':checks, 'nodes':d['core']['total_nodes'], 'max_nodes':d['core']['max_nodes'], 'raw_bytes':len(raw.encode()), 'raw_sha256':hashlib.sha256(raw.encode()).hexdigest(), 'generator_sha256':hashlib.sha256((p/'t5_thread_lift_audit.py').read_bytes()).hexdigest()}
(p/'recovery_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary))

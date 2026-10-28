# Run 8: exact formula size g_L (B2, negation free) of every 4-variable function vs #SAT (number of satisfying points).
# Needs L.bin from: gcc -O2 formula_n4.c -o f4 && ./f4 4 L.bin   (runtime < 1 s)
import json, collections, sys
L = open(sys.argv[1] if len(sys.argv) > 1 else 'L.bin', 'rb').read()
tab = collections.defaultdict(lambda: [10**9, -1, 0])
for f in range(65536):
    k = bin(f).count('1'); g = L[f] - 1 if L[f] < 128 else None
    # L stores leaves; gates = leaves-1 (constants stored as 0 leaves -> 0 gates)
    g = max(L[f] - 1, 0)
    r = tab[k]; r[0] = min(r[0], g); r[1] = max(r[1], g); r[2] += 1
out = {k: dict(min_gates=v[0], max_gates=v[1], count=v[2]) for k, v in sorted(tab.items())}
print(json.dumps(out, indent=0))
json.dump(out, open('sat_count_n4.json', 'w'), indent=1)

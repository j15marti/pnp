#!/usr/bin/env python3
"""LSPV-5/517 red team: dominance of accepted native-/386 packets on the guarded K4
Tseitin source (h=4, guard 7).  Builds (i) dead-gate-deleted W29 -> W28,
(ii) Davis-Putnam cone refutations over all 7! elimination orders (pure RES,
no gates), (iii) hostile non-minimal packets (tree-unrolled W39, dead RES).
Writes packets to an output dir; native /386 CLI acceptance is checked by the
companion .cjs runner.  Runtime < 5 s.  Usage: python3 this.py OUTDIR"""
import json, sys, itertools, copy, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W29 = os.path.join(ROOT, 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json')
W38 = os.path.join(ROOT, 'results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json')
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
key = lambda c: sorted(set(c), key=lambda x: (abs(x), x))
a = json.load(open(W29)); b = json.load(open(W38))
assert a['spec'] == b['spec']
src = [(r['c'], r['source']) for r in a['records'] if r['kind'] == 'SOURCE']
assert len(src) == 17
def summary(recs, ngates, ndef=0):
    nres = sum(r['kind'] == 'RES' for r in recs)
    return {'source': 17, 'def_views': ndef, 'resolution': nres, 'paid_gates': ngates,
            'paid_total': nres + ngates, 'live_records': len(recs)}
def dump(name, d):
    p = os.path.join(out, name); s = json.dumps(d) + '\n'; open(p, 'w').write(s)
    return p
res = {}
# (i) W29 with its unused paid gate removed
dv = sum(r['kind'] == 'DEF' for r in a['records'])
lits = {abs(x) for r in a['records'] for x in r['c']}
w28 = copy.deepcopy(a); w28['gate_defs'] = []; w28['summary'] = summary(w28['records'], 0)
res['w29_def_views'] = dv; res['w29_gate_var_8_occurs'] = 8 in lits
dump('W28_dead_gate_deleted.json', w28)
# (ii) DP elimination cone over all orders
def dp(order):
    recs = [{'kind': 'SOURCE', 'c': key(c), 'parents': [], 'source': s} for c, s in src]
    live = list(range(len(recs))); idx = {json.dumps(recs[i]['c']): i for i in live}
    for v in order:
        P = [i for i in live if v in recs[i]['c']]; N = [i for i in live if -v in recs[i]['c']]
        rest = [i for i in live if i not in P and i not in N]
        for i in P:
            for j in N:
                r = key([x for x in recs[i]['c'] if x != v] + [x for x in recs[j]['c'] if x != -v])
                if any(-x in r for x in r): continue
                k = json.dumps(r)
                if k in idx: 
                    if idx[k] not in rest: rest.append(idx[k])
                    continue
                recs.append({'kind': 'RES', 'c': r, 'parents': [i, j], 'pivot': v})
                idx[k] = len(recs) - 1; rest.append(len(recs) - 1)
                if r == []: return recs, len(recs) - 1
        live = rest
    return recs, idx.get('[]')
best = None; hist = {}
for order in itertools.permutations(range(1, 8)):
    recs, e = dp(order)
    if e is None: continue
    need = set(); st = [e]
    while st:
        i = st.pop()
        if i in need: continue
        need.add(i); st += recs[i]['parents']
    nres = sum(recs[i]['kind'] == 'RES' for i in need)
    hist[nres] = hist.get(nres, 0) + 1
    if best is None or nres < best[0]: best = (nres, order, recs, need, e)
nres, order, recs, need, e = best
keep = sorted(set(range(17)) | need)          # all 17 sources must be present
remap = {o: n for n, o in enumerate(keep)}
pk = []
for o in keep:
    r = copy.deepcopy(recs[o]); r['parents'] = [remap[p] for p in r['parents']]; pk.append(r)
assert pk[-1]['c'] == []
dpk = {'spec': a['spec'], 'gate_defs': [], 'records': pk, 'summary': summary(pk, 0)}
dump('DP_best_pure_RES.json', dpk)
res['dp_orders'] = 5040; res['dp_cone_res_histogram'] = dict(sorted(hist.items()))
res['dp_best_res'] = nres; res['dp_best_order'] = list(order)
# (iii) hostile non-minimal packets accepted with larger paid counts
t = copy.deepcopy(b); r23 = copy.deepcopy(t['records'][23])
users = [i for i, r in enumerate(t['records']) if 23 in r['parents']]
t['records'].insert(24, r23)                                   # duplicate at 24
for r in t['records'][25:]:
    r['parents'] = [p + 1 if p >= 24 else p for p in r['parents']]
u2 = users[1] + 1                                              # second user -> copy
t['records'][u2]['parents'] = [24 if p == 23 else p for p in t['records'][u2]['parents']]
t['summary'] = summary(t['records'], 3, 6); dump('W39_tree_unrolled_idx23.json', t)
d = copy.deepcopy(a); dead = copy.deepcopy(d['records'][-2]); d['records'].insert(len(d['records']) - 1, dead)
d['records'][-1]['parents'] = list(d['records'][-1]['parents'])
d['summary'] = summary(d['records'], 1); dump('W30_dead_duplicate_res.json', d)
res['w38_idx23_users'] = users
json.dump(res, open(os.path.join(out, 'py_summary.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))

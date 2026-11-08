#!/usr/bin/env python3
"""Rebalance authenticated /341 proofs; independently check their exact semantics.
Run in this directory after regenerating baseline.json from the historical producer.
No change to the historical checker, source clauses, rule tags, or logical weights.
"""
from __future__ import annotations
import copy, hashlib, json, math, subprocess, time
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
CHECKER = ROOT / 'historical/lspv2_341_independent_verify.js'
checks = 0

def require(test: bool, message: str) -> None:
    global checks
    checks += 1
    if not test:
        raise ValueError(message)

def clause_value(literals: list[int], bits: list[int] | str) -> bool:
    return any(int(bits[abs(l)-1]) == (1 if l > 0 else 0) for l in literals)

def source_table(literals: list[int], support: list[int]) -> int:
    result = 0
    for a in range(1 << len(support)):
        values = {v:(a >> j)&1 for j,v in enumerate(support)}
        if any(values[abs(l)-1] == int(l > 0) for l in literals):
            result |= 1 << a
    return result

def rebalance(f: dict) -> dict:
    out = copy.deepcopy(f)
    proof = []
    rows = []
    for v in range(f['graph']['n']):
        src = [c for c in f['clauses'] if c['vertex'] == v]
        support = [i for i,e in enumerate(f['graph']['edges']) if v in e]
        factors = [{'id':c['id'], 'table':source_table(c['literals'],support)} for c in src]
        while len(factors) > 1:
            nxt = []
            for i in range(0,len(factors),2):
                a,b = factors[i:i+2]
                d = {'id':f'd{len(proof)}','kind':'factor','rule':'AND3',
                     'parents':[a['id'],b['id']],'support':support[:],'table':a['table'] & b['table']}
                proof.append(d); nxt.append(d)
            factors = nxt
        d = factors[0]
        d['row'] = {'mask':hex(sum(1 << e for e in support)), 'rhs':f['charges'][v]}
        rows.append(d)
    while len(rows) > 1:
        nxt = []
        for i in range(0,len(rows),2):
            if i + 1 == len(rows):
                nxt.append(rows[i]); continue
            a,b = rows[i:i+2]
            d = {'id':f'd{len(proof)}','kind':'affine','rule':'XOR',
                 'parents':[a['id'],b['id']],
                 'row':{'mask':hex(int(a['row']['mask'],0)^int(b['row']['mask'],0)),
                        'rhs':a['row']['rhs']^b['row']['rhs']}}
            proof.append(d); nxt.append(d)
        rows = nxt
    out['proof'] = proof
    return out

def independently_check(f: dict, original: dict, balanced: bool) -> dict:
    """Separate Python semantic/source audit, not the historical JS implementation."""
    h = f['graph']['n']; edges = f['graph']['edges']; ne = len(edges)
    require(f['clauses'] == original['clauses'],'external source changed')
    require(f['graph'] == original['graph'] and f['charges'] == original['charges'],'graph/charge binding')
    require(len(f['clauses']) == 4*h, 'source count')
    byid = {}; depth = {}; degree = Counter()
    for c in f['clauses']:
        support = [i for i,e in enumerate(edges) if c['vertex'] in e]
        require(c['id'] not in byid and type(c['id']) is str,'unique string source id')
        require(sorted(abs(l)-1 for l in c['literals']) == sorted(support),'source incidence')
        byid[c['id']] = {'kind':'factor','support':support,'table':source_table(c['literals'],support)}
        depth[c['id']] = 0
    for p in f['proof']:
        require(type(p['id']) is str and p['id'] not in byid,'fresh output')
        require(len(p['parents']) == 2 and len(set(p['parents'])) == 2,'binary distinct parents')
        require(all(k in byid for k in p['parents']),'prior parent')
        a,b = (byid[k] for k in p['parents'])
        if p['rule'] == 'AND3':
            require(a['kind'] == b['kind'] == p['kind'] == 'factor','AND3 types')
            sup = p['support']
            require(set(sup) == set(a['support'])|set(b['support']) and len(sup) <= 3,'AND3 support')
            require(len(sup) == len(set(sup)), 'duplicate support')
            actual = 0
            for val in range(1 << len(sup)):
                env = {x:(val>>j)&1 for j,x in enumerate(sup)}
                def ev(t: dict) -> int:
                    ix = sum(env[x] << j for j,x in enumerate(t['support']))
                    return (t['table'] >> ix)&1
                if ev(a) and ev(b): actual |= 1 << val
            require(actual == p['table'],'conjunction false')
            if 'row' in p:
                mask = int(p['row']['mask'],0); rhs = p['row']['rhs']
                require(0 <= mask < 1 << ne and rhs in (0,1),'row domain')
                require(set(i for i in range(ne) if mask >> i & 1) <= set(sup),'row support')
                for val in range(1 << len(sup)):
                    assignment = sum(((val >> j)&1) << x for j,x in enumerate(sup))
                    require(bool(p['table'] >> val & 1) == (((assignment & mask).bit_count() & 1) == rhs), 'row alias')
        elif p['rule'] == 'XOR':
            require('row' in a and 'row' in b and p['kind'] == 'affine','XOR types')
            require(int(p['row']['mask'],0) == int(a['row']['mask'],0)^int(b['row']['mask'],0),'XOR mask')
            require(p['row']['rhs'] == a['row']['rhs']^b['row']['rhs'],'XOR RHS')
        else:
            raise ValueError('unknown native rule')
        depth[p['id']] = 1 + max(depth[k] for k in p['parents'])
        degree.update(p['parents']); byid[p['id']] = p
    last = f['proof'][-1]
    require(last['kind'] == 'affine' and last['row'] == {'mask':'0x0','rhs':1},'sink')
    live = set(); stack = [last['id']]
    while stack:
        u = stack.pop()
        if u in live: continue
        live.add(u); stack.extend(byid[u].get('parents',[]))
    require(len(live) == len(byid),'dead or unauthenticated source')
    require(len(f['proof']) == 4*h-1,'work')
    m = len(f['clauses']); q = len(f['proof']); arc = sum(len(p['parents']) for p in f['proof'])
    sharing = sum(degree[u]-1 for u in live if u != last['id'])
    deficit = sum(2-len(p['parents']) for p in f['proof'])
    require(q-m+1 == sharing+deficit == 0, 'ancestry excess')
    if balanced: require(depth[last['id']] == (m-1).bit_length(),'optimal ideal span')
    essential = 0
    for c,d in zip(f['clauses'],f['deleted'],strict=True):
        require(c['id'] == d['sourceId'],'deletion identity')
        if d['assignment'] is None: continue
        essential += 1
        require(len(d['assignment']) == ne,'witness width')
        for other in f['clauses']:
            require(clause_value(other['literals'],d['assignment']) == (other['id'] != c['id']), 'deletion witness')
    require(essential == f['properties']['essential'],'essential count')
    for v in range(h):
        require(sum(int(f['evenWitness'][i]) for i,e in enumerate(edges) if v in e)%2 == 0,'SAT control')
    return {'graph':f['graph']['name'],'vertices':h,'source_clauses':m,'paid_work':q,
            'ideal_span':depth[last['id']],'essential':essential,'exact_optimum_certified':essential==m,
            'proof_json_bytes':len(json.dumps(f['proof'],separators=(',',':')).encode()),
            'arity_deficit':deficit,'sharing_excess':sharing}

def native_run(packet: dict, filename: str) -> subprocess.CompletedProcess[str]:
    path = ROOT/filename
    path.write_text(json.dumps(packet,separators=(',',':'))+'\n')
    return subprocess.run(['node',str(CHECKER),str(path)],capture_output=True,text=True,timeout=20)

def main() -> None:
    start = time.perf_counter()
    baseline = json.loads((ROOT/'baseline.json').read_text())
    packet = copy.deepcopy(baseline)
    packet['fixtures'] = [rebalance(f) for f in baseline['fixtures']]
    original_metrics = [independently_check(f,f,False) for f in baseline['fixtures']]
    balanced_metrics = [independently_check(f,o,True) for f,o in zip(packet['fixtures'],baseline['fixtures'])]
    native = native_run(packet,'balanced.json')
    require(native.returncode == 0,'historical verifier rejected balanced packet: '+native.stderr)
    historical = json.loads(native.stdout)
    require(native.stdout == (ROOT/'baseline_verified.json').read_text(),'native result differs')
    negatives = []
    for case in ('bad_xor','bad_table','source_flip','missing_parent','forward_parent','duplicate_id','RES','LOCAL-CONVERT','DEF','even_charge'):
        x = copy.deepcopy(packet); f=x['fixtures'][0]
        if case=='bad_xor': f['proof'][-1]['row']['rhs']=0
        elif case=='bad_table': f['proof'][0]['table'] ^= 1
        elif case=='source_flip': f['clauses'][0]['literals'][0] *= -1
        elif case=='missing_parent': f['proof'][0]['parents'][0]='absent'
        elif case=='forward_parent': f['proof'][0]['parents'][0]=f['proof'][-1]['id']
        elif case=='duplicate_id': f['proof'][1]['id']=f['proof'][0]['id']
        elif case=='even_charge': f['charges'][0] ^= 1
        else: f['proof'][0]['rule']=case
        out = native_run(x,'mutation.json')
        require(out.returncode != 0,'accepted mutation '+case)
        try: independently_check(f,baseline['fixtures'][0],False)
        except (ValueError,KeyError): py_rejected=True
        else: py_rejected=False
        require(py_rejected,'python accepted '+case)
        negatives.append({'case':case,'historical_rejected':True,'python_rejected':True})
    (ROOT/'mutation.json').unlink()
    result={'status':'PROVED-RESTRICTED theorem application; COMPUTATIONAL new native-byte replay',
            'historical_checker_blob':'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
            'historical_check_count':historical['checks'],'python_assertions':checks,
            'original':original_metrics,'balanced':balanced_metrics,'negative_controls':negatives,
            'balanced_packet_sha256':hashlib.sha256((ROOT/'balanced.json').read_bytes()).hexdigest(),
            'wall_seconds':time.perf_counter()-start,
            'peak_RSS':'not measured','machine_model':'Python/Node host; logical span is unit-node unlimited-processors only'}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()

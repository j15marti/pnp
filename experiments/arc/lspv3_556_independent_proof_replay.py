#!/usr/bin/env python3
"""Independent typed binary-Resolution replay for LSPV-3/556.
Counterfactual syntaxes only; does not authenticate the historical R_mix341 checker.
"""
import hashlib
import json
import pathlib
import sys


def norm(xs):
    assert all(isinstance(t, int) and not isinstance(t, bool) and t != 0 for t in xs)
    assert len(xs) == len(set(xs))
    assert not any(-v in xs for v in xs)
    return tuple(sorted(xs, key=lambda x: (abs(x), -x)))


def parser(raw):
    toks = raw.split()
    assert toks[:2] == ["p", "cnf"]
    nv, nc = int(toks[2]), int(toks[3])
    assert nv >= 0 and nc >= 0
    clauses, working = [], []
    for s in toks[4:]:
        assert s == "0" or (s.lstrip("-").isdigit() and int(s) != 0)
        v = int(s)
        assert abs(v) <= nv
        if not v:
            clauses.append(norm(working))
            working = []
        else:
            working.append(v)
    assert not working and len(clauses) == nc
    return clauses, nv


def resolve(a, b, pivot):
    assert pivot > 0 and ((pivot in a and -pivot in b) or (-pivot in a and pivot in b))
    out = set(a) | set(b)
    out.discard(pivot)
    out.discard(-pivot)
    return norm(list(out))


def verify(src, packet, tag):
    assert packet['source_sha256'] == hashlib.sha256(src.encode()).hexdigest()
    assert packet['source_length'] == len(src.encode())
    clauses, _ = parser(src)
    env = {f's{i}': c for i,c in enumerate(clauses)}
    for r in packet['nodes']:
        assert r['rule'] == tag
        assert r['id'] not in env and r['left'] != r['right']
        assert r['left'] in env and r['right'] in env
        ans = resolve(env[r['left']], env[r['right']], r['pivot'])
        assert ans == norm(r['clause'])
        env[r['id']] = ans
    assert packet['terminal'] == packet['nodes'][-1]['id']
    assert env[packet['terminal']] == ()
    return len(packet['nodes'])


def clause_sat(c, val):
    return any((bool((val >> (abs(l)-1)) & 1)) == (l > 0) for l in c)


def run(filename):
    d = json.loads(pathlib.Path(filename).read_text())
    src = d['source']
    ca, nv = parser(src)
    assert (nv,len(ca)) == (3,8)
    assert verify(src,d['A'],'RES') == verify(src,d['B'],'R2') == 7
    models = [a for a in range(1<<nv) if all(clause_sat(c,a) for c in ca)]
    assert models == []
    deletions = []
    for i in range(len(ca)):
        models_after = [a for a in range(1<<nv) if all(clause_sat(c,a) for j,c in enumerate(ca) if i!=j)]
        assert len(models_after) == 1
        assert not clause_sat(ca[i],models_after[0])
        deletions.append({'source_id':f's{i}','witness':format(models_after[0],f'0{nv}b')})
    # Distinct counterfactual bytes with identical semantic trace and seven paid nodes.
    assert len({json.dumps(d['A']['nodes'][i],sort_keys=True) for i in range(7)}) == 7
    assert all(d['A']['nodes'][i]['rule'] != d['B']['nodes'][i]['rule'] for i in range(7))
    assert all({k:v for k,v in d['A']['nodes'][i].items() if k!='rule'} ==
               {k:v for k,v in d['B']['nodes'][i].items() if k!='rule'} for i in range(7))
    return dict(run='LSPV-3/556',independent='Python',status='PASS',sources=8,paid=7,models=0,
                minimal_by_source_essentiality=True,source_deletion_witnesses=deletions,
                disclaimer='No historical R_mix341 accepted-byte checker was executed.')

if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),indent=2))

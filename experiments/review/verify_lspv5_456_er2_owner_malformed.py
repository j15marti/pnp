#!/usr/bin/env python3
"""Independent Python audit of the exact accepted zero-literal packet from LSPV-5/456."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

RAW=Path('results/raw/arc/2026-11-09_0215_LSPV5_456_ER2_OWNER_MALFORMED_RAW.json')

def norm(xs):
    return sorted(set(xs), key=lambda x:(abs(x),x))

def main():
    d=json.loads(RAW.read_text())
    pkt=d['exact_zero_literal_packet']['packet']
    compact=json.dumps(pkt,separators=(',',':'),ensure_ascii=False)
    assert len(compact.encode())==d['exact_zero_literal_packet']['utf8_bytes']
    assert hashlib.sha256(compact.encode()).hexdigest()==d['exact_zero_literal_packet']['sha256']
    L,G=pkt['lines'],pkt['defs']
    assert len(L)==459 and len(G)==68
    assert [n['id'] for n in L]==list(range(459))
    assert [g['owner'] for g in G]==list(range(68))
    assert [g['id'] for g in G]==list(range(13,81))

    # Replay the published peer verifier's mathematical checks.
    counts={'SOURCE':0,'FACET':0,'RES':0}
    for i,n in enumerate(L):
        counts[n['kind']]+=1
        assert norm(n['clause'])==norm(norm(n['clause']))
        if n['kind']=='SOURCE':
            assert i<21
        elif n['kind']=='FACET':
            g=G[n['owner']]
            k=g['facets'].index(i)
            expect=[[-g['id'],g['a']],[-g['id'],g['b']],[g['id'],-g['a'],-g['b']]][k]
            assert norm(n['clause'])==norm(expect)
        else:
            assert n['left']<i and n['right']<i and n['pivot']>0
            a,b=L[n['left']]['clause'],L[n['right']]['clause']
            assert n['pivot'] in a and -n['pivot'] in b
            expect=[x for x in a if x!=n['pivot']]+[x for x in b if x!=-n['pivot']]
            assert norm(n['clause'])==norm(expect)
    assert counts=={'SOURCE':21,'FACET':204,'RES':234}

    z=G[22]
    assert z['id']==35 and z['a']==-29 and z['b']==0 and z['facets']==[174,175,176]
    assert L[175]['clause']==[0,-35] and L[176]['clause']==[0,29,35]
    zeros=[(n['id'],j) for n in L for j,x in enumerate(n['clause']) if x==0]
    assert zeros==[(175,0),(176,0)]
    used={p for n in L if n['kind']=='RES' for p in (n['left'],n['right'])}
    assert 174 in used and 175 not in used and 176 not in used

    # Literal zero is not a Boolean literal. Under DIMACS serialization it is a
    # terminator, so the object cannot be a valid signed-clause certificate.
    receipt={
      'status':'PASS_INDEPENDENT_PYTHON',
      'packet_sha256':hashlib.sha256(compact.encode()).hexdigest(),
      'peer_rule_replay_counts':counts,
      'invalid_zero_literal_locations':zeros,
      'owner_22_used_facets':[f for f in z['facets'] if f in used],
      'owner_22_unused_facets':[f for f in z['facets'] if f not in used],
      'strict_valid_certificate':False,
      'base_theorem_falsified':False,
      'checker_completeness_falsified':True,
    }
    print(json.dumps(receipt,sort_keys=True))
    return 0

if __name__=='__main__':
    sys.exit(main())

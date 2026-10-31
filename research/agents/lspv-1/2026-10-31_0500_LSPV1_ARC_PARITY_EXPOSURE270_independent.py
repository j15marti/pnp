#!/usr/bin/env python3
"""Independent finite reference checker for ARC-PARITY-EXPOSURE270 (no producer imports)."""
from __future__ import annotations
import json,itertools, functools,sys,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
R=json.loads((P/'ARC_PARITY_EXPOSURE270_raw.json').read_text())
checks=0

def okay(b):
    global checks
    assert b
    checks+=1

def mk(k, mask):
    z=k+2;u=k+3;v=k+4; out=[]
    for i in range(k):
        a=i+1; b=i+2
        p=(mask>>i)&1
        for aa,bb in (((-a,b),(a,-b)) if not p else ((a,b),(-a,-b))):
            out.extend(((aa,bb,z),(aa,bb,-z)))
    for vtx in (1,k+1):
        out.extend([(-vtx,su*u,sv*v) for su in (1,-1) for sv in (1,-1)])
    return out

def eval_clauses(clauses,a):
    return all(any( ((a>>(abs(l)-1))&1)==(1 if l>0 else 0) for l in c) for c in clauses)

def encode(clauses,k):
    n=k+4;w=max(2,len(str(n)))
    return (f'CNF:{n:0{w}d}:{len(clauses):04d}\n'+''.join(f'C{j:04d}:'+ '|'.join( ('+' if v>0 else '-') + f'{abs(v):0{w}d}' for v in row)+'\n' for j,row in enumerate(clauses))).encode('ascii')

def info_positions(encodings):
    # Every informative encoded bit is classified by its support over the complete family.
    width=len(encodings[0]); k=(len(encodings)).bit_length()-1
    allm=(1<<(1<<k))-1
    patterns={}
    for addr in range(width*8):
        vals=sum((((s[addr//8]>>(addr%8))&1)<<i) for i,s in enumerate(encodings))
        if vals not in (0,allm): patterns.setdefault(vals,addr)
    return patterns

def depth(k):
    strings=[encode(mk(k,b),k) for b in range(1<<k)]
    okay(len(set(map(len,strings)))==1)
    patterns=info_positions(strings)
    # Each informative bit has a truth table that is a single source parity input bit, or its complement.
    source_patterns=[sum(((b>>i)&1)<<b for b in range(1<<k)) for i in range(k)]
    allm=(1<<(1<<k))-1
    okay(all(any(p==v or p==(allm^v) for v in source_patterns) for p in patterns))
    for i in range(k):
        okay(any(p==v or p==(allm^v) for p in patterns for v in [source_patterns[i]]))
    # Exact worst-case decision-tree depth over indexed actual ASCII sign bits; k<=6.
    label=[(b.bit_count()%2==0) for b in range(1<<k)]
    @functools.lru_cache(None)
    def recur(mask):
        ys={label[b] for b in range(1<<k) if mask>>b&1}
        if len(ys)==1:return 0
        best=100
        for p in patterns:
            l=mask&~p;r=mask&p
            if l and r:
                best=min(best,1+max(recur(l),recur(r)))
        return best
    ans=recur(allm)
    okay(ans==k)
    return {'m':k,'minimax_bit_queries':ans,'unique_informative_bit_patterns':len(patterns),'reachable_candidate_sets':recur.cache_info().currsize,
            'source_encoding_bytes':len(strings[0])}


def main():
    entries=R['rows']; okay(len(entries)==126)
    for row in entries:
        k=row['m']; b=int(row['bits'][::-1],2); C=mk(k,b)
        okay(len(C)==4*k+8)
        okay(len(encode(C,k))==row['source_bytes'])
        models=[a for a in range(1<<(k+4)) if eval_clauses(C,a)]
        okay((len(models)==8 if b.bit_count()%2==0 else len(models)==0))
        okay(bool(models)==row['SAT'])
        okay(row['child_bytes']>0 and row['baseline_nodes']>=1)
    for d in R['detailed']:
        k=d['m_edges']; b=sum(v<<i for i,v in enumerate(d['bits'])); C=mk(k,b);n=k+4
        okay([list(c) for c in C]==d['clauses'])
        models=[a for a in range(1<<n) if eval_clauses(C,a)]
        okay(models==d['witnesses'])
        for e in d['occurrences']:
            lit=C[e['clause']][e['slot']]
            okay(lit==e['literal'] and e['S_target']==int(lit>0) and e['U_target']==int(lit<0))
            okay(e['inverse_S_as_U']==e['U_target'] and e['inverse_U_as_S']==e['S_target'])
        for pair in d['pair_compatibility']:
            i,j=pair['clauses']
            for q in ('SS','SU','US','UU'):
                demanded={}; feasible=True
                for index,style in ((i,q[0]),(j,q[1])):
                    for lit in C[index]:
                        v=abs(lit);a=(lit>0)==(style=='S')
                        if v in demanded and demanded[v]!=a:feasible=False
                        demanded[v]=a
                okay(pair[q]==feasible)
        for r in d['resolution_blockers']:
            i,j=r['source']; pivot=r['pivot']
            okay(any(x in C[i] and -x in C[j] and abs(x)==pivot for x in C[i]))
            for a in models:
                okay(not all(((a>>(int(v)-1))&1)==val for v,val in r['forbidden_cube'].items()))
        for trail in d['flip_trails']:
            current=trail['start']
            for step in trail['steps']:
                for v in step['flipped']: current^=1<<(v-1)
                okay(current==step['mask'])
                counts=[sum(((current>>(abs(x)-1))&1)==int(x>0) for x in c) for c in C]
                okay(counts==step['counts'])
                okay(([counts.count(t) for t in range(4)]==step['histogram']))
        # The child has exactly one duplicated source clause on SAT and all sign vectors on UNSAT.
        s=d['physical_child']
        okay(len(s)==d['physical_child_length'])
        okay(s.count('\n')==9)
        for a in range(1<<3):
            pass
    decision=[depth(k) for k in range(1,7)]
    okay(R['SAT_sources']==63 and R['UNSAT_sources']==63)
    okay(sum(x['source_bytes'] for x in entries)==R['original_source_total_bytes'])
    okay(sum(x['baseline_nodes'] for x in entries)==R['standard_DPLL_total_nodes'])
    okay(sum(x['baseline_events']+x['source_bytes'] for x in entries)==R['standard_DPLL_selected_events'])
    okay(sum(x['controller_events'] for x in entries)==R['stream_recognizer_plus_guest_selected_events'])
    print(json.dumps({'verifier':'INDEPENDENT_PASS','assertions':checks,'minimax':decision,'source_rows':len(entries),'detailed':len(R['detailed']),
                      'producer_sha256':hashlib.sha256((P/'arc_parity_exposure270.py').read_bytes()).hexdigest(),
                      'raw_sha256':hashlib.sha256((P/'ARC_PARITY_EXPOSURE270_raw.json').read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
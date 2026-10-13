#!/usr/bin/env python3
"""LIVEPREFIX1: finite checks for causal, source-matched wrapper obligations.
Standard library only. Each --batch is separate and has a 25-second deadline.
The finite prefix oracle is BRUTE FORCE; it is not a polynomial SAT solver.
The two-tree reduction implements the source specification of TWOTREEBRIDGE1,
parent code blob 861b509c25fb2067c59de1695a0d953f31a55f5c.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import time

COLORS = (0, 1, 2)
MAGIC = '01010100'

class Audit:
    def __init__(self):
        self.start = time.monotonic()
        self.counts: Counter[str] = Counter()
    def check(self, condition: bool, name: str) -> None:
        self.counts[name] += 1
        if not condition:
            raise AssertionError(name)
        if time.monotonic() - self.start > 25:
            raise TimeoutError('25-second deadline; split the batch')


def graph_ok(n: int, edges: list[tuple[int, int]]) -> None:
    if type(n) is not int or n < 1:
        raise ValueError('positive explicit vertex count required')
    if any(type(u) is not int or type(v) is not int or not 0 <= u < v < n for u,v in edges):
        raise ValueError('invalid edge')
    if len(set(edges)) != len(edges):
        raise ValueError('duplicate edge')


def components(vertices, edges):
    adj = {v: [] for v in vertices}
    for u,v in edges:
        if u not in adj or v not in adj:
            raise ValueError('endpoint outside vertex set')
        adj[u].append(v); adj[v].append(u)
    unseen = set(vertices); out = []
    while unseen:
        start = min(unseen); unseen.remove(start); todo = [start]
        for v in todo:
            for u in adj[v]:
                if u in unseen:
                    unseen.remove(u); todo.append(u)
        out.append(sorted(todo))
    return out


def reduce_two_trees(n, edges):
    graph_ok(n, edges)
    incident = [[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        incident[u].append(i); incident[v].append(i)
    next_id = 0; blocks = []; ports = {}
    for v in range(n):
        block = []
        for ei in incident[v] or [-1]:
            block.append(next_id); ports[v,ei] = next_id; next_id += 1
        blocks.append(block)
    forests = [[], []]; diamonds = []
    for block in blocks:
        for x,y in zip(block, block[1:]):
            a,b = next_id,next_id+1; next_id += 2
            forests[0].extend([(x,a),(a,b),(b,y)])
            forests[1].extend([(x,b),(a,y)])
            diamonds.append((x,y,a,b))
    forests[1].extend((ports[u,i], ports[v,i]) for i,(u,v) in enumerate(edges))
    shared = list(range(next_id)); trees = []
    for forest in forests:
        forest = sorted(tuple(sorted(e)) for e in forest)
        parts = components(shared, forest)
        if len(forest) != len(shared)-len(parts):
            raise AssertionError('forest partition failed')
        hub = next_id; next_id += 1; vs = shared+[hub]; joins = []
        es = list(forest)
        for part in parts:
            endpoint = min(part); mid = next_id; next_id += 1
            vs.append(mid); joins.append((endpoint,mid,hub))
            es.extend([(endpoint,mid),(mid,hub)])
        trees.append({'vertices': vs, 'edges': sorted(tuple(sorted(e)) for e in es),
                      'hub': hub, 'joins': joins})
    return {'universe': next_id, 'trees': trees, 'blocks': blocks, 'diamonds': diamonds}


def encode_pair(R):
    h = R['universe']; out = MAGIC+'1'*h+'0'
    for T in R['trees']:
        vs,es = set(T['vertices']),set(T['edges'])
        out += ''.join('1' if v in vs else '0' for v in range(h))
        out += ''.join('1' if (u,v) in es else '0' for u,v in it.combinations(range(h),2))
    return out


def decode_pair(bits):
    if type(bits) is not str or not bits.startswith(MAGIC) or any(c not in '01' for c in bits):
        raise ValueError('binary header')
    stop = bits.find('0',8); h = stop-8
    if h < 1 or len(bits) != 9+h*h+2*h:
        raise ValueError('length')
    offset = stop+1; trees = []
    for _ in range(2):
        vs = [v for v in range(h) if bits[offset+v]=='1']; offset += h; es = []
        for u,v in it.combinations(range(h),2):
            if bits[offset]=='1': es.append((u,v))
            offset += 1
        if not vs or any(u not in vs or v not in vs for u,v in es):
            raise ValueError('endpoints')
        if len(es)!=len(vs)-1 or len(components(vs,es))!=1:
            raise ValueError('not tree')
        trees.append({'vertices': vs, 'edges': es})
    if set(trees[0]['vertices']) | set(trees[1]['vertices']) != set(range(h)):
        raise ValueError('unused label')
    return {'universe':h,'trees':trees}


def is_coloring(c, edges):
    return all(v in COLORS for v in c) and all(c[u]!=c[v] for u,v in edges)


def valid_target(R, w):
    return len(w)==R['universe'] and all(is_coloring(w,T['edges']) for T in R['trees'])


def lift(R, c):
    w = [0]*R['universe']
    for color,block in zip(c,R['blocks']):
        for v in block: w[v]=color
    for x,y,a,b in R['diamonds']:
        w[a],w[b] = [s for s in COLORS if s!=w[x]]
    for T in R['trees']:
        w[T['hub']]=0
        for x,m,h in T['joins']:
            w[m]=next(s for s in COLORS if s!=w[x] and s!=w[h])
    return tuple(w)


def palette_repair(w, vertex, color):
    before = w[vertex]
    return tuple(color if c==before else before if c==color else c for c in w)


def brute_solutions(n, edges):
    return [c for c in it.product(COLORS, repeat=n) if is_coloring(c,edges)]


def prefix_select(solutions, n, pins):
    """Finite existential oracle, explicitly scans complete source solutions."""
    calls = scans = 0
    def exists(prefix):
        nonlocal calls, scans
        calls += 1
        for w in solutions:
            scans += 1
            if w[:len(prefix)]==prefix and all(w[v]==c for v,c in pins.items()):
                return True
        return False
    if not exists(()): return None, calls, scans
    prefix = ()
    for _ in range(n):
        for c in COLORS:
            if exists(prefix+(c,)):
                prefix += (c,); break
        else: raise AssertionError('prefix invariant')
    return prefix, calls, scans


def independent_target_solve(R, pins):
    """Exact target-side 3-colouring backtracking with domain propagation."""
    h=R['universe']; adj=[set() for _ in range(h)]
    for T in R['trees']:
        for u,v in T['edges']: adj[u].add(v); adj[v].add(u)
    dom=[7]*h
    for v,c in pins.items(): dom[v]=1<<c
    def search(ds):
        queue=[v for v,x in enumerate(ds) if x and x&(x-1)==0]
        seen=set()
        while queue:
            v=queue.pop()
            if v in seen: continue
            seen.add(v)
            for u in adj[v]:
                old=ds[u]; new=old & ~ds[v]
                if not new: return None
                if new!=old:
                    ds[u]=new
                    if new&(new-1)==0: queue.append(u)
        choices=[v for v,x in enumerate(ds) if x&(x-1)]
        if not choices: return tuple(x.bit_length()-1 for x in ds)
        v=min(choices,key=lambda v:(ds[v].bit_count(),-len(adj[v])))
        for c in COLORS:
            if ds[v]&(1<<c):
                trial=ds.copy(); trial[v]=1<<c
                ans=search(trial)
                if ans is not None: return ans
        return None
    return search(dom)


def batch_quantifiers(A):
    counts=Counter(); example=None
    index=lambda r,a,s,b:(r<<3)|(a<<2)|(s<<1)|b
    for mask in range(1<<16):
        V=lambda r,a,s,b: bool(mask & (1<<index(r,a,s,b)))
        offline=all(any(V(r,a,s,b) for a in (0,1) for b in (0,1))
                    for r in (0,1) for s in (0,1))
        causal=all(any(all(any(V(r,a,s,b) for b in (0,1)) for s in (0,1))
                       for a in (0,1)) for r in (0,1))
        strategies=all(any(V(r,a,0,b0) and V(r,a,1,b1)
                          for a,b0,b1 in it.product((0,1),repeat=3)) for r in (0,1))
        A.check(causal==strategies,'strategy_enumeration_matches_nested_quantifiers')
        A.check(not causal or offline,'causal_implies_offline')
        counts[f'offline_{int(offline)}_causal_{int(causal)}'] += 1
        if offline and not causal and example is None: example=mask
    mask=sum(1<<index(r,a,s,b) for r,a,s,b in it.product((0,1),repeat=4) if a==s)
    A.check(all(any(a==s for a in (0,1)) for s in (0,1)),'future_equality_offline')
    A.check(not any(all(a==s for s in (0,1)) for a in (0,1)),'future_equality_not_causal')
    return {'relations':65536,'classification':dict(counts),'first_gap_mask':example,
            'equality_of_early_response_and_future_bit_mask':mask,
            'point':'This enumerates all Boolean relations on four bits, not all algorithms.'}


def batch_trees(A):
    counts=Counter(); rows=[]
    for n in range(1,5):
        possible=list(it.combinations(range(n),2))
        for mask in range(1<<len(possible)):
            edges=[e for i,e in enumerate(possible) if mask>>i&1]
            R=reduce_two_trees(n,edges); enc=encode_pair(R); dec=decode_pair(enc)
            A.check(encode_pair(dec)==enc,'exact_pair_roundtrip')
            A.check(len(enc)==9+R['universe']**2+2*R['universe'],'exact_bit_length')
            sols=brute_solutions(n,edges); counts['graphs']+=1
            for c in sols:
                w=lift(R,c); counts['source_assignments']+=1
                A.check(valid_target(dec,w),'forward_lift')
                A.check(tuple(w[b[0]] for b in R['blocks'])==c,'source_projection')
                for v in range(n):
                    for color in COLORS:
                        z=palette_repair(w,R['blocks'][v][0],color)
                        A.check(valid_target(dec,z) and z[R['blocks'][v][0]]==color,'palette_repair')
                        counts['palette_repairs']+=1
            for length in range(n+1):
                for pref in it.product(COLORS,repeat=length):
                    pins=dict(enumerate(pref)); ans,calls,scans=prefix_select(sols,n,pins)
                    expected=next((w for w in sols if w[:length]==pref),None)
                    A.check(ans==expected,'prefix_solver_lexicographic_answer')
                    A.check(calls<=1+3*n,'prefix_query_bound')
                    counts['prefix_queries']+=calls; counts['oracle_solution_rows_scanned']+=scans
                    counts['prefix_instances']+=1
            # Independent target-side search, including a NO pin pattern.
            pinsets=[{}, {0:0}, {0:0,1:0}] if n>1 else [{},{0:0}]
            for pins in pinsets:
                target_pins={R['blocks'][v][0]:c for v,c in pins.items()}
                got=independent_target_solve(dec,target_pins)
                expected=any(all(w[v]==c for v,c in pins.items()) for w in sols)
                A.check((got is not None)==expected,'independent_target_decision')
                counts['target_decisions']+=1
                if got is not None:
                    p=tuple(got[b[0]] for b in R['blocks'])
                    A.check(valid_target(dec,got) and is_coloring(p,edges),'independent_reverse_witness')
                    counts['target_witnesses']+=1
            rows.append({'n':n,'mask':mask,'source_models':len(sols),'target_vertices':R['universe'],
                         'encoded_bits':len(enc)})
    good=encode_pair(reduce_two_trees(1,[]))
    for bad in (None,True,'',good[:-1],good+'0','x'+good, '00000000'+good[8:],MAGIC+'1'*50):
        try: decode_pair(bad)
        except ValueError: A.check(True,'malformed_rejected')
        else: A.check(False,'malformed_rejected')
    return {'counts':dict(counts),'graphs':rows,
            'warning':'Finite prefix queries scan an exhaustive source solution list; no P solver was tested.'}


def hash_event(previous, event, width):
    raw=json.dumps(event,sort_keys=True,separators=(',',':')).encode()
    digest=int.from_bytes(hashlib.sha256(previous.to_bytes(32,'big')+raw).digest(),'big')
    return digest & ((1<<width)-1) if width else 0, len(raw)+32


def make_transcript(n,edges,tape,width,persistent):
    R=reduce_two_trees(n,edges); sols=brute_solutions(n,edges)
    history=[]; digest=0; pins={}; bytes_hashed=0; calls=scans=0
    for stage,r in enumerate(tape):
        # The challenge block is already supplied at this stage. No future access.
        vertex=(r+digest)%n; color=(r+stage)%3
        if not persistent: pins={}
        pins[vertex]=color
        w,q,s=prefix_select(sols,n,pins); calls+=q;scans+=s
        event={'stage':stage,'sample':r,'pins':sorted(pins.items()),
               'source_witness':list(w) if w is not None else None,
               'status':'SAT' if w is not None else 'NO_EXTENSION'}
        if w is not None:
            event['target_witness']=list(lift(R,w))
        digest,b=hash_event(digest,event,width); bytes_hashed+=b
        history.append({'event':event,'digest':digest})
        if w is None:break
    return history,{'queries':calls,'oracle_rows_scanned':scans,'hash_input_bytes':bytes_hashed,
                    'record_bytes':len(json.dumps(history,separators=(',',':')).encode())}


def batch_hash(A):
    fixtures=[(3,[(0,1),(0,2),(1,2)]),(4,[(0,1),(1,2),(2,3)]),
              (4,list(it.combinations(range(4),2)))]
    counts=Counter(); rows=[]
    for fi,(n,edges) in enumerate(fixtures):
        for width in (0,2,256):
            for persistent in (False,True):
                for tape in it.product(range(4),repeat=3):
                    h,m=make_transcript(n,edges,tape,width,persistent)
                    replay,_=make_transcript(n,edges,tape,width,persistent)
                    A.check(h==replay,'exact_replay_given_sample_tape')
                    R=decode_pair(encode_pair(reduce_two_trees(n,edges)))
                    for row in h:
                        e=row['event']; counts['events']+=1
                        if e['status']=='SAT':
                            A.check(is_coloring(e['source_witness'],edges),'live_source_witness')
                            A.check(valid_target(R,e['target_witness']),'live_target_witness')
                            counts['witnesses']+=1
                        else:
                            pins=dict(e['pins']);sols=brute_solutions(n,edges)
                            A.check(not any(all(w[v]==c for v,c in pins.items()) for w in sols),'no_extension_is_local_not_source_unsat')
                            counts['no_extension']+=1
                    # Exact comparison catches sample alteration even for a constant digest.
                    tampered=json.loads(json.dumps(h));tampered[0]['event']['sample']^=1
                    A.check(tampered!=replay,'full_record_detects_tamper')
                    counts['runs']+=1
                    for k,v in m.items():counts[k]+=v
                    if tape==(0,0,0):rows.append({'fixture':fi,'hash_bits':width,'persistent':persistent,'history':h,'ledger':m})
    # Every one-color challenge is statically satisfiable; no committed color wins all.
    A.check(all(any(c==r for c in COLORS) for r in COLORS),'color_offline_total')
    A.check(not any(all(c==r for r in COLORS) for c in COLORS),'color_commitment_impossible')
    A.check(all(sum(c==r for r in COLORS)==1 for c in COLORS),'color_precommit_success_one_third')
    return {'counts':dict(counts),'sample_transcripts':rows,
            'hash_scope':'Includes an identically zero digest. Exact sample record remains authoritative; no cryptographic assumption.'}


def batch_cnf(A):
    xor=[tuple((i+1)*(1 if b[i] else -1) for i in range(3)) for b in it.product((0,1),repeat=3) if sum(b)%2]
    cases={'Horn':(3,[(-1,-2,3),(-3,)]),'dual_Horn':(3,[(1,2,-3),(3,)]),
           '2SAT':(3,[(1,2),(-1,3),(-2,-3)]),'affine':(3,xor),
           'treewidth_path':(4,[(1,2),(-2,3),(-3,4)]),
           'independent_product':(4,[(1,2),(3,4)]),'padding':(4,[(1,2)]),
           'contradiction':(1,[(1,),(-1,)])}
    rows=[]
    for name,(n,F) in cases.items():
        good=[w for w in it.product((0,1),repeat=n) if all(any(bool(w[abs(l)-1])==(l>0) for l in c) for c in F)]
        # A separate binary prefix construction, rather than the ternary helper.
        for j in range(n+1):
            for p in it.product((0,1),repeat=j):
                candidates=[w for w in good if w[:j]==p]
                s=p
                if candidates:
                    while len(s)<n:
                        s+= (0,) if any(w[:len(s)+1]==s+(0,) for w in candidates) else (1,)
                    A.check(s==min(candidates),'binary_prefix_reconstruction')
                else:A.check(not any(w[:j]==p for w in good),'binary_empty_prefix')
        rows.append({'case':name,'models':len(good)})
    return {'cases':rows}


def main():
    p=argparse.ArgumentParser();p.add_argument('--batch',choices=('quantifiers','trees','hash','cnf'),required=True)
    p.add_argument('--out',type=Path,required=True);args=p.parse_args(); A=Audit()
    body=globals()['batch_'+args.batch](A)
    out={'run_id':'LIVEPREFIX1','status':'COMPUTATIONAL','batch':args.batch,'seed':None,
         'assertions':sum(A.counts.values()),'failures':0,'checks':dict(A.counts),
         'elapsed_seconds':time.monotonic()-A.start,'results':body,
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'limitations':['No polynomial-time SAT solver implemented.',
                        'No asymptotic lower bound follows from finite cases.',
                        'Hash is an index; full supplied samples and records are checked.',
                        'No time/space count is inferred from semantic state cardinality.']}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ('batch','assertions','elapsed_seconds','failures')}))

if __name__=='__main__':main()

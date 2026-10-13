#!/usr/bin/env python3
"""PINCORE1: exact canonical decoding, arbitrary-pin compression and same-language queries.
Python 3.10+, standard library; keep the unchanged two_tree_bridge_audit.py beside this file.
New mathematical claims remain CANDIDATE pending independent review.
Each audit batch has a 25-second cooperative limit; no production algorithm has a size cap.
Examples: --batch local, --batch decode --n 5, --batch exhaustive --n 2,
--batch sampled --n 4, --batch closure. Every invocation also requires --out FILE.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import time
import two_tree_bridge_audit as old

SEED = 202610140750
EXPECTED_DEPENDENCY = '70d2e28d14ed371ce4d0783ba629ace92b95a6a1aabdee39b7841530f9bf3554'
COLORS = (0, 1, 2)

def require_dependency() -> None:
    if hashlib.sha256(Path(old.__file__).read_bytes()).hexdigest() != EXPECTED_DEPENDENCY:
        raise RuntimeError('dependency revision mismatch')

def union_edges(record: dict) -> list[tuple[int, int]]:
    return sorted({e for t in record['trees'] for e in t['edges']})

def validate_pins(h: int, pins: dict[int, int]) -> None:
    if type(pins) is not dict or any(type(v) is not int or type(c) is not int or
            not 0 <= v < h or c not in COLORS for v, c in pins.items()):
        raise ValueError('invalid partial coloring')

def recover(bits: str) -> tuple[int, list[tuple[int, int]], dict] | None:
    """Strict canonical image recognition. None is NOT a decision of full TWO-TREE.
    Malformed pair records raise ValueError. Recompilation checks every original bit.
    No source graph, occurrence tags, original witness or field advice is supplied.
    """
    pair = old.decode_pair(bits)
    shared = set(pair['trees'][0]['vertices']) & set(pair['trees'][1]['vertices'])
    if not shared:
        return None
    forests = []
    for tree in pair['trees']:
        vertices = set(tree['vertices']); private = vertices - shared
        adj = {v: set() for v in vertices}
        for u, v in tree['edges']:
            adj[u].add(v); adj[v].add(u)
        hubs = [v for v in private if not (adj[v] & shared)]
        if len(hubs) != 1:
            return None
        hub = hubs[0]
        if adj[hub] != private - {hub}:
            return None
        for p in private - {hub}:
            if len(adj[p]) != 2 or hub not in adj[p] or len(adj[p] & shared) != 1:
                return None
        forests.append([e for e in tree['edges'] if set(e) <= shared])
    red, blue = forests
    adj = {v: set() for v in shared}
    for u, v in red:
        adj[u].add(v); adj[v].add(u)
    if any(len(a) > 2 for a in adj.values()):
        return None
    paths = []
    for block in old.components(shared, red):
        ends = [v for v in block if len(adj[v]) <= 1]
        if not ends:
            return None
        path = [min(ends)]; prev = None
        while True:
            nxt = adj[path[-1]] - ({prev} if prev is not None else set())
            if not nxt:
                break
            if len(nxt) != 1:
                return None
            prev, v = path[-1], next(iter(nxt)); path.append(v)
        if len(path) != len(block) or len(path) % 3 != 1:
            return None
        paths.append(path)
    paths.sort(key=lambda p: p[0])
    owners = {}; expected_blue = set()
    for source, path in enumerate(paths):
        for v in path[::3]:
            owners[v] = source
        for j in range(0, len(path)-1, 3):
            x, a, b, y = path[j:j+4]
            expected_blue.update((tuple(sorted((x, b))), tuple(sorted((a, y)))))
    blue = set(blue)
    if not expected_blue <= blue:
        return None
    source_edges = set(); used = set()
    for u, v in blue - expected_blue:
        if u not in owners or v not in owners or u in used or v in used or owners[u] == owners[v]:
            return None
        edge = tuple(sorted((owners[u], owners[v])))
        if edge in source_edges:
            return None
        source_edges.add(edge); used.update((u, v))
    n = len(paths); edges = sorted(source_edges)
    rebuilt = old.reduce_two_trees(n, edges)
    if old.encode_pair(rebuilt) != bits:
        return None
    return n, edges, rebuilt

def diamond_options(c: int, a: int | None, b: int | None) -> list[tuple[int, int]]:
    return [(x, y) for x in COLORS for y in COLORS
            if x != y and x != c and y != c and (a is None or x == a) and (b is None or y == b)]

def compress(record: dict, pins: dict[int, int]) -> tuple[list[int], list[int]]:
    """Requires the exact reconstructed compiler image; compress ALL vertex pins."""
    validate_pins(record['universe'], pins)
    lists = [7] * len(record['occurrences'])
    owner = {x: v for v, block in enumerate(record['occurrences']) for x in block}
    for x, v in owner.items():
        if x in pins:
            lists[v] &= 1 << pins[x]
    for x, y, a, b in record['diamonds']:
        possible = sum(1 << c for c in COLORS if diamond_options(c, pins.get(a), pins.get(b)))
        lists[owner[x]] &= possible
    hub_masks = []
    for tree in record['trees']:
        hub = tree['hub']; mask = (1 << pins[hub]) if hub in pins else 7
        for endpoint, mid, _ in tree['joins']:
            if endpoint not in owner:
                raise AssertionError('canonical hub representative is not an occurrence')
            if mid in pins:
                forbidden = 1 << pins[mid]
                lists[owner[endpoint]] &= 7 ^ forbidden
                mask &= 7 ^ forbidden
        hub_masks.append(mask)
    return lists, hub_masks

def core_models(n: int, edges: list[tuple[int, int]], lists: list[int]):
    """Exhaustive reference solver, NOT claimed polynomial."""
    return [c for c in it.product(COLORS, repeat=n)
            if all(lists[v] & (1 << c[v]) for v in range(n)) and old.coloring(c, edges)]

def lift(record: dict, pins: dict[int, int], source: tuple[int, ...], hubs: list[int]) -> dict[int, int]:
    out = {}
    for c, block in zip(source, record['occurrences']):
        for x in block:
            out[x] = c
    for x, y, a, b in record['diamonds']:
        choices = diamond_options(out[x], pins.get(a), pins.get(b))
        if not choices:
            raise ValueError('source is incompatible with gadget pins')
        out[a], out[b] = choices[0]
    for tree, mask in zip(record['trees'], hubs):
        if not mask:
            raise ValueError('empty hub domain')
        out[tree['hub']] = next(c for c in COLORS if mask & (1 << c))
        for endpoint, mid, hub in tree['joins']:
            out[mid] = pins[mid] if mid in pins else next(c for c in COLORS if c not in (out[endpoint], out[hub]))
    if not old.valid_target(record, out) or any(out[v] != c for v, c in pins.items()):
        raise AssertionError('full original target or pins failed')
    return out

def pin_query(bits: str, pins: dict[int, int]) -> str:
    """For EVERY valid two-tree input, output another instance of the SAME language.
    Palette vertices encode fixed labels only up to a single global color permutation.
    """
    pair = old.decode_pair(bits); h = pair['universe']; validate_pins(h, pins)
    edges = set(union_edges(pair)); palette = [h, h+1, h+2]
    edges.update(it.combinations(palette, 2))
    for v, c in pins.items():
        edges.update((v, palette[d]) for d in COLORS if d != c)
    reduced = old.reduce_two_trees(h+3, sorted(edges))
    result = old.encode_pair(reduced)
    if reduced['universe'] > 31*h+6 or len(result) > 1369*len(bits):
        raise AssertionError('proved same-language encoded-size bound failed')
    return result

def pinned_search(h: int, edges: list[tuple[int, int]], pins: dict[int, int], cap: int = 1000000):
    """Independent DSATUR test oracle, does not access decoder/gadgets/core lists.
    A node cap is an explicit TEST failure, never an UNSAT result.
    """
    old.graph_ok(h, edges); validate_pins(h, pins)
    adj = [set() for _ in range(h)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    colors = [pins.get(v, -1) for v in range(h)]; nodes = 0
    if any(colors[u] == colors[v] >= 0 for u, v in edges):
        return None, nodes
    def visit(left):
        nonlocal nodes
        nodes += 1
        if nodes > cap:
            raise RuntimeError('independent test oracle reached node cap')
        if not left:
            return tuple(colors)
        v = max(left, key=lambda x: (len({colors[u] for u in adj[x] if colors[u] >= 0}), len(adj[x]), -x))
        used = {colors[u] for u in adj[v]}
        for c in COLORS:
            if c not in used:
                colors[v] = c
                ans = visit(left-{v})
                if ans is not None:
                    return ans
        colors[v] = -1
        return None
    return visit({v for v in range(h) if colors[v] < 0}), nodes

class Audit:
    def __init__(self):
        self.start = time.monotonic(); self.counts = Counter()
    def check(self, value: bool, label: str):
        self.counts[label] += 1
        if not value:
            raise AssertionError(label)
        if time.monotonic()-self.start > 25:
            raise TimeoutError('audit exceeded 25 seconds; split batch')

def local_batch(a: Audit):
    for values in it.product((-1, 0, 1, 2), repeat=4):
        pins = {v: c for v, c in enumerate(values) if c >= 0}
        # Local vertex order x,y,a,b, and five edges of a diamond.
        models = [w for w in it.product(COLORS, repeat=4)
                  if all(w[v] == c for v, c in pins.items()) and
                  all(w[u] != w[v] for u, v in [(0,2),(0,3),(2,3),(1,2),(1,3)])]
        for c in COLORS:
            predicted = (pins.get(0,c) == c == pins.get(1,c)) and bool(diamond_options(c,pins.get(2),pins.get(3)))
            a.check(predicted == any(w[0] == c for w in models), 'all_diamond_pins_exact')
    for values in it.product((-1,0,1,2), repeat=3):
        pins = {v:c for v,c in enumerate(values) if c >= 0}
        for c,d in it.product(COLORS,repeat=2):
            expected = any(c != p and p != d and all((c,p,d)[v] == z for v,z in pins.items()) for p in COLORS)
            predicted = (pins.get(0,c)==c and pins.get(2,d)==d and (1 not in pins or (pins[1]!=c and pins[1]!=d)))
            a.check(predicted == expected, 'all_connector_pins_exact')
    badpins = [{True:0},{0:True},{0:3},{-1:0},{99:0},[]]
    r = old.reduce_two_trees(1,[])
    for p in badpins:
        try:
            compress(r,p)
        except ValueError:
            a.check(True,'malformed_pins_reject')
        else:
            a.check(False,'malformed_pins_reject')
    return {'diamond_pin_patterns':256,'connector_pin_patterns':64,'bad_pin_records':6}

def decode_batch(a: Audit, n: int):
    pairs = list(it.combinations(range(n),2)); rows=[]
    for mask in range(1 << len(pairs)):
        es = [e for j,e in enumerate(pairs) if (mask >> j)&1]
        r = old.reduce_two_trees(n,es); bits=old.encode_pair(r); back=recover(bits)
        a.check(back is not None and back[0] == n and back[1] == es, 'recover_source_no_metadata')
        a.check(old.encode_pair(back[2]) == bits, 'exact_bit_recompilation')
        rows.append({'mask':mask,'source_vertices':n,'target_vertices':r['universe'],'bits':len(bits)})
    # A valid noncanonical NO instance: edge-disjoint paths whose union is K4.
    noncanonical={'universe':4,'trees':[{'vertices':list(range(4)),'edges':[(0,1),(1,2),(2,3)]},
                                       {'vertices':list(range(4)),'edges':[(0,2),(0,3),(1,3)]}]}
    a.check(recover(old.encode_pair(noncanonical)) is None, 'noncanonical_not_decided_by_image_recognizer')
    return {'graphs':len(rows),'rows':rows}

def exhaustive_batch(a: Audit, n: int):
    if n not in (1,2):
        raise ValueError('exhaustive target pins use source n=1 or edge n=2')
    es=[] if n==1 else [(0,1)]; r=old.reduce_two_trees(n,es); h=r['universe']; edge=union_edges(r)
    # Independent original-target full coloring enumeration.
    models=[w for w in it.product(COLORS,repeat=h) if old.coloring(w,edge)]
    queries=positive=lifts=0; sample=[]
    for values in it.product((-1,0,1,2),repeat=h):
        pins={v:c for v,c in enumerate(values) if c>=0}
        lists,hubs=compress(r,pins)
        eligible=core_models(n,es,lists) if all(hubs) else []
        targets=[w for w in models if all(w[v] == c for v,c in pins.items())]
        projected={old.project_source(r,dict(enumerate(w))) for w in targets}
        a.check(set(eligible)==projected,'every_target_pin_projection_exact')
        if eligible:
            w=lift(r,pins,eligible[0],hubs); lifts+=1
            a.check(tuple(w[v] for v in range(h)) in targets,'full_pinned_target_lift')
        queries+=1;positive+=bool(eligible)
        if len(sample)<20 and (not eligible or pins):
            sample.append({'pins':pins,'lists':lists,'hubs':hubs,'source_models':eligible})
    return {'source_vertices':n,'target_vertices':h,'target_models':len(models),'pin_patterns':queries,
            'positive_patterns':positive,'lifts':lifts,'sample':sample}

def sampled_batch(a: Audit, n: int, start: int, count: int):
    rng=random.Random(SEED+n+start); pairs=list(it.combinations(range(n),2)); stop=min(1<<len(pairs),start+count)
    rows=[]
    for mask in range(start,stop):
        es=[e for j,e in enumerate(pairs) if (mask>>j)&1]; r=old.reduce_two_trees(n,es); h=r['universe']; edges=union_edges(r)
        back=recover(old.encode_pair(r)); a.check(back is not None,'sampled_source_recovery')
        patterns=[{}]
        # Positive source-independent target witness, plus varied random restrictions.
        full,nodes=pinned_search(h,edges,{})
        if full is not None:
            for p in (.1,.4,.8,1.):
                patterns.append({v:full[v] for v in range(h) if rng.random()<p})
        for _ in range(12):
            patterns.append({v:rng.randrange(3) for v in range(h) if rng.random()<.25})
        results=[]
        for pins in patterns:
            lists,hubs=compress(r,pins); cs=core_models(n,es,lists) if all(hubs) else []
            witness,cost=pinned_search(h,edges,pins)
            a.check(bool(cs)==(witness is not None),'independent_pinned_target_decision')
            if cs:
                got=lift(r,pins,cs[0],hubs)
                a.check(old.valid_target(r,got),'sampled_full_witness_lift')
                a.check(old.project_source(r,dict(enumerate(witness))) in cs,'noncanonical_witness_projection')
            results.append({'pins':pins,'lists':lists,'hub_masks':hubs,'answer':bool(cs),'oracle_nodes':cost})
        rows.append({'mask':mask,'target_vertices':h,'queries':results})
    return {'source_vertices':n,'graphs':len(rows),'rows':rows,'seed':SEED+n+start}

def closure_batch(a: Audit):
    rng=random.Random(SEED); rows=[]
    examples=[]
    # Include all ordered pairs of trees on three labels and the noncanonical K4 pair.
    for h in (1,2,3):
        possible=list(it.combinations(range(h),2))
        trees=[list(es) for es in it.combinations(possible,h-1) if old.tree_ok(list(range(h)),list(es))]
        for e1,e2 in it.product(trees,repeat=2):
            examples.append({'universe':h,'trees':[{'vertices':list(range(h)),'edges':e1},{'vertices':list(range(h)),'edges':e2}]})
    examples.append({'universe':4,'trees':[{'vertices':list(range(4)),'edges':[(0,1),(1,2),(2,3)]},
                                          {'vertices':list(range(4)),'edges':[(0,2),(0,3),(1,3)]}]})
    for i,r in enumerate(examples):
        bits=old.encode_pair(r); h=r['universe']; edges=union_edges(r)
        patterns=list(it.product((-1,0,1,2),repeat=h)) if h<=3 else [tuple(-1 if rng.random()<.5 else rng.randrange(3) for _ in range(h)) for _ in range(24)]
        for vals in patterns:
            pins={v:c for v,c in enumerate(vals) if c>=0}; original,cost=pinned_search(h,edges,pins)
            query=pin_query(bits,pins); decoded=recover(query)
            a.check(decoded is not None,'same_language_query_valid_canonical')
            g,ges,_=decoded; projected,_=pinned_search(g,ges,{})
            a.check((original is not None)==(projected is not None),'same_language_reduction_equivalence')
            a.check(len(query)<=1369*len(bits),'constant_factor_encoded_query_bound')
            if projected is not None:
                palette=projected[h:h+3]; inv={c:j for j,c in enumerate(palette)}
                source=tuple(inv[projected[v]] for v in range(h))
                a.check(old.coloring(source,edges) and all(source[v]==c for v,c in pins.items()),'palette_orientation_witness_map')
            rows.append({'input':i,'h':h,'pins':pins,'query_vertices':old.decode_pair(query)['universe'],'input_bits':len(bits),'query_bits':len(query),'answer':original is not None})
        # Search using ONLY decisions on query strings; decider here is exact exponential, not claimed P.
        def decider(query):
            back=recover(query)
            if back is not None:
                return pinned_search(back[0],back[1],{})[0] is not None
            rec=old.decode_pair(query)
            return pinned_search(rec['universe'],union_edges(rec),{})[0] is not None
        pins={}; calls=1
        yes=decider(bits)
        if yes:
            for v in range(h):
                for c in COLORS:
                    calls+=1
                    if decider(pin_query(bits,pins|{v:c})):
                        pins[v]=c; break
                else:
                    raise AssertionError('correct decider lost an extending color')
            a.check(old.coloring(tuple(pins[v] for v in range(h)),edges),'decision_only_witness_search')
        a.check(calls<=1+3*h,'decision_query_count')
    return {'inputs':len(examples),'queries':len(rows),'rows':rows}

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batch',choices=['local','decode','exhaustive','sampled','closure'],required=True)
    p.add_argument('--n',type=int,default=3); p.add_argument('--start',type=int,default=0)
    p.add_argument('--count',type=int,default=256);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();require_dependency();audit=Audit()
    result={'run_id':'PINCORE1','status':'COMPUTATIONAL','batch':args.batch,'parameters':vars(args)|{'out':str(args.out)},
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dependency_sha256':EXPECTED_DEPENDENCY,
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'failures':0}
    try:
        if args.batch=='local':result['data']=local_batch(audit)
        elif args.batch=='decode':result['data']=decode_batch(audit,args.n)
        elif args.batch=='exhaustive':result['data']=exhaustive_batch(audit,args.n)
        elif args.batch=='sampled':result['data']=sampled_batch(audit,args.n,args.start,args.count)
        else:result['data']=closure_batch(audit)
    except Exception as exc:
        result['failures']=1;result['error']=repr(exc);raise
    finally:
        result.update(counts=dict(audit.counts),assertions=sum(audit.counts.values()),elapsed_seconds=time.monotonic()-audit.start)
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('batch','assertions','failures','elapsed_seconds')}))

if __name__=='__main__':
    main()

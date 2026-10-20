"""ARC-CHILD-WIDTH-AUDIT25: does the pinned-child builder of ARC-INTERFACE-PROJECTION8
increase live width?  Deterministic (seeded), stdlib only, well under 30 s.
Events: ('O',v) ('C',(l1,l2,l3)) ('X',v).  Child = block with boundary variables
pinned, 1/2-literal clauses padded by locally scoped fresh gadget variables,
re-scoped to first/last occurrence and renumbered."""
import random
from itertools import product

def width(E):
    live, w = set(), 0
    for t, x in E:
        if t == 'O': live.add(x); w = max(w, len(live))
        elif t == 'X': live.discard(x)
    return w

def sat_clauses(cl):
    names = sorted({abs(l) for c in cl for l in c})
    for bits in product((False, True), repeat=len(names)):
        a = dict(zip(names, bits))
        if all(any(a[abs(l)] == (l > 0) for l in c) for c in cl):
            return True
    return False

def clauses_of(E): return [x for t, x in E if t == 'C']

def valid(E):
    live = set()
    for t, x in E:
        if t == 'O': assert x not in live; live.add(x)
        elif t == 'X': live.remove(x)
        else: assert len({abs(l) for l in x}) == 3 and all(abs(l) in live for l in x)
    assert not live

def blocks(E, chunk):
    """yield (events, S_in, S_out)"""
    live = set(); out = []
    for lo in range(0, len(E), chunk):
        B = E[lo:lo+chunk]; sin = frozenset(live)
        for t, x in B:
            if t == 'O': live.add(x)
            elif t == 'X': live.remove(x)
        out.append((B, sin, frozenset(live)))
    return out

def child(B, pins):
    """pinned child as a valid scoped proper-3CNF stream, or None if the child is trivially UNSAT"""
    cls = []
    for t, c in B:
        if t != 'C': continue
        r, sat = [], False
        for l in c:
            if abs(l) in pins:
                if pins[abs(l)] == (l > 0): sat = True
            else: r.append(l)
        if sat: continue
        if not r: return None
        cls.append(r)
    first, last = {}, {}
    for i, c in enumerate(cls):
        for l in c:
            first.setdefault(abs(l), i); last[abs(l)] = i
    ren, nxt, E = {}, [1], []
    def new():
        v = nxt[0]; nxt[0] += 1; return v
    for i, c in enumerate(cls):
        for l in c:
            v = abs(l)
            if first[v] == i and v not in ren:
                ren[v] = new(); E.append(('O', ren[v]))
        aux = []
        for _ in range(3 - len(c)):
            z = new(); aux.append(z); E.append(('O', z))
        base = [(ren[abs(l)] if l > 0 else -ren[abs(l)]) for l in c]
        if not aux: E.append(('C', tuple(base)))
        else:
            for signs in product((1, -1), repeat=len(aux)):
                E.append(('C', tuple(base + [s*z for s, z in zip(signs, aux)])))
        for z in aux: E.append(('X', z))
        for l in c:
            if last[abs(l)] == i: E.append(('X', ren[abs(l)]))
    return E

def join_sat(E, chunk, stats, depth):
    """exact join; records width of every emitted child; recurses `depth` more levels on children"""
    reach = {()}
    bl = blocks(E, chunk)
    for B, sin, sout in bl:
        sin_l, sout_l = sorted(sin), sorted(sout)
        nxt = set()
        for ab in reach:
            aa = dict(zip(sin_l, ab))
            fresh = [v for v in sout_l if v not in aa]
            for bb in product((False, True), repeat=len(fresh)):
                pins = dict(aa); pins.update(zip(fresh, bb))
                # block-internal variables closed in block / opened in block are pinned iff boundary
                ch = child(B, pins)
                if ch is None: continue
                valid(ch)
                pw = width(B_as_stream(B, sin))
                stats.append((depth, width(ch), pw))
                if depth > 0:
                    ok = join_sat(ch, max(2, len(ch)//2), stats, depth-1)
                else:
                    ok = sat_clauses(clauses_of(ch))
                if ok: nxt.add(tuple(pins[v] for v in sout_l))
        reach = nxt
    return () in reach

def B_as_stream(B, sin):
    """block as a stream: incoming live vars treated as opened at the start (parent width inside the block)"""
    return [('O', v) for v in sorted(sin)] + list(B)

def rand_stream(rng, w, nclauses):
    E, live, nv, cnt = [], [], 0, 0
    while cnt < nclauses or live:
        r = rng.random()
        if cnt < nclauses and len(live) >= 3 and r < .5:
            vs = rng.sample(live, 3)
            E.append(('C', tuple(v if rng.random() < .5 else -v for v in vs))); cnt += 1
        elif cnt < nclauses and len(live) < w and (r < .8 or len(live) < 3):
            nv += 1; live.append(nv); E.append(('O', nv))
        elif live and (cnt >= nclauses or len(live) >= w or r > .9):
            v = rng.choice(live); live.remove(v); E.append(('X', v))
    return E

def cyclic(w, blocks_):
    E = [('O', i) for i in range(1, w+1)]
    for _ in range(blocks_):
        for i in range(w):
            a, b, c = i+1, (i+1) % w+1, (i+2) % w+1
            E.append(('C', (a, b, c)))
    return E + [('X', i) for i in range(1, w+1)]

def main():
    rng = random.Random(25); checks = 0; worst = -99; stats = []
    streams = []
    for _ in range(60):
        w = rng.randint(3, 5); streams.append(rand_stream(rng, w, rng.randint(4, 9)))
    for w in (3, 4, 5): streams.append(cyclic(w, 2))
    for E in streams:
        valid(E)
        chunk = max(3, len(E)//rng.randint(2, 4))
        st = []
        got = join_sat(E, chunk, st, 1)
        assert got == sat_clauses(clauses_of(E)); checks += 1
        stats += st
    # width(child) - width(parent block incl. incoming live set)
    for d, wc, wp in stats:
        worst = max(worst, wc - wp); checks += 1
        assert wc <= wp, (d, wc, wp)
    print({'streams': len(streams), 'child_records': len(stats), 'checks': checks,
           'max_child_minus_parent_block_width': worst, 'failures': 0})

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""LSPV-5/527 red team: polynomial-size native /386 refutations of odd cubic Tseitin
sources via nested AND2 gates (XOR-chain extension), i.e. Extended-Resolution power.

Usage: python3 lspv5_527_native386_xor_chain_er_compiler.py OUT_DIR [CHECKER386_JS]
Each case is a separate small graph; every packet is written to OUT_DIR and, when a
checker path is given, replayed by the UNCHANGED /386 checker as an OS Node subprocess.
Chunking: each graph is an independent job of well under 30 s.

Construction (Gaussian elimination by cut chains):
  * resolve every guarded source clause with the guard unit (guard-free vertex clauses);
  * process vertices v_1..v_V; after j vertices, the summed equation is
    XOR(cut edges C_j) = Q_j, stored as a unit on the final literal of the sorted
    XOR chain over C_j.  xor(a,b) = NOT g, g = AND(NOT u, NOT w), u = AND(a, NOT b),
    w = AND(NOT a, b): three paid gates, memoised so equal prefixes share gates;
  * along edge positions x, the invariant B_x XOR A_x XOR D_x = 0 (new prefix, old
    prefix, new vertex's incident edges <= x) is derived from the previous invariant
    and DEF views by a LOCAL tree-resolution derivation on O(1) variables;
  * at the end the cut is empty and Q_V = 1: the empty clause.
Every RES is strict, every DEF view is a true gate view, and each gate is paid once.
"""
import json, os, sys, subprocess, hashlib, itertools, random

def key(c):
    return sorted(set(c), key=lambda x: (abs(x), x))

class Proof:
    def __init__(self, h, edges, charge):
        self.h, self.edges, self.charge = h, edges, charge
        self.E = len(edges); self.guard = self.E + 1; self.nextvar = self.E + 2
        self.records, self.gate_defs, self.gmemo, self.defmemo = [], [], {}, {}
        self.occ = [[] for _ in range(h)]
        for i, (u, v) in enumerate(edges):
            self.occ[u].append(i + 1); self.occ[v].append(i + 1)

    def add(self, rec):
        rec['c'] = key(rec['c']); self.records.append(rec); return len(self.records) - 1

    def gate(self, a, b):
        k = (a, b)
        if k not in self.gmemo:
            z = self.nextvar; self.nextvar += 1
            self.gate_defs.append([len(self.gate_defs), z, a, b]); self.gmemo[k] = z
        return self.gmemo[k]

    def defview(self, z, c):
        k = tuple(key(c))
        if k not in self.defmemo:
            gid = next(g[0] for g in self.gate_defs if g[1] == z)
            self.defmemo[k] = self.add({'kind': 'DEF', 'gate': gid, 'c': list(k), 'parents': []})
        return self.defmemo[k]

    def views(self, z):
        g = next(g for g in self.gate_defs if g[1] == z); a, b = g[2], g[3]
        out = []
        for c in ([-z, a], [-z, b], [z, -a, -b]):
            kc = key(c)
            if not any(-x in kc for x in kc): out.append(self.defview(z, kc))
        return out

    def xor(self, a, b):
        """a is a value (None = constant 0, else literal); b an edge literal."""
        if a is None: return b, []
        u = self.gate(a, -b); w = self.gate(-a, b); g = self.gate(-u, -w)
        return -g, [u, w, g]

    def derive(self, prem, target):
        """Tree-resolution derivation of a subclause of target from premise ids."""
        cls = {i: self.records[i]['c'] for i in prem}
        alpha = {abs(l): (l < 0) for l in target}  # falsify target: var -> bool value
        def val(l, a):
            v = a.get(abs(l)); return None if v is None else (v if l > 0 else not v)
        def rec(a):
            unit = None
            for i, c in cls.items():
                vals = [val(l, a) for l in c]
                if all(x is False for x in vals): return i
                if any(x is True for x in vals): continue
                un = [l for l, x in zip(c, vals) if x is None]
                if len(un) == 1 and unit is None: unit = un[0]
            if unit is None:
                free = sorted({abs(l) for c in cls.values() for l in c if abs(l) not in a})
                if not free: raise RuntimeError('premises do not imply target')
                unit = free[0]
            x = abs(unit)
            first = unit > 0
            res = {}
            for bval in (first, not first):
                b2 = dict(a); b2[x] = bval; res[bval] = rec(b2)
                cb = self.records[res[bval]]['c']
                if (-x if bval else x) not in cb: return res[bval]
            c1, c0 = res[True], res[False]  # c1 contains -x, c0 contains x
            A, B = self.records[c0]['c'], self.records[c1]['c']
            r = key([l for l in A if l != x] + [l for l in B if l != -x])
            return self.add({'kind': 'RES', 'c': r, 'parents': [c0, c1], 'pivot': x})
        return rec(alpha)

    def eq_clauses(self, lits, rhs):
        """Clauses for XOR(lits) = rhs, lits literal list (constants removed)."""
        vs, r = {}, rhs
        for l in lits:
            if l < 0: r ^= 1
            vs[abs(l)] = vs.get(abs(l), 0) ^ 1
        vs = sorted(v for v, m in vs.items() if m)
        if not vs: return None if r == 0 else [[]]
        out = []
        for bits in itertools.product([0, 1], repeat=len(vs)):
            if sum(bits) % 2 != r: out.append(key([-v if b else v for v, b in zip(vs, bits)]))
        return out

    def build(self, order):
        E, guard = self.E, self.guard
        src = {}
        for v in range(self.h):
            for x in range(8):
                bits = [x & 1, (x >> 1) & 1, (x >> 2) & 1]
                if sum(bits) % 2 != self.charge[v]:
                    c = [-e if b else e for e, b in zip(self.occ[v], bits)]
                    src.setdefault(v, []).append(self.add({'kind': 'SOURCE', 'source': v, 'c': c + [-guard], 'parents': []}))
        gu = self.add({'kind': 'SOURCE', 'source': -1, 'c': [guard], 'parents': []})
        vcl = {v: [self.add({'kind': 'RES', 'c': [l for l in self.records[i]['c'] if l != -guard], 'parents': [gu, i], 'pivot': guard}) for i in ids] for v, ids in src.items()}
        cut, Q, chain_end, unit_ids = set(), 0, None, []
        def chain(cs):
            vals, a = [None], None
            for e in sorted(cs):
                a, _ = self.xor(a, e); vals.append(a)
            return vals
        for v in order:
            inc = set(self.occ[v]); new = cut ^ inc
            old_sorted, new_sorted = sorted(cut), sorted(new)
            # prefix values at each position x (0..E)
            A = {0: None}; B = {0: None}; a = b = None
            for x in range(1, E + 1):
                if x in cut: a, _ = self.xor(a, x)
                if x in new: b, _ = self.xor(b, x)
                A[x], B[x] = a, b
            inv = []  # ids of current invariant clauses
            for x in range(1, E + 1):
                D = [e for e in inc if e <= x]
                lits = [l for l in (A[x], B[x]) if l is not None] + D
                tgt = self.eq_clauses(lits, 0)
                if tgt is None: inv = []; continue
                prem = list(inv)
                for val in (A[x], B[x]):
                    if val is not None and val < 0 and (x in cut or x in new):
                        # gates feeding this xor step
                        g = -val; gd = next(t for t in self.gate_defs if t[1] == g)
                        for z in (g, abs(gd[2]), abs(gd[3])): prem += self.views(z)
                if not prem and all(len(c) for c in tgt):
                    # first nonempty invariant is a tautological identity only if lits cancel
                    pass
                inv = [self.derive(prem, t) for t in tgt]
            # combine: invariant (A_E xor B_E xor D=0), old unit (A_E = Q), vertex clauses
            newQ = Q ^ self.charge[v]
            prem = inv + unit_ids + vcl[v]
            tgt = self.eq_clauses([B[E]] if B[E] is not None else [], newQ)
            if tgt == [[]]:
                last = self.derive(prem, [])
                cut = new; break
            unit_ids = [self.derive(prem, t) for t in tgt]
            cut, Q = new, newQ
        assert self.records[-1]['c'] == [] or self.records[last]['c'] == []
        # truncate after the empty clause
        self.records = self.records[:last + 1]
        used_g = len(self.gate_defs)
        nres = sum(r['kind'] == 'RES' for r in self.records)
        return {'spec': {'h': self.h, 'edges': [list(e) for e in self.edges], 'charge': self.charge, 'guard': guard},
                'gate_defs': self.gate_defs, 'records': self.records,
                'summary': {'source': sum(r['kind'] == 'SOURCE' for r in self.records),
                            'def_views': sum(r['kind'] == 'DEF' for r in self.records),
                            'resolution': nres, 'paid_gates': used_g, 'paid_total': nres + used_g,
                            'live_records': len(self.records)}}

def cubic_graphs():
    K4 = (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    K33 = (6, [(a, b) for a in range(3) for b in range(3, 6)])
    cube = (8, sorted({tuple(sorted((i, i ^ (1 << d)))) for i in range(8) for d in range(3)}))
    out = [('K4', *K4), ('K33', *K33), ('CUBE', *cube)]
    for n in (10, 12, 16, 20, 24, 32, 40):
        rng = random.Random(527 + n)
        while True:  # configuration model, simple + connected
            pts = [v for v in range(n) for _ in range(3)]; rng.shuffle(pts)
            es = [tuple(sorted(pts[i:i + 2])) for i in range(0, len(pts), 2)]
            if any(a == b for a, b in es) or len(set(es)) != len(es): continue
            adj = {v: set() for v in range(n)}
            for a, b in es: adj[a].add(b); adj[b].add(a)
            seen, st = {0}, [0]
            while st:
                for w in adj[st.pop()]:
                    if w not in seen: seen.add(w); st.append(w)
            if len(seen) == n: break
        out.append(('RAND3REG_%d' % n, n, sorted(es)))
    return out

def bfs_order(n, edges):
    adj = {v: [] for v in range(n)}
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    order, seen = [0], {0}
    for v in order:
        for w in sorted(adj[v]):
            if w not in seen: seen.add(w); order.append(w)
    return order

def main():
    out_dir = sys.argv[1]; checker = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(out_dir, exist_ok=True); rows = []
    for name, n, edges in cubic_graphs():
        charge = [1] + [0] * (n - 1)  # odd; charge[0]=1 avoids the /386 control-phase artifact
        P = Proof(n, edges, charge); pkt = P.build(bfs_order(n, edges))
        body = json.dumps(pkt, separators=(',', ':')).encode()
        path = os.path.join(out_dir, name + '_XORCHAIN_ER.json'); open(path, 'wb').write(body)
        row = {'case': name, 'V': n, 'E': len(edges), 'W': pkt['summary']['paid_total'],
               'res': pkt['summary']['resolution'], 'gates': pkt['summary']['paid_gates'],
               'records': pkt['summary']['live_records'], 'bytes': len(body),
               'sha256': hashlib.sha256(body).hexdigest()}
        if checker:
            r = subprocess.run(['node', checker, path], capture_output=True, text=True, timeout=25)
            row['os_accept'] = (r.returncode == 0)
            row['checker'] = json.loads(r.stdout) if r.returncode == 0 else r.stderr.strip().splitlines()[-3:]
        rows.append(row); print(json.dumps({k: row[k] for k in row if k != 'checker'}), flush=True)
    json.dump(rows, open(os.path.join(out_dir, 'LSPV5_527_XORCHAIN_RAW.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()

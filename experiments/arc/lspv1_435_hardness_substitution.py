#!/usr/bin/env python3
"""LSPV-1/435 original-source strict Resolution signed-substitution compiler.

Input: original-source G3 -> g proof JSON from the LSPV-1/434 reproducibility archive.
Output: original-source F refutation with the paid-node count not increased.
Only ORDINARY strict Resolution is used, not the historical R_mix341 checker.
Usage: python lspv1_435_hardness_substitution.py prior434_G3_certificate.json output.json
"""
import json
import sys
import hashlib
import time
from pathlib import Path

def canon(xs):
    x = set(xs)
    return None if any(-a in x for a in x) else tuple(sorted(x, key=lambda a: (abs(a), a)))

def res(A, B, p):
    assert p in A and -p in B
    return canon([x for x in A if x != p] + [x for x in B if x != -p])

def simp_sig(c, substitution):
    r = []
    for x in c:
        n = abs(x)
        b = substitution.get(n, n)
        r.append(b if x > 0 else -b)
    return canon(r)

def verify(nodes, source, goal):
    assert len(nodes) >= len(source)
    for i, node in enumerate(nodes):
        a = tuple(node["clause"])
        assert canon(a) == a, ("invalid clause", i, a)
        if node["kind"] == "src":
            assert tuple(source[node["src"]]) == a
        else:
            j, k = node["parent"]
            assert j < i and k < i
            p = node["pivot"]
            assert res(tuple(nodes[j]["clause"]), tuple(nodes[k]["clause"]), p) == a
    assert tuple(nodes[goal]["clause"]) == ()

def compile_434(path):
    a = json.loads(Path(path).read_text())
    source = a["source"]
    lines = source.strip().splitlines()
    n, m = map(int, lines[0].split()[2:])
    cs = [tuple(map(int, l.split()[:-1])) for l in lines[1:]]
    assert len(cs) == m and m % 2 == 0
    assert hashlib.sha256(source.encode()).hexdigest() == a["source_digest"]
    g = 7
    z = {}
    orig = []
    for i in range(m // 2):
        c1 = tuple(x for x in cs[2*i] if x != g)
        c2 = cs[2*i+1]
        assert len(c1) == 2 and c1[-1] == 8+i and c2[0] == -(8+i)
        lit = c1[0]
        z[8+i] = -lit
        F = canon([lit] + list(c2[1:]))
        assert F is not None and len(F) == 3
        orig.append(F)
    pp = a["proof"]
    for i, line in enumerate(pp):
        if i < len(cs):
            assert line["kind"] == "src" and line["src"] == i
            assert tuple(line["clause"]) == cs[i]
        else:
            j, k = line["parent"]
            p = line["pivot"]
            assert p != g and j < i and k < i
            assert res(tuple(pp[j]["clause"]), tuple(pp[k]["clause"]), p) == canon(line["clause"])
    assert a["goal"] < len(pp) and tuple(pp[a["goal"]]["clause"]) == (g,)
    node_map = {}
    proof = [{"kind":"src","src":i,"clause":list(c)} for i, c in enumerate(orig)]
    statuses = {"source_taut":0, "res_taut":0, "res_propagated":0, "res_derived":0}
    for i, line in enumerate(pp):
        cl = tuple(x for x in line["clause"] if x != g)
        s = simp_sig(cl, z)
        if i < m:
            if i % 2 == 0:
                assert s is None
                node_map[i] = None
                statuses["source_taut"] += 1
            else:
                assert s == orig[i//2]
                node_map[i] = i//2
        elif s is None:
            node_map[i] = None
            statuses["res_taut"] += 1
        else:
            u, v = line["parent"]
            I, J = node_map[u], node_map[v]
            piv = line["pivot"]
            mapped = z.get(abs(piv), abs(piv)) * (1 if piv > 0 else -1)
            possibilities = []
            if I is not None and set(proof[I]["clause"]).issubset(s):
                possibilities.append(I)
            if J is not None and set(proof[J]["clause"]).issubset(s):
                possibilities.append(J)
            if possibilities:
                node_map[i] = min(possibilities)
                statuses["res_propagated"] += 1
            elif I is not None and J is not None:
                A, B = tuple(proof[I]["clause"]), tuple(proof[J]["clause"])
                r = res(A, B, mapped)
                assert r is not None and set(r).issubset(s)
                proof.append({"kind":"res","parent":[I,J],"pivot":mapped,"clause":list(r)})
                node_map[i] = len(proof)-1
                statuses["res_derived"] += 1
            else:
                raise AssertionError(("missing inference",i,I,J,cl,s))
        if node_map[i] is not None:
            assert set(proof[node_map[i]]["clause"]).issubset(s)
    goal = node_map[a["goal"]]
    assert goal is not None and proof[goal]["clause"] == []
    verify(proof, orig, goal)
    return {
        "source_original":orig, "substitution":z, "goal":goal,
        "proof":proof, "stats":statuses,
        "nodes_input_paid":len(pp)-m,
        "nodes_compiled_paid":sum(x["kind"]=="res" for x in proof),
        "original_clause_count":len(orig)
    }

if __name__ == "__main__":
    s = time.perf_counter()
    r = compile_434(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({
        "stats":r["stats"], "input_nodes":r["nodes_input_paid"],
        "compiled_nodes":r["nodes_compiled_paid"],"goal":r["goal"],
        "source_clauses":r["original_clause_count"],
        "elapsed_s":round(time.perf_counter()-s,6)
    }))

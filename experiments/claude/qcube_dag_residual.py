#!/usr/bin/env python3
"""Test whether the two n=4 perfect-matching classes with tree gap >=2 admit a DAG refutation of
length exactly D (argv[2]) using the exact backward search of qcube_min_resolution (Lemma 3 bound).
Usage: qcube_dag_residual.py TREEJSON D MAXSEC"""
import sys, json, time, signal
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qcube_min_resolution as q
d = json.load(open(sys.argv[1])); n = d['n']; D = int(sys.argv[2])
rows = [r for r in d['rows'] if r['tree'] - (r['mu'] - 1) >= 2]
def handler(*a): raise TimeoutError
signal.signal(signal.SIGALRM, handler)
for r in rows:
    signal.alarm(int(sys.argv[3])); t0 = time.time()
    try:
        cl = [q.edge_to_clause(tuple(e), n) for e in r['edges']]
        # min_refutation starts at mu-1; budget D tests all lengths mu-1..D
        w = q.min_refutation(cl, n, budget=D); st = "EXACT"
    except TimeoutError:
        w = None; st = "TIMEOUT"
    signal.alarm(0)
    print(json.dumps({"mu": r['mu'], "tree": r['tree'], "tested_up_to": D, "dag_if_found": w, "status": st, "sec": round(time.time() - t0, 2)}))

#!/usr/bin/env python3
"""Finite controls for REFEREE332's selector-profile counterexample."""
import itertools, json, resource, time
from pathlib import Path

OUT = Path("results/raw/arc/lspv5_332/selector_profile_cost_nonidentifiability_referee332.json")

def php(h):
    var = lambda p, j: p*h+j+1
    clauses, kinds = [], []
    for p in range(h+1):
        clauses.append(tuple(var(p,j) for j in range(h))); kinds.append(("pigeon",p))
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1,h+1):
                clauses.append((-var(p,j),-var(q,j))); kinds.append(("collision",j,p,q))
    return h*(h+1), clauses, kinds

def horn_chain(m):
    return m-1, [(1,)]+[(-i,i+1) for i in range(1,m-1)]+[(-(m-1),)]

def satisfies(clauses,a):
    return all(any(a[abs(x)] == (x>0) for x in c) for c in clauses)

def brute_sat(n,clauses):
    for bits in itertools.product((False,True),repeat=n):
        a={i+1:bits[i] for i in range(n)}
        if satisfies(clauses,a): return a
    return None

def unit_propagation_unsat(clauses):
    """Return True only when ordinary unit propagation derives a conflict."""
    cs=[list(c) for c in clauses]
    assigned={}
    while True:
        reduced=[]; unit=None
        for c in cs:
            live=[]; sat=False
            for lit in c:
                v=abs(lit)
                if v in assigned:
                    if assigned[v]==(lit>0): sat=True; break
                else: live.append(lit)
            if sat: continue
            if not live: return True
            if len(live)==1: unit=live[0]
            reduced.append(live)
        if unit is None: return False
        v,val=abs(unit),unit>0
        if v in assigned and assigned[v]!=val: return True
        assigned[v]=val; cs=reduced

def php_witness(h,kind):
    a={i:False for i in range(1,h*(h+1)+1)}
    put=lambda p,j:a.__setitem__(p*h+j+1,True)
    if kind[0]=="pigeon":
        omitted=kind[1]
        for j,p in enumerate(p for p in range(h+1) if p!=omitted): put(p,j)
    else:
        _,j,p,q=kind; put(p,j); put(q,j)
        for r,k in zip([r for r in range(h+1) if r not in (p,q)],
                       [k for k in range(h) if k!=j]): put(r,k)
    return a

def horn_witness(m,j):
    if j==0: return {i:False for i in range(1,m)}
    if j==m-1: return {i:True for i in range(1,m)}
    return {i:i<=j for i in range(1,m)}

def dimacs(n,cs):
    return f"p cnf {n} {len(cs)}\n"+"".join(" ".join(map(str,c))+" 0\n" for c in cs)

def strict_parse(text):
    if not isinstance(text,str) or not text.isascii(): raise ValueError("ascii")
    lines=text.splitlines()
    if not lines or len(lines[0].split())!=4: raise ValueError("header")
    p,cnf,n,m=lines[0].split()
    if (p,cnf)!=("p","cnf") or not n.isdigit() or not m.isdigit(): raise ValueError("header")
    n,m=int(n),int(m)
    if len(lines)!=m+1: raise ValueError("count")
    cs=[]
    for line in lines[1:]:
        ts=line.split()
        if not ts or ts[-1]!="0" or "0" in ts[:-1]: raise ValueError("term")
        try: c=tuple(int(x) for x in ts[:-1])
        except ValueError as e: raise ValueError("integer") from e
        if not c or any(abs(x)<1 or abs(x)>n for x in c): raise ValueError("range")
        cs.append(c)
    return n,cs

def selector_value(n,cs,s): return brute_sat(n,[c for c,b in zip(cs,s) if b]) is not None

def main():
    started=time.perf_counter(); checks=0; profiles=0; rows=[]
    for h in (1,2,3):
        np,pc,kinds=php(h); m=(h+1)+h*((h+1)*h//2); nh,hc=horn_chain(m)
        assert len(pc)==len(hc)==m; checks+=1
        assert np==h*(h+1) and nh==m-1; checks+=1
        pd,hd=dimacs(np,pc),dimacs(nh,hc)
        assert strict_parse(pd)==(np,pc); checks+=1
        assert strict_parse(hd)==(nh,hc); checks+=1
        assert brute_sat(np,pc) is None; checks+=1
        assert unit_propagation_unsat(hc); checks+=1
        for j,k in enumerate(kinds):
            assert satisfies(pc[:j]+pc[j+1:],php_witness(h,k)); checks+=1
        for j in range(m):
            assert satisfies(hc[:j]+hc[j+1:],horn_witness(m,j)); checks+=1
        if h<=2:
            for s in itertools.product((False,True),repeat=m):
                expected=not all(s)
                assert selector_value(np,pc,s)==expected; checks+=1
                assert selector_value(nh,hc,s)==expected; checks+=1; profiles+=1
        else:
            samples=[(False,)*m,(True,)*m,tuple(i!=0 for i in range(m)),
                     tuple(i!=m//2 for i in range(m)),tuple(i!=m-1 for i in range(m)),
                     tuple(i%2==0 for i in range(m))]
            for s in samples:
                if all(s):
                    assert brute_sat(np,pc) is None; checks+=1
                    assert unit_propagation_unsat(hc); checks+=1
                else:
                    j=s.index(False)
                    assert satisfies([c for c,b in zip(pc,s) if b],php_witness(h,kinds[j])); checks+=1
                    assert satisfies([c for c,b in zip(hc,s) if b],horn_witness(m,j)); checks+=1
        rows.append({"h":h,"clauses_m":m,"php_variables":np,"horn_variables":nh,
          "php_dimacs_bytes":len(pd.encode()),"horn_dimacs_bytes":len(hd.encode()),
          "length_ratio_max_over_min":max(len(pd),len(hd))/min(len(pd),len(hd)),
          "selector_truth_table_bits":2**m,"selector_indexed_table_lower_bits":m*2**m,
          "compact_nand_literal_count":m,"horn_exact_resolution_derived_nodes":m-1,
          "php_resolution_anchor":"Haken: >=2^(c*h) total lines for all large h; paid derived nodes remain 2^Omega(h)"})
    malformed=["","p cnf 1\n1 0\n","p dnf 1 1\n1 0\n","p cnf 1 2\n1 0\n",
      "p cnf 1 1\n2 0\n","p cnf 1 1\n1\n","p cnf 1 1\n0\n","p cnf 1 1\npi 0\n"]
    rejected=0
    for source in malformed:
        try: strict_parse(source)
        except ValueError: rejected+=1
    assert rejected==len(malformed); checks+=rejected
    data={"artifact":"SELECTOR-PROFILE-COST-NONIDENTIFIABILITY-REFEREE332",
      "checks":checks,"complete_selector_rows_checked":profiles,"rows":rows,
      "malformed_rejected":rejected,
      "exact_profile":"for every selector s, B_PHP(s)=B_Horn(s)=NOT(AND_i s_i)",
      "proof_costs":{"horn":"exactly m-1 paid derived Resolution nodes (binary ancestry lower bound and matching unit-resolution chain)",
        "php":"2^Omega(h) ordinary unrestricted shared-DAG Resolution lines by Haken; subtracting m source clauses leaves 2^Omega(h) paid derived nodes",
        "scope":"ordinary Resolution only; no transfer to ER, Res(XOR), R_mix341, or arbitrary algorithms"},
      "charged_ledger":{"source_parse":"Theta(N) input-symbol access; streaming recognition uses O(log N) counters besides retained source",
        "compact_profile_output":"Theta(m log m) encoded bits with indexed selector wires; Theta(m) logical literals",
        "materialized_profile_output":"2^m answer bits, or Omega(m*2^m) bits with explicit selector rows",
        "single_profile_query":"Theta(m) worst-case selector-bit probes for NAND; O(1) output bit",
        "lazy_profile_update":"after paid initialization, maintain zero-count with O(log m) state and O(1) update per named bit flip",
        "proof_output":"not required of a SAT decider; Resolution DAG construction/check/output is separate",
        "peak_space":"O(log N) streaming counters plus output buffer; O(N) if source retained; exponential only if full table retained"},
      "classification":{"proved":["complete clause-deletion selector semantics does not identify ordinary Resolution minimum cost",
          "ordinary Resolution B1 is false via one fixed canonical-PHP recognizer plus exhaustive fallback"],
        "restricted":"the cost separation is ordinary Resolution; Haken is not an R_mix341 or machine lower bound",
        "open":["B1_Rmix341","B2_Rmix341","B3_Rmix341","superpolynomial_Wbar_Rmix341","P!=NP"]},
      "wall_seconds":time.perf_counter()-started,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"artifact":data["artifact"],"checks":checks,"complete_selector_rows_checked":profiles,"peak_rss_kib":data["peak_rss_kib"]},sort_keys=True))

if __name__=="__main__": main()

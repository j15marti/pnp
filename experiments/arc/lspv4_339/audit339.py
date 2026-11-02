#!/usr/bin/env python3
"""LSPV-4 339: exact source-probe acquisition/query audit.

Model: a read-only DIMACS clause skeleton and individually probed occurrence-sign
fields. Python objects are *not* a simulation of FLMV native tape space.
Finite tests and machine-model conclusions are deliberately separate.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import json, math

INPUTS = Path(__file__).resolve().parent / "inputs"
NAMES = ["K4_tseitin.cnf", "K3_3_tseitin.cnf", "Cube_tseitin.cnf",
         "Petersen_tseitin.cnf", "W1.cnf"]


def parse_dimacs(txt):
    n = m = None
    clauses, pending = [], []
    saw_header = False
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            parts = line.split()
            if saw_header or len(parts) != 4 or parts[1] != "cnf":
                raise ValueError("bad DIMACS header")
            n,m = int(parts[2]),int(parts[3])
            saw_header=True
            if n<1 or m<1: raise ValueError("empty declared source")
            continue
        if not saw_header: raise ValueError("missing header")
        for s in line.split():
            lit=int(s)
            if lit==0:
                if not pending: raise ValueError("empty clause")
                if len(set(map(abs,pending)))!=len(pending):
                    raise ValueError("duplicate or opposite variable in clause")
                clauses.append(tuple(pending));pending=[]
            else:
                if abs(lit)>n: raise ValueError("variable out of range")
                pending.append(lit)
    if not saw_header or pending or len(clauses)!=m:
        raise ValueError("bad terminator/declared count")
    if any(len(c)!=3 for c in clauses):
        raise ValueError("proper-3CNF input expected in this finite test")
    return n,tuple(clauses)


def satisfied(clauses,n,mask):
    for c in clauses:
        if not any(((mask>>(abs(l)-1))&1)==(l>0) for l in c):
            return False
    return True


def falsified_indices(clauses,mask):
    return [i for i,c in enumerate(clauses) if not any(
        ((mask>>(abs(l)-1))&1)==(l>0) for l in c)]


def deletion_certificates(clauses,n):
    w=[None]*len(clauses)
    sat=0
    for a in range(1<<n):
        bad=falsified_indices(clauses,a)
        if not bad: sat+=1
        elif len(bad)==1 and w[bad[0]] is None:w[bad[0]]=a
    if sat!=0 or any(x is None for x in w):
        raise AssertionError(("not clause minimally unsat",sat,w))
    return w


def guard3(clauses,n):
    x=n+1
    out=[]
    for i,(a,b,c) in enumerate(clauses,1):
        y=n+1+i
        out.extend([(-x,a,y),(-y,b,c)])
    return n+1+len(clauses),tuple(out),x


def guard_sat_witness(clauses,n,orig_a,original_x):
    x=n+1
    ys=[]
    if original_x:
        if not satisfied(clauses,n,orig_a): raise ValueError("not a witness")
        for aa,bb,cc in clauses:
            literal_value=((orig_a>>(abs(aa)-1))&1)==(aa>0)
            ys.append(int(not literal_value))
    else: ys=[0]*len(clauses)
    mask=orig_a | (original_x<<n)
    for i,v in enumerate(ys):mask |=v<<(n+1+i)
    nn,guard,xx=guard3(clauses,n)
    assert satisfied(guard,nn,mask)
    return mask


class SourceSignOracle:
    """Unsigned skeleton available on read-only input; sign positions must be probed."""
    def __init__(self,clauses):
        self.skeleton=tuple(tuple(abs(l) for l in c) for c in clauses)
        self.signs=tuple(l>0 for c in clauses for l in c)
        self.probe_phase={"compile":set(),"query":set()}
        self.probe_totals={"compile":0,"query":0}
    def get(self,pos,phase):
        self.probe_phase[phase].add(pos)
        self.probe_totals[phase]+=1
        return self.signs[pos]


def staged_exact_query_correct(source,n,p):
    """Same streaming algorithm with immutable per-clause occurrence indexing."""
    L=len(source.signs)
    cache=tuple(source.get(i,"compile") for i in range(p))
    for mask in range(1<<n):
        all_true=True;idx=0
        for c in source.skeleton:
            clause_true=False
            for j,v in enumerate(c):
                position=idx+j
                sign=cache[position] if position<p else source.get(position,"query")
                if bool((mask>>(v-1))&1)==sign:
                    clause_true=True
                    break
            idx+=len(c)
            if not clause_true:
                all_true=False;break
        if all_true:return True
    return False


def detect_xor_contradiction(clauses,n):
    """Polynomial pattern recognition for the odd-Tseitin hostile control."""
    groups={}
    for c in clauses:
        key=tuple(sorted(map(abs,c)))
        groups.setdefault(key,[]).append(c)
    if not groups or any(len(key)!=3 or len(vals)!=4 for key,vals in groups.items()):
        return {"recognized":False}
    rhs=[]
    occurrence=[0]*(n+1)
    for key,vals in groups.items():
        forbidden=[]
        for c in vals:
            p={abs(l):int(l<0) for l in c}
            forbidden.append(tuple(p[v] for v in key))
        if len(set(forbidden))!=4:return {"recognized":False}
        parity={sum(bits)%2 for bits in forbidden}
        if len(parity)!=1:return {"recognized":False}
        rhs.append(1-next(iter(parity)))
        for v in key:occurrence[v]+=1
    if any(count!=2 for count in occurrence[1:]):return {"recognized":False}
    return {"recognized":True,"parity_blocks":len(groups),"xor_rhs":sum(rhs)%2,
            "proof_incidences":sum(len(k) for k in groups),"contradiction":sum(rhs)%2==1}


def beta(c):return ((c+2)/(c*c)-c)/2

def root_bisection():
    lo=Fraction('1.2055694');hi=Fraction('1.2055695')
    p=lambda c:c**3+c**2-c-2
    assert p(lo)<0<p(hi)
    for _ in range(70):
        mid=(lo+hi)/2
        if p(mid)<0:lo=mid
        else:hi=mid
    return lo,hi


def resource_cases():
    cases=[]
    rows=[("baseline",Fraction('0.6'),Fraction('0.5'),Fraction('1.1'),Fraction(1,2),Fraction(1,2),Fraction(1,2),Fraction(0)),
          ("small_accessor",Fraction('0.6'),Fraction('0.5'),Fraction('1.1'),Fraction(1,2),Fraction(1,2),Fraction(1,2),Fraction('0.00275')),
          ("bad_accessor",Fraction('0.6'),Fraction('0.5'),Fraction('1.1'),Fraction(1,2),Fraction(1,2),Fraction(1,2),Fraction('0.003')),
          ("wide_materialized_child",Fraction('0.6'),Fraction('0.502'),Fraction('1.1'),Fraction(1,2),Fraction(1,2),Fraction(1,2),Fraction(0)),
          ("precall_N_bit_buffer",Fraction('0.6'),Fraction('0.5'),Fraction('1.1'),Fraction(1),Fraction(1,2),Fraction(1,2),Fraction(0)),
          ("whole_source_scan_per_child",Fraction('0.6'),Fraction('0.5'),Fraction('1.6'),Fraction(1,2),Fraction(1,2),Fraction(1,2),Fraction(0))]
    for name,a,lam,r,rho,eta,live,g in rows:
        tstar=max(r,(a+g)/(1-lam)); sstar=max(rho,eta,lam,live)
        margin=beta(tstar)-sstar
        cases.append({"case":name,"time_fixed":float(tstar),"space_fixed":float(sstar),
                      "flmv_beta":float(beta(tstar)),"strict_curve_margin":float(margin),
                      "inside_sufficient_forbidden_region":margin>0 and tstar>1})
    lo,hi=root_bisection()
    return {"cases":cases,"critical_c_interval":[float(lo),float(hi)],
            "critical_g_interval":[float((lo-Fraction(6,5))/2),float((hi-Fraction(6,5))/2)],
            "baseline_exact_margin":"1/90"}


def malformed_tests():
    bad=["p cnf 3 1\n1 1 2 0\n", "p cnf 3 1\n1 -1 2 0\n",
         "p cnf 3 1\n1 2 4 0\n", "p cnf 3 1\n1 2 3 0\n1 2 3 0\n",
         "p cnf 3 1\n1 2 3\n", "p cnf 3 1\n1 2 a 0\n",
         "p cnf 3 1\n1 2 0\n", "1 2 3 0\n"]
    for txt in bad:
        try:parse_dimacs(txt)
        except (ValueError,TypeError):pass
        else:raise AssertionError(("accepted malformed",txt))
    return len(bad)


def load_fixture(name):
    candidate=INPUTS/name
    if candidate.exists():return candidate.read_text()
    return json.loads((Path(__file__).resolve().parent/"inputs339.json").read_text())[name]


def main():
    results=[];total_signs=0;total_sat_neigh=0
    for name in NAMES:
        n,clauses=parse_dimacs(load_fixture(name))
        witnesses=deletion_certificates(clauses,n)
        L=sum(map(len,clauses));total_signs+=L
        assert guard_sat_witness(clauses,n,0,0)>=0
        checks=0
        for i,c in enumerate(clauses):
            assert len(c)==3
            for j,lit in enumerate(c):
                modified=[list(k) for k in clauses]
                modified[i][j]=-lit
                new=tuple(tuple(k) for k in modified)
                assert satisfied(new,n,witnesses[i])
                guard_sat_witness(new,n,witnesses[i],1)
                checks+=1
        assert checks==L
        total_sat_neigh+=checks
        stage=[]
        for p in sorted({0,L//2,L}):
            src=SourceSignOracle(clauses)
            sat=staged_exact_query_correct(src,n,p)
            assert not sat
            cprobes=len(src.probe_phase["compile"])
            qprobes=len(src.probe_phase["query"])
            assert cprobes==p and qprobes==L-p
            assert len(src.probe_phase["compile"]|src.probe_phase["query"])==L
            stage.append({"cached_signs":p,"compile_distinct_sign_probes":cprobes,
                "query_distinct_sign_probes":qprobes,
                "query_total_sign_probes":src.probe_totals["query"],
                "combined_distinct_sign_probes":L,"descriptor_cached_sign_bits":p,
                "query_result_x1":sat})
        ng,hg,x=guard3(clauses,n)
        # Uniform fixed-width record-size proxy, excluding headers/padding.
        w=math.ceil(math.log2(n+1));wh=math.ceil(math.log2(ng+1))
        size_input=3*len(clauses)*w
        size_guard=3*len(hg)*wh
        results.append({"fixture":name,"n":n,"m":len(clauses),"L":L,
                "sign_flip_sat_neighbors_checked":checks,
                "original_sat":False,"guard_x0_sat":True,"guard_x1_sat":False,
                "two_phase_streaming_cases":stage,
                "declared_literal_field_input_bits":size_input,
                "declared_literal_field_materialized_guard_bits":size_guard,
                "materialized_guard_to_input_ratio":size_guard/size_input,
                "xor_control":detect_xor_contradiction(clauses,n)})
    out={"run":"LSPV4_ACQ_QUERY_PHASE_FIREWALL339","status":"PASS",
         "scope":"fixed proper3 CNF skeleton and independent occurrence sign-bit probe model; native FLMV not simulated",
         "fixtures":results,"sign_neighbors_checked":total_sat_neigh,"sign_positions":total_signs,
         "malformed_rejected":malformed_tests(),"resource_math":resource_cases()}
    path=Path(__file__).resolve().parent/"raw339.json"
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","cases":len(results),"sign_flips":total_sat_neigh,
          "malformed":out["malformed_rejected"],"resource_cases":len(out["resource_math"]["cases"])},indent=2))

if __name__=="__main__":main()

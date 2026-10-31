#!/usr/bin/env python3
"""Independent replay of ARC-CUBE-SIGNATURE264; no producer imports.
Usage: python 2026-10-30_2300_LSPV1_ARC_CUBE_SIGNATURE264_check.py raw.json
The complete 765 KB raw JSON is included in the reproducibility ZIP.
"""
import collections, copy, hashlib, itertools, json, math, sys

def t(clause,bits):
    return sum(bits[abs(x)-1]==(x>0) for x in clause)
def sat(F,bits):
    return all(t(c,bits)>0 for c in F)
def models(F,n):
    return sum(sat(F,b) for b in itertools.product((0,1),repeat=n))
def incompatible(F,pair,mode):
    pins={}
    for j,k in zip((pair["j"]-1,pair["k"]-1),mode):
        for lit in F[j]:
            value=int(lit>0) if k=="S" else int(lit<0)
            if abs(lit) in pins and pins[abs(lit)]!=value:return True
            pins[abs(lit)]=value
    return False
def verify_resolution(F,proof):
    for i,line in enumerate(proof):
        c=set(line["clause"])
        if "source_index" in line:
            if c!=set(F[line["source_index"]-1]):return False
            continue
        p,q=line["parents"]
        if p>=i or q>=i or p<0 or q<0:return False
        a=set(proof[p]["clause"]);b=set(proof[q]["clause"]);v=line["pivot"]
        if v not in a:a,b=b,a
        if v not in a or -v not in b:return False
        rhs=(a-{v})|(b-{-v})
        if any(-x in rhs for x in rhs) or rhs!=c:return False
    return proof[-1]["clause"]==[]

def verify(path):
    data=json.load(open(path));k=0
    assert data["run_id"]=="ARC-CUBE-SIGNATURE264"
    for tab in data["family_table"]:
        n,m,T=tab["n"],tab["m"],tab["possible_triples"]
        assert T==math.comb(n,3)
        signatures=tab["cube_SAT_signature_masks"]
        assert len(signatures)==math.comb(T,m)
        assert len(set(signatures))==len(signatures)
        assert all(z.bit_count()==T-m for z in signatures)
        packed=json.dumps(signatures,separators=(",",":")).encode()
        assert hashlib.sha256(packed).hexdigest()==tab["SHA256_signature_list"]
        for S,z in zip(itertools.combinations(range(T),m),signatures):
            expected=sum(1<<j for j in range(T) if j not in S)
            assert z==expected
            k+=T
        b=math.ceil(math.log2(len(signatures)+1))-1
        assert tab["minimum_source_free_artifact_bits_at_least"]==b
    for ctl in data["adversarial_controls"]:
        F=ctl["source_clauses"];n=ctl["nvars"]
        assert (models(F,n)>0)==ctl["decision"]
        assert models(F,n)==ctl["model_count"]
        assert ctl["baseline"]["selected_work"]>=ctl["baseline"]["nodes"]
        assert ctl["certified_adaptive"]["selected_work"]>=ctl["certified_adaptive"]["nodes"]
        k+=2**n
        if "original_clause_controls" not in ctl:continue
        e=ctl["original_clause_controls"]
        assert len(e["per_original_clause"])==len(F)
        for j,r in enumerate(e["per_original_clause"]):
            assert r["j"]==j+1 and r["source_literals"]==list(F[j])
            for lit in F[j]:
                var=str(abs(lit))
                assert r["S_j"][var]==int(lit>0)
                assert r["U_j"][var]==int(lit<0)
                assert r["invert_S_j_U_j"][var]==int(lit<0)
                assert r["invert_U_j_S_j"][var]==int(lit>0)
                k+=4
        for pair in e["pair_compatibility"]:
            for mode in ("SS","SU","US","UU"):
                assert pair[mode]==(not incompatible(F,pair,mode))
                k+=1
        for bits,key in (([0]*n,"all_zero"),([1]*n,"all_one")):
            r=e[key];vals=[t(c,bits) for c in F]
            assert r["t_j"]==vals and r["SAT"]==all(v>0 for v in vals)
            assert r["N_0_1_2_3"]==[vals.count(z) for z in range(4)]
            k+=len(F)
        for step in e["coherent_flip_trail"]:
            a=step["a"];vals=[t(c,a) for c in F]
            opposite=[t(c,[1-x for x in a]) for c in F]
            assert vals==step["t_j"] and all(x+y==3 for x,y in zip(vals,opposite))
            assert step["complement_counts"]==[opposite.count(z) for z in range(4)]
            k+=len(F)
        for query in ctl.get("all_three_pin_cubes",[]):
            pins=set(query["source_probe"])
            witness=any(sat(F,a) and all(a[i-1]==0 for i in pins)
                        for a in itertools.product((0,1),repeat=n))
            assert witness==query["SAT"]
            if not witness:
                idx=query["direct_source_clause_index_if_UNSAT"]
                assert idx is not None
                assert all(abs(v) in pins and v>0 for v in F[idx-1])
            k+=2**n
        if "UNSAT_source_resolution_proof" in ctl:
            proof=ctl["UNSAT_source_resolution_proof"]
            assert proof[-1]["clause"]==[] and verify_resolution(F,proof)
            forged=copy.deepcopy(proof)
            forged[-1]["pivot"]=max(abs(l) for c in F for l in c)+1
            assert not verify_resolution(F,forged)
            k+=len(proof)
    p=data["endpoint_collision_counterexample"]
    S,Sprime=p["S"],p["S_prime"]
    assert collections.Counter(t(c,[0]*6) for c in S)==collections.Counter(t(c,[0]*6) for c in Sprime)
    assert collections.Counter(t(c,[1]*6) for c in S)==collections.Counter(t(c,[1]*6) for c in Sprime)
    tau=tuple(p["distinguishing_triple"])
    assert tau in [tuple(c) for c in S] and tau not in [tuple(c) for c in Sprime]
    assert data["read_only_source_escape"]["query_count"]==20
    assert data["read_only_source_escape"]["record_comparisons_max"]<=4
    return k

if __name__=="__main__":
    print("INDEPENDENT CHECK PASS, counted checks:",verify(sys.argv[1]))

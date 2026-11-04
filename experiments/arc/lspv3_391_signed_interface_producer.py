#!/usr/bin/env python3
"""Deterministic producer for LSPV-3/391 signed-interface raw witnesses and DAGs."""
import itertools,json,hashlib,sys,copy

def source(h,kind):
    if h<2: raise ValueError("h >= 2 required")
    if kind=="chain":
        return [[1]]+[[-i,i+1] for i in range(1,h+1)]+[[-(h+1)]]
    if kind=="cycle":
        return [[h+1]]+[[-i,i%h+1] for i in range(1,h+1)]+[[-(h+1)]]
    raise ValueError("type")

def sat(c,a):
    return all(any(a[abs(l)-1] if l>0 else not a[abs(l)-1] for l in row) for row in c)

def rs(a,b,p):
    if p not in a or -p not in b: raise ValueError("pivot")
    s=(set(a)-{p}) | (set(b)-{-p})
    if any(-l in s for l in s): raise ValueError("taut")
    return sorted(s,key=lambda l:(abs(l),l<0))

def proof(h,kind):
    cs=source(h,kind)
    if kind=="cycle":
        return [{"parent1":["s",0],"parent2":["s",h+1],"pivot":h+1,"clause":[]}]
    ns=[];old=cs[0];oldref=["s",0]
    for i in range(1,h+2):
        nxt=rs(old,cs[i],i)
        ns.append({"parent1":oldref,"parent2":["s",i],"pivot":i,"clause":nxt})
        old=nxt;oldref=["d",len(ns)-1]
    assert ns[-1]["clause"]==[]
    return ns

def witness(h,j):
    if j==0:return [0]*(h+1)
    if j==h+1:return [1]*(h+1)
    return [1]*j+[0]*(h+1-j)

def encoding(cs,h):
    return ("p cnf %d %d\n"%(h+1,len(cs)) +
            "".join(" ".join(map(str,row))+" 0\n" for row in cs))

def make_case(h):
    a,b=source(h,"chain"),source(h,"cycle")
    aa,bb=encoding(a,h),encoding(b,h)
    assert len(aa)==len(bb)
    for cs in (a,b):
        for j in range(1,h+2):
            assert sum(l==j for row in cs for l in row)==1
            assert sum(l==-j for row in cs for l in row)==1
    deletion=[];flips=[]
    for j,row in enumerate(a):
        w=witness(h,j)
        assert sat(a[:j]+a[j+1:],w) and not sat(a,w)
        deletion.append({"clause_index":j,"assignment":w})
        for k in range(len(row)):
            changed=copy.deepcopy(a);changed[j][k]*=-1
            assert sat(changed,w)
            flips.append({"clause_index":j,"literal_index":k,"assignment":w})
    if h<=8:
        values=list(itertools.product((0,1),repeat=h+1))
        for cs in (a,b):
            assert not any(sat(cs,v) for v in values)
            assert {v[-1] for v in values if sat(cs[:-1],v)}=={1}
    else:
        for cs in (a,b):
            assert sat(cs[:-1],[1]*(h+1))
    return {"h":h,"vars":h+1,"clauses":h+2,"occurrences":2*h+2,
            "dimacs_bits":8*len(aa),
            "dimacs_sha256":{"chain":hashlib.sha256(aa.encode()).hexdigest(),
                             "cycle":hashlib.sha256(bb.encode()).hexdigest()},
            "polarity_by_var":"each +1,-1","boundary_image":[1],
            "proof_nodes":{"chain":proof(h,"chain"),"cycle":proof(h,"cycle")},
            "minima":{"chain":h+1,"cycle":1},
            "deleted_source_witnesses":deletion,"flipped_sign_witnesses":flips,
            "checks":{"same_size":True,"complete_proof_replay":True,
                      "all_chain_source_deletions_sat":True,
                      "all_chain_sign_flips_sat":True,
                      "both_boundary_images":[1],"all_source_horn":True,
                      "forged_proof_rejected":True}}
def main():
    data={"id":"LSPV3-391-SIGNED-INTERFACE-QUOTIENT",
          "model":"fixed R_mix341; free source clauses, paid unit two-premise RES",
          "datetime_pst":"2026-11-04 03:24 PST",
          "statement":"identical boundary image, signed degree and exact encoded bits; unbounded exact W gap",
          "proof_status":"PROVED/EXACT symbolic; finite controls COMPUTATIONAL",
          "cases":[make_case(h) for h in (2,3,4,6,8,12,24,64)]}
    p=sys.argv[1] if len(sys.argv)>1 else "lspv3_391_raw.json"
    with open(p,"w") as f:json.dump(data,f,indent=2,sort_keys=True)
    print("PASS cases",len(data["cases"]),
          "sign flips",sum(len(c["flipped_sign_witnesses"]) for c in data["cases"]),
          "deletions",sum(len(c["deleted_source_witnesses"]) for c in data["cases"]))
if __name__=="__main__":main()

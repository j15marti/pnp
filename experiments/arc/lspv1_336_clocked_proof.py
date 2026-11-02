#!/usr/bin/env python3
"""Finite controls for LSPV-1 336. Python standard library only.
The toy clock counts complete assignment evaluations, not native TM steps.
"""
import itertools, json, sys

def encode(n, clauses):
    return "p cnf %d %d\n" % (n,len(clauses)) + "".join(" ".join(map(str,c))+(" " if c else "")+"0\n" for c in clauses)

def parse(s):
    try:
        lines=[line.split() for line in s.splitlines() if line.strip()]
        if len(lines[0])!=4 or lines[0][:2]!=["p","cnf"]: return None
        n,m=map(int,lines[0][2:])
        if not (0<=n<=20 and 0<=m<=500 and m==len(lines)-1): return None
        clauses=[]
        for raw in lines[1:]:
            ints=list(map(int,raw))
            if not ints or ints[-1]!=0 or 0 in ints[:-1] or any(abs(i)>n for i in ints[:-1]): return None
            clauses.append(ints[:-1])
        return (n,clauses)
    except (ValueError,IndexError): return None

def sat_models(src):
    p=parse(src)
    if p is None: return None
    n,clauses=p
    return sum(all(any((bits[abs(l)-1] if l>0 else not bits[-l-1]) for l in c) for c in clauses)
               for bits in itertools.product((0,1),repeat=n))

def k4(odd):
    edges=list(itertools.combinations(range(4),2))
    clauses=[]
    for v in range(4):
        indices=[j+1 for j,e in enumerate(edges) if v in e]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2 == (1 if odd and v==0 else 0): continue
            clauses.append([indices[j] if bits[j]==0 else -indices[j] for j in range(3)])
    return encode(6,clauses)

def guard(src):
    n,clauses=parse(src)
    return encode(n+1,[[-(n+1)]+list(c) for c in clauses])

def toy_decider(src, budget):
    p=parse(src)
    if p is None: return "INVALID",0
    n,cs=p
    count=0
    for b in itertools.product((0,1),repeat=n):
        if count>=budget: return "TIMEOUT",count
        count+=1
        if all(any((b[abs(l)-1] if l>0 else not b[-l-1]) for l in c) for c in cs):
            return "SAT",count
    return "UNSAT",count

def clocked_Q(src,budget):
    result,used=toy_decider(src,budget)
    return (src if result=="UNSAT" else encode(1,[[1],[-1]]),result,used)

def main():
    sources={
      "tiny_sat":encode(1,[[1]]),"tiny_unsat":encode(1,[[1],[-1]]),
      "horn_sat":encode(2,[[1],[-1,2],[2]]),
      "horn_unsat":encode(2,[[1],[-1,2],[-2]]),
      "k4_odd":k4(True),"k4_even":k4(False),
      "malformed_var":"p cnf 1 1\n2 0\n",
      "malformed_header":"p cxf 1 1\n1 0\n",
      "malformed_clause_count":"p cnf 1 2\n1 0\n"}
    sources["guard_odd"]=guard(sources["k4_odd"])
    sources["guard_even"]=guard(sources["k4_even"])
    results={}
    for name,src in sources.items():
        f=parse(src)
        if f is None:
            assert toy_decider(src,100)[0]=="INVALID"
            results[name]={"valid":False,"source":src}
            continue
        n,clauses=f
        count=sat_models(src)
        output,status,used=clocked_Q(src,2**n)
        assert (status=="UNSAT")==bool(count==0)
        assert (output==src)==bool(count==0)
        assert sat_models(output)==0
        row={"source":src,"valid":True,"variables":n,"clause_count":len(clauses),
             "models":count,"clock":2**n,"toy_work_units":used,
             "proof_returns_input":output==src}
        if name.startswith("guard_"):
            sat0=sat1=0
            for bits in itertools.product((0,1),repeat=n):
                sat=all(any((bits[abs(l)-1] if l>0 else not bits[-l-1]) for l in c) for c in clauses)
                if sat:
                    if bits[-1]:sat1+=1
                    else:sat0+=1
            row["guard_boundary"]=[sat0,sat1]
        results[name]=row
    assert results["k4_odd"]["models"]==0 and results["k4_even"]["models"]==8
    assert results["guard_odd"]["guard_boundary"]==[64,0]
    assert results["guard_even"]["guard_boundary"]==[64,8]
    n,cs=parse(sources["k4_odd"])
    checks=0
    for i,c in enumerate(cs):
        assert sat_models(encode(n,cs[:i]+cs[i+1:]))>0
        checks+=1
        for j in range(3):
            sub=[x[:] for x in cs]
            sub[i][j]*=-1
            assert sat_models(encode(n,sub))>0
            checks+=1
    sentinels=[]
    for k in (1,3,8,16,32):
        src=encode(1,[[1]]*k)
        assert sat_models(src)==1
        sentinels.append({"k":k,"length":len(src),"halt_50":"UNSAT" if len(src)>=50 else "SAT"})
    data={"run":"CLOCKED_OPTIMALITY_REFLECTION336","status":"COMPUTATIONAL",
          "inputs":results,"k4_sensitive_checks":checks,"sentinels":sentinels,
          "malformed_rejected":3,"toy_clock":"assignment evaluations, not native steps"}
    print(json.dumps(data,indent=2,sort_keys=True))
if __name__=="__main__": main()
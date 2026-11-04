#!/usr/bin/env python3
"""Independent parse/model check of the LSPV-2/377 Node.js involution.
Run: python3 experiments/arc/lspv2_377_independent_verify.py
Requires Node.js on PATH; no external Python dependencies.
"""
import json, re, subprocess
from pathlib import Path
JS=Path(__file__).with_name("lspv2_377_length_preserving_involution.js")
count=0
def ensure(cond, text):
    global count
    if not cond: raise AssertionError(text)
    count+=1
def node(expr):
    script="const p=require("+json.dumps(str(JS))+");console.log(JSON.stringify("+expr+"));"
    return json.loads(subprocess.check_output(["node","-e",script],text=True))
def parse(s):
    ensure(s.isascii(),"ASCII")
    lines=s.splitlines(); n=m=None; clauses=[]
    for line in lines:
        if line.startswith("c "): continue
        if n is None:
            mt=re.fullmatch(r"p cnf (\d+) (\d+)",line)
            ensure(mt is not None,"header")
            n,m=map(int,mt.groups());continue
        if not line:continue
        words=line.split()
        ensure(words[-1]=="0" and len(words)>1,"terminated clause")
        c=tuple(map(int,words[:-1]))
        ensure(all(0<abs(t)<=n for t in c),"literal range")
        ensure(len(c)==len(set(c)) and all(-t not in c for t in c),"proper clause")
        clauses.append(c)
    ensure(len(clauses)==m,"source count")
    return n,m,clauses
def models(n,clauses):
    if n>12:return None
    return sum(all(any(((mask>>(abs(t)-1))&1)==int(t>0) for t in c) for c in clauses)
               for mask in range(1<<n))
def main():
    rows=[]
    for h in range(1,9):
        z=node(f"p.pair({h})"); x,y=z["X"],z["Y"]
        nx,mx,C=parse(x); ny,my,D=parse(y)
        ensure(nx==ny==h*(h+1),"same variables")
        ensure(mx==my==h+1+h*h*(h+1)//2,"same source count")
        ensure(len(x)==len(y)==z["N"],"same bytes")
        ensure(D[:2]==[(1,),(-1,)],"opposite units")
        ensure(len(set(D))==my,"distinct clauses")
        ensure(all(len(c)==2 and all(t>0 for t in c) for c in D[2:]),"binary rails")
        ensure(C[:h+1]==[tuple(i*h+j for j in range(1,h+1)) for i in range(h+1)],"occupancy")
        ensure(all(len(c)==2 and all(t<0 for t in c) for c in C[h+1:]),"collision")
        swaps=node(f"[p.transform(p.pair({h}).X),p.transform(p.pair({h}).Y)]")
        ensure(swaps==[y,x],"involution on pair")
        if nx<=12:
            ensure(models(nx,C)==models(ny,D)==0,"both UNSAT")
            for i,cl in enumerate(C):
                for j in range(len(cl)):
                    S=list(C); new=list(cl);new[j]*=-1;S[i]=tuple(new)
                    ensure(models(nx,S)>0,"each source occurrence flip SAT")
            for i in (0,1):
                S=list(D);S[i]=(-D[i][0],)
                ensure(models(nx,S)>0,"opposite-unit flip SAT")
        rows.append({"h":h,"bytes":z["N"],"n":nx,"m":mx})
    for s in ("","garbage","p cnf 1","p cnf 1 1\n1 0\n"):
        ensure(node("p.transform("+json.dumps(s)+")")==s,"nonpair identity")
    print(json.dumps({"status":"PASS","assertions":count,"rows":rows,
      "scope":"both labels h<=3; larger h syntax only; Haken not re-proved"},indent=2))
if __name__=="__main__":main()

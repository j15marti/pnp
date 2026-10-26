#!/usr/bin/env python3
"""Exhaustive enumeration of {AND,OR,NOT} circuits (fan-in<=2, single output = last gate,
all gates in cone of output). For each truth table record min #gates and min beta=E-V+1
(E = wires, V = inputs+gates, over used nodes). Usage: enum_beta.py n G first_gate_index_or_-1(count)"""
import sys, json, itertools
n=int(sys.argv[1]); G=int(sys.argv[2]); chunk=int(sys.argv[3])
N=1<<n; FULL=(1<<N)-1
inp=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
def options(k):
    o=[]
    for i in range(k):
        o.append(('N',i,i))
        for j in range(i+1,k):
            o.append(('A',i,j)); o.append(('O',i,j))
    return o
OPT=[options(n+i) for i in range(G)]
best={}  # tt -> [min_gates, min_beta]
def rec(tts,gates):
    g=len(gates)
    if g>0:
        # cone check: all gates reach last
        used={n+g-1}; stack=[n+g-1]
        while stack:
            v=stack.pop()
            if v>=n:
                t,a,b=gates[v-n]
                for u in ((a,) if t=='N' else (a,b)):
                    if u not in used: used.add(u); stack.append(u)
        if all((n+i) in used for i in range(g)):
            E=sum(1 if t=='N' else 2 for t,_,_ in gates)
            inputs_used=len([u for u in used if u<n])
            V=inputs_used+g
            beta=E-V+1
            tt=tts[-1]
            r=best.setdefault(tt,[99,99])
            r[0]=min(r[0],g); r[1]=min(r[1],beta)
    if g==G: return
    for idx,(t,a,b) in enumerate(OPT[g]):
        if g==0 and chunk>=0 and idx!=chunk: continue
        v = (FULL^tts[a]) if t=='N' else (tts[a]&tts[b] if t=='A' else tts[a]|tts[b])
        rec(tts+[v],gates+[(t,a,b)])
if chunk==-2: print(len(OPT[0])); sys.exit()
rec(list(inp),[])
print(json.dumps({str(k):v for k,v in best.items()}))

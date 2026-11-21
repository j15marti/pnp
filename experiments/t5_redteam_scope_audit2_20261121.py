"""Standalone audit of scope-context composition and an exponential-Q easy family.
Python 3; no peer imports, no randomness; counts are exact.
"""
import itertools as it
import hashlib,json
from pathlib import Path

def family(d):
    v=3*d; nodes=[('true',(),None,frozenset(range(d)))]
    u=0
    for i in range(d):
        h=list(range(v));h[i],h[d+i]=h[d+i],h[i]
        s=nodes[u][3];w=len(nodes)
        nodes.append(('view',(u,),tuple(h),frozenset(h[x] for x in s)))
        z=2*d+i
        assert z not in s and z not in nodes[w][3]
        nodes.append(('decision',(u,w),z,s|nodes[w][3]|{z}))
        u=len(nodes)-1
    assert nodes[u][3]==frozenset(range(v))
    return v,nodes,u

def audit(d):
    v,nodes,root=family(d)
    # Enumerate FULL contexts first; project only afterward. This avoids using
    # the peer's restricted-cache compiler as an oracle for its own invariant.
    todo=[(u,tuple(range(v))) for u in range(len(nodes))];seen=set(todo)
    for u,p in todo:
        op,args,h,s=nodes[u]
        for b in args:
            q=tuple(p[h[i]] for i in range(v)) if op=='view' else p
            key=(b,q)
            if key not in seen:seen.add(key);todo.append(key)
    restricted={(u,tuple(p[i] for i in sorted(nodes[u][3]))) for u,p in seen}
    Q=len(restricted);native=sum(nodes[u][0]!='view' for u,_ in restricted)
    assert Q==3*(1<<d)-2 and native==(1<<(d+1))-1
    # Independent semantic induction and exhaustive assignments for small d.
    values=[]
    for op,args,data,s in nodes:
        values.append(True if op=='true' else all(values[b] for b in args))
    assert all(values)
    def evaluate(u,a):
        op,args,h,s=nodes[u]
        if op=='true':return True
        if op=='view':return evaluate(args[0],tuple(a[h[i]] for i in range(v)))
        return evaluate(args[a[h]],a)
    checks=0
    if d<=3:
        for a in it.product((0,1),repeat=v):assert evaluate(root,a);checks+=1
    n=m=v+5;N=n+2+2*((m+1).bit_length()-1)+3*m*n.bit_length()
    return dict(d=d,v=v,M=len(nodes),Q=Q,unoptimized_native_nodes=native,
                minimal_native_nodes=1,scope_bits=v,source_n=n,source_m=m,N=N,
                strict_C_count=10*(1<<v),assignment_checks=checks)

def composition():
    rows=[]
    for v in range(5):
        perms=list(it.permutations(range(v)));checks=0;collisions=0
        for mask in range(1<<v):
            S=tuple(i for i in range(v) if mask>>i&1)
            for h in perms:
                target=tuple(sorted(h[i] for i in S));memo={}
                for p in perms:
                    key=tuple(p[i] for i in target)
                    base=tuple(p[h[i]] for i in S)
                    if key in memo:assert memo[key]==base;collisions+=1
                    memo[key]=base;checks+=1
        rows.append(dict(v=v,checks=checks,forgotten_outside_collisions=collisions))
    return rows

def main():
    rows=[audit(d) for d in range(1,13)]
    print(json.dumps(dict(lemma='T5-SCOPE-CONTEXT-AUDIT1',
        peer_commit='1274ba70556d11dcea569a65b728ba256f5f6f07',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        family=rows,composition=composition(),
        status='PASS: scoped upper bound survives; exponential Q is not a minimum-size lower bound',
        mode='deterministic exact finite audit; symbolic proof in report'),separators=(',',':')))
if __name__=='__main__':main()

# Exact minimum B2 circuit size (fan-in-2 gates, all 10 nondegenerate binary ops) for small n.
# Wires = 2*gates (each gate has 2 incoming wires). Exhaustive DFS, chunked by target; runs < 30 s.
import itertools, json, sys
def tables(n):
    N=1<<n; mask=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    return N,mask,ins
OPS=[o for o in range(16) if o not in (0,15,3,5,10,12)]  # drop consts, x, y, ~x, ~y
def ap(o,a,b,mask):
    r=0
    if o&1: r|=(~a&~b)
    if o&2: r|=(a&~b)
    if o&4: r|=(~a&b)
    if o&8: r|=(a&b)
    return r&mask
def minsize(n,target,maxg):
    N,mask,ins=tables(n)
    tw=set([target,(~target)&mask])
    for g in range(0,maxg+1):
        def dfs(nodes,left):
            if left==0: return any(t in tw for t in nodes)
            m=len(nodes)
            for i in range(m):
                for j in range(i+1,m):
                    for o in OPS:
                        v=ap(o,nodes[i],nodes[j],mask)
                        if v in nodes: continue
                        if left==1:
                            if v in tw: return True
                        elif dfs(nodes+[v],left-1): return True
            return False
        if any(t in tw for t in ins) and g==0: return 0
        if dfs(list(ins),g): return g
    return None
def maj3(): return sum(1<<x for x in range(8) if bin(x).count('1')>=2)
def fn(n,f):
    return sum(1<<x for x in range(1<<n) if f(x))
pc=lambda x:bin(x).count('1')
T={'AND2':(2,fn(2,lambda x:x==3),3),'XOR2':(2,fn(2,lambda x:pc(x)%2),3),
   'AND3':(3,fn(3,lambda x:x==7),3),'XOR3':(3,fn(3,lambda x:pc(x)%2),3),
   'MAJ3':(3,maj3(),5),'MUX3':(3,fn(3,lambda x:(x>>1&1) if x&1==0 else (x>>2&1)),5),
   'EXACT1_3':(3,fn(3,lambda x:pc(x)==1),5),'AND4':(4,fn(4,lambda x:x==15),3),'XOR4':(4,fn(4,lambda x:pc(x)%2),3)}
sel=sys.argv[1:] or list(T)
out={}
for k in sel:
    n,t,mg=T[k]; g=minsize(n,t,mg); out[k]={'n':n,'min_gates':g,'min_wires':None if g is None else 2*g}
    print(k,out[k],flush=True)
json.dump(out,open('minwires_results_%s.json'%('_'.join(sel) if sys.argv[1:] else 'all'),'w'),indent=1)

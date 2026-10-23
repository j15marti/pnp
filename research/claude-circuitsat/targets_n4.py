"""IDDFS exact B2 size for selected n=4 targets. Usage: python3 targets_n4.py <name> <maxg>; ordered-gate pruning
(new gate must use the previous gate OR be lexicographically >= previous pair) to cut symmetry."""
import sys, itertools, time
n=4;N=16;FULL=(1<<N)-1
ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
def tt(f): return sum(1<<x for x in range(N) if f([(x>>i)&1 for i in range(n)]))
T={"AND4":tt(lambda v:all(v)),"XOR4":tt(lambda v:sum(v)%2==0),
 "MAJ4ge2":tt(lambda v:sum(v)>=2),"EXACT2":tt(lambda v:sum(v)==2),
 "THR3of4":tt(lambda v:sum(v)>=3),
 "CNF3":tt(lambda v:(v[0] or v[1] or v[2]) and ((not v[0]) or v[1] or v[3]) and (v[0] or (not v[2]) or (not v[3]))),
 "CNF4":tt(lambda v:(v[0] or v[1] or v[2]) and ((not v[0]) or v[1] or v[3]) and (v[0] or (not v[2]) or (not v[3])) and ((not v[1]) or (not v[2]) or (not v[3])) and (v[1] or v[2] or v[3]))}
name=sys.argv[1]; maxg=int(sys.argv[2]); target=T[name]
def gates(a,b):
    na,nb=FULL^a,FULL^b
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,FULL^(a^b)}
t0=time.time()
def dfs(L,k,lastkey):
    if target in L or (FULL^target) in L: return True
    if k==0: return False
    # target must be reachable: if k==1 only need direct gate
    m=len(L)
    for i in range(m):
        for j in range(i+1,m):
            key=(j,i)
            if key<=lastkey and j<m-1: continue  # canonical order: gate must use newest or be later key
            a,b=L[i],L[j]
            for t in gates(a,b):
                if t in L or t in(0,FULL): continue
                if k==1 and t!=target and t!=FULL^target: continue
                if dfs(L+[t],k-1,key): return True
        if time.time()-t0>25: raise TimeoutError
    return False
for g in range(0,maxg+1):
    try: ok=dfs(list(ins),g,(-1,-1))
    except TimeoutError: print(name,"timeout at g",g,"(>=",g,"unproven)");break
    print(name,"g",g,ok,round(time.time()-t0,1),flush=True)
    if ok: print(name,"MIN_GATES",g,"wires",2*g);break

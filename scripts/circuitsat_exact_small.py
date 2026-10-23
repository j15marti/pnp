import itertools,sys
def tt_inputs(n):
    N=1<<n; return [sum(1<<a for a in range(N) if a>>i&1) for i in range(n)],(1<<N)-1
def minsize(n,target,maxg):
    ins,full=tt_inputs(n)
    ops=range(16)
    def ap(op,x,y):
        r=0
        for k in range(4):
            if op>>k&1:
                a,b=k&1,k>>1
                r|=(x if a else full^x)&(y if b else full^y)
        return r
    def rec(sigs,g):
        if target in sigs or (full^target) in sigs: return True if target in sigs else 'neg'
        if g==0: return False
        for i,j in itertools.combinations(range(len(sigs)),2):
            for op in range(1,15):
                v=ap(op,sigs[i],sigs[j])
                if v in sigs: continue
                r=rec(sigs+[v],g-1)
                if r: return True
        return False
    for g in range(0,maxg+1):
        if rec(list(ins),g): return g
    return None
# SAT for 1-CNF n vars: inputs p_i,q_i ; SAT = AND_i NAND(p_i,q_i)
def f(n):
    ins,full=tt_inputs(2*n); t=full
    for i in range(n): t&=full^(ins[2*i]&ins[2*i+1])
    return t
def nand4():
    ins,full=tt_inputs(4); a=full
    for x in ins:a&=x
    return full^a
print("1-CNF n=1:",minsize(2,f(1),3))
print("1-CNF n=2:",minsize(4,f(2),4))
print("2-CNF pair clauses n=2 (NAND4):",minsize(4,nand4(),4))

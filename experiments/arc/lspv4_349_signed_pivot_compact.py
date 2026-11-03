# LSPV-4/349 independently executable signed-pivot membership checker.
def eager(src,lines):
    a=[set(c) for c in src];m=len(src)
    for i,(l,r,p) in enumerate(lines):
        if min(l,r)<0 or max(l,r)>=m+i or p<1:return False
        if p not in a[l] or -p not in a[r]:return False
        a.append((a[l]-{p})|(a[r]-{-p}))
    return (not a[-1]) if lines else any(not c for c in src)
def member(src,lines,lit,node):
    m=len(src);reach={j for j,c in enumerate(src) if lit in c}
    for j,(l,r,p) in enumerate(lines):
        if (lit!=p and l in reach) or (lit!=-p and r in reach):
            reach.add(m+j)
    return node in reach
def check(src,lines,n):
    m=len(src)
    if not lines:return any(not c for c in src)
    for j,(l,r,p) in enumerate(lines):
        if min(l,r)<0 or max(l,r)>=m+j or not 1<=p<=n:return False
        if not member(src,lines,p,l) or not member(src,lines,-p,r):return False
    return not any(member(src,lines,v*s,m+len(lines)-1) for v in range(1,n+1) for s in (-1,1))
def horn(m):
    n=m-1
    src=[(1,)]+[(-i,i+1) for i in range(1,n)]+[(-n,)]
    proof=[(0 if i==0 else m+i-1,i+1,i+1) for i in range(m-1)]
    return n,src,proof
def main():
    assertions=0
    for m in range(2,25):
        n,src,proof=horn(m)
        assert eager(src,proof) and check(src,proof,n);assertions+=2
        sat=src.copy();sat[-1]=(n,)
        assert not eager(sat,proof) and not check(sat,proof,n);assertions+=2
    source=[(1,-1),(-1,)];fraud=[(0,1,1)]
    assert not eager(source,fraud) and not check(source,fraud,1);assertions+=2
    diamond=[(1,),(-1,2),(-1,3),(-2,-3)]
    dp=[(0,1,1),(0,2,1),(4,3,2),(5,6,3)]
    assert eager(diamond,dp) and check(diamond,dp,3);assertions+=2
    assert eager([()],[]) and check([()],[],1);assertions+=2
    print({'status':'PASS','assertions':assertions,'tautological_SAT_fraud':'REJECTED'})
if __name__=='__main__':main()

import json, math

def walk(x, j, invalid, oldpos):
    L=len(x); w=(L+2-1).bit_length(); origin=oldpos; t=0; scratch=list(map(int, format(j, f'0{w}b')))
    seen=set()
    if invalid: return '#',origin,1,len(seen)
    # Simulate physical local counter tape head, zero tests and decrements
    p=0
    def slide(dst):
        nonlocal p,t
        while p!=dst:
            p += 1 if p<dst else -1; seen.add(p); t +=1
    for i in range(w):
        slide(i); seen.add(i);t+=2 # charge address motion and copying
    while origin>0: origin-=1;t+=1
    origin+=1;t+=1
    while origin<=L:
        is_zero=True
        slide(0)
        for i in range(w):
            slide(i);t+=1
            if scratch[i]:is_zero=False
        if is_zero: return x[origin-1],origin,t+1,len(seen)
        origin+=1;t+=1
        if origin==L+1:break
        slide(w-1)
        i=w-1
        while True:
            seen.add(i);scratch[i]^=1;t+=1
            if scratch[i]==0:break
            i-=1
            assert i>=0
            slide(i)
    return '#',origin,t+1,len(seen)

stats={'pairs':0,'repeated':0,'mismatch':0,'maxCost':0,'maxScratch':0,'bothLabels':[0,0]}
for L in range(11):
    w=(L+1).bit_length()
    for a in range(1<<L):
        x=format(a,f'0{L}b') if L else ''
        oldpos=0
        for j in range(1<<w):
            for head in (0,(L+1)//2,L+1):
                got,p,t,s=walk(x,j,False,head)
                expected=x[j] if j<L else '#'
                assert got==expected and p<=L+1 and s<=w
                assert t<=50*(L+2)*(w+1)
                stats['pairs']+=1;stats['maxCost']=max(stats['maxCost'],t);stats['maxScratch']=max(stats['maxScratch'],s)
        for j in (0,(1<<w)-1):
            a1,p1,t1,s1=walk(x,j,False,oldpos)
            a2,p2,t2,s2=walk(x,j,False,p1)
            assert a1==a2
            stats['repeated']+=1
        # Finite controller observes parity of the queries 0..L-1
        parity=0
        for j in range(L):
            b,oldpos,_,_=walk(x,j,False,oldpos)
            parity^=int(b)
        assert parity==sum(map(int,x))%2
        stats['bothLabels'][parity]+=1
print(json.dumps(stats,sort_keys=True))

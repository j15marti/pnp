#!/usr/bin/env python3
"""Exact streamed optimal-cut traceback for a read-only width array.
The extended audit implements the faster width-bucket recurrence and
source-event-delta scans. This mini uses O(L*b*log L) work, O(b+log L)
numerical work entries, excludes output callback storage. NOT unrestricted SAT.
"""
import random, json

def reference(w,b):
    L=len(w)-1;d=b//2;D=[None]*(L+1);P=[None]*(L+1);D[0]=0
    for j in range(1,L+1):
        for i in range(max(0,j-b),j):
            if j<L and j-i<d:continue
            if D[i] is None:continue
            z=D[i]+(1<<(w[i]+w[j]))
            if D[j] is None or (z,i)<(D[j],P[j]):D[j]=z;P[j]=i
    assert D[L] is not None
    out=[];j=L
    while j:out.append((P[j],j));j=P[j]
    return D[L],out[::-1]

def memory_traceback(w,b,emit):
    L=len(w)-1;d=b//2
    stats={'source_probes':0,'max_buffer_entries':0,'max_depth':0}
    def access(i):stats['source_probes']+=1;return w[i]
    def peak(*arr):stats['max_buffer_entries']=max(
        stats['max_buffer_entries'],sum(len(z) for z in arr))
    def legal(i,j):return 1<=j-i<=b and (j==L or j-i>=d)
    def path(a,c,depth):
        stats['max_depth']=max(stats['max_depth'],depth)
        if a>=c:return
        if c-a<=2*b:
            D={a:0};P={}
            for j in range(a+1,c+1):
                opts=[(D[i]+(1<<(access(i)+access(j))),i)
                      for i in range(max(a,j-b),j) if i in D and legal(i,j)]
                if opts:D[j],P[j]=min(opts)
            assert c in D
            rev=[];j=c
            while j>a:i=P[j];rev.append((i,j));j=i
            peak(D,P,rev)
            del D,P
            for e in reversed(rev):emit(*e)
            return
        h=(a+c)//2;F={a:0}
        for j in range(a+1,h+1):
            opts=[F[i]+(1<<(access(i)+access(j)))
                  for i in range(max(a,j-b),j) if i in F and legal(i,j)]
            if opts:F[j]=min(opts)
            for old in [i for i in F if i<j-b+1]:del F[old]
        R={c:0}
        for i in range(c-1,h,-1):
            opts=[R[j]+(1<<(access(i)+access(j)))
                  for j in range(i+1,min(c,i+b)+1) if j in R and legal(i,j)]
            if opts:R[i]=min(opts)
            for old in [j for j in R if j>i+b-1]:del R[old]
        opts=[(F[i]+(1<<(access(i)+access(j)))+R[j],i,j)
              for i in F for j in R if legal(i,j) and i<=h<j]
        assert opts
        _,u,v=min(opts);peak(F,R);del F,R,opts
        path(a,u,depth+1)
        emit(u,v)
        path(v,c,depth+1)
    path(0,L,1)
    return stats

def width_trace(seed,n):
    rng=random.Random(seed);active=0;w=[0]
    for _ in range(n):
        step=rng.choice((-1,0,0,1))
        if active+step<0:step=0
        if active+step>9:step=-1
        active+=step;w.append(active)
    while active>0:active-=1;w.append(active)
    return w

def ternary_label_check():
    core=[tuple((-(j+1) if mask>>j&1 else j+1)
                for j in range(3)) for mask in range(8)]
    sat=core[:];sat[0]=core[1];unsat=core[:]
    def label(clauses):
        return any(all(any(bool(a>>(abs(l)-1)&1)==(l>0)
                           for l in C) for C in clauses) for a in range(8))
    return label(sat),label(unsat)

def main():
    checked=0;largest=0
    assert ternary_label_check()==(True,False);checked+=2
    for k in range(1,151):
        w=width_trace(200000+k,k)
        for b in (2,3,4,5,8,12,20,32):
            opt,_=reference(w,b);out=[]
            stat=memory_traceback(w,b,lambda i,j:out.append((i,j)))
            got=sum(1<<(w[i]+w[j]) for i,j in out)
            assert got==opt;checked+=1
            assert out[0][0]==0 and out[-1][1]==len(w)-1;checked+=1
            assert all(1<=j-i<=b and
                       (j==len(w)-1 or j-i>=b//2) for i,j in out);checked+=1
            assert all(out[i][1]==out[i+1][0]
                       for i in range(len(out)-1));checked+=1
            largest=max(largest,stat['max_buffer_entries'])
    print(json.dumps({'name':'LINEAR-SPACE-CUT-REPLAY127-mini',
       'scope':'read-only width-array; not general SAT lower bound',
       'tests':1200,'assertions':checked,
       'largest_abstract_work_buffer_entries':largest,
       'errors':0,'ARC-EDGE-90':'OPEN'},sort_keys=True))

if __name__=='__main__':main()

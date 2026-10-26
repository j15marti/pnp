#!/usr/bin/env python3
"""CIRCUIT-SWITCH-INVERSE167: table-free inverse Rank/Select for the saved
swap-output gate of each comparator in the fixed verifier of report 166.
Standard-library only. Run: python script.py [raw.json]
"""
import json,random,sys
from collections import Counter
W1_TEXT='''-1 3 -14 2 -8 9 10 -13 14 3 7 -13 -4 -9 -11 5 8 -14 4 -8 -11 1 7 13 1 -7 10 -5 -6 -15 -2 -6 12 -4 9 -10 -2 5 -12 -3 6 -15 6 -7 11 2 -9 11 4 8 -10 -3 12 15 -5 -12 15 -1 13 14'''
T=list(map(int,W1_TEXT.split()))
W1=[tuple(T[i:i+3]) for i in range(0,len(T),3)]
def stages(h):
    return [(j,b) for j in range(1,h+1) for b in range(j-1,-1,-1)]
def loc(h,layer,p):
    s=1<<stages(h)[layer][1];i=p&~s
    return (i//(2*s))*s+i%s,i,i+s
def cidx(h,layer,p):
    return layer*(1<<h)//2+loc(h,layer,p)[0]
def sg(h,w,layer,p):
    D=w+3
    return cidx(h,layer,p)*(7*(w+2)+6*D)+7*(w+2)-5
def switch_select(h,w,layer,p,r):
    D=w+3;H=7*(w+2);A=H+6*D;K=1<<h;L=len(stages(h))
    c=cidx(h,layer,p)
    assert 0<=r<4*D+4
    if r<4*D:
        mux,t=divmod(r,2)
        return c*A+H+3*mux+t,0,(-1 if t==0 else 1)
    ci=(L-1-layer)*(K//2)+loc(h,layer,p)[0]
    base=(K//2)*L*A+19*K+(K-1)*(4*w-1)+6*ci
    t=(0,1,3,4)[r-4*D]
    return base+t,0,(-1 if t in (0,3) else 1)
def switch_rank(h,w,layer,p,g,slot):
    D=w+3;H=7*(w+2);A=H+6*D;K=1<<h;L=len(stages(h))
    c=cidx(h,layer,p)
    t=g-c*A-H
    if slot==0 and 0<=t<6*D:
        mux,j=divmod(t,3)
        if j<2:return 2*mux+j
    ci=(L-1-layer)*(K//2)+loc(h,layer,p)[0]
    base=(K//2)*L*A+19*K+(K-1)*(4*w-1)+6*ci
    t=g-base
    return 4*D+{0:0,1:1,3:2,4:3}[t] if slot==0 and t in (0,1,3,4) else None
def cnf_select(h,w,layer,p,r):
    D=w+3;g=sg(h,w,layer,p)
    assert 0<=r<5+4*(4*D+4)
    if r<5:return (13*g+8+r,2 if r==0 else 1,0 if r==0 else 1)
    u,v=divmod(r-5,4);gg,slot,s= switch_select(h,w,layer,p,u)
    assert slot==0
    return (13*gg+v,1,int(s>0) if v<2 else int(s<0))
def cnf_rank(h,w,layer,p,c,pos):
    g=sg(h,w,layer,p);gg,row=divmod(c,13)
    if gg==g and 8<=row<=12 and pos==(2 if row==8 else 1):return row-8
    if row<4 and pos==1:
        t=switch_rank(h,w,layer,p,gg,0)
        if t is not None:return 5+4*t+row
    return None
def comparator_independent(w):
    """Construct real local operator-operand descriptors, independent of Select."""
    D=w+3;A=list(range(1,D+1));B=list(range(D+1,2*D+1))
    C0=2*D+1;C1=2*D+2;gates=[]
    def gate(op,a,b):
        gates.append((op,a,b));return 2*D+2+len(gates)
    def AND(a,b):return gate('and',a,b)
    def OR(a,b):return gate('or',a,b)
    def EQ(a,b):return -OR(AND(a,-b),AND(-a,b))
    av=A[w:w+2]+A[:w];bv=B[w:w+2]+B[:w]
    less,eq=C0,C1
    for x,y in zip(reversed(bv),reversed(av)):
        less=OR(less,AND(eq,AND(-x,y)))
        eq=AND(eq,EQ(x,y))
    sigma=less;H=7*(w+2)
    for ix in range(D):
        OR(AND(-sigma,A[ix]),AND(sigma,B[ix]))
    for ix in range(D):
        OR(AND(-sigma,B[ix]),AND(sigma,A[ix]))
    assert len(gates)==H+6*D and sigma-(2*D+3)==H-5
    uses=[]
    for i,(_,a,b) in enumerate(gates):
        if abs(a)==sigma:uses.append((i,0,1 if a>0 else -1))
        if abs(b)==sigma:uses.append((i,1,1 if b>0 else -1))
    expected=[(H+3*k+t,0,-1 if t==0 else 1)
              for k in range(2*D) for t in (0,1)]
    assert uses==expected
def sat(F):
    for mask in range(1<<15):
        if all(any(((mask>>(abs(z)-1))&1)==int(z>0) for z in c) for c in F):
            return mask
    return None
def run():
    comps=ops=occ=trials=0;cases=[]
    for h in range(2,7):
        K=1<<h;L=len(stages(h))
        for w in (2,4,8):
            comparator_independent(w)
            count=0
            for layer in range(L):
                for p in range(K):
                    r,i,j=loc(h,layer,p)
                    if p!=i:continue
                    count+=1;D=w+3
                    assert loc(h,layer,j)[0]==r and sg(h,w,layer,i)==sg(h,w,layer,j)
                    S=[switch_select(h,w,layer,p,v) for v in range(4*D+4)]
                    assert len(set((a,b) for a,b,_ in S))==len(S)
                    assert all(switch_rank(h,w,layer,p,a,b)==v
                               for v,(a,b,z) in enumerate(S))
                    O=[cnf_select(h,w,layer,p,v) for v in range(5+4*len(S))]
                    assert O==sorted(O,key=lambda x:(x[0],x[1]))
                    assert len(set((a,b) for a,b,_ in O))==len(O)
                    assert Counter(v for a,b,v in O)=={0:8*D+9,1:8*D+12}
                    assert all(cnf_rank(h,w,layer,p,a,b)==v
                               for v,(a,b,z) in enumerate(O))
                    ops+=len(S);occ+=len(O)
            assert count==K*h*(h+1)//4
            comps+=count;cases.append(dict(K=K,w=w,comparators=count))
        rng=random.Random(123456+h)
        for _ in range(100):
            R=[(rng.randrange(K//2+1),rng.randrange(3),i) for i in range(K)]
            old=R[:];hist=[]
            for layer,(j,b) in enumerate(stages(h)):
                after=R[:];pair=[]
                for p in range(K):
                    rank,i,z=loc(h,layer,p)
                    if p!=i:continue
                    forward=(i&(1<<j))==0
                    sw=(R[z][:2]<R[i][:2]) if forward else (R[i][:2]<R[z][:2])
                    if sw:after[i],after[z]=R[z],R[i]
                    pair.append((i,z,sw))
                R=after;hist.append(pair)
            for pair in reversed(hist):
                for i,j,sw in pair:
                    if sw:R[i],R[j]=R[j],R[i]
            assert R==old;trials+=1
    assert sat(W1) is None and all(sat(W1[:i]+W1[i+1:]) is not None for i in range(20))
    profiles=Counter((abs(z),int(z>0)) for c in W1 for z in c)
    assert all(profiles[(v,0)]==profiles[(v,1)]==2 for v in range(1,16))
    witness=sat(W1[:-1]);controls=[]
    for k in (1,2,3,5,8):
        original=[tuple((1 if z>0 else -1)*(abs(z)+15*i) for z in c)
                  for i in range(k) for c in W1]
        connected=original+[(15*i+1,15*(i+1)+1,15*k+i+1)
                             for i in range(k-1)]
        SAT=[tuple((1 if z>0 else -1)*(abs(z)+15*i) for z in c)
             for i in range(k) for c in W1[:-1]]+connected[len(original):]
        V={15*i+j+1:(witness>>j)&1 for i in range(k) for j in range(15)}
        V.update({15*k+i+1:1 for i in range(k-1)})
        assert all(len(set(map(abs,c)))==3 for c in connected+SAT)
        assert all(any(V[abs(z)]==int(z>0) for z in c) for c in SAT)
        controls.append(dict(k=k,clauses_unsat=len(connected),clauses_sat=len(SAT),
                             global_clause_hitting_lower_bound=k))
    raw=dict(run="CIRCUIT-SWITCH-INVERSE167",comparators_checked=comps,
             swap_operand_occurrences_checked=ops,source_cnf_occurrences_checked=occ,
             inverse_sorting_trials=trials,failed_assertions=0,
             W1_minimally_unsat=True,connected_sat_unsat_controls=controls,
             comparator_cases=cases,
             status="restricted sigma-output source-CNF Rank/Select proved; full compiler inverse and ARC OPEN")
    with open(sys.argv[1] if len(sys.argv)>1 else "CIRCUIT_SWITCH_INVERSE167_raw.json","w") as f:
        json.dump(raw,f,indent=2,sort_keys=True)
    print(json.dumps({k:raw[k] for k in
          ("comparators_checked","swap_operand_occurrences_checked",
           "source_cnf_occurrences_checked","inverse_sorting_trials","failed_assertions")}))
if __name__=="__main__":run()

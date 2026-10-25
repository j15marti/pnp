#!/usr/bin/env python3
"""Deterministic exhaustive q=3 three-defect palette audit, 2026-10-24.
No external dependencies. All computational statements are finite only.
"""
import itertools, collections, json

K6=range(6)
TRIPLES=list(itertools.combinations(K6,3))
FAMS=[frozenset(x) for x in itertools.combinations(TRIPLES,4)
      if all(sum(v in e for e in x)==2 for v in K6)]
PAIRS=list(itertools.combinations(range(4),2))

def valid(P,Q,n):
    if len(set(P))!=len(P) or len(set(Q))!=len(Q):return False
    if any(len(e)!=3 or len(set(e))!=3 for e in list(P)+list(Q)):return False
    return all(sum(v in e for e in P)==sum(v in e for e in Q)==2 for v in range(n))

def lex4(P,n):
    edges=[set(e) for e in P];adj=[set() for _ in range(n)]
    for e in edges:
        for u in e:adj[u].update(e-{u})
    c=[-1]*n
    def rec(i):
        if i==n:return True
        for col in range(4):
            if all(c[u]!=col for u in adj[i]):
                c[i]=col
                if rec(i+1):return True
        c[i]=-1;return False
    assert rec(0)
    return c

def two_color_witness(P,Q,c):
    for false in PAIRS:
        bits=tuple(int(col not in false) for col in c)
        if all(any(bits[v] for v in e) for e in P) and all(any(not bits[v] for v in e) for e in Q):
            return bits, false
    return None,None

def nae_pairing_witness(P,Q,c):
    for false in [(0,1),(0,2),(0,3)]:
        bits=tuple(int(col not in false) for col in c)
        if all(0<sum(bits[v] for v in e)<3 for e in set(P)|set(Q)):
            return bits,false
    return None,None

def obstruction(Qx,c):
    colors=[frozenset(c[v] for v in e) for e in Qx]
    for a,b in itertools.combinations(range(3),2):
        if len(colors[a])==len(colors[b])==1 and colors[a]!=colors[b]:
            z=3-a-b
            if not ((colors[a]|colors[b]) & colors[z]):return True
    return False

def intersecting(E):
    return any(set(a)&set(b) for a,b in itertools.combinations(E,2))

def brute_models(P,Q,n,nae=False):
    out=[]
    for x in itertools.product((0,1),repeat=n):
        if all(any(x[v] for v in e) for e in P) and all(any(not x[v] for v in e) for e in Q):
            if not nae or all(0<sum(x[v] for v in e)<3 for e in set(P)|set(Q)):
                out.append(x)
    return out

def gamma(i):
    assert i>=1
    s=bin(i)[2:]
    return '0'*(len(s)-1)+s

def encode_len(P,Q,n):
    records=[(1,e) for e in sorted(P)]+[(0,e) for e in sorted(Q)]
    return len(gamma(n)+gamma(len(records))+''.join(gamma(len(e))+str(s)+''.join(gamma(v+1) for v in e) for s,e in records))

def restrict(P,Q,values):
    def redu(E,s):
        ans=[]
        for e in E:
            if any(v in values and values[v]==s for v in e):continue
            ans.append(tuple(v for v in e if v not in values))
        return ans
    return redu(P,1),redu(Q,0)

rows=[(0,1,2),(3,4,5),(6,7,8)]
cols=[(0,3,6),(1,4,7),(2,5,8)]
diags=[(0,4,8),(1,5,6),(2,3,7)]
GRIDP=rows+diags;GRIDQ=cols+diags

def main():
    assert len(FAMS)==75
    result={'version':'M22-Q3-INTERSECTION-HIT106','total_k6':0,'q_hist':collections.Counter(),
       'q3':{'cases':0,'nae_palette_success':0,'signed_palette_success':0,
             'signed_rescues':0,'signed_palette_fail':0,'intersecting_P':0,'intersecting_Q':0,
             'obstruction_iff_fail':0,'signed_palette_fail_bad_disjoint':0},
       'grid':{},'format':'0-based source variables and exact proper ternary support lists'}
    for P0 in FAMS:
        P=sorted(P0);col=lex4(P,6)
        for Q0 in FAMS:
            Q=sorted(Q0)
            assert valid(P,Q,6)
            H=set(P)&set(Q);q=4-len(H)
            result['total_k6']+=1;result['q_hist'][str(q)]+=1
            if q!=3:continue
            Qx=sorted(set(Q)-H);Px=sorted(set(P)-H)
            rec=result['q3'];rec['cases']+=1
            x_n,p_n=nae_pairing_witness(P,Q,col)
            x_s,p_s=two_color_witness(P,Q,col)
            if x_n is not None:rec['nae_palette_success']+=1
            if x_s is not None:rec['signed_palette_success']+=1
            else:rec['signed_palette_fail']+=1
            if x_n is None and x_s is not None:rec['signed_rescues']+=1
            obs=obstruction(Qx,col)
            assert obs==(x_s is None)
            rec['obstruction_iff_fail']+=1
            if intersecting(Px):
                rec['intersecting_P']+=1
                assert x_s is not None
            if intersecting(Qx):
                rec['intersecting_Q']+=1
                assert x_s is not None
            if x_s is None:
                assert not intersecting(Px) and not intersecting(Qx)
                rec['signed_palette_fail_bad_disjoint']+=1
            assert brute_models(P,Q,6)
    assert result['total_k6']==5625
    assert valid(GRIDP,GRIDQ,9)
    grid_H=set(GRIDP)&set(GRIDQ)
    assert len(grid_H)==3
    grid_fixed_colors=[v%3 for v in range(9)]
    assert all(len(set(grid_fixed_colors[v] for v in e))==3 for e in GRIDP)
    assert obstruction(cols,grid_fixed_colors)
    x0,p0=two_color_witness(GRIDP,GRIDQ,grid_fixed_colors)
    assert x0 is None
    grid_model=brute_models(GRIDP,GRIDQ,9)
    grid_nae=brute_models(GRIDP,GRIDQ,9,True)
    assert grid_model and grid_nae
    for vals in ({},{0:0},{0:0,1:0},{0:1,1:1}):
        pp,qq=restrict(GRIDP,GRIDQ,vals)
        independent=[x for x in grid_model if all(x[v]==b for v,b in vals.items())]
        tail=[x for x in brute_models(pp,qq,9) if all(x[v]==b for v,b in vals.items())]
        assert len(independent)==len(tail)
    sizes=[]
    for vals in ({},{0:0},{0:0,1:0}):
        pp,qq=restrict(GRIDP,GRIDQ,vals)
        sizes.append({'pins':len(vals),'bits':encode_len(pp,qq,9),
                     'clause_widths':sorted(set(len(e) for e in pp+qq)),
                     'M22_source_eligible':valid(pp,qq,9)})
    result['grid']={'k':9,'q':3,'P':GRIDP,'Q':GRIDQ,'first_palette_failure':True,
        'SAT_model_count':len(grid_model),'NAE_model_count':len(grid_nae),
        'SAT_witness':''.join(map(str,grid_model[0])),'two_pin_sizes':sizes}
    with open('M22_Q3_INTERSECTION_HIT106_results.json','w') as f:json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()

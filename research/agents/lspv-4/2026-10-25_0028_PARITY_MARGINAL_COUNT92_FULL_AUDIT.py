#!/usr/bin/env python3
"""LSPV-4 PARITY-MARGINAL-COUNT96: exact independent finite audit.

All counts include globally declared auxiliary variables even if their pin
clauses are deleted. No dependency beyond standard Python.
"""
import json, itertools, collections, hashlib

def clause(*x):
    assert len(x) in (2,3) and len({abs(v) for v in x})==len(x) and 0 not in x
    return tuple(x)

def pin(x,v,u,w):
    l=x if v else -x
    return [clause(l,u,w),clause(l,u,-w),clause(l,-u,w),clause(l,-u,-w)]

def xor3(a,b,c,e):
    out=[]
    for A,B,C in itertools.product(range(2),repeat=3):
        if (A^B^C)!=e:
            out.append(clause(-a if A else a,-b if B else b,-c if C else c))
    assert len(out)==4
    return out

def form(q,e):
    assert len(e)==q and q>=1
    x=list(range(1,q+1)); z=list(range(q+1,2*q+1))
    u0,v0=2*q+1,2*q+2
    t=1^(q&1)
    if e[0]==0: base=[clause(-z[0],x[0]),clause(z[0],-x[0])]
    else: base=[clause(z[0],x[0]),clause(-z[0],-x[0])]
    for j in range(1,q):base.extend(xor3(z[j-1],x[j],z[j],e[j]))
    base.extend(pin(z[-1],t,u0,v0))
    blocks=[]
    for j in range(q):
        u=2*q+3+2*j
        blocks.append(pin(x[j],1,u,u+1))
    n=4*q+2
    assert len(base)==4*q+2 and sum(map(len,base))==12*q+4
    full=base+[c for b in blocks for c in b]
    assert len(full)==8*q+2
    assert max(abs(t) for c in full for t in c)==n
    w=(64*(n+len(full)+1)-1).bit_length()
    assert w==(64*(12*q+5)-1).bit_length()
    N=(4*len(full)+2)*w
    return dict(q=q,e=e,n=n,m=len(full),N=N,base=base,blocks=blocks,vars=x,z=z,t=t,w=w)

def serialized(d, cs=None):
    """Header and fixed four-field clause records, with 0 padded slot."""
    clauses=cs if cs is not None else (d['base']+[c for b in d['blocks'] for c in b])
    m=len(clauses);n=d['n'];w=(64*(n+m+1)-1).bit_length()
    words=[n,m]
    for cl in clauses:
        words.extend([len(cl)]+[(abs(z)*2+int(z<0)) for z in cl]+[0]*(3-len(cl)))
    assert len(words)==4*m+2
    assert max(words) < (1<<w)
    return words,w

def satisfies(cs,mask):
    for c in cs:
        if not any((((mask>>(abs(v)-1))&1)==int(v>0)) for v in c):return False
    return True

def brute_base_profile(d):
    q=d['q']; prof=collections.Counter()
    for mask in range(1<<d['n']):
        if satisfies(d['base'],mask):
            xm=mask & ((1<<q)-1)
            prof[xm]+=1
    return prof

def pin_cnt_from_profile(prof,S,a):
    return sum(v for x,v in prof.items() if all(((x>>i)&1)==v0 for i,v0 in zip(S,a)))

def theoretical(q,e,S,a):
    assert len(S)==len(a)
    t=q&1
    if len(S)<q:return (4**(q+1))*(2**(q-len(S)-1))
    xpar=0
    for v in a:xpar^=v
    return 4**(q+1) if xpar==(t^1^ (sum(e)&1)) else 0

def all_queries(q):
    for choices in itertools.product((-1,0,1),repeat=q):
        S=[i for i,z in enumerate(choices) if z>=0]
        a=[choices[i] for i in S]
        yield S,a

def audit():
    res={'claim':'PARITY-MARGINAL-COUNT96','status':'COMPUTATIONAL','method':'independent truth-table enumeration of declared full base variables','q':{},'assertions':0,'failures':0}
    for q in range(1,4):
        pairs=0;quer=0;source_changes=0
        for e in itertools.product((0,1),repeat=q):
            d=form(q,e); prof=brute_base_profile(d)
            pairs+=1
            for xm in range(1<<q):
                # Each legal x has a unique functional XOR extension and 2(q+1) free helpers.
                expected=(4**(q+1) if (xm.bit_count()&1)==((q&1)^1^(sum(e)&1)) else 0)
                assert prof[xm]==expected,(q,e,xm,prof[xm],expected)
                res['assertions']+=1
            for S,a in all_queries(q):
                observed=pin_cnt_from_profile(prof,S,a)
                expected=theoretical(q,e,S,a)
                assert observed==expected,(q,e,S,a,observed,expected)
                quer+=1;res['assertions']+=1
                if len(S)<q:
                    assert observed == (4**(q+1))*(1<<(q-len(S)-1))
                    res['assertions']+=1
            assert len(d['blocks'])==q and len(d['base'])+sum(map(len,d['blocks']))==d['m']
            res['assertions']+=1
        for pinvalue in [0,1]:
            x,u,v=1,2,3
            cs=pin(x,pinvalue,u,v)
            assert sum(satisfies(cs,m) for m in range(8))==4
            for mask in range(8):
                assert satisfies(cs,mask)==(((mask&1)!=0)==bool(pinvalue))
                res['assertions']+=1
        for i in range(q):
            zeros=(0,)*q
            flip=tuple(int(j==i) for j in range(q))
            d0=form(q,zeros);di=form(q,flip)
            assert d0['n']==di['n'] and d0['m']==di['m'] and d0['N']==di['N']
            words0,w0=serialized(d0);wordsi,wi=serialized(di)
            assert len(words0)*w0==d0['N']==len(wordsi)*wi
            assert words0[:2]==wordsi[:2]
            changed={j for j,(a,b) in enumerate(zip(words0,wordsi)) if a!=b}
            assert changed and len(changed)<=16
            # Row i occupies source position 0/1 or four proper XOR3 clauses.
            expected_clauses=range(0,2) if i==0 else range(2+4*(i-1),2+4*i)
            authorized=set().union(*(set(range(2+4*c,2+4*c+4)) for c in expected_clauses))
            assert changed <= authorized,(q,i,changed,authorized)
            res['assertions']+=5
            assert all(d0['blocks'][j]==di['blocks'][j] for j in range(q))
            assert all(sum(map(len, b))>0 for b in d0['blocks'])
            assert theoretical(q,zeros,list(range(q)),[1]*q)==0
            assert theoretical(q,flip,list(range(q)),[1]*q)==4**(q+1)
            assert all(theoretical(q,zeros,S,a)==theoretical(q,flip,S,a) for S,a in all_queries(q) if len(S)<q)
            source_changes+=1;res['assertions']+=6
        res['q'][q]={'full_brute_orientations':pairs,'queries_verified':quer,'single_flip_sensitivities':source_changes,'n':form(q,(0,)*q)['n'],'m':form(q,(0,)*q)['m'],'N':form(q,(0,)*q)['N']}
    # independent symbolic growing controls and opposite label bookkeeping
    for q in (4,8,16,32,128,1024):
        zero=(0,)*q
        d=form(q,zero)
        for k in sorted({0,1,q//2,q-1}):
            S=list(range(k));a=[1]*k
            assert theoretical(q,zero,S,a)==4**(q+1)*(1<<(q-k-1))
            res['assertions']+=1
        assert theoretical(q,zero,list(range(q)),[1]*q)==0
        assert theoretical(q,tuple([1]+[0]*(q-1)),list(range(q)),[1]*q)==4**(q+1)
        res['assertions']+=2
        res['q'][q]={'symbolic_only':True,'n':d['n'],'m':d['m'],'N':d['N']}
    return res

if __name__=='__main__':
    r=audit()
    s=json.dumps(r,sort_keys=True,indent=2)
    p='/mnt/data/arc_parity_marginal96/PARITY_MARGINAL96_RESULTS.json'
    open(p,'w').write(s+'\n')
    print(s)

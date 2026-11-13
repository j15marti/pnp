#!/usr/bin/env python3
"""LSPV-4/584 independent seven-fixture signed SOURCE weighted resource frontier.
Stdlib Python 3.10+. This is NOT a unified historical R_mix341 checker.
Usage: python3 experiments/arc/lspv4_584_weighted_source_frontier.py [--out path]
"""
import itertools, collections, json, sys
from fractions import Fraction

def graphs():
    k4=list(itertools.combinations(range(4),2))
    k33=[(i,j) for i in range(3) for j in range(3,6)]
    cube=[(i,i^(1<<b)) for i in range(8) for b in range(3) if i<i^(1<<b)]
    pet=[e for i in range(5) for e in [(i,(i+1)%5),(i+5,(i+2)%5+5),(i,i+5)]]
    def prism(k): return [e for i in range(k) for e in [(i,(i+1)%k),(i+k,(i+1)%k+k),(i,i+k)]]
    bridge=[]
    for o in (0,5):
        bridge.extend((i+o,j+o) for i,j in itertools.combinations(range(4),2) if (i,j)!=(0,1))
        bridge.extend(((o,o+4),(o+1,o+4)))
    bridge.append((4,9))
    return [('K4',4,k4),('K33',6,k33),('CUBE',8,cube),('PETERSEN',10,pet),
            ('PRISM6',12,prism(6)),('PRISM16',32,prism(16)),('BRIDGE_K4x2',10,bridge)]

def solve(edges,charges,pin,skip):
    E=len(edges); basis={}
    for v in range(len(charges)):
        if v==skip: continue
        mask=0;rhs=charges[v]
        for e,(a,b) in enumerate(edges):
            if v not in (a,b): continue
            if e in pin: rhs^=pin[e]
            else:mask|=1<<e
        while mask:
            p=(mask&-mask).bit_length()-1
            if p not in basis: basis[p]=(mask,rhs);break
            m,r=basis[p];mask^=m;rhs^=r
        if mask==0 and rhs:return None
    ans=[0]*E
    for e,b in pin.items():ans[e]=b
    for p in sorted(basis,reverse=True):
        mask,rhs=basis[p]
        for j in range(p+1,E):
            if mask>>j&1:rhs^=ans[j]
        ans[p]=rhs
    for v in range(len(charges)):
        if v!=skip:assert charges[v]==(sum(ans[e] for e,(a,b) in enumerate(edges) if v in (a,b))%2)
    return ans

def probes(lits,w):
    for k,l in enumerate(lits,1):
        if w[abs(l)-1]==int(l>0):return k
    return 3

def comparisons(lits):
    a=[abs(l) for l in lits];n=0
    for i in (1,2):
        x=a[i];j=i-1
        while j>=0:
            n+=1
            if a[j]<=x:break
            a[j+1]=a[j];j-=1
        a[j+1]=x
    return n

def audit():
    rows=[];savings=[];source=0;witness=0;checks=0;controls=0
    for name,V,edges in graphs():
        E=len(edges);charges=[1]+[0]*(V-1)
        assert E*2==3*V and all(sum(v in e for e in edges)==3 for v in range(V))
        inc=[[i for i,e in enumerate(edges) if v in e] for v in range(V)]
        clauses=[]
        for v in range(V):
            for pat in range(8):
                if pat.bit_count()%2==charges[v]:continue
                lits=tuple(-(e+1) if pat>>i&1 else e+1 for i,e in enumerate(inc[v]))
                clauses.append((v,pat,lits))
        assert len(clauses)==4*V
        ws=[];null=0
        for v,pat,lits in clauses:
            w=solve(edges,charges,{e:pat>>i&1 for i,e in enumerate(inc[v])},v)
            if w is None:null+=1;continue
            ws.append(w)
            for _,_,other in clauses:
                assert any(w[abs(l)-1]==int(l>0) for l in other)==(other!=lits)
                checks+=1
        qmin=smin=jmin=0;positive=[]
        for v,pat,lits in clauses:
            opts=[]
            for perm in itertools.permutations(lits):
                assert sorted(perm)==sorted(lits)
                for assignment in itertools.product((0,1),repeat=3):
                    bits={e:assignment[i] for i,e in enumerate(inc[v])}
                    assert any(bits[abs(l)-1]==int(l>0) for l in perm)==any(bits[abs(l)-1]==int(l>0) for l in lits)
                    checks+=1
                q=sum(probes(perm,w) for w in ws);s=comparisons(perm)
                assert s in (2,3)
                opts.append((q,s))
            q2=min(q for q,s in opts if s==2)
            q3=min(q for q,s in opts if s==3)
            qmin+=min(q2,q3);smin+=2;jmin+=min(q2+2,q3+3)
            delta=max(0,q2-q3)
            if delta:
                assert delta>=2
                positive.append(delta);savings.append(delta)
            if name=='K4' and len(positive)==0:pass
        row={'fixture':name,'source':len(clauses),'witness':len(ws),
             'null_witness':null,'min_Q':qmin,'min_S':smin,'min_Q_plus_S':jmin,
             'positive_improvements':len(positive),'gain_to_sort_min':sum(positive)}
        rows.append(row);source+=len(clauses);witness+=len(ws)
    Q=sum(r['min_Q'] for r in rows);S=sum(r['min_S'] for r in rows)
    J=sum(r['min_Q_plus_S'] for r in rows)
    assert (Q,S,J,source,witness,len(savings))==(29238,656,30061,328,324,167)
    hist=collections.Counter(savings)
    assert (min(hist),max(hist),len(hist),sum(k*v for k,v in hist.items()))==(2,234,49,9462)
    def value(lam):return Q+S*lam+sum(min(lam,d) for d in savings)
    kinks=[];slope=S+len(savings)
    for d,n in sorted(hist.items()):
        kinks.append({'weight':d,'multiplicity':n,'slope_before':slope,
                      'slope_after':slope-n,'weighted_minimum_at_kink':value(d)})
        slope-=n
    assert slope==S
    assert value(Fraction(1))==J
    assert value(Fraction(235))==Q+9462+235*S
    return {'schema':'LSPV4_584_WEIGHTED_SOURCE_ALIAS_FRONTIER/v1',
       'date':'2026-11-13 America/Los_Angeles',
       'scope':'Independent original /341 SOURCE generation and fixed deletion-witness replay, NOT full historical mixed calculus or original-checker OS execution',
       'pins':{'original_producer_blob':'4081022e8a3841d79f751a3d3a7a10decbb026da',
               'original_checker_blob':'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
               'original_packet_blob':'fe27fe1011d0021e721ccaeb747ed58da65d7464'},
       'metrics':{'source':source,'nonnull_witnesses':witness,'literal_semantic_checks':checks,
                  'min_Q':Q,'min_S':S,'min_Q_plus_S':J,'conflicting_clauses':len(savings),
                  'min_Q_requires_S':823,'min_S_requires_Q':Q+sum(savings),
                  'gain_to_sort_min':sum(savings),'unique_positive_kinks':len(hist)},
       'theorem':'min for lambda>=0 of Q+lambda*S = 29238+656*lambda + sum_d multiplicity(d)*min(lambda,d)',
       'histogram':{str(k):v for k,v in sorted(hist.items())},'kinks':kinks,'fixtures':rows,
       'limitations':['S counts explicit insertion-sort comparisons, NOT original Node.js implementation or native logical rule cost',
                      'Original checker acceptance for SOURCE order aliases inherited from peer audits, not executed here',
                      'All other mixed-rule, branching, DEF, sharing, memory, extension and compact-representation shortcuts remain open'],
       'open':['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],'P_versus_NP':'OPEN'}

if __name__=='__main__':
    obj=audit()
    if '--out' in sys.argv:
        from pathlib import Path
        path=Path(sys.argv[sys.argv.index('--out')+1])
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','metrics':obj['metrics'],'kinks':len(obj['kinks'])}))

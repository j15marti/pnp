#!/usr/bin/env python3
"""Source-indexed S/U targets, 4-mode clause pairs, actual coherent flip/XOR,
and capped UP-DPLL controls. All offline; not native FLMV solver work.
Run from a checked out repository: python experiments/arc/lspv1_285/diagnostics285.py
"""
import collections,itertools,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
SRC=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
text=SRC.read_text();U=tuple(tuple(q) for q in json.loads(text[text.index('[['):]))
V=[list(q) for q in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(tuple(q) for q in V)

def tcounts(F,a):
    return [sum(a[abs(z)-1]==int(z>0) for z in C) for C in F]

def audit(F,n,kind):
    local=[{'j':j,'literal_occurrences':[{'x_ij':f'x_{{{abs(z)},{j}}}',
           'signed_literal':z,'S_j':int(z>0),'inverse_S_j_U_j':int(z<0),
           'U_j':int(z<0),'inverse_U_j_S_j':int(z>0)} for z in C]}
           for j,C in enumerate(F)]
    pairmasks=[];pairclasses=collections.Counter();pairdiff=[]
    for j,C in enumerate(F):
        for k in range(j+1,len(F)):
            D=F[k]
            same=any(abs(x)==abs(y) and x*y>0 for x in C for y in D)
            opp=any(abs(x)==abs(y) and x*y<0 for x in C for y in D)
            mask=(int(not opp),int(not same),int(not same),int(not opp))
            mask_string=''.join(map(str,mask))
            pairmasks.append(mask_string);pairclasses[mask_string]+=1
            if same or opp:pairdiff.append({'j':j,'k':k,'SS_SU_US_UU':mask})
    endpoints=[]
    for tag,a in [('all_zero',[0]*n),('all_one',[1]*n)]:
        ts=tcounts(F,a)
        endpoints.append({'name':tag,'histogram':[ts.count(q) for q in range(4)],
            'falsified_original_clause_IDs':[i for i,q in enumerate(ts) if q==0],
            'first_12_true_literal_counts':ts[:12]})
    a=[0]*n;last=tcounts(F,a);trail=[];binary=0;gray=0
    for i in range(n):
        a[i]=1;now=tcounts(F,a)
        changed=[j for j,(p,q) in enumerate(zip(last,now)) if p!=q]
        d_bin=sum((p^q).bit_count() for p,q in zip(last,now))
        d_gray=sum(((p^(p>>1))^(q^(q>>1))).bit_count() for p,q in zip(last,now))
        binary+=d_bin;gray+=d_gray
        if i<8 or i==n-1:
            trail.append({'flipped_original_variable':i+1,'changed_original_clause_IDs':changed,
                'clause_status_binary_XOR':d_bin,'clause_status_gray_XOR':d_gray,
                'N0_N1_N2_N3':[now.count(q) for q in range(4)]})
        last=now
    assert binary==4*len(F) and gray==3*len(F)
    return {'source':kind,'n':n,'m':len(F),'local_source_S_U_with_inverses':local,
            'pair_matrix_order':'j=0,...,m-1 and k=j+1,...,m-1',
            'pair_modes_4bit_lex':''.join(pairmasks),
            'pair_mode_histogram':dict(pairclasses),
            'overlapping_original_clause_pairs':pairdiff,
            'globally_consistent_endpoints':endpoints,'flip_trail':trail,
            'full_monotone_binary_count_XOR':binary,'full_monotone_gray_count_XOR':gray,
            'physical_XOR_not_inferred':True}

def up_dpll(F,n,cap):
    nodes=0;probes=0;calls=0
    def rec(G):
        nonlocal nodes,probes,calls
        if nodes>=cap:return None
        nodes+=1
        while True:
            if not G:return True
            if () in G:return False
            unit=next((c[0] for c in G if len(c)==1),None)
            if unit is None:break
            G=tuple(tuple(z for z in c if z!=-unit) for c in G if unit not in c)
            probes+=sum(map(len,G));calls+=1
        x=abs(G[0][0]);first=tuple(tuple(z for z in c if z!=-x) for c in G if x not in c)
        v=rec(first)
        if v is True:return True
        second=tuple(tuple(z for z in c if z!=x) for c in G if -x not in c)
        w=rec(second)
        if w is True:return True
        return False if v is False and w is False else None
    v=rec(tuple(tuple(z for z in c) for c in F))
    return {'status':'SAT' if v is True else 'UNSAT' if v is False else 'UNKNOWN',
            'nodes':nodes,'unit_actions':calls,'counted_post_UP_literal_tests':probes,
            'node_cap':cap,'not_a_proof_if_UNKNOWN':True}

if __name__=='__main__':
    out={'run':'ARC-VALID-STATE-FIREWALL285-CONTROLS',
         'sources':{},'baseline_not_native_FLMV':True}
    for name,F,n in [('Y6_SAT',Y,6),('U198_UNSAT',U,198),('V198_SAT',V,198)]:
        o=audit(F,n,name);o['UP_DPLL_cap_512']=up_dpll(F,n,512);out['sources'][name]=o
    path=ROOT/'results/raw/arc/2026-10-31_1600_LSPV1_ARC_VALID_STATE_FIREWALL285_diagnostics_generated.json'
    path.write_text(json.dumps(out,separators=(',',':')))
    print(json.dumps({'status':'PASS','path':str(path),'bytes':path.stat().st_size,
                      'pair_mode_histograms':{k:v['pair_mode_histogram'] for k,v in out['sources'].items()},
                      'UP_DPLL':{k:v['UP_DPLL_cap_512'] for k,v in out['sources'].items()}},indent=2))

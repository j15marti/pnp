#!/usr/bin/env python3
"""Independent verifier of ARC273 raw source/children/S-U/certificates.
No imports from producer. Standard library, deterministic.
"""
import copy,hashlib,itertools,json,sys
from pathlib import Path

class Invalid(Exception): pass
checks=0

def require(v,what):
    global checks
    checks+=1
    if not v:raise Invalid(what)

def clause_ok(c,a):
    return any(a[abs(l)]==int(l>0) for l in c)

def source_ok(cs,a):return all(clause_ok(c,a) for c in cs)

def bound(n):return {i:0 for i in range(1,n+1)}

def truth_counts(cs,a):
    cc=[0]*4;per=[]
    for c in cs:
        t=sum(a[abs(v)]==int(v>0) for v in c)
        per.append(t)
        if len(c)==3:cc[t]+=1
    return {'all_clauses_sat':all(t>0 for t in per),'N3':cc,'true_literals_per_clause':per}

def exhaustive_micro(cs,fix):
    vars_=sorted(set(abs(l) for c in cs for l in c)-set(fix))
    if len(vars_)>20:raise Invalid('micro too wide')
    for bits in itertools.product((0,1),repeat=len(vars_)):
        a=dict(fix);a.update(zip(vars_,bits))
        if source_ok(cs,a):return a
    return None

def independent_solver(cs):
    vs=sorted(set(abs(l) for c in cs for l in c))
    def go(f,a):
        while True:
            changed=False
            for c in f:
                if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
                un=[l for l in c if abs(l) not in a]
                if not un:return None
                if len(un)==1:
                    l=un[0];v=abs(l);val=int(l>0)
                    if v in a and a[v]!=val:return None
                    if v not in a:a[v]=val;changed=True
            if not changed:break
        if all(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in f):return a
        scores={v:sum(abs(l)==v for c in f for l in c) for v in vs if v not in a}
        if not scores:return None
        v=max(scores,key=lambda z:(scores[z],-z))
        for b in (0,1):
            w=go(f,{**a,v:b})
            if w is not None:return w
        return None
    w=go(cs,{})
    return w

def xor_relation(cs,vs):
    require(len(cs)==4,'XOR length')
    outcomes=[]
    for bits in itertools.product((0,1),repeat=3):
        a=dict(zip(vs,bits))
        outcomes.append((bits[0]^bits[1]^bits[2],all(clause_ok(c,a) for c in cs)))
    matches=[p for p in (0,1) if all(sat==(parity==p) for parity,sat in outcomes)]
    require(len(matches)==1,'XOR clauses do not encode one parity')
    return matches[0]

def unit_relation(cs,v,p,q):
    require(len(cs)==4,'PIN length')
    patterns=[]
    for bb in (0,1):
        any_ok=False
        for u,z in itertools.product((0,1),repeat=2):
            if all(clause_ok(c,{v:bb,p:u,q:z}) for c in cs):any_ok=True
        patterns.append(any_ok)
    require(patterns in ([False,True],[True,False]),'PIN not unit')
    return int(patterns[1])

def matrix_flag(a,b,s,t):
    d={}
    for c,mode in [(a,s),(b,t)]:
        for lit in c:
            val=int(lit>0) if mode=='S' else int(lit<0)
            key=abs(lit)
            if key in d and d[key]!=val:return 0
            d[key]=val
    return 1

def child_bytes(cs):
    maxid=max([abs(l) for c in cs for l in c] or [0]);return len(('p cnf %d %d\n'%(maxid,len(cs))+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode())

def verify_row(row, full=True):
    cs=[tuple(c) for c in row['original_clauses']];n=row['n'];m=len(cs)
    require(m==row['m'],'m');require(max(abs(v) for c in cs for v in c)<=n,'n')
    require(child_bytes(cs)==row['source_dimacs_bytes'],'source bytes')
    require(len(row['source_occurrences'])==m,'targets count')
    for j,(clause,rec) in enumerate(zip(cs,row['source_occurrences']),1):
        require(rec['j']==j and tuple(rec['source'])==clause,'source clause target')
        for v,occ in zip(clause,rec['occurrences']):
            require(occ['literal']==v and occ['variable']==abs(v),'occurrence literal')
            require(occ['occurrence']==f'x_{abs(v)},{j}','occurrence indexed')
            s=int(v>0)
            require([occ['S'],occ['invert_S_to_U'],occ['U'],occ['invert_U_to_S']]==[s,1-s,1-s,s],'S/U')
    endpoints=row['endpoints_and_flips']
    zero=bound(n);one={v:1 for v in zero}
    require(endpoints['all_zero']==truth_counts(cs,zero),'zero')
    require(endpoints['all_one']==truth_counts(cs,one),'one')
    for state in endpoints['gray_trail']:
        g=state['t']^(state['t']>>1)
        require(g==state['mask'],'gray mask')
        a={v:int(bool(g>>(v-1)&1)) for v in zero}
        b={v:1-a[v] for v in zero}
        t=truth_counts(cs,a);u=truth_counts(cs,b)
        require(t['N3']==state['count3'] and u['N3']==state['complement_count3'],'trail N')
        require(t['all_clauses_sat']==state['SAT'] and u['all_clauses_sat']==state['complement_SAT'],'trail statuses')
        if all(len(c)==3 for c in cs):
            require([t['N3'][i] for i in range(4)]==[u['N3'][3-i] for i in range(4)],'complement')
    matrix=row['extreme_pair_matrix'];require(len(matrix)==m*(m-1)//2,'matrix length')
    for v in matrix:
        i,j=v['i']-1,v['j']-1
        require(i<j,'matrix index')
        require(v['shared']==sorted(set(map(abs,cs[i])) & set(map(abs,cs[j]))),'shared')
        flags={p+q:matrix_flag(cs[i],cs[j],p,q) for p in 'SU' for q in 'SU'}
        require(flags==v['flags'],'matrix flags')
        if full and i<4 and j<min(m,9):
            domain=sorted(set(map(abs,cs[i]))|set(map(abs,cs[j])))
            for p,q in itertools.product('SU',repeat=2):
                present=False
                for bits in itertools.product((0,1),repeat=len(domain)):
                    assign=dict(zip(domain,bits))
                    tc=sum(assign[abs(l)]==int(l>0) for l in cs[i])
                    td=sum(assign[abs(l)]==int(l>0) for l in cs[j])
                    if (tc==len(cs[i]) if p=='S' else tc==0) and (td==len(cs[j]) if q=='S' else td==0):present=True;break
                require(int(present)==flags[p+q],'enumerated compat')
    w=row['witness'];label=row['answer']
    if w is not None:
        require(label=='SAT','witness label')
        require(source_ok(cs,{int(k):v for k,v in w.items()}),'witness invalid')
    policy=row['policy']
    if policy['policy']=='authenticated_canonical_star_two_sided_DP':
        src=policy['sources'];k=src['k'];x=src['shared']
        require(x==n and n==1+k*(5+2*k),'canonical n')
        require(m==k*(12+4*k),'canonical clauses')
        require(len(src['charges'])==k,'source charges')
        charges=[]
        for j in range(k):
            base=1+j*(5+2*k)
            block=cs[j*(12+4*k):(j+1)*(12+4*k)]
            p=xor_relation(block[0:4],(x,base,base+1))
            q=xor_relation(block[4:8],(base,base+1,base+2))
            t=unit_relation(block[8:12],base+2,base+3,base+4)
            extras=[]
            for off in range(k):extras.append(xor_relation(block[12+4*off:16+4*off],(x,base+5+2*off,base+6+2*off)))
            want={'j':j,'p':p,'q':q,'r':t,'t':p^q^t,'extras':extras}
            require(src['charges'][j]==want,'charge record')
            charges.append(want['t'])
            # This is an exhaustive check of projection for the causal 3-row factor.
            for xb in (0,1):
                extensions=0
                for aa,bb,cc in itertools.product((0,1),repeat=3):
                    if (xb^aa^bb)==p and (aa^bb^cc)==q and cc==t:extensions+=1
                require((extensions>0)==(xb==want['t']),'module source projection')
        require((label=='SAT')==(len(set(charges))==1),'algebraic SAT/UNSAT')
        if label=='UNSAT':
            blockers={rec['boundary'] for rec in policy['forbidden_cubes']}
            require(blockers=={0,1},'UNSAT lacks both boundary proof blocks')
        for bad in policy['forbidden_cubes']:
            j=bad['bad_module'];target=charges[j]
            require(bad['derived_unit']==target and bad['boundary']!=target,'invalid scoped block')
            require(bad['source_ids']==list(range(j*(12+4*k)+1,j*(12+4*k)+13)),'forged source indices')
        # Independent cofactor reconstruction and child exact decisions.
        for child in policy['children']:
            j=child['block'];b=child['xval'];block=cs[j*(12+4*k):(j+1)*(12+4*k)]
            c=[]
            for cl in block:
                if (x if b else -x) in cl:continue
                c.append(tuple(v for v in cl if abs(v)!=x))
            ids=sorted(set(abs(v) for cl in c for v in cl));mp={v:i+1 for i,v in enumerate(ids)}
            actual=[tuple((1 if v>0 else -1)*mp[abs(v)] for v in cl) for cl in c]
            require([list(z) for z in actual]==child['clauses'],'child source transfer')
            require(child_bytes(actual)==child['bytes'],'child physical bytes')
            ans=independent_solver(actual)
            require((ans is not None)==(child['guest_answer']=='SAT'),'guest child truth')
            require((ans is not None)==(b==charges[j]),'projected label')
    else:
        require(policy['policy']=='fallback_UP_DPLL','policy unexpected')
        expected=independent_solver(cs)
        require((expected is not None)==(label=='SAT'),'fallback source mismatch')
    return True

def main():
    p=Path(sys.argv[1] if len(sys.argv)>1 else 'raw273.json')
    doc=json.loads(p.read_text())
    labels=[]
    for z in doc['rows']:
        verify_row(z);labels.append(z['answer'])
    require('SAT' in labels and 'UNSAT' in labels,'both labels absent')
    # Deliberately reject four independent falsifications.
    bad_tests={}
    star_sat=next(x for x in doc['rows'] if x['name']=='STAR_K2_SAT')
    star_unsat=next(x for x in doc['rows'] if x['name']=='STAR_K2_UNSAT')
    mutations={
        'witness':(star_sat,lambda d: d['witness'].__setitem__(str(d['n']),1-d['witness'][str(d['n'])])),
        'GF2_unit':(star_unsat,lambda d: d['policy']['sources']['charges'][0].__setitem__('t',1-d['policy']['sources']['charges'][0]['t'])),
        'SS_matrix':(star_sat,lambda d: d['extreme_pair_matrix'][0]['flags'].__setitem__('SS',1-d['extreme_pair_matrix'][0]['flags']['SS'])),
        'child_byte':(star_sat,lambda d: d['policy']['children'][0].__setitem__('bytes',d['policy']['children'][0]['bytes']+1))
    }
    for name,(base,mutation) in mutations.items():
        altered=copy.deepcopy(base);mutation(altered)
        try:verify_row(altered,full=False)
        except Invalid:bad_tests[name]='rejected'
        else:raise AssertionError('corruption accepted:'+name)
    out={'status':'PASS','original_sources':len(doc['rows']),'SAT':labels.count('SAT'),'UNSAT':labels.count('UNSAT'),
         'assertions':checks,'rejected_mutations':bad_tests,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    Path(p.parent/'check273.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
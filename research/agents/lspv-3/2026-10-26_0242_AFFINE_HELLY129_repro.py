#!/usr/bin/env python3
"""Affine boundary Helly theorem 129, self-contained finite reproducibility.
No external dependencies. Source boundaries are original DIMACS names.
All full clauses are proper signed ternaries unless explicitly marked Horn/2SAT.
"""
import json, random, hashlib, itertools, sys, math
SEED=12920261026
rng=random.Random(SEED)
checks=0

def ck(x,msg='check failed'):
    global checks
    checks+=1
    if not x:raise AssertionError(msg)

def parity(a):return a.bit_count()&1

def encode_xor3(a,b,c,rhs):
    ck(len({a,b,c})==3,'non-distinct XOR names')
    out=[]
    for mask in range(8):
        if parity(mask)!=rhs:
            out.append(tuple((-v if (mask>>i)&1 else v) for i,v in enumerate((a,b,c))))
    ck(len(out)==4,'XOR quartet count')
    return out

def pin(lit,p,q):
    ck(len({abs(lit),p,q})==3,'PIN alias')
    return [(lit,p,q),(lit,p,-q),(lit,-p,q),(lit,-p,-q)]

def make_affine(b):
    ck(b>=3)
    cl=[];modules=[];nextid=b+1
    for i in range(1,b+1):
        p,q=nextid,nextid+1;nextid+=2
        row=pin(-i,p,q)
        modules.append({'name':f'pin_y{i}=0','clauses':row,'row':(1<<(i-1),0),'private':(p,q)})
        cl.extend(row)
    par=[]
    if b==3:
        par.extend(encode_xor3(1,2,3,1))
    else:
        current=1
        for i in range(2,b-1):
            t=nextid;nextid+=1
            par.extend(encode_xor3(current,i,t,0))
            current=t
        par.extend(encode_xor3(current,b-1,b,1))
    modules.append({'name':'odd_parity','clauses':par,'row':((1<<b)-1,1),'private':tuple(range(b+2*b+1,nextid))})
    cl.extend(par)
    return modules,nextid-1

def encode_forbid_word(b,w,nextid):
    lits=[-(i+1) if (w>>i)&1 else i+1 for i in range(b)]
    if b==3:return [tuple(lits)],nextid
    z=nextid;nextid+=1
    clauses=[(lits[0],lits[1],z)]
    last=z
    for j in range(2,b-2):
        z=nextid;nextid+=1
        clauses.append((-last,lits[j],z));last=z
    clauses.append((-last,lits[-2],lits[-1]))
    return clauses,nextid

def make_exclusions(b):
    ck(b>=3)
    mods=[];nextid=b+1
    for w in range(1<<b):
        clauses,nextid=encode_forbid_word(b,w,nextid)
        mods.append({'name':f'exclude_{w}', 'clauses':clauses,'forbid':w})
    return mods,nextid-1

def eval_clause(cl,w):
    return any(((w>>(abs(x)-1))&1)==int(x>0) for x in cl)

def sat_brute(clauses,n):
    for a in range(1<<n):
        if all(eval_clause(c,a) for c in clauses):return a
    return None

def serial(clauses,n):
    ck(n>=max([0]+[abs(x) for c in clauses for x in c]),'header max ID')
    for c in clauses:
        ck(len(c)==3 and len({abs(x) for x in c})==3,'not proper ternary')
    data='p cnf %d %d\n'%(n,len(clauses))+'\n'.join(' '.join(map(str,c))+' 0' for c in clauses)+'\n'
    parts=data.strip().splitlines()
    head=parts[0].split();ck(head[:2]==['p','cnf'] and int(head[2])==n and int(head[3])==len(parts)-1,'bad header')
    parsed=[]
    for row in parts[1:]:
        ints=list(map(int,row.split()));ck(ints[-1]==0,'missing terminator');parsed.append(tuple(ints[:-1]))
    ck(parsed==list(map(tuple,clauses)),'serialized mismatch')
    return len(data.encode('ascii'))

def projected_sat(clauses,b,n):
    ans=set()
    for boundary in range(1<<b):
        for ext in range(1<<(n-b)):
            a=boundary | (ext<<b)
            if all(eval_clause(c,a) for c in clauses):ans.add(boundary);break
    return ans

def support_module(mod,b):
    cnf=mod['clauses']
    priv=sorted({abs(l) for c in cnf for l in c if abs(l)>b})
    s=set()
    for w in range(1<<b):
        for bits in range(1<<len(priv)):
            env=w
            for i,v in enumerate(priv):
                if (bits>>i)&1: env|=1<<(v-1)
            if all(eval_clause(c,env) for c in cnf):s.add(w);break
    return s

def check_affine_exact(b):
    modules,n=make_affine(b)
    cl=[c for z in modules for c in z['clauses']]
    full_size=serial(cl,n)
    proj=[]
    for mod in modules:
        p=support_module(mod,b)
        expected={w for w in range(1<<b) if parity(w&mod['row'][0])==mod['row'][1]}
        ck(p==expected,f'affine projected support b={b} {mod["name"]}')
        proj.append(p)
    total=set(range(1<<b))
    for p in proj: total&=p
    ck(len(total)==0,'sharp affine family must be UNSAT')
    # Each proper subcollection has a joint source-named satisfying word.
    for drop in range(len(modules)):
        p=set(range(1<<b))
        for j,q in enumerate(proj):
            if j!=drop:p&=q
        ck(bool(p),'proper subcollection must be SAT')
    if b<=4:ck(sat_brute(cl,n) is None,'independent affine whole formula not UNSAT')
    # root + two fully encoded descendants, no source-name changes.
    prefix=[c for x in modules[:-2] for c in x['clauses']]
    sizes=[];labels=[]
    cur=list(prefix)
    for level in (0,1,2):
        if level:cur.extend(modules[-3+level]['clauses']) # level1 pin_b, level2 parity
        sizes.append(serial(cur,n))
        p=set(range(1<<b))
        for mod in modules[:(b-1+level)]:p&=support_module(mod,b)
        labels.append(bool(p))
    ck(labels==[True,True,False],'two-level path labels')
    return {'b':b,'modules':len(modules),'variables':n,'clauses':len(cl),'full_bytes':full_size,'two_level_bytes':sizes,'two_level_labels':['SAT' if z else 'UNSAT' for z in labels],'minimal_unsat_modules':b+1}

def check_exclusions(b):
    mods,n=make_exclusions(b)
    cl=[c for m in mods for c in m['clauses']]
    whole_bytes=serial(cl,n)
    supports=[]
    all_words=set(range(1<<b))
    for mod in mods:
        s=support_module(mod,b)
        ck(s==all_words-{mod['forbid']},'exclusion module projection incorrect')
        supports.append(s)
    tot=set(all_words)
    for s in supports:tot&=s
    ck(not tot,'all exclusions must be UNSAT')
    for drop in range(len(mods)):
        remains=set(all_words)
        for j,s in enumerate(supports):
            if j!=drop:remains&=s
        ck(remains=={drop},'dropping one module must restore exactly one boundary word')
    if b==3:ck(sat_brute(cl,n) is None,'exclusions full formula brute SAT')
    two=[];labels=[]
    for take in (len(mods)-2,len(mods)-1,len(mods)):
        p=[]
        for m in mods[:take]:p+=m['clauses']
        two.append(serial(p,n))
        labels.append(sat_brute(p,n) is not None if b==3 else bool(set.intersection(all_words,*supports[:take])))
    ck(labels==[True,True,False],'nonaffine two-level labels')
    return {'b':b,'modules':len(mods),'variables':n,'clauses':len(cl),'bytes':whole_bytes,'two_level_bytes':two,'labels':['SAT' if z else 'UNSAT' for z in labels],'minimal_unsat_modules':1<<b}

def streaming_affine(rows,b):
    """GF(2) elimination: O(m*b^2) bit operations, O(b^2+b*log m) bits.

    Each pivot carries (topbit, reduced LHS, reduced RHS, dependency mask)
    over at most b original independently selected source equation IDs.
    """
    basis_ids=[]
    pivots=[]
    for i,(a,c) in enumerate(rows):
        x=a; z=c; mask=0
        for bit, p_lhs, p_rhs, p_mask in pivots:
            if (x>>bit)&1:
                x^=p_lhs;z^=p_rhs;mask^=p_mask
        if x:
            ck(len(basis_ids)<b,'rank exceeds boundary dimension')
            bit=x.bit_length()-1
            mask|=1<<len(basis_ids)
            basis_ids.append(i)
            pivots.append((bit,x,z,mask))
            pivots.sort(key=lambda p:p[0],reverse=True)
        elif z:
            ids=[i]+[source for j,source in enumerate(basis_ids) if mask>>j&1]
            ck(len(ids)<=b+1,'too many original source rows')
            lhs=0;rhs=0
            for q in ids:
                lhs^=rows[q][0];rhs^=rows[q][1]
            ck(lhs==0 and rhs==1,'certificate XOR mismatch')
            return {'UNSAT':True,'source_ids':ids,'rank':len(pivots)}
    return {'UNSAT':False,'basis_ids':basis_ids,'rank':len(pivots)}

def random_affine_checks():
    tests=[]
    for b in range(1,9):
        for rep in range(32):
            witness=rng.randrange(1<<b)
            rows=[]
            for _ in range(rng.randint(b,2*b+10)):
                a=rng.randrange(1<<b);rows.append((a,parity(a&witness)))
            if rep%2==0:
                a=rng.randrange(1<<b)
                rows.append((a,parity(a&witness)^1))
            ans=streaming_affine(rows,b)
            brute_any=any(all(parity(a&w)==c for a,c in rows) for w in range(1<<b))
            ck(ans['UNSAT']==(not brute_any),'streaming row answer mismatch')
            if ans['UNSAT']:
                ck(len(ans['source_ids'])<=b+1,'Helly witness too long')
            tests.append((b,len(rows),ans['UNSAT'],ans['rank']))
    return {'systems':len(tests),'unsat':sum(z[2] for z in tests),'sat':sum(not z[2] for z in tests),'max_basis_rank':max(z[3] for z in tests)}

def exact22_w1():
    W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
    f=[tuple(map(int,c.split())) for c in W.split(';')]
    counts={v:[0,0] for v in range(1,16)}
    for c in f:
        for x in c:counts[abs(x)][int(x<0)]+=1
    ck(all(z==[2,2] for z in counts.values()),'W1 not signed (2,2)')
    ck(sat_brute(f,15) is None,'W1 should be UNSAT')
    ck(serial(f,15)>0,'W1 encoding')
    for i in range(len(f)):
        ck(sat_brute(f[:i]+f[i+1:],15) is not None,'W1 essential source clause missing')
    # Deliberately no claim that W1 is affine or under affine-join theorem.
    return {'variables':15,'clauses':len(f),'label':'UNSAT','all_clauses_essential':True,'recognized_affine_modules':False}

def other_controls():
    # Pairwise-compatible affine equations, but three-way inconsistent.
    rows=[(1,0),(2,0),(4,0),(7,1)]
    for idxs in itertools.combinations(range(4),3):
        ck(any(all(parity(rows[i][0]&w)==rows[i][1] for i in idxs) for w in range(8)),'3-wise feasibility')
    ck(not any(all(parity(a&w)==c for a,c in rows) for w in range(8)),'4-way UNSAT')
    # Odd K4 Tseitin proper CNF and GF(2) quick parity contradiction.
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    clauses=[]
    for v in range(4):
        inc=[i+1 for i,(u,w) in enumerate(edges) if u==v or w==v]
        clauses+=encode_xor3(*inc,int(v==0))
    ck(sat_brute(clauses,6) is None,'odd K4 must be UNSAT')
    ck(serial(clauses,6)>0)
    horn=[(1,),(-1,2),(-2,)]
    easy_sat=[(1,2),(-1,2)]
    ck(sat_brute(horn,2) is None,'Horn UNSAT')
    ck(sat_brute(easy_sat,2) is not None,'2SAT SAT')
    # Private alias changes semantics although each module alone satisfiable.
    def lift2(l1,l2,z):return [(l1,l2,z),(l1,l2,-z)]
    # module one z=y, module two w=1-y; originals share only y
    lhs=lift2(-2,1,4)+lift2(2,-1,5)
    rhs=lift2(-3,-1,6)+lift2(3,1,7)
    ck(sat_brute(lhs+rhs,7) is not None,'fresh private join should SAT')
    aliased=[tuple((2 if abs(x)==3 else abs(x))*(1 if x>0 else -1) for x in c) for c in rhs]
    ck(sat_brute(lhs+aliased,7) is None,'aliased private join should UNSAT')
    return {'K4_odd_Tseitin_clauses':len(clauses),'Horn_UNSAT':True,'twoSAT_SAT':True,'fresh_join_SAT':True,'wrong_alias_join_UNSAT':True,'affine_every_three_SAT_four_UNSAT':True}

def volume_checks():
    d=1.802
    for trial in range(400):
        vals=[rng.randint(1,500) for _ in range(rng.randrange(1,14))]
        M=max(vals);V=sum(vals)
        ck(sum(v**d for v in vals)<=M**(d-1)*V*(1+1e-11),'volume bound')
    return {'volume_inequality_trials':400,'d':d,'lambda':0.5,'b_strict_target':1.4008217497}

def main():
    vals={
      'name':'SOURCE-BOUNDARY-AFFINE-HELLY129','timestamp':'2026-10-26 02:42 America/Los_Angeles',
      'status':'PROVED/EXACT restricted mathematical proof; computational finite audits; all-UNSAT bounded coverage OPEN',
      'seed':SEED,'affine_sharp':[check_affine_exact(b) for b in (3,4,5)],
      'nonaffine_sharp':[check_exclusions(b) for b in (3,4)],
      'streaming':random_affine_checks(),'signed22':exact22_w1(),
      'hostile':other_controls(),'resources':volume_checks()
    }
    vals['assertion_groups']=checks
    output=json.dumps(vals,sort_keys=True,indent=2)+'\n'
    path=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv3_129/2026-10-26_0242_AFFINE_HELLY129_raw.json'
    with open(path,'w') as f:f.write(output)
    print(json.dumps({'assertion_groups':checks,'sha256':hashlib.sha256(output.encode()).hexdigest(),'path':path,'affine':[z['two_level_labels'] for z in vals['affine_sharp']],'nonaffine':[z['labels'] for z in vals['nonaffine_sharp']],'streaming':vals['streaming']},sort_keys=True))

if __name__=='__main__':main()
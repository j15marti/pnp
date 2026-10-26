#!/usr/bin/env python3
"""ARC185: signed-source authenticated PAIR2/QUAD1 refutations.

Independent standard-library finite reproducer for a restricted proof grammar.
No all-SAT ARC transformation and no physical FLMV measurements are claimed.
"""
from __future__ import annotations
import json, random, itertools, hashlib, pathlib, sys, collections
from dataclasses import dataclass

RUN='ARC-LOCAL-SOURCE-RESOLVE185'
SEED=18520261026
W1_TEXT='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1=tuple(tuple(map(int,row.split())) for row in W1_TEXT.split(';'))

class Audit:
    def __init__(self): self.assertions=0;self.failed=0
    def ck(self,cond,message='assertion'):
        self.assertions+=1
        if not cond:self.failed+=1;raise AssertionError(message)

A=Audit()

def litval(l,assignment):
    return assignment.get(abs(l),False)==(l>0)

def sat_by(cnf,assignment):
    return all(any(litval(l,assignment) for l in clause) for clause in cnf)

def brute(cnf,nvars):
    for bits in range(1<<nvars):
        ass={i+1:bool((bits>>i)&1) for i in range(nvars)}
        if sat_by(cnf,ass):return ass
    return None

def encode_cnf(n,cs):
    head=f'p cnf {n} {len(cs)}\n'.encode('ascii')
    data=bytearray(head); offsets=[]
    for clause in cs:
        offsets.append(len(data))
        data.extend((' '.join(map(str,clause))+' 0\n').encode('ascii'))
    return bytes(data),tuple(offsets)

def audit_dimacs(data):
    try:
        lines=data.decode('ascii').splitlines(keepends=True)
        if not lines or any(not line.endswith('\n') for line in lines):return None
        head=lines[0].split()
        if len(head)!=4 or head[:2]!=['p','cnf']:return None
        n,m=map(int,head[2:]);cs=[]
        if len(lines)!=m+1 or m<0 or n<0:return None
        for line in lines[1:]:
            parts=tuple(map(int,line.split()))
            if len(parts)!=4 or parts[-1]!=0:return None
            c=parts[:-1]
            if len({abs(x) for x in c})!=3 or min(map(abs,c))<1 or max(map(abs,c))>n:return None
            cs.append(c)
        return n,tuple(cs),len(lines[0].encode('ascii'))
    except (UnicodeError,ValueError,TypeError):return None

def authenticated_clause(data,off,head_end):
    if not isinstance(off,int) or off<head_end or off>=len(data):return None
    if data[off-1]!=10:return None
    end=data.find(b'\n',off)
    if end<0:return None
    try:
        record=tuple(map(int,data[off:end].split()))
        if len(record)!=4 or record[-1]!=0 or len(set(map(abs,record[:3])))!=3:return None
        return record[:3]
    except ValueError:return None

def group_encoding(n,cnf):
    """Encode nonempty 1/2-CNF using fresh pad vars, with source-offset bundles."""
    cs=[];desc=[];nextid=n+1
    for clause in cnf:
        assert len(clause) in (1,2) and all(abs(x)<=n for x in clause)
        start=len(cs)
        if len(clause)==1:
            y,z=nextid,nextid+1;nextid+=2
            for a,b in itertools.product((1,-1),repeat=2):
                cs.append((clause[0],a*y,b*z))
            desc.append({'type':'quad','base':(clause[0],),'pads':(y,z),'indices':tuple(range(start,start+4))})
        else:
            z=nextid;nextid+=1
            cs.extend([(clause[0],clause[1],z),(clause[0],clause[1],-z)])
            desc.append({'type':'pair','base':clause,'pads':(z,),'indices':tuple(range(start,start+2))})
    data,offs=encode_cnf(nextid-1,cs)
    for desc_i in desc:desc_i['offsets']=tuple(offs[i] for i in desc_i['indices'])
    return {'data':data,'nvars':nextid-1,'clauses':tuple(cs),'offsets':offs,'descs':tuple(desc)}

def derive_edges(desc):
    c=desc['base'];offs=desc['offsets']
    if desc['type']=='quad':
        a=c[0]
        return [{'tag':'QUAD1','offsets':offs,'base':c,'pads':desc['pads'],'src':-a,'dst':a}]
    a,b=c
    return [
        {'tag':'PAIR2','offsets':offs,'base':c,'pads':desc['pads'],'src':-a,'dst':b},
        {'tag':'PAIR2','offsets':offs,'base':c,'pads':desc['pads'],'src':-b,'dst':a}
    ]

def find_paths(enc,n):
    graph=collections.defaultdict(list)
    for d in enc['descs']:
        for e in derive_edges(d):graph[e['src']].append(e)
    def bfs(s,t):
        todo=collections.deque([s]); prev={s:(None,None)}
        while todo:
            cur=todo.popleft()
            if cur==t:break
            for edge in graph[cur]:
                v=edge['dst']
                if v not in prev:prev[v]=(cur,edge);todo.append(v)
        if t not in prev:return None
        out=[]; cur=t
        while cur!=s:
            parent,edge=prev[cur];out.append(edge);cur=parent
        return tuple(reversed(out))
    for x in range(1,n+1):
        p=bfs(x,-x);q=bfs(-x,x)
        if p is not None and q is not None:
            return {'pivot':x,'path_plus':p,'path_minus':q}
    return None

def source_proof_verify(data,cert):
    checked=audit_dimacs(data)
    if checked is None or not isinstance(cert,dict):return False
    n,clauses,head_end=checked
    x=cert.get('pivot')
    if not isinstance(x,int) or not 1<=x<=n:return False
    for label,start,finish in [('path_plus',x,-x),('path_minus',-x,x)]:
        chain=cert.get(label)
        if not isinstance(chain,(tuple,list)) or not 1<=len(chain)<=2*n:return False
        cur=start
        for edge in chain:
            if not isinstance(edge,dict) or edge.get('src')!=cur:return False
            endpoints=(edge.get('src'),edge.get('dst'))
            if any(not isinstance(l,int) or l==0 or abs(l)>n for l in endpoints):return False
            offsets=edge.get('offsets');base=edge.get('base');pads=edge.get('pads');tag=edge.get('tag')
            if not isinstance(offsets,(tuple,list)) or not isinstance(base,(tuple,list)) or not isinstance(pads,(tuple,list)):return False
            if tag=='PAIR2' and len(offsets)==2 and len(base)==2 and len(pads)==1:
                a,b=base;z=pads[0]
                if len({abs(a),abs(b),abs(z)})!=3 or not all(isinstance(l,int) and abs(l) in range(1,n+1) for l in (a,b,z)):return False
                expected=[frozenset((a,b,z)),frozenset((a,b,-z))]
                if not (cur==-a and edge['dst']==b or cur==-b and edge['dst']==a):return False
            elif tag=='QUAD1' and len(offsets)==4 and len(base)==1 and len(pads)==2:
                a=base[0];y,z=pads
                if not all(isinstance(l,int) and abs(l) in range(1,n+1) for l in (a,y,z)):return False
                if len({abs(a),abs(y),abs(z)})!=3:return False
                expected=[frozenset((a,p*y,q*z)) for p,q in itertools.product((1,-1),repeat=2)]
                if not(cur==-a and edge['dst']==a):return False
            else:return False
            got=[authenticated_clause(data,off,head_end) for off in offsets]
            if None in got or collections.Counter(map(frozenset,got))!=collections.Counter(expected):return False
            cur=edge['dst']
        if cur!=finish:return False
    return True

def chain(n,include_last=True):
    assert n>=2
    clauses=[(1,)]+[(-i,i+1) for i in range(1,n)]
    if include_last:clauses.append((-n,))
    return tuple(clauses)

def simple_restrict(cnf,assign):
    out=[]
    for c in cnf:
        if any(abs(l) in assign and litval(l,assign) for l in c):continue
        reduced=tuple(l for l in c if abs(l) not in assign)
        out.append(reduced)
    return tuple(out)

def min_hitting(cnf,nvars):
    supports=[set(map(abs,c)) for c in cnf]
    for k in range(nvars+1):
        for combo in itertools.combinations(range(1,nvars+1),k):
            chosen=set(combo)
            if all(s & chosen for s in supports):return k

def source_pairs(cnf):
    p=[]
    for i,a in enumerate(cnf):
        for j,b in enumerate(cnf[:i]):
            common=set(a)&set(b)
            if len(common)!=2:continue
            da=set(a)-common;db=set(b)-common
            if len(da)==len(db)==1 and next(iter(da))==-next(iter(db)):
                p.append((j,i))
    return p

def is_exact_signed(cnf,n):
    p=collections.Counter();m=collections.Counter()
    for c in cnf:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        for l in c:(p if l>0 else m)[abs(l)]+=1
    return all(p[i]==2 and m[i]==2 for i in range(1,n+1))

def witness_delete(n,enc,j):
    """Explicit model after deleting ANY one ternary clause of E(Q_n)."""
    desc=next(d for d in enc['descs'] if j in d['indices'])
    i=enc['descs'].index(desc)
    if i==0: x={v:False for v in range(1,n+1)}
    elif i==len(enc['descs'])-1:x={v:True for v in range(1,n+1)}
    else:x={v:(v<=i) for v in range(1,n+1)}
    assign={v:False for v in range(1,enc['nvars']+1)};assign.update(x)
    if desc['type']=='quad':
        target=enc['clauses'][j]
        for lit in target[1:]:assign[abs(lit)]=not(lit>0)
    else:
        partner=desc['indices'][1] if j==desc['indices'][0] else desc['indices'][0]
        lit=enc['clauses'][partner][2]
        assign[abs(lit)]=(lit>0)
    return assign

def run():
    rng=random.Random(SEED);rows=[];negative_tests=collections.Counter()
    for n in (2,3,4,5,6,8,12,20,40,80,160):
        F=chain(n,True);enc=group_encoding(n,F);cert=find_paths(enc,n)
        A.ck(cert is not None,'missing dual implication paths')
        A.ck(source_proof_verify(enc['data'],cert),'valid chain proof rejected')
        A.ck(len(cert['path_plus'])==2*n-1 and len(cert['path_minus'])==1,'nonminimal path count')
        A.ck(len(enc['clauses'])==2*n+6,'clause formula')
        A.ck(enc['nvars']==2*n+3,'variable formula')
        A.ck(not source_pairs(enc['clauses'])==[],'must have local pair')
        A.ck(len(set(tuple(sorted(c)) for c in enc['clauses']))==len(enc['clauses']),'duplicate clauses')
        A.ck(all(len(set(map(abs,c)))==3 for c in enc['clauses']),'nonproper')
        for j in range(len(enc['clauses'])):
            witness=witness_delete(n,enc,j)
            A.ck(sat_by(tuple(c for k,c in enumerate(enc['clauses']) if k!=j),witness),f'deletion witness n{n} clause{j}')
            A.ck(not sat_by(enc['clauses'],witness),'full formula incorrectly SAT')
        if n<=5:
            A.ck(brute(enc['clauses'],enc['nvars']) is None,'F_n brute UNSAT')
            A.ck(all(brute(tuple(c for k,c in enumerate(enc['clauses']) if k!=j),enc['nvars']) is not None for j in range(len(enc['clauses']))),'not minimal brute')
        if n<=6:
            minh=min_hitting(enc['clauses'],enc['nvars'])
            A.ck(minh>=n//2,'hitting matching lower bound')
        else:minh=None
        A.ck(len(enc['data'])>len(cert['path_plus'])+len(cert['path_minus']),'basic encoding sanity')
        bad=json.loads(json.dumps(cert));bad['path_plus'][0]['offsets'][0]+=1
        A.ck(not source_proof_verify(enc['data'],bad),'forged non-line-start source pointer')
        bad=json.loads(json.dumps(cert));bad['path_plus'][0]['base'][0]*=-1
        A.ck(not source_proof_verify(enc['data'],bad),'forged derived literal')
        bad=json.loads(json.dumps(cert));bad['path_plus'][-1]['dst']=1
        A.ck(not source_proof_verify(enc['data'],bad),'forged terminal')
        satenc=group_encoding(n,chain(n,False))
        expected={i:True for i in range(1,n+1)}
        expected.update({v:False for v in range(n+1,satenc['nvars']+1)})
        A.ck(sat_by(satenc['clauses'],expected),'SAT family witness failed')
        A.ck(find_paths(satenc,n) is None,'false 2SAT cycle')
        rows.append({'n':n,'N_bits':8*len(enc['data']),'vars':enc['nvars'],'clauses':len(enc['clauses']),
            'source_bytes':len(enc['data']),'path_edges':len(cert['path_plus'])+len(cert['path_minus']),
            'serialized_proof_bytes':len(json.dumps(cert,separators=(',',':')).encode()),'min_hitting':minh,
            'matching_clause_supports':sum(1 for i,c in enumerate(enc['clauses']) for d in enc['clauses'][:i] if set(map(abs,c))==set(map(abs,d)))})
    # Random 2CNF both labels, exact exhaustive original SAT, direct signed ternary expansion semantics.
    random_counts=collections.Counter();random_shortest=[]
    for n in (2,3,4):
        candidates=[(v,) for v in range(1,n+1)]+[(-v,) for v in range(1,n+1)]
        candidates+=[(a,b) for a in range(-n,n+1) if a!=0 for b in range(-n,n+1) if b!=0 and abs(a)<abs(b)]
        for trial in range(70):
            k=rng.randrange(2,10)
            F=tuple(rng.sample(candidates,min(k,len(candidates))))
            satw=brute(F,n)
            enc=group_encoding(n,F)
            cert=find_paths(enc,n)
            A.ck((cert is not None)==(satw is None),'2SAT path coverage')
            if cert is not None:
                A.ck(source_proof_verify(enc['data'],cert),'2SAT encoded proof rejected')
                random_shortest.append(len(cert['path_plus'])+len(cert['path_minus']))
            for _ in range(10):
                vals={v:bool(rng.getrandbits(1)) for v in range(1,enc['nvars']+1)}
                A.ck(sat_by(F,vals)==sat_by(enc['clauses'],vals),'pair/quad semantic equality')
            random_counts['SAT' if satw is not None else 'UNSAT']+=1
    # Connected W1: strict signed exact (2,2), non-monotone, no unconditioned PAIR2/QUAD1.
    A.ck(is_exact_signed(W1,15),'W1 exact signed (2,2) degree')
    A.ck(brute(W1,15) is None,'W1 not UNSAT')
    A.ck(not source_pairs(W1),'W1 unexpectedly has PAD PAIR2')
    mono=tuple(c for c in W1 if all(l>0 for l in c) or all(l<0 for l in c))
    A.ck(len(mono)<len(W1),'W1 unexpectedly monotone')
    # Two actual restriction/repadding levels with fixed original x values (no free guest A calls).
    heritage=[]
    for base_label,base in [('UNSAT',chain(5,True)),('SAT',chain(5,False))]:
        for depth in (0,1,2):
            restricted=simple_restrict(base,{v:True for v in range(1,depth+1)})
            A.ck(not any(len(c)==0 for c in restricted),'selected branch invalid')
            child=group_encoding(5,restricted)
            original_sat=brute(restricted,5) is not None
            got=find_paths(child,5)
            A.ck((got is None)==original_sat,'hereditary descendant label incorrect')
            if got is not None:A.ck(source_proof_verify(child['data'],got),'hereditary proof failed')
            A.ck(all(len(set(map(abs,c)))==3 for c in child['clauses']),'hereditary ternary nonproper')
            heritage.append({'parent_label':base_label,'depth':depth,'child_source_clauses':len(restricted),'repacked_3cnf_clauses':len(child['clauses']),'child_encoded_bytes':len(child['data']),'UNSAT':not original_sat,'authenticated_proof':got is not None})
    out={'run':RUN,'seed':SEED,'status':{'restricted_padded_2sat':'PROVED/EXACT symbolic; finite verification','all_signed_exact_22':'OPEN','ordinary_SAT':'OPEN','ARC_EDGE_90':'OPEN','P_vs_NP':'OPEN'},
        'assertions':A.assertions,'failed':A.failed,'family_rows':rows,'random_2cnf':dict(random_counts),'random_shortest_path_edges':{'min':min(random_shortest),'max':max(random_shortest)},
        'W1':{'variables':15,'clauses':len(W1),'label':'UNSAT exhaustive 2^15','exact_signed_22':True,'clause_monotone':False,'source_pair2_count':len(source_pairs(W1))},'two_real_levels':heritage,
        'limits':['Python counts are semantic and lexical, not FLMV instruction or space counts.','Proof generator BFS uses full graph memory.','No all-UNSAT low-cost certificate coverage on ordinary SAT or exact signed 2,2.','No structural theorem forces arbitrary SAT algorithms to use this grammar.']}
    result_path=pathlib.Path(__file__).with_name('2026-10-26_0608_ARC185_local_offset_resolution_raw.json')
    result_path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions':out['assertions'],'failed':out['failed'],'random':out['random_2cnf'],'family':[(r['n'],r['min_hitting'],r['path_edges']) for r in rows],'two_real_levels':heritage,'raw_path':str(result_path)},indent=2))

if __name__=='__main__':run()

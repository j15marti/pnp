#!/usr/bin/env python3
"""ARC186: source-authenticated adaptive BRANCH/EMPTY/PATH tree ->
explicit general-resolution DAG. Ordinary 3-CNF lower-bound firewall.
Python stdlib only. Finite tests, not FLMV Turing-machine measurements.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from itertools import product
from hashlib import sha256
import json, random
from pathlib import Path

RUN_ID = "ARC-SOURCE-RESOLUTION-BARRIER186"
SEED = 202610260758
RNG = random.Random(SEED)
CHECKS = 0

def check(test, message):
    global CHECKS
    CHECKS += 1
    if not test: raise AssertionError(message)

def clause_norm(c):
    return tuple(sorted(set(c),key=lambda v:(abs(v),v<0)))

def serialize(n, clauses):
    lines = [f"p cnf {n} {len(clauses)}\n"]
    offsets = []
    for c in clauses:
        offsets.append(sum(map(len,lines)))
        lines.append(" ".join(map(str,c)) + " 0\n")
    return "".join(lines).encode('ascii'), tuple(offsets)

def parse(raw):
    lines=raw.decode('ascii').splitlines(keepends=True)
    check(bool(lines) and lines[0].endswith('\n'),"header line")
    a=lines[0].strip().split()
    check(len(a)==4 and a[:2]==['p','cnf'],"header grammar")
    n,m=map(int,a[2:]); check(n>=1 and m>=0,'header range')
    cs=[];offsets=[];off=len(lines[0])
    for line in lines[1:]:
        check(line.endswith('\n'), 'terminated clause line')
        vals=tuple(map(int,line.strip().split()))
        check(vals and vals[-1]==0 and 0 not in vals[:-1],"clause sentinel")
        c=vals[:-1]
        check(1<=len(c)<=3 and all(1<=abs(x)<=n for x in c),'width and ids')
        check(len({abs(x) for x in c})==len(c),'proper clause')
        offsets.append(off);cs.append(c);off+=len(line)
    check(len(cs)==m and off==len(raw),'complete file')
    return n,tuple(cs),tuple(offsets)

def authentic(raw,off,n):
    # Independently read the claimed line directly from the immutable source bytes.
    head_end=raw.find(b'\n')+1
    if type(off)!=int or off<head_end or off>=len(raw) or raw[off-1:off]!=b'\n':
        raise ValueError('forged source offset')
    e=raw.find(b'\n',off)
    if e<0: raise ValueError('unterminated source line')
    try: vals=tuple(map(int,raw[off:e].decode('ascii').split()))
    except (ValueError,UnicodeError):raise ValueError('invalid clause bytes')
    if not vals or vals[-1]!=0 or any(v==0 or abs(v)>n for v in vals[:-1]) or not 1<=len(vals)-1<=3 or len({abs(v) for v in vals[:-1]})!=len(vals)-1:raise ValueError('invalid source clause')
    return tuple(vals[:-1])

def residual(c,sigma):
    r=[]
    for lit in c:
        v=abs(lit)
        if v in sigma:
            if sigma[v] == (lit>0):return None   # clause satisfied
        else:r.append(lit)
    return tuple(r)

def verify_tree(raw,n,node,sigma=None,depth=0):
    if sigma is None:sigma={}
    kind=node['type']
    if kind=='BRANCH':
        x=node['x']
        if not 1<=x<=n or x in sigma:return False
        for bit,key in [(False,'zero'),(True,'one')]:
            child=dict(sigma);child[x]=bit
            if not verify_tree(raw,n,node[key],child,depth+1):return False
        return True
    if kind=='EMPTY':
        try:c=authentic(raw,node['offset'],n)
        except ValueError:return False
        return residual(c,sigma)==()
    if kind=='PATH':
        x=node['x']
        if not 1<=x<=n or x in sigma:return False
        for k,start,finish in [('plus',x,-x),('minus',-x,x)]:
            cur=start;edges=node[k]
            if not edges or len(edges)>2*n-1:return False
            for off,u,v in edges:
                if cur!=u:return False
                try:c=authentic(raw,off,n)
                except ValueError:return False
                r=residual(c,sigma)
                if r is None or len(r) not in (1,2):return False
                if len(r)==1:
                    if not (u==-r[0] and v==r[0]):return False
                elif not ((u==-r[0] and v==r[1]) or (u==-r[1] and v==r[0])):return False
                if abs(u) in sigma or abs(v) in sigma:return False
                cur=v
            if cur!=finish:return False
        return True
    return False

def bfs_path(start,end,adj):
    q=deque([start]);parent={start:None};fromedge={}
    while q:
        u=q.popleft()
        if u==end:break
        for v,off in adj[u]:
            if v not in parent:parent[v]=u;fromedge[v]=(off,u,v);q.append(v)
    if end not in parent:return None
    out=[];cur=end
    while parent[cur] is not None:out.append(fromedge[cur]);cur=parent[cur]
    out.reverse();return out

def path_terminal(n,cs,offs,sigma):
    adj=defaultdict(list)
    for c,off in zip(cs,offs):
        r=residual(c,sigma)
        if r is None:continue
        if len(r)==0:return {'type':'EMPTY','offset':off}
        if len(r)==1:
            a=r[0];adj[-a].append((a,off))
        if len(r)==2:
            a,b=r;adj[-a].append((b,off));adj[-b].append((a,off))
    for x in range(1,n+1):
        if x in sigma:continue
        p=bfs_path(x,-x,adj);q=bfs_path(-x,x,adj)
        if p and q:return {'type':'PATH','x':x,'plus':p,'minus':q}
    return None

def build_tree(n,cs,offs,sigma=None):
    if sigma is None:sigma={}
    terminal=path_terminal(n,cs,offs,sigma)
    if terminal is not None:return terminal
    openvars=[x for x in range(1,n+1) if x not in sigma]
    if not openvars:return None
    x=openvars[0];lo=dict(sigma);lo[x]=False;hi=dict(sigma);hi[x]=True
    a=build_tree(n,cs,offs,lo);b=build_tree(n,cs,offs,hi)
    if a is None or b is None:return None
    return {'type':'BRANCH','x':x,'zero':a,'one':b}

def resolve(a,b,x):
    aa=set(a);bb=set(b)
    if x in aa and -x in bb:aa.remove(x);bb.remove(-x)
    elif -x in aa and x in bb:aa.remove(-x);bb.remove(x)
    else: raise ValueError(f'bad resolution pivot {x}: {a} {b}')
    return clause_norm(aa|bb)

class Resolution:
    def __init__(self,raw):
        self.raw=raw
        self.n,self.cs,self.offs=parse(raw)
        self.lines=[]
        self.axioms={}
        for c,off in zip(self.cs,self.offs):
            idx=len(self.lines);self.lines.append({'op':'source','offset':off,'clause':clause_norm(c)})
            self.axioms[off]=idx
    def weak(self,parent,target):
        target=clause_norm(target)
        if not set(self.lines[parent]['clause']).issubset(target):raise ValueError('nonmonotone weakening')
        k=len(self.lines);self.lines.append({'op':'weak','from':parent,'clause':target});return k
    def res(self,left,right,pivot):
        target=resolve(self.lines[left]['clause'],self.lines[right]['clause'],pivot)
        k=len(self.lines);self.lines.append({'op':'resolve','left':left,'right':right,'pivot':pivot,'clause':target});return k
    def emit(self,node,sigma=()):
        a=set(-v for v in sigma)  # sigma stores signed literal that is TRUE
        kind=node['type']
        if kind=='EMPTY':
            k=self.weak(self.axioms[node['offset']],a)
        elif kind=='PATH':
            terminals=[]
            for label in ('plus','minus'):
                start=node['x'] if label=='plus' else -node['x']
                target=-start
                prev=None
                for off,u,v in node[label]:
                    # Resolving an implication path can reach its needed
                    # endpoint early after encountering a unit edge.
                    if prev is not None and set(self.lines[prev]['clause']).issubset(a|{target}):
                        break
                    litset={-u,v};cl=litset|a
                    edge_idx=self.weak(self.axioms[off],cl)
                    if prev is not None:
                        edge_idx=self.res(prev,edge_idx,abs(u))
                    prev=edge_idx
                if prev is None or not set(self.lines[prev]['clause']).issubset(a|{target}):
                    raise ValueError('PATH lifting failed')
                terminals.append(prev)
                if set(self.lines[prev]['clause'])==a:
                    return prev
            k=self.res(*terminals,node['x'])
        elif kind=='BRANCH':
            k0=self.emit(node['zero'],sigma+(-node['x'],))
            k1=self.emit(node['one'],sigma+(node['x'],))
            k=self.res(k0,k1,node['x'])
        else:raise ValueError('unknown proof node')
        if set(self.lines[k]['clause'])!=a:raise ValueError(f'conflict clause mismatch: got {self.lines[k]["clause"]}; wanted {a}')
        return k
    def verify(self):
        for i,line in enumerate(self.lines):
            op=line['op'];c=line['clause']
            if op=='source':
                check(c==clause_norm(authentic(self.raw,line['offset'],self.n)),'source line')
            elif op=='weak':
                check(line['from']<i and set(self.lines[line['from']]['clause']).issubset(c),'weakening')
            elif op=='resolve':
                check(line['left']<i and line['right']<i,'backward proof pointer')
                check(resolve(self.lines[line['left']]['clause'],self.lines[line['right']]['clause'],line['pivot'])==c,'resolution exact')
            else:raise ValueError('invalid proof opcode')
        check(bool(self.lines) and self.lines[-1]['clause']==(),'empty at end')
        return True

def count_tree(node):
    if node['type']=='BRANCH':
        a=count_tree(node['zero']);b=count_tree(node['one'])
        return {'B':1+a['B']+b['B'],'L':a['L']+b['L'],'E':a['E']+b['E'],'h':1+max(a['h'],b['h'])}
    if node['type']=='PATH':return {'B':0,'L':1,'E':len(node['plus'])+len(node['minus']),'h':0}
    return {'B':0,'L':1,'E':0,'h':0}

def val_formula(cs,bitmask):
    return all(any(bool((bitmask>>(abs(lit)-1))&1)==(lit>0) for lit in c) for c in cs)

def graphs():
    out={}
    out['K4']=(4,[(a,b) for a in range(4) for b in range(a+1,4)])
    out['K33']=(6,[(a,b) for a in range(3) for b in range(3,6)])
    out['Cube3']=(8,[(a,a^(1<<j)) for a in range(8) for j in range(3) if a<(a^(1<<j))])
    out['Petersen']=(10,[(i,(i+1)%5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)]+[(i,5+i) for i in range(5)])
    return out

def tseitin(vnum,edges,odd):
    inc=[[] for _ in range(vnum)]
    for i,(a,b) in enumerate(edges,1):inc[a].append(i);inc[b].append(i)
    check(all(len(v)==3 and len(set(v))==3 for v in inc),'cubic graph')
    cs=[]
    for vertex,names in enumerate(inc):
        parity=int(odd and vertex==0)
        for bits in product((0,1),repeat=3):
            if sum(bits)%2!=parity:
                cs.append(tuple(x if bit==0 else -x for x,bit in zip(names,bits)))
    occ=Counter(l for c in cs for l in c)
    check(all(occ[i]==4 and occ[-i]==4 for i in range(1,len(edges)+1)),'signed exact 4,4')
    return tuple(cs)

def main():
    cases=[]
    # Genuine source-authenticated 2-SAT implication terminal, including a forged edge.
    f2=((1,2),(1,-2),(-1,2),(-1,-2))
    raw,offs=serialize(2,f2);n,cs,ofs=parse(raw)
    pi=path_terminal(n,cs,ofs,{})
    check(pi is not None and pi['type']=='PATH','two-sided implication witness')
    check(verify_tree(raw,n,pi),'verified authentic PATH')
    dag=Resolution(raw);dag.emit(pi);dag.verify()
    check(not any(val_formula(cs,a) for a in range(4)),'2SAT UNSAT')
    forg=json.loads(json.dumps(pi));forg['plus'][0][0]+=1
    check(not verify_tree(raw,n,forg),'forged source offset rejected')
    cases.append({'case':'four-clause_2SAT_UNSAT','source_bytes':len(raw),'certificate':count_tree(pi),'resolution_lines':len(dag.lines)})
    # A complete BRANCH tree with two real recursive levels on connected cubic instances.
    for name,(nv,edges) in graphs().items():
        n=len(edges)
        odd=tseitin(nv,edges,True)
        even=tseitin(nv,edges,False)
        raw,offs=serialize(n,odd);other,offs2=serialize(n,even)
        check(parse(raw)[1]==odd and parse(other)[1]==even,'serialized/reparsed')
        if n<=12:
            check(not any(val_formula(odd,a) for a in range(1<<n)),name+' odd unsat exhaustive')
            check(val_formula(even,0),name+' even zero witness')
        else:
            check(val_formula(even,0),name+' even witness')
        case={'case':name,'vertices':nv,'edge_variables':n,'clauses':len(odd),'bytes':len(raw),'signed_counts':'4+,4-','SAT_even':True,'UNSAT_odd_parity':True}
        if n<=12:
            proof=build_tree(n,odd,offs)
            check(proof is not None and proof['type']=='BRANCH','nontrivial UNSAT tree')
            check(proof['zero']['type']=='BRANCH' and proof['one']['type']=='BRANCH','two real levels')
            check(verify_tree(raw,n,proof),'authenticated connected UNSAT proof')
            check(not verify_tree(other,n,proof),'even-charge SAT forged-proof rejection')
            d=Resolution(raw);root=d.emit(proof)
            check(root==len(d.lines)-1 and d.verify(),'compiled resolution DAG independently verified')
            t=count_tree(proof)
            check(t['L']==t['B']+1,'complete binary branching')
            check(len(d.lines)<=len(odd)+3*(t['E']+t['B']+t['L']),'linear translation overhead')
            case.update({'certificate':t,'resolution_lines':len(d.lines),'max_clause_width':max(len(v['clause']) for v in d.lines),'two_real_levels':True})
        cases.append(case)
    # Additional randomized 2SAT SAT/UNSAT controls, exact truth tables and PATH soundness.
    randoms={'SAT':0,'UNSAT':0,'PATH':0}
    for _ in range(96):
        vars_=RNG.randint(2,6)
        clauses=tuple(tuple((v if RNG.getrandbits(1) else -v) for v in RNG.sample(range(1,vars_+1),k=2)) for _ in range(RNG.randint(2,16)))
        raw,offs=serialize(vars_,clauses);n,parsed,ofs=parse(raw)
        sat=any(val_formula(parsed,a) for a in range(1<<n))
        randoms['SAT' if sat else 'UNSAT']+=1
        proof=path_terminal(n,parsed,ofs,{})
        if proof is not None:
            check(not sat,'no sound proof for SAT')
            check(verify_tree(raw,n,proof),'random source-auth PATH')
            d=Resolution(raw);d.emit(proof);d.verify()
            randoms['PATH']+=1
        else:check(sat,'unsat 2CNF must have implication contradiction')
    result={'run_id':RUN_ID,'seed':SEED,'checks':CHECKS,'cases':cases,'random_2sat':randoms,
            'symbolic_theorem':'Each source-authenticated BRANCH/EMPTY/PATH proof with B binary, L terminals, E edges, depth h and m input clauses converts to general-resolution refutation with O(m+B+L+E) lines and O((m+B+L+E)(h+2)log N) explicit bits. Connected cubic-expander odd-charge Tseitin formulas have resolution size exp(Omega(v)) by Ben-Sasson-Wigderson, JACM 2001, Cor 4.5. Hence this exact proof grammar requires exp(Omega(N/log N)) records on some ordinary proper 3CNFs. Does not address stronger proof systems or exact-(2,2).',
            'proof_status':{'translator':'PROVED/EXACT symbolic; finite audit','general_size_lower_bound':'KNOWN THEOREM applied to restricted proof grammar','all_unsat_polynomial_coverage_in_this_grammar':'FALSIFIED','all_input_sat_decider_lower_bound':'OPEN','exact_2_2_transport':'OPEN'}}
    result['repro_script_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    dest=Path(__file__).with_name('arc186_results.json')
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'run_id':RUN_ID,'checks':CHECKS,'random_2sat':randoms,'cases':[{k:c[k] for k in ('case','resolution_lines','certificate') if k in c} for c in cases],'json':str(dest)},indent=2))

if __name__=='__main__':main()

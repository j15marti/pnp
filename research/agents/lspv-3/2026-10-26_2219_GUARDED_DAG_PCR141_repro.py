#!/usr/bin/env python3
"""GUARDED-DAG-PCR141 audit: authentic 3CNF guarded-DAG/SCC certificates.

Standard library only.  Run twice to verify deterministic JSON.
This is a finite syntax/control audit, NOT an experimental PCR lower bound.
"""
import collections, hashlib, itertools, json, sys

ASSERTS=0
def check(c,msg):
    global ASSERTS
    ASSERTS+=1
    if not c: raise AssertionError(msg)

def pin(lit,aux0,aux1):
    return [(lit,a,b) for a,b in
            ((aux0,aux1),(aux0,-aux1),(-aux0,aux1),(-aux0,-aux1))]
def residual(C,g):
    vals=[]
    for lit in C:
        v=abs(lit)
        if v in g:
            if (lit>0)==bool(g[v]): return None
        else: vals.append(lit)
    return tuple(vals)
def evaluate(F,assignment):
    return all(any((l>0)==bool(assignment[abs(l)]) for l in C) for C in F)
def sat(F):
    names=sorted({abs(l) for C in F for l in C})
    if len(names)>18: raise ValueError("too many names in test SAT")
    for bs in itertools.product((0,1),repeat=len(names)):
        a=dict(zip(names,bs))
        if evaluate(F,a): return True
    return False
def paths_from_2cnf(F,clause_ids,g):
    # Directed edges include source ID so the checker can authenticate each edge.
    es={}
    for i in clause_ids:
        C=residual(F[i],g)
        check(C is not None and len(C)<=2,"selected residual not 2CNF")
        if len(C)==0: return {"empty":i}
        if len(C)==1:
            u,v=-C[0],C[0]
            es.setdefault(u,[]).append((v,i))
        elif len(C)==2:
            a,b=C
            es.setdefault(-a,[]).append((b,i))
            es.setdefault(-b,[]).append((a,i))
    def bfs(a,b):
        q=collections.deque([a]); pred={a:None}
        while q:
            x=q.popleft()
            if x==b: break
            for y,i in es.get(x,[]):
                if y not in pred: pred[y]=(x,i);q.append(y)
        if b not in pred:return None
        result=[];x=b
        while x!=a:
            p,i=pred[x];result.append((p,x,i));x=p
        return list(reversed(result))
    names=sorted({abs(l) for i in clause_ids for l in F[i]}-set(g))
    for x in names:
        p=bfs(x,-x);q=bfs(-x,x)
        if p is not None and q is not None:return {"pivot":x,"fwd":p,"back":q}
    return None
def verify_leaf(F,g,leaf):
    ids=leaf["ids"]
    check(all(isinstance(i,int) and 0<=i<len(F) for i in ids),"source id")
    check(len(set(ids))==len(ids),"duplicate source ids")
    if "empty" in leaf:
        check(leaf["empty"] in ids and residual(F[leaf["empty"]],g)==(),
              "unauthenticated empty terminal");return
    x=leaf["pivot"];check(x>0 and x not in g,"pivot")
    for side,start,end in (("fwd",x,-x),("back",-x,x)):
        prev=start
        for u,v,i in leaf[side]:
            check(i in ids,"incorrect source pointer")
            C=residual(F[i],g)
            check(C is not None and len(C)<=2,"unverified source reduction")
            check(u==prev,"broken directed path")
            if len(C)==1:
                check(u==-C[0] and v==C[0],"wrong unit edge")
            else:
                check(len(C)==2 and frozenset(C)==frozenset((-u,v)),
                      "wrong binary edge")
            prev=v
        check(prev==end,"path not closed")
def dag_verify(F,nodes,root="root"):
    check(nodes[root]["guard"]=={},"root guard")
    visiting=set();finished=set();reachable=set();edges=0
    def rec(k):
        nonlocal edges
        check(k in nodes,"missing DAG node")
        if k in finished:return
        check(k not in visiting,"cyclic proof DAG")
        visiting.add(k);reachable.add(k);o=nodes[k];g=o["guard"]
        check(all(isinstance(v,int) and v in (0,1) for v in g.values()),"guard values")
        check(all(isinstance(x,int) and x>0 for x in g),"guard names")
        if o["type"]=="branch":
            x=o["var"];check(x not in g,"reassigned branch")
            check(set(o["children"])=={"0","1"},"both branches")
            for v in (0,1):
                child=o["children"][str(v)]
                check(child in nodes,"missing child")
                full={**g,x:v}
                check(all(full.get(y)==z for y,z in nodes[child]["guard"].items()),
                      "unsound guard reuse; child does not follow parent path")
                edges+=1;rec(child)
        else:
            check(o["type"]=="scc","invalid node type")
            verify_leaf(F,g,o["proof"])
        visiting.remove(k);finished.add(k)
    rec(root)
    check(reachable==set(nodes),"unreachable encoded node")
    return {"nodes":len(nodes),"edges":edges,"leaves":sum(o["type"]=="scc" for o in nodes.values())}
def negate(g):
    return frozenset((v if not b else -v) for v,b in g.items())
def resolvent(A,B,x):
    check(x in A and -x in B,"resolution pivot sign")
    C=(A-{x})|(B-{-x})
    return frozenset(C)
class RP:
    def __init__(self,F):
        self.F=F;self.lines=[];self.clauses=[]
    def add(self,op,C,p=None,q=None,src=None,pivot=None):
        C=frozenset(C)
        if op=="axiom":
            check(C==frozenset(self.F[src]),"untrusted axiom")
        elif op=="weak":
            check(self.clauses[p].issubset(C),"invalid weakening")
        elif op=="resolve":
            check(C==resolvent(self.clauses[p],self.clauses[q],pivot),
                  "incorrect resolvent")
        else:raise ValueError(op)
        i=len(self.lines);self.lines.append((op,i,p,q,src,pivot))
        self.clauses.append(C);return i
    def ax(self,cid):return self.add("axiom",self.F[cid],src=cid)
    def weak(self,i,C):
        C=frozenset(C)
        return i if C==self.clauses[i] else self.add("weak",C,p=i)
    def resolve(self,i,j,x):
        return self.add("resolve",resolvent(self.clauses[i],self.clauses[j],x),
                        p=i,q=j,pivot=x)
def leaf_to_resolution(F,g,leaf,rp):
    # Derive guarded clause from an authentic residual 2CNF subset
    guard=negate(g)
    if "empty" in leaf:
        j=rp.ax(leaf["empty"])
        return rp.weak(j,guard)
    ids=leaf["ids"]
    # Closure of residual clauses by resolution, retaining a derivation DAG.
    seen={};q=collections.deque()
    for cid in ids:
        R=residual(F[cid],g)
        if R is None or len(R)>2:continue
        K=frozenset(R)
        if K not in seen:
            j=rp.ax(cid)
            j=rp.weak(j,K|guard)
            seen[K]=j;q.append(K)
    iters=0
    while frozenset() not in seen:
        old=list(seen)
        progressed=False
        for i,A in enumerate(old):
            for B in old[i+1:]:
                for x in A:
                    if -x not in B:continue
                    C=frozenset((A-{x})|(B-{-x}))
                    if C in seen:continue
                    p=rp.resolve(seen[A],seen[B],x)
                    seen[C]=p;progressed=True
                    if not C:break
                if frozenset() in seen:break
            if frozenset() in seen:break
        iters+=1
        check(progressed and iters<100,"2CNF closure failed")
    return seen[frozenset()]
def dag_to_resolution(F,nodes):
    rp=RP(F);built={}
    def rec(k):
        if k in built:return built[k]
        o=nodes[k];g=o["guard"]
        if o["type"]=="scc":
            j=leaf_to_resolution(F,g,o["proof"],rp)
        else:
            x=o["var"];jchild=[]
            for b in (0,1):
                child=o["children"][str(b)]
                j0=rec(child)
                gg={**g,x:b}
                jchild.append(rp.weak(j0,negate(gg)))
            # branch x=0 proves D_g OR x; branch x=1 proves D_g OR !x.
            j=rp.resolve(jchild[0],jchild[1],x)
        check(rp.clauses[j]==negate(g),"constructed guard clause mismatch")
        built[k]=j;return j
    end=rec("root")
    check(rp.clauses[end]==frozenset(),"not a complete refutation")
    return {"lines":len(rp.lines),"axioms":sum(a[0]=="axiom" for a in rp.lines),
            "resolutions":sum(a[0]=="resolve" for a in rp.lines),
            "weakenings":sum(a[0]=="weak" for a in rp.lines),
            "maximum_width":max(map(len,rp.clauses),default=0)}
def make_dag(F):
    # Literal y=1 is required by source clauses 0..3.
    # Literal y=0 is required by source clauses 4..7.
    t0=paths_from_2cnf(F,range(4),{1:0})
    t1=paths_from_2cnf(F,range(4,8),{1:1})
    check(t0 is not None and t1 is not None,"missing authenticated SCC paths")
    t0["ids"]=list(range(4));t1["ids"]=list(range(4,8))
    return {
    "root":{"type":"branch","guard":{},"var":2,
            "children":{"0":"a0","1":"a1"}},
    "a0":{"type":"branch","guard":{2:0},"var":1,
          "children":{"0":"no","1":"yes"}},
    "a1":{"type":"branch","guard":{2:1},"var":1,
          "children":{"0":"no","1":"yes"}},
    "no":{"type":"scc","guard":{1:0},"proof":t0},
    "yes":{"type":"scc","guard":{1:1},"proof":t1}}
def tseitin(G,charge):
    edges=sorted(tuple(sorted(e)) for e in G)
    names={e:i+1 for i,e in enumerate(edges)}
    F=[];blocks={}
    for v in sorted(set(sum(([a,b] for a,b in G),[]))):
        inc=sorted(names[e] for e in edges if v in e)
        check(len(inc)==3,"cubic graph required")
        ids=[]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2==charge.get(v,0):continue
            C=tuple(-i if b else i for i,b in zip(inc,bits))
            ids.append(len(F));F.append(C)
        blocks[v]=ids
    return F,blocks
def check_parity_blocks(F,blocks,charge):
    counts=collections.Counter()
    for v,ids in blocks.items():
        names=sorted({abs(l) for i in ids for l in F[i]})
        check(len(ids)==4 and len(names)==3,"invalid parity bundle")
        for bits in itertools.product((0,1),repeat=3):
            a=dict(zip(names,bits))
            holds=all(any((lit>0)==bool(a[abs(lit)]) for lit in F[i])
                      for i in ids)
            check(holds == (sum(bits)%2==charge.get(v,0)),"source parity mismatch")
        for i in names:counts[i]+=1
    check(all(v==2 for v in counts.values()),"parity edge not paired")
    return {"vertex_bundles":len(blocks),"paired_edges":len(counts),
            "aggregate_charge":sum(charge.values())%2}
def regular_exact22(F):
    cnt=collections.Counter((abs(l),l>0) for C in F for l in C)
    return all(cnt[v,1]==2 and cnt[v,0]==2
               for v in {abs(l) for C in F for l in C})
def proper(F):
    return all(len(C)==3 and len({abs(l) for l in C})==3 for C in F)
def k4_encoding():
    # Four-vertex K4 standard 3-colour CNF and its source-named properization.
    vertices=range(4);edges=list(itertools.combinations(vertices,2))
    base=[]
    for v in vertices:
        xs=[3*v+c+1 for c in range(3)]
        base.append(tuple(xs))
        for a,b in itertools.combinations(xs,2):base.append((-a,-b))
    for v,w in edges:
        for c in range(3):base.append((-(3*v+c+1),-(3*w+c+1)))
    h=[];aux=13
    for C in base:
        if len(C)==3:h.append(C)
        else:
            h.extend([(*C,aux),(*C,-aux)]);aux+=1
    check(proper(h),"properization broken")
    for bits in itertools.product((0,1),repeat=12):
        a={i+1:bits[i] for i in range(12)}
        q=all(any((l>0)==bool(a[abs(l)]) for l in C) for C in base)
        proj=all(any((l>0)==bool(a[abs(l)]) for l in C)
                 for C in h if all(abs(l)<=12 for l in C)) and all(
                     (any((l>0)==bool(a[abs(l)]) for l in C[:2]))
                     for C in h if any(abs(l)>12 for l in C))
        check(q==proj,"properization existential extension mismatch")
    check(not any(
        all(any((l>0)==bool(a[abs(l)]) for l in C) for C in base)
        for bits in itertools.product((0,1),repeat=12)
        for a in ({i+1:bits[i] for i in range(12)},)), "K4 must fail 3-colour")
    return {"standard_clauses":len(base),"proper_clauses":len(h),
            "proper_variables":aux-1,"source_assignment_checks":4096}

def main():
    # Original source clause identities are 0-based.
    F=pin(1,2,3)+pin(-1,4,5)
    check(proper(F) and not sat(F),"PIN source invalid")
    nodes=make_dag(F);stats=dag_verify(F,nodes)
    pr=dag_to_resolution(F,nodes)
    check(stats=={"nodes":5,"edges":6,"leaves":2},"guard-DAG sharing count")
    invalid=0
    def hostile(fn):
        nonlocal invalid
        try:fn()
        except (AssertionError,KeyError,IndexError,ValueError):invalid+=1
        else:raise AssertionError("hostile forged proof accepted")
    hostile(lambda:dag_verify(F[:-1],nodes))
    forged={k:{**v} for k,v in nodes.items()}
    forged["no"]={**forged["no"],"guard":{1:0,5:1}}
    hostile(lambda:dag_verify(F,forged))
    forged={k:{**v} for k,v in nodes.items()}
    forged["a0"]={**forged["a0"],"children":{"0":"no"}}
    hostile(lambda:dag_verify(F,forged))
    forged={k:{**v} for k,v in nodes.items()}
    forged["no"]={**forged["no"],"proof":{**forged["no"]["proof"],
                                         "ids":[7]+list(range(1,4))}}
    hostile(lambda:dag_verify(F,forged))
    hostile(lambda:dag_verify(pin(1,2,3),nodes))
    for C in F:
        check(len(C)==3 and len({abs(x) for x in C})==3,"source nonproper")
    Wraw="""-1 3 -14; 2 -8 9; 10 -13 14; 3 7 -13; -4 -9 -11;
5 8 -14; 4 -8 -11; 1 7 13; 1 -7 10; -5 -6 -15;
-2 -6 12; -4 9 -10; -2 5 -12; -3 6 -15; 6 -7 11;
2 -9 11; 4 8 -10; -3 12 15; -5 -12 15; -1 13 14"""
    W=[tuple(map(int,c.split())) for c in Wraw.split(";")]
    check(len(W)==20 and proper(W) and regular_exact22(W),"W1 regularity")
    bs=(2,4,7,14,15)
    successes=0
    for bits in itertools.product((0,1),repeat=5):
        g=dict(zip(bs,bits))
        ids=[i for i,C in enumerate(W)
             if (r:=residual(C,g)) is not None and len(r)<=2]
        term=paths_from_2cnf(W,ids,g)
        check(term is not None,"W1 SCC leaf missing")
        term["ids"]=ids;verify_leaf(W,g,term);successes+=1
    check(not sat(W),"W1 UNSAT label")
    good_model_counts=[]
    for u,v in ((0,0),(0,1),(1,0)):
        H=list(W)
        if u==0:
            for j in (6,11):
                C=list(H[j]);C[0]=-C[0];H[j]=tuple(C)
        if v==0:
            for j in (9,17):
                C=list(H[j]);C[2]=-C[2];H[j]=tuple(C)
        check(proper(H) and regular_exact22(H) and sat(H),"signed 22 SAT control")
        good_model_counts.append((u,v))
    G=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    charges=[]
    for c in (0,1):
        ch={0:c}
        T,blocks=tseitin(G,ch)
        check(proper(T),"Tseitin not proper ternary")
        assert_stat=check_parity_blocks(T,blocks,ch)
        check(sat(T)==(c==0),"Tseitin charge parity wrong")
        charges.append(assert_stat)
    colour=k4_encoding()
    out={"id":"GUARDED-DAG-PCR141","assertions":ASSERTS,
         "failures":0,"source_pin":{"variables":5,"clauses":len(F),
                                  "guard_dag":stats,"resolution_compiler":pr,
                                  "forged_rejections":invalid},
         "strict_22":{"W1_variables":15,"W1_clauses":20,
                      "SCC_leaf_controls":successes,"SAT_sign_flips":good_model_counts},
         "odd_tseitin_K4":charges,"K4_colour_properization":colour,
         "model_scope":"finite authenticated proof syntax only; no TM runtime measured",
         "proof_hardness":"published PCR degree/size is analytic, not experimentally inferred"}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()

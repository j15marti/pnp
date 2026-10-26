#!/usr/bin/env python3
"""ARC177: occurrence-preserving M22 projected-child compiler.

Pure Python, no solver packages required. Run from any directory:
    python arc177_m22_compiler.py --output arc177_results.json
The original 198-variable 264-clause source is embedded below (also bundled as JSON).
Checks a freshly generated 32-variable DPLL refutation and its six-module
lift to U. Witnesses and small truth tables are checked directly. It does
NOT claim exhaustive search over all assignments of the large outputs,
physical FLMV instruction measurement, or an all-input ARC speedup.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
from dataclasses import dataclass
import argparse, hashlib, json, math, random, time

HERE = Path(__file__).resolve().parent
ORIGINAL_U_JSON = r'''[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]]'''
U = tuple(tuple(c) for c in json.loads(ORIGINAL_U_JSON))
W_BITS = '010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001'
W = {i+1: b == '1' for i,b in enumerate(W_BITS)}
Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
V0 = [list(c) for c in U]
V0[1][0], V0[7][0] = V0[7][0], V0[1][0]
V = tuple(tuple(c) for c in V0)
FACTORY = U[:1] + U[2:]
PORTS = U[1]


def variables(cs): return sorted({abs(l) for c in cs for l in c})
def sat_by(cs, a): return all(any(a[abs(l)] == (l>0) for l in c) for c in cs)
def canon(cs): return tuple(dict.fromkeys(tuple(sorted(c,key=lambda x:(abs(x),x))) for c in cs))
def negate(cs): return tuple(tuple(-l for l in c) for c in cs)
def restrict(cs,a):
    return canon(tuple(l for l in c if abs(l) not in a)
                 for c in cs if not any(abs(l) in a and a[abs(l)] == (l>0) for l in c))
def truth_models(cs):
    vs=variables(cs)
    if len(vs)>16: raise ValueError('Truth-table guard: more than 16 variables')
    for vals in product((False,True),repeat=len(vs)):
        a=dict(zip(vs,vals))
        if sat_by(cs,a): yield a


def m22(cs, nonpaired=True):
    if not cs: return False
    cnt=Counter(l for c in cs for l in c)
    return (all(len(c)==3 and len(set(map(abs,c)))==3 and
                (all(l>0 for l in c) or all(l<0 for l in c)) for c in cs)
            and len(set(frozenset(c) for c in cs))==len(cs)
            and all(cnt[v]==cnt[-v]==2 for v in variables(cs))
            and (not nonpaired or any(frozenset(-l for l in c) not in
                   {frozenset(d) for d in cs} for c in cs)))


def connected(cs):
    adj=defaultdict(set)
    for c in cs:
        vs=list(map(abs,c))
        for v in vs: adj[v].update(vs)
    todo=[next(iter(adj))]; seen=set(todo)
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen: seen.add(v);todo.append(v)
    return len(seen)==len(adj)


def serial(cs):
    n=max(variables(cs), default=0)
    return (f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode()


def parse(data):
    ls=data.decode().splitlines(); h=ls[0].split()
    if len(h)!=4 or h[:2]!=['p','cnf']: raise ValueError('Bad header')
    n,m=map(int,h[2:]); cs=[]
    for ln in ls[1:]:
        x=tuple(map(int,ln.split()))
        if not x or x[-1]!=0 or any(l==0 or abs(l)>n for l in x[:-1]): raise ValueError('Bad clause')
        cs.append(x[:-1])
    if len(cs)!=m: raise ValueError('Bad clause count')
    return tuple(cs)


def neutral(x,y,z,aux,sign=1):
    a,b,c,d,e,f=aux
    cs=((a,y,z),(x,b,c),(a,d,e),(b,d,f),(c,e,f),
        (-a,-b,-d),(-a,-c,-f),(-b,-c,-e),(-d,-e,-f))
    return cs if sign==1 else negate(cs)


def dpll_refute(cs):
    units=[]
    while True:
        if any(not c for c in cs): return [units,0]
        if not cs: return None
        lit=next((c[0] for c in cs if len(c)==1),None)
        if lit is None: break
        units.append(lit)
        cs=[tuple(x for x in c if x!=-lit) for c in cs if lit not in c]
    scores=Counter()
    for c in cs:
        for lit in c: scores[abs(lit)]+=4**(3-len(c))
    v=max(scores,key=scores.get)
    left=dpll_refute(cs+[(v,)])
    if left is None: return None
    right=dpll_refute(cs+[(-v,)])
    if right is None: return None
    return [units,v,left,right]


def check_refutation(source,proof):
    """Independent evaluator checks forced units and both branches from source."""
    nodes=0
    def visit(p,a):
        nonlocal nodes
        nodes+=1
        for l in p[0]:
            assert abs(l) not in a
            # Must be a unit consequence in at least one original clause.
            supported=False
            for c in source:
                if any(abs(q) in a and a[abs(q)]==(q>0) for q in c): continue
                remaining=[q for q in c if abs(q) not in a]
                if remaining==[l]: supported=True;break
            assert supported
            a[abs(l)]=(l>0)
        if p[1]==0:
            assert any(all(abs(q) in a and a[abs(q)]!=(q>0) for q in c) for c in source)
            return
        v=p[1];assert v not in a
        # Proof generator includes the decision as the first unit in each child.
        for value,child in [(True,p[2]),(False,p[3])]:
            assert child[0][0] == (v if value else -v)
            c2=[child[0][1:],*child[1:]]
            visit(c2,{**a,v:value})
    visit(proof,{})
    return nodes


@dataclass
class Compiled:
    clauses: tuple
    copies: list
    factories: list
    neutral_gadgets: list
    ymap: dict
    special: str | None
    n: int
    m: int
    literals: int
    deficits: int
    missing_positions: int


def compile_m22(source):
    """Exact SAT-preserving compiler for monotone width<=3, per-sign degree<=2.
    Output always belongs to the strict non-fully-paired M22 class.
    """
    cs=canon(source)
    if any(not c for c in cs): return Compiled(U,[],[],[],{},'UNSAT',0,0,0,0,0)
    if not cs: return Compiled(Y,[],[],[],{},'SAT',0,0,0,0,0)
    if any(len(c)>3 or not(all(l>0 for l in c) or all(l<0 for l in c))
           or len(set(map(abs,c)))!=len(c) for c in cs): raise ValueError('Outside monotone short-clause grammar')
    count=Counter(l for c in cs for l in c)
    if max(count.values())>2: raise ValueError('Per-polarity occurrence cap exceeded')
    vs=variables(cs); nxt=0
    def allocate(k):
        nonlocal nxt
        ans=list(range(nxt+1,nxt+k+1));nxt+=k;return ans
    copies=[dict(zip(vs,allocate(len(vs)))) for _ in range(3)]
    out=[]; factories=[]; ng=[]; deficit=0
    last={abs(l):i for i,c in enumerate(cs) for l in c}
    # Corresponding clauses of the three copies are emitted together.
    for ci,c in enumerate(cs):
        sign=1 if c[0]>0 else -1
        ports=[]
        for _ in range(3-len(c)):
            ids=allocate(198); mapping={i+1:v for i,v in enumerate(ids)}
            for fc in FACTORY:
                out.append(tuple(sign*(1 if l>0 else -1)*mapping[abs(l)] for l in fc))
            ports.append([mapping[v] for v in PORTS]);factories.append((mapping,sign))
        for j in range(3):
            out.append(tuple(sign*copies[j][abs(l)] for l in c)+tuple(sign*p[j] for p in ports))
        # Finish a variable's occurrence deficits immediately after its last
        # source use. No long-distance coupling between the three copies.
        for v in sorted({abs(l) for l in c}):
            if last[v]!=ci: continue
            for sg in (1,-1):
                for _ in range(2-count[sg*v]):
                    ids=allocate(6); ps=[copies[j][v] for j in range(3)]
                    g=neutral(*ps,ids,sg);out.extend(g);ng.append((ps,ids,sg));deficit+=1
    ym=dict(zip(range(1,7),allocate(6)))
    out.extend(tuple((1 if l>0 else -1)*ym[abs(l)] for l in c) for c in Y)
    L=sum(map(len,cs));E=sum(3-len(c) for c in cs)
    assert nxt==3*len(vs)+198*E+6*deficit+6
    assert len(out)==3*len(cs)+263*E+9*deficit+8
    return Compiled(tuple(out),copies,factories,ng,ym,None,len(vs),len(cs),L,deficit,E)


YMODEL=next(truth_models(Y))


def extend_witness(comp,source_model):
    if comp.special=='UNSAT': raise ValueError('No witness for contradiction')
    if comp.special=='SAT': return YMODEL.copy()
    a={}
    for mapping in comp.copies:
        for old,new in mapping.items(): a[new]=source_model[old]
    for mapping,sign in comp.factories:
        for old,new in mapping.items(): a[new]=W[old] if sign==1 else not W[old]
    for ps,ids,sign in comp.neutral_gadgets:
        g=neutral(*ps,ids,sign)
        for bits in product((False,True),repeat=6):
            trial={**a,**dict(zip(ids,bits))}
            if sat_by(g,trial):
                a.update(zip(ids,bits));break
        else: raise AssertionError('Neutral gadget lacks extension')
    for old,new in comp.ymap.items(): a[new]=YMODEL[old]
    assert sat_by(comp.clauses,a)
    return a


def monotoneize(source):
    """Linear-size ordinary width<=3 to monotone per-sign-degree<=2 compiler.
    Occurrence copies are equated by a directed implication cycle. A mixed
    clause P OR N becomes (P OR z) AND (N OR NOT z). All costs are explicit.
    """
    clean=[]
    for c in source:
        c=tuple(dict.fromkeys(c))
        if len(c)>3: raise ValueError('Expected width at most three')
        if any(-l in c for l in c): continue
        clean.append(c)
    if any(not c for c in clean): return ((),),{},[]
    clean=canon(clean);occ=defaultdict(list);out=[];links=[];nxt=0
    for c in clean:
        cc=[]
        for l in c:
            nxt+=1;occ[abs(l)].append(nxt);cc.append(nxt if l>0 else -nxt)
        out.append(tuple(cc))
    for group in occ.values():
        if len(group)>1:
            for i,v in enumerate(group): out.append((-v,group[(i+1)%len(group)]))
    mono=[]
    for c in out:
        pos=tuple(l for l in c if l>0);neg=tuple(l for l in c if l<0)
        if pos and neg:
            nxt+=1;mono.extend([pos+(nxt,),neg+(-nxt,)])
            links.append((nxt,pos))
        else: mono.append(c)
    cnt=Counter(l for c in mono for l in c)
    assert max(cnt.values(),default=0)<=2
    return tuple(mono),dict(occ),links


def monotone_witness(a,occ,links):
    b={new:a[old] for old,news in occ.items() for new in news}
    for z,pos in links: b[z]=not any(b[x] for x in pos)
    return b


def width(cs):
    count=Counter(abs(l) for c in cs for l in c);live=set();peak=0
    for c in cs:
        for l in c:
            v=abs(l);live.add(v);count[v]-=1
        for l in c:
            if count[abs(l)]==0: live.discard(abs(l))
        peak=max(peak,len(live))
    return peak


def boundary_stats(cs):
    b=math.isqrt(len(cs))+(math.isqrt(len(cs))**2<len(cs))
    occ=defaultdict(set)
    for i,c in enumerate(cs):
        for l in c: occ[abs(l)].add(i//b)
    widths=[]
    for start in range(0,len(cs),b):
        j=start//b;bv={abs(l) for c in cs[start:start+b] for l in c if len(occ[abs(l)])>1}
        widths.append(len(bv))
    return {'clauses_per_block':b,'blocks':len(widths),'max_boundary_bits':max(widths),
            'full_boundary_queries':sum(1<<w for w in widths),'boundary_bits':widths}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'arc177_results.json')
    args=ap.parse_args();start=time.perf_counter();checks=0
    def check(ok):
        nonlocal checks
        assert ok;checks+=1
    for f in (U,V,Y):check(m22(f));check(connected(f));check(parse(serial(f))==f)
    check(len(W)==198);check(sat_by(FACTORY,W));check(not sat_by(U,W));check(sat_by(V,W))
    check(all(not W[v] for v in PORTS))
    # Fresh independent refutation of the 32-variable enforcer.
    M=[tuple(l for l in c if abs(l)<=32) for c in U[2:44]]
    proof=dpll_refute(M);check(proof is not None)
    proofnodes=check_refutation(M,proof)
    core=list(U[:2])
    for j in range(6):
        block=U[2+42*j:2+42*(j+1)];sign=1 if j<3 else -1
        normalized=[tuple(sign*(1 if l>0 else -1)*(abs(l)-32*j)
                          for l in c if 32*j<abs(l)<=32*j+32) for c in block]
        check(normalized==M)
        terminals=tuple(dict.fromkeys(l for c in block for l in c if abs(l)>192))
        core.append(terminals)
    check(not any(truth_models(core)))
    (HERE/'M32_refutation.json').write_text(json.dumps(proof))
    neutral_counts={}
    for sign in (1,-1):
        counts=[]
        g=neutral(1,2,3,range(4,10),sign)
        for bits in product((False,True),repeat=3):
            count=sum(sat_by(g,dict(zip(range(1,10),bits+aux))) for aux in product((False,True),repeat=6))
            check(count>0);counts.append(count)
        neutral_counts[str(sign)]=counts
    # Small arbitrary ordinary-CNF controls, then both concrete compilers.
    rng=random.Random(177);small=[]
    for _ in range(40):
        cs=[]
        for _ in range(rng.randrange(1,8)):
            vs=rng.sample(range(1,5),rng.randrange(1,4));cs.append(tuple(v*rng.choice((-1,1)) for v in vs))
        small.append(tuple(cs))
    small.extend([((1,),(-1,)),(),((1,2,3),(-1,-2,-3)),((1,-1),)])
    records=[];extensions=0;sat_roots=unsat_roots=0;encoded_total=0
    for f in small:
        ms=list(truth_models(f));sat_roots+=bool(ms);unsat_roots+=not bool(ms)
        h,occ,links=monotoneize(f);c=compile_m22(h)
        check(m22(c.clauses));check(parse(serial(c.clauses))==c.clauses)
        check(width(c.clauses)<=3*width(h)+210)
        if len(variables(h))<=16: check(bool(list(truth_models(h)))==bool(ms))
        for model in ms[:4]:
            hm=monotone_witness(model,occ,links)
            check(sat_by(h,hm));cm=extend_witness(c,hm);check(sat_by(c.clauses,cm));extensions+=1
        encoded_total+=len(serial(c.clauses))
        records.append({'source_variables':len(variables(f)),'source_clauses':len(f),
                        'sat':bool(ms),'target_variables':len(variables(c.clauses)),
                        'target_clauses':len(c.clauses)})
    # Genuine two-level restriction + class-restoration, on genuine M22 roots.
    # U truth is certificate-controlled, Y by exhaustive truth tables, V witness path.
    nested=[];first_calls=second_calls=0
    for name,f,x,y,wit in [('Y',Y,1,2,None),('U',U,194,196,None),('V',V,194,196,W)]:
        for bx in ((False,True) if wit is None else (wit[x],)):
            h1=restrict(f,{x:bx});c1=compile_m22(h1);first_calls+=1
            check(m22(c1.clauses));check(parse(serial(c1.clauses))==c1.clauses)
            labels1= False if name=='U' else (bool(list(truth_models(h1))) if name=='Y' else True)
            if wit:
                w1=extend_witness(c1,wit)
            # Choose y in the first source copy, not in the neutral gadgets.
            py=c1.copies[0][y]
            for by in ((False,True) if wit is None else (wit[y],)):
                h2=restrict(c1.clauses,{py:by});c2=compile_m22(h2);second_calls+=1
                check(m22(c2.clauses));check(parse(serial(c2.clauses))==c2.clauses)
                hsource=restrict(f,{x:bx,y:by})
                label=False if name=='U' else (bool(list(truth_models(hsource))) if name=='Y' else True)
                if name=='Y' and label:
                    original={**next(truth_models(hsource)),x:bx,y:by}
                    w1=extend_witness(c1,original)
                    check(w1[py]==by);w2=extend_witness(c2,w1);check(sat_by(c2.clauses,w2))
                if wit: w2=extend_witness(c2,w1);check(sat_by(c2.clauses,w2))
                nested.append({'root':name,'pin1':int(bx),'pin2':int(by),'sat':label,
                    'parent_clauses':len(f),'first_clauses':len(c1.clauses),'second_clauses':len(c2.clauses),
                    'first_variables':len(variables(c1.clauses)), 'second_variables':len(variables(c2.clauses))})
    # Neutral exact-count restoration after projecting clauses in actual U blocks.
    # Sample boundaries, never pretend to enumerate the astronomical full fanout.
    block_records=[];sample_calls=0
    for name,f,wit in [('U',U,None),('V',V,W)]:
        b=math.isqrt(len(f))+1
        for starti in range(0,len(f),b):
            block=f[starti:starti+b];inside=set(variables(block));outside=set(variables(f[:starti]+f[starti+b:]));boundary=inside&outside
            a={v:(wit[v] if wit else bool((v+starti)%2)) for v in boundary}
            residual=restrict(block,a);child=compile_m22(residual);sample_calls+=1
            check(m22(child.clauses))
            boundary_occ=sum(abs(l) in boundary for cc in block for l in cc)
            if child.special is None:
                check(child.deficits<=2*(boundary_occ-child.missing_positions))
                check(len(child.clauses)<=3*len(block)+263*boundary_occ+8)
                check(width(child.clauses)<=3*width(residual)+210)
            if wit:
                check(sat_by(residual,wit));check(sat_by(child.clauses,extend_witness(child,wit)))
            block_records.append({'root':name,'block_start':starti,'boundary_bits':len(boundary),
                'residual_clauses':len(residual),'compiled_clauses':len(child.clauses),'compiled_variables':len(variables(child.clauses)), 'boundary_occurrences':boundary_occ,'E':child.missing_positions,'D':child.deficits,'residual_width':width(residual),'compiled_width':width(child.clauses)})
    out={'id':'ARC-M22-PROJECTED-CLOSURE177','status':'Restricted exact compiler and finite controls; all-input ARC-EDGE-90 OPEN',
         'fixed_source':{'U_variables':198,'U_clauses':264,'U_unsat_certificate_nodes':proofnodes,
         'core_assignments_checked':64,'U_connected':True,'V_connected':True,'V_swap':[[1,0],[7,0]],
         'deleted_positive_clause':list(PORTS),'factory_variables':198,'factory_clauses':263},
         'small_controls':{'roots':len(small),'SAT':sat_roots,'UNSAT':unsat_roots,'witness_extensions':extensions,
             'compiled_encoded_bytes':encoded_total},'neutral_extension_counts':neutral_counts,
         'two_real_levels':{'first_calls':first_calls,'second_calls':second_calls,'records':nested},
         'actual_doecker_blocks':{'sampled_calls':sample_calls,'records':block_records,
             'U_boundary_fanout':boundary_stats(U),'V_boundary_fanout':boundary_stats(V)},
         'checks':checks,'failed_checks':0,'seed':177,'small_records':records,
         'compiler_exact_counts':'n_out=3n+198E+6D+6; m_out=3m+263E+9D+8; E=3m-L; D=4n-L',
         'compiler_bounds':'n_out<=417m+6, m_out<=556m+8; for a q-clause M22 block with b boundary variables, m_out<=3q+789b+8; special empty-clause case uses U',
         'limitations':['Large compiled outputs were not all solved by an independent general SAT solver.',
             'UNSAT control uses a checked M32 refutation, exhaustive six-variable core, and the proved compiler semantics.',
             'The two pin/restoration levels expand; they test class closure, not resource contraction.',
             'Neutral gadgets are placed after their ports last source use; the proved width bound is 3w+210, not unchanged width.',
             'High-boundary block assignments are sampled, not fully enumerated; full counts are reported.',
             'No all-input simultaneous FLMV improvement or free parent-scale reduction is claimed.'],
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'U_normalized_sha256':hashlib.sha256(json.dumps(U,separators=(',',':')).encode()).hexdigest(),
         'elapsed_seconds':time.perf_counter()-start}
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ('id','checks','failed_checks','small_controls','elapsed_seconds')},indent=2))
    print(json.dumps(out['fixed_source'],indent=2));print('First/second:',first_calls,second_calls)
    print('U full block fanout:',out['actual_doecker_blocks']['U_boundary_fanout'])

if __name__=='__main__':main()

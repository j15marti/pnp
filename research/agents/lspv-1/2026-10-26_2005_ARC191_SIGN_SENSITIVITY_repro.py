#!/usr/bin/env python3
"""ARC191: connected cubic Tseitin source bit-sensitivity and balanced two-flip controls.
All mathematical conclusions are proved in the companion LaTeX; tests are finite.
This script uses only Python's standard library. Usage:
    python 2026-10-26_2005_ARC191_SIGN_SENSITIVITY_repro.py [output.json]
"""
import hashlib, itertools, json, pathlib, sys, time

checks = 0

def require(condition, label="assertion"):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

def prism(h):
    require(h >= 3)
    V = [(a, i) for a in range(2) for i in range(h)]
    edges = set()
    def add(x,y):
        edges.add(tuple(sorted((V.index(x),V.index(y)))))
    for a in (0,1):
        for i in range(h):
            add((a,i),(a,(i+1)%h))
    for i in range(h):
        add((0,i),(1,i))
    E = sorted(edges)
    require(len(E)==3*h and len(V)==2*h)
    inc = [sorted([j for j,(u,v) in enumerate(E) if x in (u,v)]) for x in range(len(V))]
    require(all(len(t)==3 for t in inc))
    return V,E,inc

def connected_minus(V,E,k):
    todo = set(range(len(V)))-{k}
    reachable={next(iter(todo))}
    while True:
        x=reachable.copy()
        for (a,b) in E:
            if a in reachable and b!=k: x.add(b)
            if b in reachable and a!=k: x.add(a)
        if x==reachable: break
        reachable=x
    return reachable==todo

def connected_minus_two(V,E,v,u):
    remaining=set(range(len(V)))-{v,u}
    if not remaining:return True
    reachable={next(iter(remaining))}
    while True:
        newer=reachable.copy()
        for a,b in E:
            if a in reachable and b in remaining:newer.add(b)
            if b in reachable and a in remaining:newer.add(a)
        if newer==reachable:break
        reachable=newer
    return reachable==remaining

def tseitin(V,E,inc,charges):
    F=[]; meta=[]
    for v in range(len(V)):
        ee=inc[v]
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2 == charges[v]: continue
            clause=tuple((e+1 if bit==0 else -(e+1)) for e,bit in zip(ee,a))
            F.append(clause);meta.append((v,a,ee))
    return F,meta

def evaluate(F,assignment):
    return all(any(((lit>0)==bool(assignment[abs(lit)-1])) for lit in c) for c in F)

def counts(F,n):
    tally=[[0,0] for _ in range(n)]
    for c in F:
        require(len(c)==3)
        require(len({abs(x) for x in c})==3)
        for lit in c:tally[abs(lit)-1][int(lit>0)]+=1
    return tally

def solve_parity(V,E,inc,charges,pin=None,omit_vertex=None):
    """Solve charged vertex equations by elimination on a spanning tree.
    Pinned edges are typically the three incident edges at one vertex v.
    """
    pin=dict(pin or {})
    rhs=list(charges)
    answer=[0]*len(E)
    for i,x in pin.items():
        answer[i]=x
        u,v=E[i]
        rhs[u]^=x;rhs[v]^=x
    # The zero residual equation is required at any fully pinned vertex.
    unpinned=[i for i in range(len(E)) if i not in pin]
    adj=[[] for _ in V]
    for i in unpinned:
        u,v=E[i];adj[u].append((v,i));adj[v].append((u,i))
    seen=set();parent={};order=[]
    for root in range(len(V)):
        if root in seen: continue
        seen.add(root);order.append(root);parent[root]=None
        head=len(order)-1
        while head<len(order):
            u=order[head];head+=1
            for v,e in adj[u]:
                if v in seen:continue
                seen.add(v);parent[v]=(u,e);order.append(v)
        # This BFS lists the whole connected component, not just the first tree.
        comp=[x for x in order if parent[x] is None and x==root or x!=root and parent[x] is not None]
        # Process only vertices reached since this component root:
        # Components are processed serially; the tail is from this root.
        end=len(order)
        start=end
        while start>0 and order[start-1]!=root:start-=1
        start-=1
        for v in reversed(order[start+1:end]):
            par=parent[v]
            if par is None:continue
            p,e=par
            other=0
            for t in inc[v]:
                if t!=e and t not in pin:other^=answer[t]
            answer[e]=rhs[v]^other
        lhs=0
        for t in inc[root]:
            if t not in pin: lhs^=answer[t]
        if lhs!=rhs[root] and root!=omit_vertex:return None
    for v in range(len(V)):
        if v != omit_vertex:
            require(sum(answer[e] for e in inc[v])%2==charges[v],"parity verification")
    return answer

def signed_mutation(F,index,slot):
    B=list(F)
    c=list(B[index]);c[slot]=-c[slot];B[index]=tuple(c)
    return B

def encode_fixed(F,n):
    width=max(1,n.bit_length())
    require(len(F)<2**32 and n<2**32)
    bits="1010011011100101" +format(width,'08b')+format(n,'032b')+format(len(F),'032b')
    starts=[]
    for c in F:
        require(len(c)==3)
        for lit in c:
            starts.append(len(bits))
            bits+=('0' if lit>0 else '1')+format(abs(lit),'0%db'%width)
    return bits,starts,width

def decode_fixed(bits):
    require(bits[:16]=="1010011011100101")
    w=int(bits[16:24],2);n=int(bits[24:56],2);m=int(bits[56:88],2)
    require(w>=1 and len(bits)==88+3*m*(w+1))
    F=[];pos=88
    for _ in range(m):
        c=[]
        for _ in range(3):
            neg=bits[pos]=='1';i=int(bits[pos+1:pos+1+w],2)
            require(1<=i<=n)
            c.append(-i if neg else i);pos+=w+1
        F.append(tuple(c))
    return F

def restrict(F,pins):
    G=[]
    for c in F:
        new=[];sat=False
        for lit in c:
            if abs(lit) in pins:
                if (pins[abs(lit)]==(lit>0)):sat=True;break
            else:new.append(lit)
        if not sat:G.append(tuple(new))
    return G

def dimacs_roundtrip(F,n):
    txt='p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,c))+' 0\n' for c in F)
    lines=txt.splitlines();parts=lines[0].split()
    require(parts==['p','cnf',str(n),str(len(F))])
    decoded=[]
    for line in lines[1:]:
        z=list(map(int,line.split()))
        require(z and z[-1]==0)
        decoded.append(tuple(z[:-1]))
    require(decoded==F)
    return len(txt.encode('utf-8'))

def dpll(F):
    """Independent unit-propagating tiny SAT solver for finite controls."""
    clauses=[frozenset(c) for c in F]
    def recur(cls,ass):
        while True:
            if any(not c for c in cls):return None
            if not cls:return ass
            units=[next(iter(c)) for c in cls if len(c)==1]
            if not units:break
            lit=units[0];v=abs(lit);b=(lit>0)
            if v in ass and ass[v]!=b:return None
            ass=ass.copy();ass[v]=b
            cls=[frozenset(t for t in c if t!=-lit) for c in cls if lit not in c]
        lit=next(iter(min(cls,key=len)))
        for guess in (lit,-lit):
            v=abs(guess);b=guess>0
            if v in ass and ass[v]!=b:continue
            nxt=ass.copy();nxt[v]=b
            res=recur([frozenset(t for t in c if t!=-guess) for c in cls if guess not in c],nxt)
            if res is not None:return res
        return None
    return recur(clauses,{})

def main():
    started=time.time()
    records=[];total_single=total_double=0;total_perfect_pairs=0;total_dpll=0;total_twolevel=0
    for h in (3,4,5,6,8):
        V,E,inc=prism(h)
        n=len(E);vcount=len(V)
        require(all(connected_minus(V,E,k) for k in range(vcount)))
        odd=[0]*vcount;odd[0]=1
        even=[0]*vcount
        F,meta=tseitin(V,E,inc,odd)
        Fe,metae=tseitin(V,E,inc,even)
        require(len(F)==4*vcount and len(Fe)==len(F))
        require(all(c==[4,4] for c in counts(F,n)))
        bits,starts,w=encode_fixed(F,n)
        require(decode_fixed(bits)==F)
        nsigns=3*len(F)
        require(len(starts)==nsigns)
        expectedN=88+nsigns*(w+1)
        require(expectedN==len(bits))
        require(not evaluate(F,[0]*n))
        if h<=5:
            require(dpll(F) is None,'odd source UNSAT DPLL')
            require(dpll(Fe) is not None,'even source SAT DPLL')
            total_dpll+=2
        # Algebraic even-charge satisfaction is separately checked.
        even_w=solve_parity(V,E,inc,even)
        require(even_w is not None and evaluate(Fe,even_w))
        twoflip_rung_pairs=[]
        for ci,(v,a,ee) in enumerate(meta):
            pins=dict(zip(ee,a))
            witness=solve_parity(V,E,inc,odd,pins,omit_vertex=v)
            require(witness is not None,"2-vertex-connectivity completion")
            require(not evaluate(F,witness),'baseline must reject witness')
            for slot,e in enumerate(ee):
                p=starts[3*ci+slot]
                single=bits[:p]+('1' if bits[p]=='0' else '0')+bits[p+1:]
                Fs=decode_fixed(single)
                require(Fs==signed_mutation(F,ci,slot))
                require(evaluate(Fs,witness),"every literal sign is sensitive")
                total_single+=1
                # The OTHER endpoint has an all-three-true clause: its forbidden
                # word is the complement of its currently satisfying local assignment.
                u=next(x for x in E[e] if x!=v)
                target=tuple(1-witness[q] for q in inc[u])
                qci=next((i for i,mm in enumerate(meta) if mm[0]==u and mm[1]==target),None)
                require(qci is not None)
                qslot=inc[u].index(e)
                require((F[ci][slot]>0)!=(F[qci][qslot]>0),'opposite sign companion')
                q=starts[3*qci+qslot]
                two=bits[:p]+('1' if bits[p]=='0' else '0')+bits[p+1:]
                two=two[:q]+('1' if two[q]=='0' else '0')+two[q+1:]
                Ft=decode_fixed(two)
                require(evaluate(Ft,witness),"two flip SAT")
                require(all(z==[4,4] for z in counts(Ft,n)),"balanced signed quotas")
                require(len(set(Ft))==len(Ft),"unique clauses")
                if h<=4:
                    require(dpll(Fs) is not None,'independent single flip SAT DPLL')
                    require(dpll(Ft) is not None,'independent paired flip SAT DPLL')
                    total_dpll+=2
                total_double+=1
                if E[e][0]==v and V[v][0]==0 and V[u][0]==1: 
                    twoflip_rung_pairs.append((p,q))
        # Stronger quota-preserving claim: every edge has a perfect matching
        # between its four occurrences at its two endpoints, matching OPPOSITE
        # literal polarities. Each of the 4|E| sign-disjoint two-bit mutants
        # is SAT provided G-{u,v} is connected (true for these prisms).
        matching=[]
        for e,(v,u) in enumerate(E):
            require(connected_minus_two(V,E,v,u),"3-vertex connectivity")
            sides=[]
            for vertex in (v,u):
                items=[]
                for ci,(cv,a,ee) in enumerate(meta):
                    if cv!=vertex:continue
                    slot=ee.index(e)
                    items.append((ci,slot,F[ci][slot]>0))
                require(len(items)==4)
                sides.append(items)
            for sign in (True,False):
                xs=sorted((ci,slot) for ci,slot,p in sides[0] if p==sign)
                ys=sorted((ci,slot) for ci,slot,p in sides[1] if p!=sign)
                require(len(xs)==len(ys)==2)
                for (ci,slot),(cj,slotj) in zip(xs,ys):
                    a=meta[ci][1];ae=meta[ci][2]
                    b=meta[cj][1];be=meta[cj][2]
                    pins=dict(zip(ae,a))
                    for ex,bit in zip(be,b):
                        val=1-bit
                        if ex in pins:require(pins[ex]==val,"shared edge matching")
                        pins[ex]=val
                    witness_pair=solve_parity(V,E,inc,odd,pins,omit_vertex=v)
                    require(witness_pair is not None,"pair completion")
                    pp=starts[3*ci+slot];qq=starts[3*cj+slotj]
                    both=list(bits)
                    both[pp]='1' if both[pp]=='0' else '0'
                    both[qq]='1' if both[qq]=='0' else '0'
                    mut=decode_fixed(''.join(both))
                    require(evaluate(mut,witness_pair),"matched pair SAT")
                    require(all(z==[4,4] for z in counts(mut,n)))
                    require(len(set(mut))==len(mut))
                    if h<=4:
                        require(dpll(mut) is not None,'matched SAT independently')
                        total_dpll+=1
                    matching.append((pp,qq))
                    last_pair_mutant,last_pair_witness=mut,witness_pair
        require(len(matching)==4*n)
        require(len({x for pair in matching for x in pair})==nsigns,
                "perfect partition of all literal sign coordinates")
        total_perfect_pairs+=len(matching)
        # Rung pairs are disjoint physical sign coordinates, one per rung.
        disjoint={};
        for p,q in twoflip_rung_pairs:
            # take one per rung edge using the first chosen primary sign position
            ci=starts.index(p)//3;slot=starts.index(p)%3
            e=meta[ci][2][slot]
            if e not in disjoint:disjoint[e]=(p,q)
        rungs=[e for e,(v,u) in enumerate(E) if V[v][0]!=V[u][0]]
        require(len(rungs)==h)
        require(all(e in disjoint for e in rungs))
        positions=[x for e in rungs for x in disjoint[e]]
        require(len(set(positions))==2*h,"disjoint exact44 mutation pairs")
        # Genuine two-level ordinary CNF restrictions with source bits reserialized.
        # Odd source: any restrictions remain UNSAT. Even and two-flip sources:
        # choose the known satisfying witness and pin two original edge names.
        for label,src,wit,expected in (("odd",F,witness,False),("even",Fe,even_w,True),
                                       ("paired",last_pair_mutant,last_pair_witness,True)):
            cur=src
            for level in (1,2):
                cur=restrict(cur,{level:bool(wit[level-1])})
                dimacs_roundtrip(cur,n)
                if expected:require(evaluate(cur,wit))
                if h<=4:
                    ans=dpll(cur)
                    require((ans is not None)==expected,'two real levels '+label)
                    total_dpll+=1
                total_twolevel+=1
        records.append({"h":h,"graph_vertices":vcount,"edge_variables":n,
          "clauses":len(F),"sign_positions":nsigns,"encoded_bits":len(bits),
          "encoded_bit_sha256":hashlib.sha256(bits.encode()).hexdigest(),
          "single_sign_SAT_mutants_verified":nsigns,
          "balanced_two_sign_SAT_mutants_verified":nsigns,
          "disjoint_rung_mutation_pairs":h,
          "disjoint_exact44_mutation_pairs":len(matching),
          "independent_dpll_h":h if h<=4 else None})
    return {"run":"ARC191_SIGN_SENSITIVITY","status":"COMPUTATIONAL SUPPORT TO FORMAL LEMMAS",
            "cases":records,"one_bit_sat_mutants":total_single,
            "two_bit_exact44_sat_mutants":total_double,
            "perfect_matched_exact44_sat_mutants":total_perfect_pairs,
            "dpll_controls":total_dpll,
            "two_level_descendant_serializations":total_twolevel,
            "assertions":checks,"failures":0,
            "elapsed_seconds":round(time.time()-started,3),
            "caveat":"Connected signed exact-(4,4), NOT exact-(2,2); no SAT lower bound beyond source access; finite checks only."}

if __name__=='__main__':
    result=main()
    dest=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).with_name('2026-10-26_2005_ARC191_SIGN_SENSITIVITY_raw.json')
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
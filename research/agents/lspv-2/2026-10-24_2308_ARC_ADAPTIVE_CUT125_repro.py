#!/usr/bin/env python3
"""ARC-ADAPTIVE-CUT125: scoped-event lookahead versus fixed cuts.
Restricted input grammar only. Physical FLMV tape work/space not measured.
Standard-library Python; no dependency on the original HEREDITARY-SCOPED10.
"""
from itertools import product
import json, math

def scan(events):
    active=set(); used=set(); cuts=[tuple()]; clauses=[]; width=0
    for op,arg in events:
        if op=="O":
            assert arg>0 and arg not in used
            active.add(arg); used.add(arg)
        elif op=="C":
            assert len(arg)==3 and len({abs(x) for x in arg})==3
            assert all(abs(x) in active for x in arg)
            clauses.append(tuple(arg))
        else:
            assert op=="D" and arg in active
            active.remove(arg)
        cuts.append(tuple(sorted(active))); width=max(width,len(active))
    assert not active
    return cuts,clauses,width

def family(pairs,motifs,unsat):
    events=[("O",1)]; nxt=2
    for _ in range(motifs):
        local=[]
        for __ in range(pairs):
            a,b=nxt,nxt+1; nxt+=2; local.extend((a,b))
            events.extend((("O",a),("O",b)))
        for k in range(pairs):
            events.append(("C",(1,local[2*k],local[2*k+1])))
        for x in reversed(local): events.append(("D",x))
    c,d=nxt,nxt+1
    events.extend((("O",c),("O",d)))
    triples=[tuple(sign[i]*x for i,x in enumerate((1,c,d)))
             for sign in product((1,-1),repeat=3)]
    for i in range(8):
        events.append(("C",triples[i if unsat or i!=0 else 1]))
    events.extend((("D",d),("D",c),("D",1)))
    return tuple(events)

def fixed_cuts(L,b):
    return list(range(0,L,b))+[L]

def adaptive_cuts(cuts,b):
    L=len(cuts)-1; out=[0]; pos=0; visits=0
    while pos<L:
        hi=min(L,pos+b)
        lo=min(hi,pos+max(1,b//2))
        visits+=hi-pos
        nxt=min(range(lo,hi+1),key=lambda j:(len(cuts[j]),j))
        assert nxt>pos
        out.append(nxt);pos=nxt
    return out,visits

def proxy(bounds,cuts):
    return sum(1<<(len(cuts[a])+len(cuts[b]))
               for a,b in zip(bounds,bounds[1:]))

def pin(clauses,z,bit,next_id):
    a,b=next_id,next_id+1
    signed=z if bit else -z
    for sa,sb in product((1,-1),repeat=2):
        clauses.append((signed,sa*a,sb*b))
    return next_id+2

def child(events,left,right,u,v):
    names={}; next_id=1; clauses=[]
    def local(z):
        nonlocal next_id
        if z not in names: names[z]=next_id; next_id+=1
        return names[z]
    for x in left: local(x)
    for x,bit in zip(left,u):
        next_id=pin(clauses,local(x),bit,next_id)
    for op,arg in events:
        if op=="O": local(arg)
        if op=="C":
            clauses.append(tuple((1 if z>0 else -1)*local(abs(z))
                                 for z in arg))
    for x in right: local(x)
    for x,bit in zip(right,v):
        next_id=pin(clauses,local(x),bit,next_id)
    return tuple(clauses),len(names)+2*(len(left)+len(right))

def dpll(cnf):
    def solve(cs):
        while True:
            if not cs:return True
            if any(len(c)==0 for c in cs):return False
            units=[c[0] for c in cs if len(c)==1]
            if not units:break
            lit=units[0]
            cs=tuple(tuple(z for z in c if z!=-lit)
                     for c in cs if lit not in c)
        lit=cs[0][0]
        for chosen in (lit,-lit):
            rest=tuple(tuple(z for z in c if z!=-chosen)
                       for c in cs if chosen not in c)
            if solve(rest):return True
        return False
    return solve(tuple(map(tuple,cnf)))

def source_join(events,cuts,bounds):
    reachable={()}; calls=skipped=bits_written=0
    for start,stop in zip(bounds,bounds[1:]):
        left,right=cuts[start],cuts[stop]
        common=set(left)&set(right)
        upcoming=set()
        for ua in product((0,1),repeat=len(left)):
            if ua not in reachable:continue
            for vb in product((0,1),repeat=len(right)):
                if any(ua[left.index(x)]!=vb[right.index(x)]
                       for x in common):
                    skipped+=1;continue
                clauses,n=child(events[start:stop],left,right,ua,vb)
                calls+=1
                h=max(1,(64*(n+len(clauses)+1)-1).bit_length())
                bits_written+=(4*len(clauses)+2)*h
                if dpll(clauses):upcoming.add(tuple(vb))
        reachable=upcoming
        if not reachable:break
    return {"label":() in reachable,"calls":calls,
            "skipped":skipped,"serialized_bits":bits_written,
            "reachable_final":len(reachable)}

def tests():
    candidates=[]; tested=0
    for pairs in (1,2,3):
      for motifs in (3,4,5,6,8):
        ev=family(pairs,motifs,False)
        cuts,_,_=scan(ev)
        for b in range(4,min(25,len(ev)//2)+1):
            tested+=1
            regular=fixed_cuts(len(ev),b)
            adaptive,vis=adaptive_cuts(cuts,b)
            c0=proxy(regular,cuts); c1=proxy(adaptive,cuts)
            if c1<c0:
                candidates.append((c0/c1,pairs,motifs,b,c0,c1,regular,adaptive,vis))
    candidates.sort(reverse=True)
    assert len(candidates)>=200
    selected=[]
    for item in candidates:
        if item[1]<=2 and item[2]<=5 and len(item[6])<14 and len(item[7])<20:
            if all((item[1],item[2])!=(x[1],x[2]) for x in selected):
                selected.append(item)
        if len(selected)==3:break
    assert len(selected)==3
    cases=[]
    for ratio,pairs,motifs,b,c0,c1,regular,adaptive,vis in selected:
      for unsat in (False,True):
        ev=family(pairs,motifs,unsat)
        cuts,cs,w=scan(ev)
        assert cuts[-1]==()
        exact=dpll(cs)
        base=source_join(ev,cuts,regular)
        improved=source_join(ev,cuts,adaptive)
        assert exact==base["label"]==improved["label"]==(not unsat)
        assert all(0<j-i<=b for i,j in zip(adaptive,adaptive[1:]))
        assert all(j-i>=b//2 or j==len(ev) for i,j in zip(adaptive,adaptive[1:]))
        cases.append({"pairs":pairs,"motifs":motifs,"bound":b,
                      "unsat":unsat,"events":len(ev),"width":w,
                      "cost_fixed":c0,"cost_adaptive":c1,
                      "regular":regular,"adaptive":adaptive,
                      "planning_source_visit_upper":len(ev)+vis,
                      "solver_fixed":base,"solver_adaptive":improved})
    return {"run":"ARC-ADAPTIVE-CUT125","status":"COMPUTATIONAL",
            "candidate_schedules_tested":tested,
            "favorable_schedule_count":len(candidates),
            "full_both_label_cases":len(cases),
            "planning_only_largest_ratio":round(candidates[0][0],4),
            "planning_only_largest_params":list(candidates[0][1:4]),
            "cases":cases,
            "note":"Exact restricted 3CNF child calls, not universal SAT or physical bit-TM time."}
if __name__=="__main__":
    print(json.dumps(tests(),indent=2))

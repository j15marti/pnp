#!/usr/bin/env python3
"""LSPV-2 INTERFACE-GUARD256: independent small exhaustive theorem and update check.
No external packages. Run: python compact_checker256.py
"""
import itertools,json

def gen(contradiction):
    clauses=[]
    def eq(x,y):clauses.extend([(-x,y),(x,-y)])
    def ne(x,y):clauses.extend([(x,y),(-x,-y)])
    eq(3,1);eq(3,2);eq(4,1)
    (ne if contradiction else eq)(4,2)
    for x in range(5,11):eq(x,1)
    return clauses

def truth(clause,a):return any(a[abs(l)]==(l>0) for l in clause)

def brute(F,pins):
    v=sorted({abs(l) for c in F for l in c})
    for bits in itertools.product((False,True),repeat=len(v)):
        a=dict(zip(v,bits))
        if all(a[k]==val for k,val in pins.items()) and all(truth(c,a) for c in F):return a
    return None

def profiles(F,pins):
    modules={}
    for c in F:
        v={abs(l) for l in c if abs(l)>2}
        assert len(v)==1
        x=next(iter(v));modules.setdefault(x,[]).append(c)
    result={}
    for b in itertools.product((False,True),repeat=2):
        beta={1:b[0],2:b[1]};h={}
        for x,clauses in modules.items():
            h[x]=int(any(all(truth(c,{**beta,x:v}) for c in clauses) and (x not in pins or pins[x]==v) for v in (False,True)))
        result[b]=h
    return result

def main():
    checked=0
    for unsat in (False,True):
        F=gen(unsat);table=profiles(F,{})
        assert (any(all(t.values()) for t in table.values())) is (not unsat)
        for x in range(3,11):
            for val in (False,True):
                pins={x:val};new=profiles(F,pins)
                for b in table:
                    for key in table[b]:
                        if key!=x:assert table[b][key]==new[b][key]
                    old_bad=sum(1-v for v in table[b].values())
                    new_bad=sum(1-v for v in new[b].values())
                    assert new_bad==old_bad+table[b][x]-new[b][x]
                    checked+=1
                expected=any(all(t.values()) for t in new.values())
                assert expected==(brute(F,pins) is not None)
    print(json.dumps({'profile_delta_checks':checked,'labels':['SAT','UNSAT'],'status':'PASS','restriction':'supplied two-variable separator'}))
if __name__=='__main__':main()

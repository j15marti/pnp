#!/usr/bin/env python3
"""SCOPE-ALIAS-COMPLETENESS96, peer subset. Only stdlib.
Exhausts the 255 nonempty 3-variable signed-clause subsets and 24
occurrence-release witnesses; validates 120 matched SAT/UNSAT controls.
The extended 585-instance/7196-assertion audit is a separate script.
"""
from itertools import product
import json


def evaluate(c, a):
    return any((x > 0) == a[abs(x)] for x in c)


def exact_sat(F):
    ids = sorted({abs(x) for c in F for x in c})
    for bits in product((False, True), repeat=len(ids)):
        a = dict(zip(ids, bits))
        if all(evaluate(c, a) for c in F):
            return True
    return False


def scoped(F, fresh=False):
    events = []
    mapping = []
    for i, c in enumerate(F):
        u = tuple(3*i+j+1 for j in range(3)) if fresh else tuple(map(abs, c))
        events.extend(('OPEN', x) for x in u)
        events.append(('CLAUSE', tuple(v if x>0 else -v for v,x in zip(u,c))))
        events.extend(('CLOSE', x) for x in reversed(u))
        mapping.extend(zip(u,map(abs,c)))
    return events,mapping


def is_valid(E):
    seen, live = set(), set()
    width=0;good=True
    for tag,x in E:
        if tag=='OPEN':
            if x in seen or x in live:good=False
            seen.add(x);live.add(x)
        elif tag=='CLOSE':
            if x not in live:good=False
            live.discard(x)
        else:
            if set(map(abs,x)) - live or len(set(map(abs,x)))!=3:good=False
        width=max(width,len(live))
    return good and not live,width


def local_dp(E):
    live=[];rows={()}
    for tag,x in E:
        if tag=='OPEN':
            live.append(x)
            rows={z+(b,) for z in rows for b in (False,True)}
        elif tag=='CLOSE':
            k=live.index(x)
            rows={z[:k]+z[k+1:] for z in rows}
            live.pop(k)
        else:
            rows={z for z in rows if any((lit>0)==z[live.index(abs(lit))] for lit in x)}
    assert not live
    return () in rows


def alias_join(F,occurrences):
    originals=sorted({old for _,old in occurrences})
    for bits in product((False,True),repeat=len(originals)):
        a=dict(zip(originals,bits))
        b={new:a[old] for new,old in occurrences}
        if all(evaluate(tuple(v if x>0 else -v for (v,_),x in
                              zip(occurrences[j*3:j*3+3],c)),b)
               for j,c in enumerate(F)):
            return True
    return False


def check(F):
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    raw,_=scoped(F)
    fresh,pins=scoped(F,True)
    assert len(raw)==len(fresh)==7*len(F)
    assert is_valid(raw)[1]==is_valid(fresh)[1]==3
    assert is_valid(fresh)[0]
    assert local_dp(raw) and local_dp(fresh)
    assert exact_sat(F)==alias_join(F,pins)
    return exact_sat(F)


def main():
    all8=[tuple((-v if b else v) for v,b in zip((1,2,3),bits))
          for bits in product((0,1),repeat=3)]
    counts={'sources':0,'sat':0,'unsat':0,'freed_incidence':0,'matched_pairs':0}
    def record(F):
        ans=check(F);counts['sources']+=1
        counts['sat' if ans else 'unsat']+=1
        return ans
    for subset in product((False,True),repeat=8):
        F=[c for c,keep in zip(all8,subset) if keep]
        if F:record(F)
    assert not exact_sat(all8)
    for i in range(8):
        for j in range(3):
            F=list(all8);row=list(F[i]);x=row[j]
            row[j]=4 if x>0 else -4;F[i]=tuple(row)
            assert exact_sat(F)
            counts['freed_incidence']+=1
    for k in range(60):
        Fu=all8+[(1,2,4)]
        Fs=all8[:7]+[(1,2,4),(1,-2,4)]
        assert not record(Fu)
        assert record(Fs)
        counts['matched_pairs']+=1
    assert counts=={'sources':375,'sat':314,'unsat':61,
                    'freed_incidence':24,'matched_pairs':60}
    print(json.dumps({'scope':'COMPUTATIONAL finite semantic test only',
                      'run':'SCOPE-ALIAS-COMPLETENESS96-PEER',
                      'counts':counts,'discrepancies':0},indent=2))

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Finite controls for an uncomputable worst-case paid-node profile.
The toy machine is DECIDABLE and does not constitute the universal-U proof.
Deterministic, Python standard library only, no random seed.
"""
import json
from pathlib import Path
ROOT=Path(__file__).parent
def special(n):
    return [[1],[-1]]+[[j,-j] for j in range(2,n+2)]
def recognized(F):
    if not isinstance(F,list) or not all(isinstance(c,list) for c in F): return None
    n=len(F)-2
    return n if n>=0 and F==special(n) else None
def parse(F):
    if not isinstance(F,list):return False
    for c in F:
        if not isinstance(c,list):return False
        if any(not isinstance(x,int) or isinstance(x,bool) or x==0 for x in c):return False
    return True
def toy_next(n,s):
    return s-1 if n%3==0 and s>0 else s
def toy_halting_trace(n):
    s=n%9+1
    if n%3: return None
    trace=[s]
    for _ in range(s):
        s=toy_next(n,s);trace.append(s)
    assert trace[-1]==0
    return trace
def verify_res_proof(F,steps):
    known=[tuple(c) for c in F]
    for step in steps:
        if not isinstance(step,dict):return False
        a,b,p=step.get('a'),step.get('b'),step.get('pivot')
        if not all(isinstance(k,int) and not isinstance(k,bool) for k in [a,b,p]):return False
        if a<0 or b<0 or a>=len(known) or b>=len(known) or p==0:return False
        A,B=known[a],known[b]
        if p not in A or -p not in B:return False
        derived=tuple(sorted(set(A)-{p}|(set(B)-{-p})))
        if any(-x in derived for x in derived):return False
        if step.get('out')!=list(derived):return False
        known.append(derived)
    return len(steps)>0 and known[-1]==()
def verify(F,cert):
    if not parse(F) or not isinstance(cert,dict):return False
    n=recognized(F)
    kind=cert.get('kind')
    if n is None:
        return kind=='PACK' and verify_res_proof(F,cert.get('steps')) if isinstance(cert.get('steps'),list) else False
    if kind=='FAST':
        trace=cert.get('trace')
        if not isinstance(trace,list) or not trace or any(not isinstance(x,int) or isinstance(x,bool) or x<0 for x in trace):return False
        if trace[0]!=n%9+1 or trace[-1]!=0:return False
        return all(toy_next(n,a)==b for a,b in zip(trace,trace[1:]))
    if kind=='SLOW':
        steps=cert.get('stages')
        return isinstance(steps,list) and steps==list(range(1,n+3))
    return False
def cost(cert):
    return 1 if cert['kind'] in ('FAST','PACK') else len(cert['stages'])
def main():
    checks=0
    def ok(cond,msg):
        nonlocal checks
        checks+=1
        assert cond,msg
    records=[]; running=1; generic_unsat=[[1],[-1],[2]]
    pack={'kind':'PACK','steps':[{'a':0,'b':1,'pivot':1,'out':[]}]}
    ok(verify(generic_unsat,pack),'generic-res-pack')
    ok(not verify([[1]],pack),'SAT cannot be packed')
    ok(not verify([[0]],pack),'malformed')
    ok(not verify(generic_unsat,{'kind':'PACK','steps':[{'a':0,'b':1,'pivot':1,'out':[1]}]}),'corrupt-resolvent')
    for n in range(1,21):
        F=special(n);slow={'kind':'SLOW','stages':list(range(1,n+3))}
        fast_trace=toy_halting_trace(n)
        ok(recognized(F)==n,'recognized')
        ok(verify(F,slow),'valid fallback')
        ok(cost(slow)==n+2,'slow cost')
        ok(not verify(F,pack),'no special pack shortcut')
        ok(not verify(F,{'kind':'SLOW','stages':list(range(1,n+2))}),'short chain reject')
        ok(not verify(F,{'kind':'SLOW','stages':list(range(1,n+3))+[n+3]}),'extra stage reject')
        ok(not verify(F,{'kind':'FAST','trace':[n%9+1,0]}),'forged fast') if n%3 else ok(True,'not forge applicable')
        if fast_trace is not None:
            fast={'kind':'FAST','trace':fast_trace}
            ok(verify(F,fast),'halt certificate')
            ok(cost(fast)==1,'fast cost')
            ok(not verify(F,{'kind':'FAST','trace':fast_trace[:-1]+[1]}),'bad ending')
            minimum=1
        else:
            ok(not verify(F,{'kind':'FAST','trace':[n%9+1,0]}),'nonhalting false proof')
            minimum=n+2
        running=max(running,minimum)
        ok(running==(n+2 if n%3 else max([1]+[j+2 for j in range(1,n) if j%3])),'prefix max')
        records.append({'n':n,'source':F,'source_clause_count':len(F),'toy_halts':n%3==0,'fast_trace':fast_trace,'min_nodes':minimum,'prefix_wbar':running})
    raw={'model':'finite toy control for symbolic P_U; this is NOT universal halting',
         'source_grammar':'ordered signed clause arrays, special S_n = [x1, not x1] + n tautological pairs',
         'n_max':20,'test_records':records,'checks':checks,'generic_pack_cost':1,
         'malformed_rejected':True,'no_seed':True}
    (ROOT/'lspv1_395_profile_raw.json').write_text(json.dumps(raw,indent=2)+'\n')
    print(json.dumps({'checks':checks,'records':len(records),'prefix_wbar':running,'fast':sum(z['toy_halts'] for z in records),'slow':sum(not z['toy_halts'] for z in records)}))
if __name__=='__main__':main()

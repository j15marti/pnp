#!/usr/bin/env python3
"""LSPV-2/398: conservative AND2-gate literal-collapse backdoor controls.
No external dependencies; deterministic, exhaustive for stated small cases.
Includes strict source/definition/resolution certificate replay.
"""
import itertools, json, hashlib
from pathlib import Path

def norm(clause):
    a=frozenset(clause)
    if 0 in a or any(-x in a for x in a):
        raise ValueError('ill-formed/tautological clause')
    return a

def resolve(a,b,p):
    if p not in a or -p not in b: raise ValueError('bad resolution pivot')
    c=(a-{p}) | (b-{-p})
    if any(-x in c for x in c): raise ValueError('tautological resolvent')
    return frozenset(c)

def val(lit,assignment):
    return bool(assignment[abs(lit)]) == (lit>0)

def model(clauses,assignment):
    return all(any(val(l,assignment) for l in c) for c in clauses)

def sat(clauses,vars_):
    for bits in itertools.product([False,True],repeat=len(vars_)):
        a=dict(zip(vars_,bits))
        if model(clauses,a): return a
    return None

def make_case(g,mode='parallel'):
    assert 1<=g<=16
    x=1;ws=list(range(2,g+2));ys=list(range(g+2,2*g+2))
    sources=[norm([x])]+[norm([w]) for w in ws]+[norm([-x]+[-w for w in ws])]
    defs=[]
    for idx,y in enumerate(ys):
        a=x;b=ws[idx] if mode=='parallel' or idx==0 else ys[idx-1]
        defs.append((y,a,b))
    return sources,defs,ws,ys

def definition_clauses(defs):
    out=[]
    for y,a,b in defs:
        out.extend([norm([-y,a]),norm([-y,b]),norm([y,-a,-b])])
    return out

def strict_certificate(g):
    src,defs,ws,ys=make_case(g,'parallel')
    bank=src+definition_clauses(defs)
    lines=[{'type':'input','clause':sorted(c)} for c in bank]
    def do(i,j,p):
        a=norm(lines[i]['clause']);b=norm(lines[j]['clause'])
        c=resolve(a,b,p)
        lines.append({'type':'res','parents':[i,j],'pivot':p,'clause':sorted(c)})
        return len(lines)-1
    x_idx=0;w_source_idx={w:i+1 for i,w in enumerate(ws)}
    neg_src_idx=len(src)-1;w_derived=[]
    for idx,(y,x,w) in enumerate(defs):
        base=len(src)+3*idx
        r1=do(x_idx,base+2,x)
        r2=do(w_source_idx[w],r1,w)
        r3=do(r2,base+1,y)
        w_derived.append(r3)
    r=do(x_idx,neg_src_idx,x)
    for idx,w in enumerate(ws):r=do(w_derived[idx],r,w)
    assert lines[-1]['clause']==[]
    return src,defs,lines

def eval_atom(a,branch,prior):
    if abs(a) in branch:z=branch[abs(a)]
    else:z=prior.get(abs(a),a if a>0 else -a)
    if a<0:return (not z) if isinstance(z,bool) else -z
    return z

def and_simplify(a,b):
    if isinstance(a,bool):return b if a else False
    if isinstance(b,bool):return a if b else False
    if a==b:return a
    if a==-b:return False
    return None

def collapse(defs,branch):
    vals={}
    for y,a,b in defs:
        v=and_simplify(eval_atom(a,branch,vals),eval_atom(b,branch,vals))
        if v is None:return None
        vals[y]=v
    return vals

def partial_substitute(clause,branch,values):
    result=[]
    for lit in clause:
        z=eval_atom(lit,branch,values)
        if z is True:return None
        if z is False:continue
        result.append(z)
    if any(-l in result for l in result):return None
    return norm(result)

def check_certificate(src,defs,lines):
    bank=src+definition_clauses(defs)
    assert len(lines)>=len(bank)
    for i,c in enumerate(bank):
        assert lines[i]['type']=='input' and norm(lines[i]['clause'])==c
    for i in range(len(bank),len(lines)):
        z=lines[i];pa,pb=z['parents']
        assert z['type']=='res' and 0<=pa<i and 0<=pb<i
        assert resolve(norm(lines[pa]['clause']),norm(lines[pb]['clause']),z['pivot'])==norm(z['clause'])
    assert not lines[-1]['clause']
    return len(lines)-len(bank)

def check_projection(src,defs,lines,branch):
    bank=src+definition_clauses(defs)
    vals=collapse(defs,branch); assert vals is not None
    assert all(partial_substitute(c,branch,vals) is None for c in definition_clauses(defs))
    images=[];paid=0
    for idx,z in enumerate(lines):
        target=partial_substitute(z['clause'],branch,vals)
        if idx<len(bank):
            images.append(target);continue
        if target is None:
            images.append(None);continue
        pa,pb=z['parents'];a,b=images[pa],images[pb]
        choices=[c for c in [a,b] if c is not None and c.issubset(target)]
        if choices:
            images.append(min(choices,key=len));continue
        choices=[]
        if a is not None and b is not None:
            for p in a:
                if -p in b:
                    c=(a-{p}) | (b-{-p})
                    if not any(-k in c for k in c) and c.issubset(target):choices.append(c)
        if not choices:raise AssertionError(('projection fails',idx,branch,a,b,target))
        images.append(frozenset(choices[0]));paid+=1
    assert images[-1]==frozenset()
    return paid

def run():
    cases=[];checks=0
    for mode in ['parallel','chain']:
        for g in [1,2,3,4,6,8,12,16]:
            sources,defs,ws,ys=make_case(g,mode)
            r=None
            if mode=='parallel':
                _,_,lines=strict_certificate(g)
                r=check_certificate(sources,defs,lines);checks+=r
                for b in [False,True]:
                    paid=check_projection(sources,defs,lines,{1:b});checks+=len(lines)
                    assert paid<=r
            for b in [False,True]:
                vals=collapse(defs,{1:b}); assert vals is not None
                for y,a,c in defs:
                    for d in definition_clauses([(y,a,c)]):
                        assert partial_substitute(d,{1:b},vals) is None
                        checks+=1
            if g<=4:
                vars_=list(range(1,g+2))
                assert sat(sources,vars_) is None;checks+=1
                for i in range(len(sources)):
                    assert sat(sources[:i]+sources[i+1:],vars_) is not None;checks+=1
            bad=[(ys[0],ws[0],ws[-1])] if ws[0]!=ws[-1] else [(ys[0],ws[0],1)]
            assert collapse(bad,{1:False}) is None or g==1
            checks+=1
            cases.append({'mode':mode,'g':g,'gate_backdoor_B':[1],
               'collapse_branches':2,'strict_resolution_nodes':r,
               'old_397_bound':None if r is None else 2**g*(r+1)-1,
               'new_398_bound':None if r is None else 2*(r+1)-1,
               'source_only_witness_nodes':g+1})
    data={'experiment':'LSPV2_398_LITERAL_COLLAPSE_BACKDOOR','seed':None,
      'claim':'finite tests of strict resolution replay, all gate clauses tautological after B restriction, projected proof closure, both labels and bad backdoor',
      'tested_cases':len(cases),'checks':checks,'cases':cases}
    p=Path(__file__).resolve().parent/'2026-11-04_1213_LSPV2_GATE_COLLAPSE_BACKDOOR398_raw.json'
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(cases),'checks':checks,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
       'g16_parallel':cases[7]},indent=2))

if __name__=='__main__':run()

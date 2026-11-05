#!/usr/bin/env python3
"""LSPV4/413: finite JSON-whitespace acquisition falsifier, not a logspace TM."""
import json, hashlib, pathlib, sys

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
def sha(x): return hashlib.sha256(canon(x).encode('ascii')).hexdigest()
def source(): return {'nvars':1,'clauses':[[1],[-1]]}
def proof():
    s=source()
    return {'format':'Rmix341-CANON2','source':s,'source_sha256':sha(s),
      'nodes':[{'id':0,'rule':'RES','left':{'src':0,'view':'clause'},
                'right':{'src':1,'view':'clause'},'pivot':1,'clause':[]}],
      'final':{'node':0,'view':'clause'}}
def resolvents(a,b,p):
    got=set()
    for v in (p,-p):
        if v in a and -v in b:
            c=(set(a)-{v}) | (set(b)-{-v})
            got.add(tuple(sorted(c,key=lambda x:(abs(x),x<0))))
    return got
def verify_fixture(d,s):
    if set(d)!={'format','source','source_sha256','nodes','final'}: return False
    if d['format']!='Rmix341-CANON2' or d['source']!=s or d['source_sha256']!=sha(s):return False
    if s!={'nvars':1,'clauses':[[1],[-1]]}:return False
    if len(d['nodes'])!=1 or d['final']!={'node':0,'view':'clause'}:return False
    r=d['nodes'][0]
    return (set(r)=={'id','rule','left','right','pivot','clause'} and r['id']==0 and
       r['rule']=='RES' and r['pivot']==1 and r['clause']==[] and
       r['left']=={'src':0,'view':'clause'} and r['right']=={'src':1,'view':'clause'} and
       () in resolvents((1,),(-1,),1))
def add_small(s,k):
    if not s or s[0]=='0' or not s.isascii() or not s.isdigit() or k<0:raise ValueError
    i=len(s)-1;c=k;out=[]
    while i>=0 or c:
        a=(ord(s[i])-48 if i>=0 else 0)+c
        out.append(str(a%10));c=a//10;i-=1
    return ''.join(reversed(out))
def main():
    d=proof(); base=canon(d)
    sizes=[0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096]
    cases=[];count=0;mutations=0
    for m in sizes:
        raw=base[:-1]+' '*m+'}'
        assert verify_fixture(json.loads(raw),source());count+=1
        assert len(raw)==len(base)+m;count+=1
        for i in range(m):
            j=len(base)-1+i
            bad=raw[:j]+'#'+raw[j+1:]
            try:json.loads(bad)
            except json.JSONDecodeError: pass
            else:raise AssertionError('corrupt raw JSON accepted')
            count+=1;mutations+=1
        cases.append({'padding':m,'raw_bytes':len(raw),'q':1,'N_canonical_source_bytes':len(canon(source()))})
    assert resolvents((1,-1,-2),(1,),1)=={(1,-2)};count+=1
    assert resolvents((1,-1,2),(1,),1)=={(1,2)};count+=1
    assert () not in resolvents((1,-1,-2),(1,),1);count+=1
    assert not verify_fixture(dict(d,source={'nvars':1,'clauses':[[1]]}),source());count+=1
    assert not verify_fixture(dict(d,source_sha256='0'*64),source());count+=1
    assert add_small('9'*20000,1)=='1'+'0'*20000;count+=1
    for i in range(1,501):
        assert add_small(str(i),i)==str(2*i);count+=1
    limit=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
    guarded=False
    if limit and limit>0:
        try:json.loads('{"nvars":'+'9'*(limit+1)+',"clauses":[[1],[-1]]}')
        except ValueError:guarded=True
    result={'run':'LSPV4_413','source':source(),'source_bytes':len(canon(source())),
      'canonical_proof_bytes':len(base),'padding_cases':cases,
      'mutation_rejections':mutations,'assertion_groups':count,
      'python_decimal_guard_limit':limit,'python_guard_rejects_legal_huge_decimal':guarded,
      'status':'restricted exact theorem, finite controls, native grammar/B3 OPEN',
      'note':'Python buffers data and cannot validate logarithmic physical space'}
    dest=pathlib.Path('results/raw/arc/2026-11-05_0540_LSPV4_413_LOGSPACE_PADDING.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'PASS':True,'checks':count,'mutations':mutations,'base':len(base)}))
if __name__=='__main__':main()

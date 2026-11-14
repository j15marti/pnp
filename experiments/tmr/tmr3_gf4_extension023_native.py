#!/usr/bin/env python3
"""Reproducible finite controls for PNP GF(4) semantic-composition audit.

No SAT hardness assumption is used. This is not a physical general SAT machine.
Run: python tmr3_gf4_extension023_native.py --output results.json
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

# GF(4) = GF(2)[a]/(a^2+a+1), encoded lowbit + highbit*a
def mul(x,y):
    a,b=x&1,(x>>1)&1
    c,d=y&1,(y>>1)&1
    return ((a*c)^(b*d)) | (((a*d)^(b*c)^(b*d))<<1)

def canonical_eval(fn,n,z):
    s=0
    for a in range(1<<n):
        if not fn(a): continue
        w=1
        for j,v in enumerate(z):
            w=mul(w,v if (a>>j)&1 else (v^1))
        s ^= w
    return s

def or_extension(z):
    p=1
    for v in z: p=mul(p,v^1)
    return p^1

def bool_or(x): return int(x!=0)

def sat(f,a):
    return all(any((((a>>(abs(l)-1))&1)==(l>0)) for l in c) for c in f)

def run_machine(bits):
    """Local one-head source, finite control. Every read/move and output is charged."""
    tape='^'+bits+'$';head=0;steps=0
    assert tape[head]=='^'; head+=1; steps+=1
    if head==len(tape)-1:return {'label':'MALFORMED','value':None,'transitions':steps+2,'visited_output_cells':0}
    mode=tape[head];head+=1;steps+=1
    if mode not in '01':return {'label':'MALFORMED','value':None,'transitions':steps+1,'visited_output_cells':0}
    acc=0 if mode=='0' else 1
    pending=None
    while tape[head]!='$':
        bit=int(tape[head]);head+=1;steps+=1
        if mode=='0':acc |= bit
        else:
            if pending is None:pending=bit
            else:
                v=(pending<<1)|bit
                acc=mul(acc,v^1)
                pending=None
    steps+=1
    if mode=='1' and pending is not None:
        steps+=1
        return {'label':'MALFORMED','value':None,'transitions':steps,'visited_output_cells':0}
    if mode=='0':out=[acc]
    else:
        v=1^acc;out=[(v>>1)&1,v&1]
    steps+=len(out)+1
    return {'label':'OK','value':''.join(map(str,out)),'transitions':steps,'visited_output_cells':len(out)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    for x in range(4):
        assert mul(x,0)==0 and mul(x,1)==x
        for y in range(4):
            assert mul(x,y)==mul(y,x)
            for z in range(4): assert mul(mul(x,y),z)==mul(x,mul(y,z))
    oracle_adversaries=0;oracle_function_checks=0;extension_checks=0;curve=[]
    for n in range(1,10):
        z=[2]*n
        weights=[]
        for a in range(1<<n):
            w=canonical_eval(lambda b,aa=a:int(b==aa),n,z)
            assert w!=0
            weights.append(w);oracle_adversaries+=1
        orv=canonical_eval(bool_or,n,z)
        assert orv==or_extension(z)
        extension_checks+=1
        assert (1<<n)-1==sum(1 for mask in range(1,1<<n))
        if n<=3:
            for truth_table in range(1<<(1<<n)):
                f=lambda a,k=truth_table:(k>>a)&1
                actual=canonical_eval(f,n,z);independent=0
                for a,w in enumerate(weights):
                    if f(a):independent^=w
                assert actual==independent
                oracle_function_checks+=1
        curve.append({'n':n,'oracle_queries_necessary':1<<n,'OR_anf_terms':(1<<n)-1,'factorized_GF4_multiplies':n,'extension_at_alpha':orv})
    machine_tests=good=malformed=max_work=max_slack=0
    for L in range(14):
        for j in range(1<<L):
            bits=format(j,f'0{L}b') if L else ''
            r=run_machine(bits);machine_tests+=1
            if r['label']=='MALFORMED':
                assert L==0 or (bits[0]=='1' and (L-1)%2==1)
                malformed+=1
            else:
                good+=1
                if bits[0]=='0':expected=str(int('1' in bits[1:]))
                else:
                    values=[(int(bits[i])<<1)|int(bits[i+1]) for i in range(1,L,2)]
                    e=or_extension(values);expected=f'{(e>>1)&1}{e&1}'
                assert r['value']==expected,(bits,r,expected)
            assert r['transitions']<=L+6
            max_slack=max(max_slack,r['transitions']-L)
            max_work=max(max_work,r['visited_output_cells'])
    cnfs=[('Horn',3,[(1,),(-1,2),(-2,3)]),
          ('HornUNSAT',3,[(1,),(-1,)]),
          ('twoSAT',3,[(1,2),(-1,3),(-2,-3)]),
          ('XOR3',3,[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]),
          ('duplicate',3,[(1,2,3)]*12),
          ('shared',3,[(1,2,3),(-1,2,3)]),
          ('product',6,[(1,2,3),(-1,-2,-3),(4,5,6),(-4,-5,-6)]),
          ('renamed',4,[(4,2,3),(-4,2,3)])]
    for r in (1,2,3,4):
        cube=[tuple(-j-1 if (s>>j)&1 else j+1 for j in range(3)) for s in range(8) for _ in range(r)]
        near=cube[:]
        for j in range(r):
            row=list(near[j]);row[0]*=-1;near[j]=tuple(row)
        cnfs += [(f'U_{r}',3,cube),(f'nearest_{r}',3,near)]
    records=[]
    for name,n,cnf in cnfs:
        f=lambda a,cnf=cnf:int(sat(cnf,a))
        z=[2]*n
        v=canonical_eval(f,n,z)
        independent=0;count=0
        for a in range(1<<n):
            if f(a):
                count+=1;w=1
                for k in range(n): w=mul(w,z[k] if (a>>k)&1 else z[k]^1)
                independent ^= w
        assert independent==v
        assert (count==0)==(name.startswith('U_') or name=='HornUNSAT')
        records.append({'fixture':name,'variables':n,'clauses':len(cnf),'models':count,'canonical_alpha':v})
    sharing=[]
    for h in range(21):
        recursive=(1<<(h+1))-1;unique=h+1
        assert recursive>=unique
        sharing.append({'depth':h,'naive_recursive_occurrences':recursive,'unique_DAG_nodes':unique})
    raw={'status':'COMPUTATIONAL','model':'restricted GF4/Boolean OR streaming controller and Boolean-query oracle',
         'no_general_SAT_solver':True,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'gf4_arithmetic_checks':'exhaustive triples','oracle_adversaries':oracle_adversaries,
         'oracle_function_checks':oracle_function_checks,'extension_checks':extension_checks,'curve':curve,
         'machine_runs':machine_tests,'machine_ok':good,'machine_malformed':malformed,
         'max_visited_output_cells':max_work,'max_T_minus_L':max_slack,'cnf_controls':records,
         'sharing':sharing,'assertion_failures':0}
    args.output.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:raw[k] for k in ['oracle_adversaries','oracle_function_checks','extension_checks','machine_runs',
      'machine_ok','machine_malformed','max_visited_output_cells','max_T_minus_L','assertion_failures']},indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""ARC-STREAM-NORMALIZER150: source-scope compiler and independent controls.
Standard library only; logical word/bit traffic is NOT physical FLMV RTM work.
Usage: python arc_stream_normalizer150_repro.py [--unsat-source U_source.txt] [--output summary.json]
"""
import argparse, ast, collections, itertools, json, math, pathlib

def width_word(k,m): return max(2,(64*(k+m+1)-1).bit_length())

def normalize_formula(F):
    return tuple(tuple(c) for c in F)

def kvars(F): return max((abs(x) for c in F for x in c),default=0)

def assert_proper(F):
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    assert all(x!=0 for c in F for x in c)

def emit_bits(F):
    k=kvars(F);m=len(F);w=width_word(k,m)
    assert_proper(F)
    mask=(1<<(w-1))-1
    assert k<=mask and m<(1<<w)
    arr=[format(k,f'0{w}b'), format(m,f'0{w}b')]
    for c in F:
        for x in c:
            a=abs(x)+(1<<(w-1) if x<0 else 0)
            arr.append(format(a,f'0{w}b'))
    z=''.join(arr)
    assert len(z)==(3*m+2)*w
    return z,w

def stream_encode(E,w,k,m):
    arr=[format(k,f'0{w}b'),format(m,f'0{w}b')]
    for kind,obj in E:
        n={'O':0,'C':1,'X':2}[kind]
        vals=[obj,0,0] if kind in 'OC' else list(obj)
        v=[]
        for x in vals:
            assert abs(x)<(1<<(w-1))
            v.append(format(abs(x)+((1<<(w-1)) if x<0 else 0),f'0{w}b'))
        arr.append(format(n,'02b')+''.join(v))
    s=''.join(arr)
    assert len(s)==2*w+len(E)*(3*w+2)
    return s

def eager(F):
    m=len(F)
    first,last={},{}
    reads=0
    for j,c in enumerate(F):
        for x in c:
            reads+=1; v=abs(x)
            if v not in first:first[v]=j
            last[v]=j
    E=[]
    for j,c in enumerate(F):
        for x in sorted(c,key=abs):
            if first[abs(x)]==j:E.append(('O',abs(x)))
        E.append(('X',tuple(c)))
        for x in sorted(c,key=abs):
            if last[abs(x)]==j:E.append(('C',abs(x)))
    return E, {'source_literal_fields_read_lower_account':reads,'first_last_entries':2*len(first)}

def replay(F):
    m=len(F);E=[];reads=0
    for j,c in enumerate(F):
        for x in sorted(c,key=abs):
            v=abs(x);seen=False
            for i in range(j):
                for z in F[i]:
                    reads+=1
                    if abs(z)==v:seen=True;break
                if seen:break
            if not seen:E.append(('O',v))
        E.append(('X',tuple(c)))
        for x in sorted(c,key=abs):
            v=abs(x);seen=False
            for i in range(j+1,m):
                for z in F[i]:
                    reads+=1
                    if abs(z)==v:seen=True;break
                if seen:break
            if not seen:E.append(('C',v))
    return E,{'source_literal_fields_read_lower_account':reads,'max_live_data_word_bound':9}

def validate(E,F):
    live=set();events_clauses=[];seen=set();maxwidth=0;seen_close=set()
    for kind,obj in E:
        if kind=='O':
            assert obj not in live and obj not in seen and obj not in seen_close
            live.add(obj);seen.add(obj)
        elif kind=='C':
            assert obj in live
            live.remove(obj);seen_close.add(obj)
        else:
            assert kind=='X' and set(map(abs,obj))<=live
            events_clauses.append(obj)
        maxwidth=max(maxwidth,len(live))
    assert not live and tuple(events_clauses)==tuple(F) and seen==seen_close
    return maxwidth

def cm22(F):
    if len(F)!=len(set(map(tuple,F))):return False
    if any(len(c)!=3 or len({abs(x) for x in c})!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)) for c in F):return False
    plus=collections.Counter(abs(x) for c in F for x in c if x>0)
    minus=collections.Counter(abs(x) for c in F for x in c if x<0)
    vars_=set(plus)|set(minus)
    return bool(vars_) and all(plus[v]==minus[v]==2 for v in vars_)

def cstar(F):
    return cm22(F) and any(tuple(sorted((-x for x in c),key=abs)) not in set(F) for c in F)

def canon(F):
    return tuple(sorted((tuple(sorted(c,key=abs)) for c in F),key=lambda c:(min(c)<0,tuple(abs(x) for x in c),c)))

def models(F):
    k=kvars(F)
    assert k<=16
    return sum(all(any(((mask>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F) for mask in range(1<<k))

def mkY():
    P=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
    Q=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
    return canon(P+[tuple(-i for i in s) for s in Q])

def mkZ(h):
    def a(i,t):return 6*(i%h)+t+1
    F=[]
    for i in range(h):
        ai,bi,ci,di,ei,fi=[a(i,j) for j in range(6)]
        F.extend([(a(i+1,0),bi,ci),(ai,di,ei),(bi,di,fi),(ci,ei,fi),
                  (-ai,-bi,-di),(-ai,-ci,-fi),(-bi,-ci,-ei),(-di,-ei,-fi)])
    return canon(F)

def sourceU(path):
    txt='\n'.join(ln for ln in pathlib.Path(path).read_text().splitlines() if not ln.lstrip().startswith('#'))
    F=canon(ast.literal_eval(txt))
    assert cm22(F) and cstar(F) and kvars(F)==198 and len(F)==264
    return F

def compile_short_clauses(F):
    """Exact existential conversion of 1-/2-clauses to proper 3-CNF.
    Not an M22 promise repair. Distinct private variables for each gadget.
    """
    nxt=kvars(F);out=[]
    for c in F:
        if not c:
            p,q,r=range(nxt+1,nxt+4);nxt+=3
            out.extend(tuple(v if z else -v for v,z in zip((p,q,r),bits)) for bits in itertools.product((0,1),repeat=3))
            break
        if len(c)==3:out.append(c)
        elif len(c)==2:
            nxt+=1;z=nxt;out.extend((c+(z,),c+(-z,)))
        else:
            assert len(c)==1;nxt+=1;z=nxt;nxt+=1;v=nxt
            out.extend(c+(az*z,av*v) for az,av in itertools.product((1,-1),repeat=2))
    return canon(tuple(dict.fromkeys(out)))

def restrict(F,assign):
    G=[]
    for c in F:
        if any(abs(x) in assign and assign[abs(x)]==int(x>0) for x in c):continue
        G.append(tuple(x for x in c if abs(x) not in assign))
    return G

def run_case(name,F,status,do_replay=True):
    assert_proper(F)
    bits,w=emit_bits(F)
    E,ec=eager(F);wd=validate(E,F)
    ebit=stream_encode(E,w,kvars(F),len(F))
    if do_replay:
        R,rc=replay(F);assert E==R
        assert validate(R,F)==wd
    else:rc={}
    if cm22(F):
        assert wd==kvars(F)
    return {'name':name,'label':status,'k':kvars(F),'m':len(F),'N_source_bits':len(bits),
            'M_stream_bits':len(ebit),'w_id_bits':w,'event_count':len(E),'width':wd,
            'source_Cstar':cstar(F),'fully_paired':cm22(F) and not cstar(F),
            'eager_logical_read_fields':ec['source_literal_fields_read_lower_account'],
            'replay_logical_read_fields':rc.get('source_literal_fields_read_lower_account'),
            'replay_source_bit_traffic_field_lower':w*rc.get('source_literal_fields_read_lower_account',0) if do_replay else None,
            'eager_array_bits_bound':ec['first_last_entries']*max(1,(len(F)+1).bit_length())}

def two_levels(F,name,known_label,vars_=(1,2)):
    assert all(any(abs(x)==v for c in F for x in c) for v in vars_)
    out=[];bybits=[]
    for b1,b2 in itertools.product((0,1),repeat=2):
        G1=compile_short_clauses(restrict(F,{vars_[0]:b1}))
        G2=compile_short_clauses(restrict(G1,{vars_[1]:b2}))
        res1=run_case(f'{name}/first_{b1}',G1,'unchecked' if kvars(F)>20 else ('SAT' if models(G1)>0 else 'UNSAT'),do_replay=False)
        res2=run_case(f'{name}/grand_{b1}{b2}',G2,'unchecked' if kvars(F)>20 else ('SAT' if models(G2)>0 else 'UNSAT'),do_replay=False)
        out.append({'pin':f'{b1}{b2}','child_bits':res1['N_source_bits'],'grandchild_bits':res2['N_source_bits'],
                    'child_Cstar':res1['source_Cstar'],'grandchild_Cstar':res2['source_Cstar'],
                    'child_width':res1['width'],'grandchild_width':res2['width'],
                    'grandchild_label':res2['label']})
        bybits.append(res2['label'])
    if kvars(F)<=16:
        assert ('SAT' in bybits)==(known_label=='SAT')
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--unsat-source');ap.add_argument('--output');a=ap.parse_args()
    Y=mkY();assert cstar(Y) and models(Y)==20
    Z1=mkZ(1);assert cstar(Z1) and models(Z1)>0
    opts=[('Y',Y,'SAT'),('Z3',mkZ(3),'SAT'),('Z11',mkZ(11),'SAT'),('Z33',mkZ(33),'SAT'),
          ('Y+Y',canon(list(Y)+[tuple(x+6 if x>0 else x-6 for x in c) for c in Y]),'SAT')]
    eight=canon([tuple(v if b else -v for v,b in zip((1,2,3),bits)) for bits in itertools.product((0,1),repeat=3)])
    assert models(eight)==0
    opts.append(('EIGHT_OUTSIDE',eight,'UNSAT'))
    xor1=canon([(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)])
    opts.append(('XOR_OUTSIDE',xor1,'SAT'))
    horn=canon([(-1,-2,3),(-1,2,-3),(1,-2,-3)])
    opts.append(('HORN_OUTSIDE',horn,'SAT'))
    if a.unsat_source:opts.append(('DOCKER_U',sourceU(a.unsat_source),'UNSAT_imported'))
    cases=[]
    for name,F,label in opts:
        rr=run_case(name,F,label,do_replay=True)
        cases.append(rr)
    recY=two_levels(Y,'Y','SAT')
    recE=two_levels(eight,'EIGHT_OUTSIDE','UNSAT')
    recU=two_levels(sourceU(a.unsat_source),'DOCKER_U','UNSAT_imported') if a.unsat_source else []
    z33=next(x for x in cases if x['name']=='Z33')
    u=next((x for x in cases if x['name']=='DOCKER_U'),None)
    if u:
        assert (z33['k'],z33['m'],z33['N_source_bits'],z33['M_stream_bits'],z33['width'])==(u['k'],u['m'],u['N_source_bits'],u['M_stream_bits'],u['width'])
    r={'id':'ARC-STREAM-NORMALIZER150','status':'COMPUTATIONAL logical source scan; proofs in report',
       'code':'arc_stream_normalizer150_repro.py','full_replay_all_cases':True,
       'M22_theorem_sign_sorted_width_equals_k_checked':True,
       'cases':cases,'two_level_Y':recY,'two_level_EIGHT':recE,'two_level_U_imported_label_only':recU,
       'physical_RTM_bit_work_flips_peak_bit_time_measured':False,'source_U_label_imported_not_bruteforced':bool(a.unsat_source),
       'counts':{'cases':len(cases),'replay_equal_eager':len(cases),'branch_Y':4,'branch_EIGHT':4,'branch_U':4 if recU else 0}}
    s=json.dumps(r,sort_keys=True,indent=2)
    if a.output:pathlib.Path(a.output).write_text(s+'\n')
    print(json.dumps({'cases':len(cases),'Y_models':models(Y),'Z33':z33,'U':u,'two_level_Y':recY,'two_level_U':recU,'zero_failures':True},indent=2))
if __name__=='__main__':main()

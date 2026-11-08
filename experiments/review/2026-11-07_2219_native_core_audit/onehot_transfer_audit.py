#!/usr/bin/env python3
"""Independent literal-exact one-hot to bit Tseitin transfer.
The target proof language is explicitly Res(PC_1/F_p), not R_mix341.
Each RES is expanded to a linear-combination line and false-constant deletion.
"""
from pathlib import Path
import json, copy
BASE=Path(__file__).resolve().parent
checks=0

def ck(b,msg):
    global checks
    checks+=1
    if not b: raise ValueError(msg)

def atom(lit,p):
    # Positive Boolean literal x is x-1=0; negative literal is x=0.
    return (abs(lit),1,(-1 if lit>0 else 0)%p)

def build(f,p):
    h=f['graph']['n']; e=len(f['graph']['edges']); src={}; nodes=[]; byid={}; outputs=[]
    def axi(k,c):
        src[k]=tuple(c); byid[k]=frozenset(atom(l,p) for l in c)
    for i in range(1,e+1):
        axi(f'a{i}',[i+e,i]); axi(f'u{i}',[-i-e,-i])
    for c in f['clauses']:
        axi('v'+c['id'],[-(abs(l)+e) if l>0 else l for l in c['literals']])
    ck(len(src)==7*h,'onehot clauses')
    for c in f['clauses']:
        par='v'+c['id']
        for l in c['literals']:
            if l<0: continue
            pivot=l+e; other=f'a{l}'; a=(pivot,1,0); b=(pivot,1,p-1)
            ck(a in byid[par] and b in byid[other],'oriented resolution')
            false=(0,0,1)
            rest=(byid[par]-{a})|(byid[other]-{b})
            k=f'z{len(nodes)}'
            line=rest|{false}
            nodes.append({'id':k,'rule':'LINCOMB','parents':[par,other],
                          'selected':[list(a),list(b)],'coefficients':[1,p-1],
                          'line':[list(x) for x in sorted(line)]})
            byid[k]=line
            d=f'z{len(nodes)}'
            nodes.append({'id':d,'rule':'DELETE_FALSE','parents':[k],
                          'line':[list(x) for x in sorted(rest)]})
            byid[d]=rest; par=d
        ck(byid[par]==frozenset(atom(l,p) for l in c['literals']),'wrong bit source result')
        outputs.append({'original_source':c['id'],'derived_id':par})
    ck(len(nodes)==12*h,'target step count')
    return {'prime':p,'onehot_sources':{k:list(v) for k,v in src.items()},'nodes':nodes,'outputs':outputs}

def verify(proof,f):
    p=proof['prime']; byid={k:frozenset(atom(l,p) for l in v) for k,v in proof['onehot_sources'].items()}
    for d in proof['nodes']:
        ck(d['id'] not in byid,'duplicate id')
        ck(all(x in byid for x in d['parents']),'bad parent')
        result=frozenset(tuple(x) for x in d['line'])
        if d['rule']=='LINCOMB':
            ck(len(d['parents'])==2,'binary combination')
            left,right=(byid[k] for k in d['parents']); a,b=(tuple(x) for x in d['selected'])
            ck(a in left and b in right,'selected atoms absent')
            al,be=d['coefficients']; coeff={}; const=0
            for s,(v,c,k) in [(al,a),(be,b)]:
                if v: coeff[v]=(coeff.get(v,0)+s*c)%p
                const=(const+s*k)%p
            coeff={v:c for v,c in coeff.items() if c}
            ck(not coeff and const!=0,'expected syntactically false nonzero constant')
            expected=(left-{a})|(right-{b})|{(0,0,const)}
            ck(result==expected,'false linear combination')
        elif d['rule']=='DELETE_FALSE':
            ck(len(d['parents'])==1,'unary deletion')
            parent=byid[d['parents'][0]]
            ck(result==frozenset(a for a in parent if not(a[0]==0 and a[1]==0 and a[2]%p!=0)), 'illegal deletion')
        else: raise ValueError('unknown target rule')
        byid[d['id']]=result
    wanted={c['id']:frozenset(atom(l,p) for l in c['literals']) for c in f['clauses']}
    for out in proof['outputs']: ck(byid[out['derived_id']]==wanted[out['original_source']],'source conclusion')

base=json.loads((BASE/'baseline.json').read_text()); result=[]; certificates=[]
for f in base['fixtures']:
    h=f['graph']['n']; e=len(f['graph']['edges'])
    for p in (2,3,5):
        proof=build(f,p); verify(proof,f); certificates.append({'graph':f['graph']['name'],**proof})
        result.append({'graph':f['graph']['name'],'prime':p,'bit_clauses':4*h,'onehot_clauses':7*h,'ordinary_RES_steps':6*h,'target_derived_lines':len(proof['nodes']),'total_prefix_nodes':7*h+len(proof['nodes'])})
    # Check one-hot source semantics on all 64 local assignments, no global one-hot enumeration.
    for v in range(h):
        incident=[i+1 for i,uv in enumerate(f['graph']['edges']) if v in uv]
        clauses=[c['literals'] for c in f['clauses'] if c['vertex']==v]
        for assignment in range(64):
            vals={i:((assignment>>j)&1) for j,i in enumerate(incident)}
            zeros={i:((assignment>>(j+3))&1) for j,i in enumerate(incident)}
            unique=all(vals[i]+zeros[i]==1 for i in incident)
            oh=all(any((zeros[abs(l)] if l>0 else vals[abs(l)])==0 for l in c) for c in clauses)
            bit=all(any(vals[abs(l)]==int(l>0) for l in c) for c in clauses)
            ck((unique and oh)==(unique and bit),'onehot-bit local equivalence')
f=base['fixtures'][0]; good=build(f,3); rejected=[]
for mode in ['wrong_coefficient','bad_parent','delete_real_atom','source_output_mismatch']:
    bad=copy.deepcopy(good)
    if mode=='wrong_coefficient': bad['nodes'][0]['coefficients']=[1,1]
    elif mode=='bad_parent': bad['nodes'][0]['parents'][0]='absent'
    elif mode=='delete_real_atom': bad['nodes'][1]['line']=[]
    else: bad['outputs'][0]['derived_id']=bad['outputs'][1]['derived_id']
    try: verify(bad,f)
    except (ValueError,KeyError): rejected.append(mode)
    else: raise AssertionError('hostile certificate accepted')
summary={'checks':checks,'cases':result,'negative_controls_rejected':rejected,
         'scope':'Independent syntactic simulation in published Res(PC_1/F_p). NOT historical mixed grammar; no all-size lower bound tested numerically.'}
(BASE/'onehot_results.json').write_text(json.dumps(summary,indent=2)+'\n')
(BASE/'onehot_certificates.json').write_text(json.dumps(certificates,separators=(',',':'))+'\n')
print(json.dumps({'checks':checks,'cases':len(result),'rejected':rejected}))

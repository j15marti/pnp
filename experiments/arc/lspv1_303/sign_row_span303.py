#!/usr/bin/env python3
"""Producer. Exact canonical original-source parity row-span, independently checkable."""
from __future__ import annotations
import itertools,json,hashlib,sys,time

F9_POS=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9_NEG=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
Y6_POS=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Y6_NEG=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]

def fmake(pos,neg):return tuple((1,tuple(z)) for z in pos)+tuple((-1,tuple(z)) for z in neg)
def grammar(f,n):
    assert len(f)*3==4*n and len(set(f))==len(f)
    cnt={(v,s):0 for v in range(1,n+1) for s in (1,-1)}
    for s,c in f:
        assert s in (1,-1) and len(c)==3 and len(set(c))==3
        for v in c:
            assert v in range(1,n+1);cnt[v,s]+=1
    assert all(v==2 for v in cnt.values())

def truth(s,c,a):return sum((a[v]==1 if s==1 else a[v]==0) for v in c)
def rank(rows):
    piv={};r=0
    for mask,b in rows:
        v=(mask<<1)|b
        while v:
            j=(v>>1).bit_length()-1
            if j<0:break
            if j in piv:v^=piv[j]
            else:piv[j]=v;r+=1;break
    consistent=all((v&1)==0 for v in [*piv.values()])
    return r,consistent

def source_rows(f,n,p,a):
    free=tuple(v for v in range(1,n+1) if v not in p)
    splus={v:0 for v in free};sminus={v:0 for v in free}
    rows=[];sign={1:[],-1:[]};ex={1:0,-1:0};u={1:0,-1:0}
    for j,(sgn,c) in enumerate(f):
        if any(v in p and ((p[v]==1)==(sgn==1)) for v in c):
            for v in c:
                if v in splus:(splus if sgn==1 else sminus)[v]+=1
            continue
        if all(v in p for v in c):raise AssertionError('falsified partial cube')
        available=[v for v in c if v not in p]
        mask=sum(1<<(v-1) for v in available)
        q=truth(sgn,c,a)&1
        rhs=q ^ ((len(available)&1) if sgn==-1 else 0)
        row=(mask,rhs)
        rows.append(row);sign[sgn].append(row)
        u[sgn]+=1
        ex[sgn]+=truth(sgn,c,a)-1
        assert (sum((a[v] if sgn==1 else 1-a[v]) for v in available)&1)==q
    return rows,sign,ex,u,splus,sminus

def eval_formula(f,a):return all(truth(s,c,a)>=1 for s,c in f)

def main():
  out={'id':'ARC-SIGN-ROW-SPAN303','status':'COMPUTATIONAL','date':'2026-11-01 06:00 PST','families':{},'controls':{},'model':'offline Python word arithmetic, not native FLMV time or space'}
  for name,pp,nn,n in [('Y6',Y6_POS,Y6_NEG,6),('F9',F9_POS,F9_NEG,9)]:
    f=fmake(pp,nn);grammar(f,n)
    models=[a for bits in itertools.product((0,1),repeat=n) if (a:={i+1:b for i,b in enumerate(bits)}) and eval_formula(f,a)]
    counts={'partial_states_scanned':0,'sat_extendible_cubes':0,'unsat_cubes':0,'sat_cube_completion_incidences':0,'row_span_tests':0,'rank_increases_after_full_rows':0,'derived_sign_row_mismatches':0,'partial_falsified_skipped':0,'row_XOR_source_id_tests':0,'positive_nontrivial_early_rows':0,'negative_nontrivial_early_rows':0}
    for pa in itertools.product((-1,0,1),repeat=n):
        p={i+1:v for i,v in enumerate(pa) if v!=-1}
        counts['partial_states_scanned']+=1
        bad=any(all(v in p and ((p[v]==0)==(sgn==1)) for v in c) for sgn,c in f)
        if bad:
            counts['partial_falsified_skipped']+=1
            continue
        ext=[a for a in models if all(a[v]==val for v,val in p.items())]
        counts['sat_extendible_cubes' if ext else 'unsat_cubes']+=1
        for a in ext:
            rows,by,ex,u,sp,sm=source_rows(f,n,p,a)
            allrank,_=rank(rows)
            for s in (1,-1):
                mask=0;rhs=0
                for m,b in by[s]:mask^=m;rhs^=b
                ss=sp if s==1 else sm
                needmask=sum(((v&1)<< (x-1)) for x,v in ss.items())
                needrhs=((ex[s]+u[s]+ (sum((v&1) for v in ss.values()) if s==-1 else 0))&1)
                if (mask,rhs)!=(needmask,needrhs):counts['derived_sign_row_mismatches']+=1
                if rank(rows+[(mask,rhs)])[0]>allrank:counts['rank_increases_after_full_rows']+=1
                counts['row_XOR_source_id_tests']+=1
                if mask:counts['positive_nontrivial_early_rows' if s==1 else 'negative_nontrivial_early_rows']+=1
            counts['row_span_tests']+=1
            counts['sat_cube_completion_incidences']+=1
    assert counts['rank_increases_after_full_rows']==counts['derived_sign_row_mismatches']==0
    out['families'][name]={'n':n,'m':len(f),'global_models':len(models),'checks':counts}
  f=fmake(Y6_POS,Y6_NEG)
  p={1:0}
  mates=[]
  for bits in itertools.product((0,1),repeat=5):
      a={1:0,**{i+2:b for i,b in enumerate(bits)}}
      if eval_formula(f,a):
          _,_,ex,_,_,_=source_rows(f,6,p,a)
          mates.append({'witness':''.join(str(a[i]) for i in range(1,7)),'Eplus_parity':ex[1]&1,'Eminus_parity':ex[-1]&1})
  assert {z['Eminus_parity'] for z in mates}=={0,1}
  out['controls']['Y6_pin_x1_0']={'partial':p,'sat_extensions':len(mates),'opposing_parity_models':[next(z for z in mates if z['Eminus_parity']==t) for t in (0,1)],'odd_Eminus':sum(z['Eminus_parity'] for z in mates)}
  f=fmake(F9_POS,F9_NEG)
  for nm,p in [('F9_sat',{1:0,2:0,8:1,9:1}),('F9_unsat',{3:0,6:1,7:1,9:1}),('F9_sixpin_unsat',{8:0,3:0,7:0,6:0,1:1,5:1})]:
    avail=[v for v in range(1,10) if v not in p]
    models=[]
    for bits in itertools.product((0,1),repeat=len(avail)):
        a=dict(p);a.update(dict(zip(avail,bits)))
        if eval_formula(f,a):models.append(''.join(str(a[i]) for i in range(1,10)))
    out['controls'][nm]={'partial':p,'SAT_extensions':len(models),'witnesses':models[:8]}
  rows=[]
  for j,(sgn,c) in enumerate(f):
      mask=sum(1<<(v-1) for v in c)
      wantedtruth=0 if (j==0 or (6<=j<=10)) else 1
      rhs=wantedtruth ^ ((len(c)&1) if sgn==-1 else 0)
      rows.append((mask,rhs))
  odd_positive=(0,0)
  for m,b in rows[:6]:odd_positive=(odd_positive[0]^m,odd_positive[1]^b)
  assert odd_positive==(0,1)
  odd_negative=(0,0)
  for m,b in rows[6:]:odd_negative=(odd_negative[0]^m,odd_negative[1]^b)
  assert odd_negative==(0,1)
  out['controls']['F9_root_odd_positive_ticket']={'positive_clause_row_xor':list(odd_positive),'negative_clause_row_xor':list(odd_negative),'contradiction':'0=1','original_positive_clause_ids':list(range(6)),'ticket_excess_by_sign':{'positive':1,'negative':5},'total_ticket_excess':6,'required_root_excess':6,'negative_clause_ids_even_parity':list(range(6,11))}
  out['reference_search']={'claim':'No controlled comparison of this sign-row prepass to full CDCL or native indexed TM; row-span audit is not a speedup.','method':'exact complete model enumeration for n<=9, no uncharged SAT inference'}
  dest='sign_row_span303_raw.json'
  with open(dest,'w') as h:json.dump(out,h,sort_keys=True,indent=2)
  print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()

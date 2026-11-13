#!/usr/bin/env python3
"""Reproducible /386 SOURCE+RES prism DP compiler, not an authoritative checker.
Usage: python lspv2_605_compact_native_dp.py CHECKER386.js OUT_DIR
"""
import hashlib,itertools,json,pathlib,subprocess,sys

def norm(c):
 s=set(c)
 return None if 0 in s or any(-x in s for x in s) else tuple(sorted(s,key=lambda x:(abs(x),x)))

def build(m):
 h=2*m
 es=sorted({tuple(sorted(e)) for i in range(m) for e in
   ((i,(i+1)%m),(m+i,m+(i+1)%m),(i,m+i))})
 ids={e:i+1 for i,e in enumerate(es)}; g=len(es)+1;occ=[[] for _ in range(h)]
 for i,(u,v) in enumerate(es,1):occ[u].append(i);occ[v].append(i)
 assert len(es)==3*m and all(len(o)==3 for o in occ)
 charges=[1]+[0]*(h-1);rows=[]
 for v in range(h):
  for a in itertools.product((0,1),repeat=3):
   if (sum(a)&1)==charges[v]:continue
   c=norm([(-x if bit else x) for x,bit in zip(occ[v],a)]+[-g])
   rows.append(dict(kind='SOURCE',source=v,parents=[],c=list(c)))
 rows.append(dict(kind='SOURCE',source=-1,parents=[],c=[g]))
 def num(a,b):return ids[tuple(sorted((a,b)))]
 order=[z for i in range(m) for z in (num(i,(i+1)%m),num(m+i,m+(i+1)%m),num(i,m+i))]+[g]
 return {'h':h,'edges':[list(e) for e in es],'charge':charges,'guard':g},rows,order

def compile(spec,rows,order):
 rec=list(rows);active={tuple(r['c']):i for i,r in enumerate(rec)};known=dict(active)
 maxw=0;maxactive=len(active)
 for x in order:
  neighbors={abs(z) for c in active if x in c or -x in c for z in c if abs(z)!=x}
  maxw=max(maxw,len(neighbors))
  p=[(c,i) for c,i in active.items() if x in c]
  n=[(c,i) for c,i in active.items() if -x in c]
  nxt={c:i for c,i in active.items() if x not in c and -x not in c}
  for a,ia in p:
   for b,ib in n:
    c=norm([z for z in a if z!=x]+[z for z in b if z!=-x])
    if c is None or c in nxt:continue
    if c in known:i=known[c]
    else:
     i=len(rec);rec.append(dict(kind='RES',c=list(c),pivot=x,parents=[ia,ib]));known[c]=i
    nxt[c]=i
    if not c:break
   if () in nxt:break
  if () in nxt:break
  active=nxt;maxactive=max(maxactive,len(active))
 assert rec[-1]['kind']=='RES' and not rec[-1]['c']
 res=len(rec)-len(rows)
 return {'spec':spec,'gate_defs':[[0,spec['guard']+1,1,2]],'records':rec,
         'summary':{'source':len(rows),'def_views':0,'resolution':res,
            'paid_gates':1,'paid_total':res+1,'live_records':len(rec)}},maxw,maxactive

def main():
 checker=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 for m in (3,4,5,6,7,8,9,10,12):
  spec,src,order=build(m);d,w,a=compile(spec,src,order)
  f=out/f'prism{m}.json';b=(json.dumps(d,separators=(',',':'),sort_keys=True)+'\n').encode();f.write_bytes(b)
  cnf=('p cnf %d %d\n'%(spec['guard'],len(src))+''.join(' '.join(map(str,r['c']))+' 0\n' for r in src))
  (out/f'prism{m}.cnf').write_text(cnf)
  p=subprocess.run(['node',str(checker),str(f)],capture_output=True,text=True)
  if p.returncode:raise RuntimeError((m,p.stderr,p.stdout))
  print(json.dumps({'m':m,'paid':d['summary']['paid_total'],'width':w,'max_active':a,
       'certificate_bytes':len(b),'certificate_sha256':hashlib.sha256(b).hexdigest(),
       'source_sha256':hashlib.sha256(cnf.encode()).hexdigest(),'verdict':'ACCEPT'}))

if __name__=='__main__':main()

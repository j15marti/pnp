from pathlib import Path
src=Path(__file__).with_name('2026-11-25_1840_P3RC01_audit.py').read_text().split('for T,n in [(Q,2),(S,3),(U,4)]:valid')[0]
exec(src.replace('def closure(T,n):\n live=set(range(len(T)));','def closure(T,n,dead=()):\n live=set(range(len(T)))-set(dead);'))
def motif(T):
 incidence={}
 for i,t in enumerate(T):
  for c,v in enumerate(t):incidence.setdefault((c,v),set()).add(i)
 found=[]
 for i,t in enumerate(T):
  sets=[incidence[c,t[c]]-{i} for c in range(3)]
  if any(len(s)!=2 for s in sets):continue
  p=[sets[1]&sets[2],sets[0]&sets[2],sets[0]&sets[1]]
  if any(len(s)!=1 for s in p):continue
  ids=[next(iter(s)) for s in p]
  if len(set(ids))==3 and all(i not in s for s in p):found.append((i,ids))
 return found
out=[]
for label,idx in [('SAT',0),('UNSAT',2)]:
 T,n=graft(S,3,idx)
 for target in (4,8,16,32,64):
  while n<target:T,n=graft(T,n,len(T)-1)
  valid(T,n);m=motif(T);dead={i for _,p in m for i in p};status,scans,calls=closure(T,n,dead);assert status in (label,'UNKNOWN');out.append([label,n,len(m),len(dead),status,scans,calls])
print(json.dumps(out))

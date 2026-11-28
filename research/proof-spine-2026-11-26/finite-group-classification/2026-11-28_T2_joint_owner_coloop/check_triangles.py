"""Independent native source checker for pair-period classification; Python 3 stdlib."""
import sys,json,hashlib,itertools as it,collections as co
enc=lambda x:(json.dumps(x,separators=(',',':'))+'\n').encode('ascii')
sha=lambda b:hashlib.sha256(b).hexdigest()
EXPECTED={'joint':('e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209',5363624,'EB-JOINT-24@e84a0ab6dc6f'),'random':('8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb',5027816,'EB-RANDOM-3CNF-40@8a18e86479df')}
def basis(xs):
 p={};cost=0
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k not in p:p[k]=x;break
   x^=p[k];cost+=1
 return p,cost
def rem(x,p):
 for k,y in sorted(p.items(),reverse=True):
  if x>>k&1:x^=y
 return x
def check(raw,label):
 h,N,short=EXPECTED[label];assert sha(raw)==h and len(raw)*8==N
 G=json.loads(raw);T=G['types'];E=G['edges'];assert G['format']=='STRICT-EB4-v1';n=4*len(T);adj=[[] for _ in range(n)];seen=set();ports=set()
 for a,b,s in E:
  assert 0<=a<n and 0<=b<n and a//4!=b//4 and s in (0,1) and a not in ports and b not in ports
  ports.update([a,b]);key=tuple(sorted((a//4,b//4)));assert key not in seen;seen.add(key);adj[a].append((b,s));adj[b].append((a,s))
 assert len(ports)==n
 for i,t in enumerate(T):
  assert t in ('E','B')
  if t=='E':
   for j in range(1,4):adj[4*i].append((4*i+j,0));adj[4*i+j].append((4*i,0))
 mp=[None]*n
 for root in range(n):
  if mp[root] is not None:continue
  mp[root]=(root,0);q=[root]
  for a in q:
   for b,s in adj[a]:
    v=(root,mp[a][1]^s)
    if mp[b] is None:mp[b]=v;q.append(b)
    else:assert mp[b]==v
 tabs={}
 for i,t in enumerate(T):
  if t!='B':continue
  ps=mp[4*i:4*i+4];scope=tuple(sorted({p for p,s in ps}));ix={p:j for j,p in enumerate(scope)};A=tuple(w for w in range(1<<len(scope)) if sum(((w>>ix[p])&1)^s for p,s in ps)==2);assert A;tabs.setdefault((scope,A),[]).append(i)
 R=[(s,a,o) for (s,a),o in tabs.items()];occ=co.defaultdict(list)
 for i,(s,a,o) in enumerate(R):
  for v in s:occ[v].append(i)
 masks=[{} for _ in R];k=0
 for v,ii in sorted(occ.items()):
  masks[ii[0]][v]=0
  for j in ii[1:]:masks[ii[0]][v]^=1<<k;masks[j][v]=1<<k;k+=1
 S=[];lift=[];H=[]
 for i,(s,A,o) in enumerate(R):
  D={}
  for w in A:
   z=0
   for j,v in enumerate(s):
    if w>>j&1:z^=masks[i][v]
   D.setdefault(z,w)
  a=sorted(D);S.append(a);lift.append([[hex(z),w] for z,w in sorted(D.items())]);H.append([a[0]^z for z in a if {x^a[0]^z for x in a}==set(a)])
 B,_=basis(h for a in H for h in a);Q=[sorted({rem(x,B) for x in a}) for a in S];U=[[x^a[0] for x in a] for a in Q];assert all(len(a)==3 and len(basis(a)[0])==2 for a in U)
 C=co.Counter();work=0
 for A,D in it.combinations(U,2):
  b,c=basis(A+D);C[4-len(b)]+=1;work+=c
 assert C[2]==0
 art={'dictionaries':[[hex(x) for x in a] for a in Q],'period_basis':[hex(x) for x in B.values()]};maps={'port_map':mp,'tables':R,'occurrence_masks':[{str(v):hex(x) for v,x in a.items()} for a in masks],'syndrome_lifts':lift,'local_periods':[[hex(x) for x in a] for a in H]};ah,mh=sha(enc(art)),sha(enc(maps));iid='STRICT-EB4-v1:sha256:'+h;rid='RESIDUAL-v1:sha256:'+sha(enc(['PNP-RESIDUAL-v1',iid,'EMPTY','TRIANGLE-STAR-QUOTIENT-v1',ah,mh]));return {'problem_id':'STRICT-EB4-v1','instance':short,'instance_id':iid,'original_N_bits':N,'source_pin':{'registry':'0c14cdc57925788cf7a451dcd5aa171dce860f2c','corpus':'e315349cd6c1fe3fa696504859f28312f6aab69a','compiler':'21b9d53fb8166c819b24e708656c742cd3c24f10'},'guard_id':'EMPTY','residual_id':rid,'residual_sha256':ah,'map_sha256':mh,'original_ids':{'vertices':[0,len(T)-1],'ports':[0,n-1],'edges':[0,len(E)-1]},'parents':[],'claim':'Every pair of three-option centered dictionaries on the exact singleton-period quotient has trivial translation stabilizer. Pair span intersection dimension 0 or 1 implies sumset size 9 or 7, both odd. This is a scoped recognition refusal, not a decision.','local_period_rank':len(B),'blocks':len(Q),'pair_intersections':dict(sorted(C.items())),'pair_rank_xors':work},art,maps
if __name__=='__main__':
 raw=open(sys.argv[2],'rb').read();c,a,m=check(raw,sys.argv[1]);prefix=sys.argv[1];open(prefix+'.triangle-cert.json','wb').write(enc(c));open(prefix+'.triangle-residual.json','wb').write(enc(a));open(prefix+'.triangle-map.json','wb').write(enc(m));print(enc(c).decode(),end='');print('CERT-v1:sha256:'+sha(enc(c)))

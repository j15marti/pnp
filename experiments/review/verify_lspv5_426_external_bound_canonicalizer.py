#!/usr/bin/env python3
"""Independent Python reconstruction of LSPV-5/426.

Scope: exact external CNF multiset/variable-bound binding composed with the
recovered SOURCE/AND3/XOR parsed-object canonicalizer only.
"""
from __future__ import annotations
import copy, hashlib, json, re, subprocess, tempfile
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PACKET=ROOT/'replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json'
CHECKER=ROOT/'replay/413/lspv2_341_independent_verify.js'
checks=0; rejections=0
def need(x,msg='check'):
 global checks
 checks+=1
 if not x: raise AssertionError(msg)
def digest(b): return hashlib.sha256(b).hexdigest()
def jskey(x):
 if isinstance(x,bool): return ('bool',x)
 if isinstance(x,(int,float)): return ('number',0.0 if float(x)==0 else float(x))
 return (type(x).__name__,x)

def canonicalize(data):
 out=[]
 for f in data['fixtures']:
  E=len(f['graph']['edges']); keep=(1<<E)-1; ids={}
  def put(old,new):
   k=jskey(old)
   if k in ids: raise ValueError('duplicate identity')
   ids[k]=new; return new
  def get(old): return ids[jskey(old)]
  clauses=[{'id':put(c['id'],f's{i}'),'vertex':c['vertex'],'literals':list(c['literals'])} for i,c in enumerate(f['clauses'])]
  def row(r): return {'mask':hex(int(r['mask'],0)&keep),'rhs':r['rhs']}
  proof=[]
  for i,p in enumerate(f['proof']):
   q={'id':f'd{i}','kind':p['kind'],'rule':p['rule'],'parents':[get(x) for x in p['parents']]};put(p['id'],q['id'])
   if p['rule']=='AND3':
    q.update(support=list(p['support']),table=p['table'])
    if 'row' in p:q['row']=row(p['row'])
   elif p['rule']=='XOR':q['row']=row(p['row'])
   else:raise ValueError('unknown rule')
   proof.append(q)
  out.append({'graph':{'name':'BRIDGE_K4x2' if f['graph']['name']=='BRIDGE_K4x2' else 'G','n':f['graph']['n'],'edges':copy.deepcopy(f['graph']['edges'])},'charges':list(f['charges']),'clauses':clauses,'proof':proof,'deleted':[{'sourceId':get(d['sourceId']),'assignment':d['assignment']} for d in f['deleted']],'evenWitness':f['evenWitness'],'properties':{'essential':f['properties']['essential']}})
 return {'fixtures':out,'summary':[None]*len(out)}
def encoded(x):return (json.dumps(x,separators=(',',':'))+'\n').encode()
def accepted(b):
 with tempfile.NamedTemporaryFile(suffix='.json') as f:
  f.write(b);f.flush();return subprocess.run(['node',str(CHECKER),f.name],capture_output=True).returncode==0

def parse(src):
 a=src.strip().split()
 if len(a)<4 or a[:2]!=['p','cnf'] or not re.fullmatch(r'(0|[1-9]\d*)',a[2]) or not re.fullmatch(r'(0|[1-9]\d*)',a[3]):raise ValueError('header')
 nv,m=map(int,a[2:4]); cs=[]; now=[]
 for t in a[4:]:
  if not re.fullmatch(r'-?(0|[1-9]\d*)',t):raise ValueError('token')
  x=int(t)
  if x==0:cs.append(now);now=[]
  else:
   if abs(x)>nv:raise ValueError('range')
   now.append(x)
 if now or len(cs)!=m:raise ValueError('count')
 return nv,cs
def bag(cs):return Counter(tuple(sorted(c)) for c in cs)
def bind(f,src):
 nv,cs=parse(src); inside=[c['literals'] for c in f['clauses']]
 if nv!=len(f['graph']['edges']) or bag(cs)!=bag(inside):raise ValueError('binding')
 return True
def serialize(f,at=-1,repl=None):
 rows=[f"p cnf {len(f['graph']['edges'])} {len(f['clauses'])}"]
 for i,c in enumerate(f['clauses']):rows.append(''.join(f'{x:10d}' for x in (repl if i==at else c['literals']))+' 0')
 return '\n'.join(rows)+'\n'
def sat(cs,b):return all(any((b[abs(x)-1]=='1') if x>0 else (b[abs(x)-1]=='0') for x in c) for c in cs)
def reject(fn):
 global rejections
 try:fn()
 except Exception:rejections+=1;need(True);return
 need(False,'expected rejection')

data=json.loads(PACKET.read_text()); canon=canonicalize(data); cb=encoded(canon)
need(accepted(PACKET.read_bytes()));need(accepted(cb));need(len(cb)==71853);need(digest(cb)=='1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25')
mutants=0;bindings=0
for f,c in zip(data['fixtures'],canon['fixtures']):
 src=serialize(f);need(bind(c,src));bindings+=1
 perm=[list(reversed(x['literals'])) for x in reversed(f['clauses'])]
 psrc=f"p cnf {len(f['graph']['edges'])} {len(perm)}\n"+'\n'.join(' '.join(map(str,x))+' 0' for x in perm)+'\n'
 need(bind(c,psrc));bindings+=1
 dup=[list(x['literals']) for x in f['clauses']];dup[1]=dup[0]
 dsrc=f"p cnf {len(f['graph']['edges'])} {len(dup)}\n"+'\n'.join(' '.join(map(str,x))+' 0' for x in dup)+'\n'
 reject(lambda:bind(c,dsrc))
 for j,d in enumerate(f['deleted']):
  if d['assignment'] is None:continue
  lits=f['clauses'][j]['literals'];t=[abs(lits[0]),-abs(lits[0]),abs(lits[1])];bad=serialize(f,j,t)
  need(len(bad)==len(src));need(sat([x['literals'] for k,x in enumerate(f['clauses']) if k!=j],d['assignment']));need(sat([t],d['assignment']));reject(lambda bad=bad,c=c:bind(c,bad));mutants+=1
 reject(lambda:bind(c,re.sub(r'^p cnf \d+','p cnf 999',src)))
 reject(lambda:bind(c,src.replace(' 0\n',' \n',1)))

print(json.dumps({'status':'PASS independent Python reconstruction','checks':checks,'rejections':rejections,'fixtures':len(canon['fixtures']),'accepted_bindings':bindings,'essential_sat_mutants':mutants,'canonical_bytes':len(cb),'canonical_sha256':digest(cb),'scope':'distinct external binder + recovered SOURCE/AND3/XOR canonicalizer only'},indent=2))

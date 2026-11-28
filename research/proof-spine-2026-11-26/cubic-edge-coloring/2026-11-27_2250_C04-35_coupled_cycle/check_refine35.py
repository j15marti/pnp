"""Check a five-root marginal-extension refusal. Chart/map must first be independently reconstructed from native input."""
import json,hashlib,itertools as it,sys
from pathlib import Path

def H(b):return hashlib.sha256(b).hexdigest()
def J(x):return (json.dumps(x,separators=(',',':'))+'\n').encode()
def check(src,chart,mapraw,graw,parent,cert):
 C=json.loads(cert);P=json.loads(parent);F=json.loads(chart);G=json.loads(graw);M=json.loads(mapraw);x=C['instance_id'];assert x=='STRICT-EB4-v1:sha256:'+H(src) and C['original_N_bits']==8*len(src)
 assert H(chart)==C['chart_sha256']==P['chartHash'] and H(mapraw)==C['map_sha256']==P['mapHash'] and H(graw)==C['guard_artifact_sha256'];assert 'CERT-v1:sha256:'+H(parent) in C['parents'];assert G==[[10,0]] and M['gauge']==10
 assert C['guard_id']=='GUARD-v1:sha256:'+H(J(['PNP-GUARD-v1',x,'EB-PORT-PINS-v1',H(graw)]));assert C['residual_id']=='RESIDUAL-v1:sha256:'+H(J(['PNP-RESIDUAL-v1',x,C['guard_id'],'FP51-ENERGY-TABLE-v1',H(chart),H(mapraw)]))
 q=C['proof'];S=q['union_original_roots'];W=dict(q['positive_word_original_roots']);A=q['factors'];assert sorted({v for a in A for v in a['roots']})==S
 for a in A:
  i=a['index'];assert a['roots']==F[i]['vs'] and a['owners']==F[i]['ids'] and a['support']==P['support'][i];assert all(F[i]['cost'][r]==0 for r in a['support'])
 a=next(a for a in A if a['index']==q['factor']);z=sum(W[v]<<j for j,v in enumerate(a['roots']));assert a['support'].count(z)==q['mass_numerator']>0 and len(a['support'])==q['mass_denominator']
 tested=0
 for t in it.product((0,1),repeat=len(S)):
  h=dict(zip(S,t))
  if any(h[v]!=b for v,b in W.items()):continue
  tested+=1;assert any(sum(h[v]<<j for j,v in enumerate(a['roots'])) not in a['support'] for a in A)
 assert tested==2**(len(S)-len(W));return {'status':'REFUSED particular packet','extensions_checked':tested}
if __name__=='__main__':
 x=[Path(p).read_bytes() for p in sys.argv[1:]];print('CERT-v1:sha256:'+H(x[-1]),check(*x))

"""Verify compact certificate on its authenticated chart and reconstruction map.
Use makecert.py for source reconstruction, independent projection replay and CNF checks.
"""
import hashlib,json,sys,pathlib
P=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:(json.dumps(x,separators=(',',':'))+'\n').encode('ascii')
def check(label):
    q=json.loads((P/(label+'.local-cert.json')).read_bytes());b=(P/(label+'.chart.json')).read_bytes();m=(P/(label+'.map.json')).read_bytes();assert sha(b)==q['residual_sha256'] and sha(m)==q['map_sha256'];s=q['instance_id'];g='GUARD-v1:sha256:'+sha(enc(['PNP-GUARD-v1',s,'EB-PORT-PINS-v1',sha(enc(q['guard']))]));assert g==q['guard_id'];assert q['residual_id']=='RESIDUAL-v1:sha256:'+sha(enc(['PNP-RESIDUAL-v1',s,g,'T2-UCAC-CNF-v1',sha(b),sha(m)]));C=json.loads(b);D=[set(c) for c in C['clauses']];O=[set(x) for x in json.loads(m)['B_support']];ix={p+1:i+1 for i,p in enumerate(C['ports'])};steps=0
    for t in q['trace']:
        target={ix[abs(l)]*(1 if l>0 else -1) for l in t['relative_port_plus_one_clause']};assert target==set(t['dense_clause']);a={abs(l):l<0 for l in target};support=set()
        for j,l in t['unit_steps']:
            assert l in D[j] and abs(l) not in a and all(a.get(abs(x))==(x<0) for x in D[j] if x!=l);a[abs(l)]=l>0;support.update(O[j]);steps+=1
        j=t['conflict_clause_index'];assert all(a.get(abs(l))==(l<0) for l in D[j]);support.update(O[j]);assert support==set(t['support_B']);D.append(target);O.append(support)
    print(label,'PASS',steps,'unit steps',sha((P/(label+'.local-cert.json')).read_bytes()))
if __name__=='__main__':
    for label in sys.argv[1:] or ['joint','random']:check(label)

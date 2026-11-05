#!/usr/bin/env python3
"""LSPV-4/408 semantic live-port constructor (declared fragment only).
The exported-wire byte grammar is not native R_mix341-certified.
"""
import json,random,pathlib
P=pathlib.Path(__file__).resolve().parent
SEED=4082026
def gate(m,a,b):
    return (m>>(2*a+b))&1
def compute(net,bits):
    values=list(bits)
    for m,a,b in net:
        if not (0<=m<16 and 0<=a<len(values) and 0<=b<len(values)):
            raise ValueError('invalid or forward gate')
        values.append(gate(m,values[a],values[b]))
    return values
def truth8(net,port):
    return [compute(net,((i>>j)&1 for j in range(3)))[port] for i in range(8)]
def canonical8(table):
    m0=sum(table[0+2*a+4*b]<<(2*a+b) for a in range(2) for b in range(2))
    m1=sum(table[1+2*a+4*b]<<(2*a+b) for a in range(2) for b in range(2))
    net=[[m0,1,2],[m1,1,2],[6,3,4],[8,0,5],[6,3,6]]
    assert all(compute(net,[(i>>j)&1 for j in range(3)])[-1]==table[i] for i in range(8))
    return net
def generate(seed,L,r,q,longnames):
    rng=random.Random(seed)
    net=[[rng.randrange(16),rng.randrange(3+i),rng.randrange(3+i)] for i in range(L)]
    choices=[3+L-1]+[3+rng.randrange(L) for _ in range(r-1)]
    chosen=[]
    for p in choices:
        if p not in chosen: chosen.append(p)
    while len(chosen)<r:
        p=3+rng.randrange(L)
        if p not in chosen: chosen.append(p)
    names={p:('v'+'9'*777+str(p) if longnames and i==0 else 'source_port_'+str(p)+'_'+str(17*i+3)) for i,p in enumerate(chosen)}
    consumers=[]
    for j in range(q):
        a,b=[rng.choice(chosen) for _ in range(2)]
        consumers.append({'rule':'semantic-port-pair','refs':[names[a],names[b]],'neg':[rng.randrange(2),rng.randrange(2)]})
    for i,p in enumerate(chosen):
        consumers[i//2]['refs'][i%2]=names[p]
    return {'source':{'sat':[[1],[-2],[1,2]],'unsat':[[1],[-1]]},'net':net,
            'ports':[{'name':names[p],'gate':p} for p in chosen],'consumers':consumers}
def normalize(case):
    remap={};ports=[]
    for i,p in enumerate(case['ports']):
        name='p'+str(i+1)
        remap[p['name']]=name
        ports.append({'name':name,'circuit':canonical8(truth8(case['net'],p['gate']))})
    records=[{'rule':c['rule'],'refs':[remap[p] for p in c['refs']],'neg':c['neg']} for c in case['consumers']]
    return {'source':case['source'],'ports':ports,'consumers':records,
            'expected':{p['name']:sum(compute(p['circuit'],[(k>>j)&1 for j in range(3)])[-1]<<k for k in range(8)) for p in ports}}
def test(old,new):
    ids={p['name']:p['gate'] for p in old['ports']}
    checks=0
    for k in range(8):
        bits=[(k>>j)&1 for j in range(3)]
        ova=compute(old['net'],bits)
        nva={p['name']:compute(p['circuit'],bits)[-1] for p in new['ports']}
        for i,p in enumerate(old['ports']):
            assert ova[p['gate']]==nva['p'+str(i+1)];checks+=1
        for c,d in zip(old['consumers'],new['consumers']):
            assert c['rule']==d['rule']
            for i in range(2):
                assert ova[ids[c['refs'][i]]]^c['neg'][i]==nva[d['refs'][i]]^d['neg'][i];checks+=1
        for label,cnf in old['source'].items():
            sat=all(any(bits[abs(l)-1] if l>0 else 1-bits[abs(l)-1] for l in clause) for clause in cnf)
            assert (not sat) if label=='unsat' else True
    return checks
def main():
    configs=[(15,5,3,False),(31,10,5,False),(127,24,12,False),(511,32,16,True),(1023,40,20,True)]
    stats=[]
    for i,(L,r,q,huge) in enumerate(configs):
        old=generate(SEED+i,L,r,q,huge);new=normalize(old)
        count=test(old,new)
        ob=len(json.dumps(old,separators=(',',':')).encode())
        nb=len(json.dumps(new,separators=(',',':')).encode())
        assert r<=2*q and count==8*(r+2*q)
        stats.append({'gates':L,'ports':r,'consumers':q,'old_bytes':ob,'new_bytes':nb,'checks':count})
        if i==3:
            (P/'case_original.json').write_text(json.dumps(old,indent=2))
            (P/'case_normalized.json').write_text(json.dumps(new,indent=2))
    malformed=0
    for bad in ([[[16,0,0]]],[[[-1,0,0]]],[[[4,0,4]]],[[[0,3,0]]]):
        try:compute(bad[0],(0,0,0))
        except ValueError:malformed+=1
    assert malformed==4
    summary={'claim':'conditional fragment only','seed':SEED,'row_checks':sum(x['checks'] for x in stats),'malformed_rejections':malformed,'cases':stats}
    (P/'summary_local.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()

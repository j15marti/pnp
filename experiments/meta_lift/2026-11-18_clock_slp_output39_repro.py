#!/usr/bin/env python3
"""Independent finite-control reproducer for CLOCKSLPOUT39 using pure brute-force substring oracle.
Does not import the primary DP audit. Python 3, no dependencies.
"""
import itertools, json, hashlib, pathlib
nodes=[('t','a'),('t','b'),('c',0,1),('c',1,0),('c',2,3),('c',4,4)]
root=5

def expand(j):
    x=nodes[j]
    return x[1] if x[0]=='t' else expand(x[1])+expand(x[2])

def walk(bits, schedule, transitions, p=0):
    out=''
    for symbol,bit in zip(schedule,bits):
        p,w=transitions[(symbol,p,bit)]
        out+=w
    return p,out

def run(transition_variant):
    transitions={}
    emit=['','0','1','01']
    for zz,z in enumerate('ab'):
        for p in range(2):
            for b in range(2):
                q=(p + b +zz*(transition_variant+1))%2
                word=emit[(transition_variant+2*zz+3*p+b)%len(emit)]
                transitions[(z,p,b)]=(q,word)
    schedule=expand(root)
    allsources=list(itertools.product((0,1), repeat=len(schedule)))
    attainable={(s,e) for v in allsources for e,s in [walk(v,schedule,transitions)] if len(s)<=6}
    checks=0; tested=0
    # Oracle obtained independently by enumerating possible source words for each grammar nonterminal.
    def possible(j,p,q,s):
        z=expand(j)
        return any(walk(v,z,transitions,p)==(q,s) for v in itertools.product((0,1),repeat=len(z)))
    def invert(j,p,q,s):
        if nodes[j][0]=='t':
            z=nodes[j][1]
            return (next(b for b in (0,1) if transitions[(z,p,b)]==(q,s)),)
        a,b=nodes[j][1:]
        for t in range(2):
            for cut in range(len(s)+1):
                if possible(a,p,t,s[:cut]) and possible(b,t,q,s[cut:]):
                    return invert(a,p,t,s[:cut])+invert(b,t,q,s[cut:])
        raise AssertionError('target not reachable')
    for out,end in sorted(attainable):
        assert possible(root,0,end,out)
        g=invert(root,0,end,out)
        checks+=1
        assert walk(g,schedule,transitions)==(end,out)
        tested+=1
    return len(attainable),checks,tested

results=[run(v) for v in range(8)]
stat={'variant_count':len(results),'targets':sum(x[0] for x in results),'checks':sum(x[1] for x in results), 'tested':sum(x[2] for x in results),'failures':0,'method':'independent brute oracle for each grammar node of length at most eight; all 256 original sources per variant; each reached short (output,end) target','code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(stat,indent=2))
pathlib.Path(__file__).with_name('2026-11-18_CLOCKSLPOUT39_repro_raw.json').write_text(json.dumps(stat,indent=2)+'\n')

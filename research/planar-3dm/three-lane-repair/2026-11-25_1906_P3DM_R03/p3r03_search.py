from pathlib import Path
exec(Path(__file__).with_name('p3r03.py').read_text().split('def parse(s):')[0])
stat=collections.Counter();examples={};skips=0
for job in range(2400):
    n=rng.randrange(4,9);T=[];i=0
    while i<n:
        if i+1<n and rng.random()<.5:
            V=rng.sample(range(n),4)
            T += [(i,i,V[0]),(i,i+1,V[1]),(i+1,i,V[2]),(i+1,i+1,V[3])];i+=2
        else:
            T += [(i,i,z) for z in rng.sample(range(n),rng.choice([2,2,3]))];i+=1
    if not planar(n,T):skips+=1;continue
    a=run(n,T);o=oracle(n,T);ck(a[0] is None or a[0]==o);stat[f'{a[1]}:{a[0]}:{o}']+=1
    if a[1] in ('hybrid','hybrid_2sat','higher_circuit','nonbijunctive'):
        b=run(n,T,True);ck(b[0] is None or b[0]==o)
        key=f'{a[1]}:{o}:{b[1]}'
        if key not in examples:examples[key]=dict(n=n,T=T,before=a[:2],after=b[:2],removed=b[3])
print(json.dumps(dict(stat=stat,examples=examples,skips=skips,checks=checks),sort_keys=True))

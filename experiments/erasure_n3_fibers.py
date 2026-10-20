import json,itertools
cc={int(k):v for k,v in json.load(open("cc3.json")).items()}
res={}
for u in range(0,9):
    md=0;fd=0
    for U in itertools.combinations(range(8),u):
        mask=sum(1<<x for x in U)
        fib={}
        for f in range(256):
            g=f&~mask
            md=max(md,abs(cc[f]-cc[g])); fib.setdefault(g,[]).append(cc[f])
        fd=max(fd,max(max(v)-min(v) for v in fib.values()))
    res[u]=(md,fd)
print(res)

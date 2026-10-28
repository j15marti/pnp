import itertools, json
L=open('L.bin','rb').read(); h0=open('h0.bin','rb').read(); h1=open('h1.bin','rb').read()
n=4
def tr(f,perm,neg):
    g=0
    for a in range(16):
        b=0
        for i in range(4): b|=(((a>>perm[i])&1)^((neg>>i)&1))<<i
        if (f>>b)&1: g|=1<<a
    return g
maps=[[tr(1<<b,p,s) for b in range(16)] for p in itertools.permutations(range(4)) for s in range(16)]
def img(f,m):
    r=0
    for b in range(16):
        if (f>>b)&1: r|=m[b]
    return r
closed=set()
for f in range(65536):
    if h0[f] or h1[f]:
        for m in maps: closed.add(img(f,m))
closed|={f^0xFFFF for f in closed}
def C(f):
    g=L[f]-1
    if g<=5: return g
    if g==6: return 6
    return 6 if f in closed else 7
pc=[bin(a).count('1') for a in range(16)]
rows=[]; gap=0
for v in range(32):  # v bit k = value at weight k
    f=sum(1<<a for a in range(16) if (v>>pc[a])&1)
    rows.append((v,L[f]-1,C(f)))
from collections import Counter
print(Counter((g,c) for _,g,c in rows)); print([r for r in rows if r[1]!=r[2]])
print('max sym C',max(c for *_,c in rows))
# threshold/ majority-type
for k in range(1,5):
    v=sum(1<<w for w in range(k,5)); f=sum(1<<a for a in range(16) if (v>>pc[a])&1); print('T%d'%k,L[f]-1,C(f))
v=sum(1<<w for w in (1,3)); f=sum(1<<a for a in range(16) if (v>>pc[a])&1); print('XOR4',L[f]-1,C(f))
v=sum(1<<w for w in (2,)); f=sum(1<<a for a in range(16) if (v>>pc[a])&1); print('EXACT2',L[f]-1,C(f))
v=sum(1<<w for w in (1,)); f=sum(1<<a for a in range(16) if (v>>pc[a])&1); print('EXACT1',L[f]-1,C(f))
v=sum(1<<w for w in (0,2,4)); f=sum(1<<a for a in range(16) if (v>>pc[a])&1); print('XNOR4',L[f]-1,C(f))

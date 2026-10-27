# Closes the hit sets of b2_n4_k6 under input permutations/negations and compares with formula sizes L (formula_n4.c output).
import sys, itertools, json
h0,h1,Lf=[open(p,'rb').read() for p in sys.argv[1:4]]
n=4
def tr(f,perm,neg):
    g=0
    for a in range(16):
        b=0
        for i in range(4):
            b|=(((a>>perm[i])&1)^((neg>>i)&1))<<i
        if (f>>b)&1: g|=1<<a
    return g
maps=[[tr(1<<b,p,s) for b in range(16)] for p in itertools.permutations(range(4)) for s in range(16)]
def img(f,m):
    r=0
    for b in range(16):
        if (f>>b)&1: r|=m[b]
    return r
base={f for f in range(65536) if h0[f] or h1[f]}
# group closure on the (small) set of hits; first gate was fixed up to group, so close under all 384 maps
closed=set()
for f in base:
    for m in maps: closed.add(img(f,m))
closed|={f^0xFFFF for f in closed}
Lv=lambda f:Lf[f]  # formula leaves; g_L=L-1
le5={f for f in range(65536) if Lf[f]-1<=5}
gl6={f for f in range(65536) if Lf[f]-1==6}
gl7={f for f in range(65536) if Lf[f]-1==7}
c6=closed-le5
out=dict(hit_closed=len(closed),new_at_6=len(c6),gL6=len(gl6),gL7=len(gl7),
 c6_eq_gL6=(c6==gl6),c6_in_gL7=len(c6&gl7),gL6_missed=len(gl6-c6))
print(json.dumps(out)); json.dump(out,open('b2_n4_k6.json','w'))

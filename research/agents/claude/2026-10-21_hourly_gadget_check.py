# Exhaustive check of the RANKBRIDGE-PRIVATE-WITNESS44 gadget G_b(y,u,v) and the 2^q counting step. Runs in <1s.
import itertools
def clauses_ok(b,y,u,v):
    l = y if b else (1-y)
    # four clauses (l|u|v)(l|u|~v)(l|~u|v)(l|~u|~v)
    return all(l or (uu if su else 1-uu) or (vv if sv else 1-vv)
               for su,sv in itertools.product((1,0),(1,0)) for uu,vv in [(u,v)])
ok=True
for b in (0,1):
    for y in (0,1):
        sat = any(clauses_ok(b,y,u,v) for u in (0,1) for v in (0,1))
        ok &= (sat == (y==b))
print("gadget satisfiable iff y==b:", ok)
# counting: 2^q distinct forced projections vs advice strings of length <= s
for q in (4,8,12):
    for s in range(q+1):
        outs = 2**s
        assert (outs >= 2**q) == (s >= q)
print("fixed-length advice needs s>=q: ok")

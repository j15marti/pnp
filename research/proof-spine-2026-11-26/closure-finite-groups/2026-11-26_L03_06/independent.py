import hashlib, json, random

SEED = 2611260602
rng = random.Random(SEED)

def matching(a, n):
    mate = [-1] * n
    def visit(i, seen):
        for j in range(n):
            if a[i*n+j] and j not in seen:
                seen.add(j)
                if mate[j] < 0 or visit(mate[j], seen):
                    mate[j] = i
                    return True
        return False
    return all(visit(i, set()) for i in range(n))

def grid(a, n):
    k = n+2
    out = []
    for i in range(k):
        for j in range(k):
            m = 0
            for w in range(16):
                N,E,S,W = [(w >> b)&1 for b in (3,2,1,0)]
                if i<n and 0<j<=n:
                    ok = (N==S and E==W) or (a[i*n+j-1] and w==6)
                elif j==0:
                    ok = E==0 and (S==1 if i==k-1 else N==S)
                elif j==k-1:
                    ok = W==int(i<n) and (S==1 if i==k-1 else N==S)
                else:
                    ok = N==S and E==W
                if ok: m |= 1 << w
            out.append(m)
    return out

def digest(a,n):
    data = b''.join(x.to_bytes(2,'little') for x in grid(a,n))
    return hashlib.sha256(data).hexdigest()

def audit():
    results=[]
    for n in (14,16,32,64,128):
        no=[int(i>=3 or j<2) for i in range(n) for j in range(n)]
        yes=no.copy(); yes[2*n+2]=1
        assert not matching(no,n) and matching(yes,n)
        mix=0
        for rep in range(32):
            ids=rng.sample(range(n*n),13)
            pins={i:rng.randrange(2) for i in ids}
            mix += int(len(set(pins.values()))==2)
            a=[1]*(n*n); b=[0]*(n*n)
            for i,x in pins.items(): a[i]=b[i]=x
            assert matching(a,n) and not matching(b,n)
            # Count destroyed cyclic permutations independently of the matcher.
            blocked={(i%n-i//n)%n for i,x in pins.items() if not x}
            shift=next(j for j in range(n) if j not in blocked)
            assert all(a[i*n+(i+shift)%n] for i in range(n))
            assert sum(b)<n and all(a[i]==b[i]==x for i,x in pins.items())
        results.append(dict(n=n,patterns=32,mixed_pins=mix,
                            no_sha256=digest(no,n),yes_sha256=digest(yes,n)))
    return dict(seed=SEED,encoding='row-major unsigned 16-bit masks, little-endian; dimension n+2 specified separately',results=results)

if __name__=='__main__':
    print(json.dumps(audit(),indent=2))

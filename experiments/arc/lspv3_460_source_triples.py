#!/usr/bin/env python3
"""LSPV-3/460 source-triple collision controls; exact theorem concerns IID,
not the deterministic SHA256-counter stream used here for reproducibility."""
import hashlib, itertools, json, math, os, time

class HashStream:
    def __init__(self, seed):
        if not isinstance(seed, int) or seed <= 0 or seed >= 2**32:
            raise ValueError("invalid seed")
        self.seed = seed.to_bytes(4,'big')
        self.counter = 0
    def word(self):
        c = self.counter.to_bytes(8,'big')
        self.counter += 1
        return int.from_bytes(hashlib.sha256(self.seed+c).digest()[:8], 'big')
    def bounded(self, bound):
        limit = (2**64 // bound) * bound
        while True:
            x = self.word()
            if x < limit:
                return x % bound

def proper3(n, seed):
    rng = HashStream(seed)
    for _ in range(8*n):
        ids = []
        while len(ids) < 3:
            t = rng.bounded(n) + 1
            if t not in ids: ids.append(t)
        ids.sort()
        mask = rng.bounded(8)
        yield tuple((-v if mask & (1<<i) else v) for i,v in enumerate(ids))

def source_bytes(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n' +
            ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')

def count(clauses):
    triple_hist, signed_hist = {}, {}
    for c in clauses:
        assert len(c)==3 and len(set(map(abs,c)))==3
        t = tuple(sorted(map(abs,c)))
        triple_hist[t] = triple_hist.get(t,0)+1
        signed_hist[c] = signed_hist.get(c,0)+1
    return {
        'pair_candidates_source_AND3':sum(k*(k-1)//2 for k in triple_hist.values()),
        'repeated_variable_triples':sum(k>=2 for k in triple_hist.values()),
        'max_triple_multiplicity':max(triple_hist.values(),default=0),
        'duplicate_signed_source_pairs':sum(k*(k-1)//2 for k in signed_hist.values()),
        'distinct_variable_triples':len(triple_hist)
    }

def literal_sat(lit, bits):
    v = bits[abs(lit)-1]
    return v if lit>0 else not v

def parity_control():
    clauses=[]
    for bits in itertools.product((0,1),repeat=3):
        if sum(bits)%2 == 0:
            clauses.append(tuple(-i-1 if b else i+1 for i,b in enumerate(bits)))
    assert len(clauses)==4 and count(clauses)['pair_candidates_source_AND3']==6
    for bits in itertools.product((0,1),repeat=3):
        outcomes=[any(literal_sat(l,bits) for l in c) for c in clauses]
        f1=outcomes[0] and outcomes[1]
        f2=outcomes[2] and outcomes[3]
        assert (f1 and f2)==(sum(bits)%2==1)
    return {'source_clauses':[list(c) for c in clauses],
            'truth_rows_verified':8,
            'exact_row':'x1 XOR x2 XOR x3 = 1',
            'paid_AND3_nodes':3,'total_source_pair_candidates':6}

def main():
    stamp=time.perf_counter()
    results=[]
    for n in (256,512,2048,8192):
        m=8*n
        expectation=math.comb(m,2)/math.comb(n,3)
        for seed in (11,23,47,89):
            cs=list(proper3(n,seed))
            digest=hashlib.sha256(source_bytes(n,cs)).hexdigest()
            results.append({'n':n,'m':m,'seed':seed,'source_sha256':digest,
                            'expected_collision_pairs_iid':expectation, **count(cs)})
    for r in results:
        assert r['pair_candidates_source_AND3']>=r['repeated_variable_triples']
    data={'status':'COMPUTATIONAL, pseudorandom validation only; original xorshift low-bit artifacts rejected',
          'family':'8n iid uniform proper signed strict-3 clauses (theorem); SHA256 counter stream (finite controls)',
          'theory':{'triple_universe':'C(n,3)',
                    'expected_pairs':'C(8n,2)/C(n,3)',
                    'no_pair_probability_bound':'Pr(Z>0)<=C(8n,2)/C(n,3)=O(1/n)',
                    'exact_probability_no_collision':'(C(n,3))_(8n) / C(n,3)^(8n)',
                    'strongest_conclusion':'No original/source-source AND3 pair when all variable triples distinct; does not exclude RES or DEF shortcuts'},
          'results':results,'host_seconds':round(time.perf_counter()-stamp,5),
          'forced_parity_control':parity_control(),
          'prng_falsifier':'Rejected earlier xorshift32 modulo powers-of-two output because observed n=8192 collisions were grossly inconsistent with iid expectation; SHA256-counter stream is still deterministic, not iid.',
          'corrupted_control':{'mutation':'add one signed source clause on the first triple',
                               'expected_increase_in_collision_pairs':1}}
    cs=list(proper3(256,89))
    before=count(cs)['pair_candidates_source_AND3']
    t=tuple(sorted(map(abs,cs[0])))
    occ=sum(tuple(sorted(map(abs,c)))==t for c in cs)
    cs.append(cs[0])
    after=count(cs)['pair_candidates_source_AND3']
    assert after-before==occ
    data['corrupted_control']['actual_pair_increase']=after-before
    data['corrupted_control']['expected_increase_in_collision_pairs']=occ
    out=os.path.join(os.path.dirname(__file__),'lspv3_460_raw.json')
    with open(out,'w') as f:json.dump(data,f,indent=2,sort_keys=True)
    print('CASES',len(results),'COLLISIONS',
          sum(r['pair_candidates_source_AND3'] for r in results),'JSON',out)

if __name__=='__main__':
    main()

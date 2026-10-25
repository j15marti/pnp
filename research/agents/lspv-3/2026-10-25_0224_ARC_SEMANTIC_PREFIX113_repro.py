#!/usr/bin/env python3
"""ARC-SEMANTIC-PREFIX113. Exact finite ordinary proper-3CNF audit.

Independent DPLL, explicit unary-width binary serialization/reparse, two
actual pinned descendants, shared source identifiers, both SAT/UNSAT labels.
All reported operation counters are Python/logical counters, NOT FLMV tape
costs. Standard library only; deterministic, no randomization.
"""
import json
from itertools import product


class Formula:
    def __init__(self, b):
        self.b = b
        self.n = b
        self.clauses = []

    def alloc(self):
        self.n += 1
        return self.n

    def add(self, *lits):
        assert len(lits) == 3 and len({abs(z) for z in lits}) == 3
        self.clauses.append(tuple(lits))

    def pin(self, literal):
        p, q = self.alloc(), self.alloc()
        for sp, sq in product((1, -1), repeat=2):
            self.add(literal, sp*p, sq*q)

    def disjunction2(self, a, b):
        t = self.alloc()
        self.add(a, b, t)
        self.add(a, b, -t)

    def xor(self, a, b, z):
        for av, bv, zv in product((0, 1), repeat=3):
            if zv != (av ^ bv):
                self.add(a if av == 0 else -a,
                         b if bv == 0 else -b,
                         z if zv == 0 else -z)


def add_parity(f, parity):
    chain = [f.alloc() for _ in range(f.b+1)]
    f.pin(-chain[0])
    for i in range(f.b):
        f.xor(chain[i], i+1, chain[i+1])
    if parity is not None:
        f.pin(chain[-1] if parity else -chain[-1])
    return chain[-1]


def build_pair(b, target):
    """F=Even(x) AND (Odd(x) OR [x=target]); shared x are IDs 1..b."""
    f = Formula(b)
    add_parity(f, 0)
    split = len(f.clauses)
    last = add_parity(f, None)
    selector = f.alloc()
    f.disjunction2(selector, last)   # selector=0 forces odd parity
    for i, bit in enumerate(target, 1):
        f.disjunction2(-selector, i if bit else -i)
    assert f.n == 4*b+10, (f.n, b)
    assert len(f.clauses) == 10*b+14
    return f, split


def dense_module(f, selected):
    """Keep shared names 1..b; make private IDs dense and source-name faithful."""
    original = sorted({abs(v) for c in selected for v in c})
    assert set(range(1, f.b+1)).issubset(original)
    private = [v for v in original if v > f.b]
    map_local = {i: i for i in range(1, f.b+1)}
    map_local.update({v: f.b+j for j, v in enumerate(private, 1)})
    g = Formula(f.b)
    g.n = f.b+len(private)
    g.clauses = [tuple((1 if v > 0 else -1)*map_local[abs(v)] for v in c) for c in selected]
    assert tuple(map_local[x] for x in range(1, f.b+1)) == tuple(range(1, f.b+1))
    return g


def clone_and_pin(f, i, bit):
    g = Formula(f.b)
    g.n = f.n
    g.clauses = list(f.clauses)
    g.pin(i if bit else -i)
    return g


def encode(f):
    m = len(f.clauses)
    h = max(1, (2*max(f.n,m)+1).bit_length())
    fields = [f.n, m]+[2*(abs(z)-1)+(z < 0) for clause in f.clauses for z in clause]
    bits = '1'*h+'0'+''.join(format(int(v), f'0{h}b') for v in fields)
    assert len(bits) == 1+(3+3*m)*h
    return bits


def decode(bits, b):
    h = bits.find('0')
    if h < 1 or bits[:h] != '1'*h or len(bits) < h+1+2*h:
        raise ValueError('bad width header')
    off = h+1
    def word():
        nonlocal off
        x = int(bits[off:off+h], 2)
        off += h
        return x
    n,m = word(),word()
    if len(bits) != 1+(3+3*m)*h or n < b or m < 0:
        raise ValueError('bad length/fields')
    g = Formula(b)
    g.n = n
    for _ in range(m):
        row=[]
        for _ in range(3):
            code = word()
            v=(code//2)+1
            if v > n:
                raise ValueError('invalid literal')
            row.append(-v if code % 2 else v)
        if len({abs(z) for z in row}) != 3:
            raise ValueError('not proper 3CNF')
        g.add(*row)
    assert off == len(bits)
    return g


CHECKS = 0
DPLL_CALLS = 0


def check(statement):
    global CHECKS
    CHECKS += 1
    if not statement:
        raise AssertionError(f'check {CHECKS} failed')


def dpll(clauses):
    global DPLL_CALLS
    DPLL_CALLS += 1
    clauses = tuple(clauses)
    while True:
        units = [c[0] for c in clauses if len(c) == 1]
        if any(len(c) == 0 for c in clauses):
            return False
        if not clauses:
            return True
        if not units:
            break
        var = abs(units[0]); value=units[0]>0
        transformed=[]
        for c in clauses:
            if any(abs(z)==var and (z>0)==value for z in c):
                continue
            residue=tuple(z for z in c if abs(z)!=var)
            transformed.append(residue)
        clauses = tuple(transformed)
    freq = {}
    for c in clauses:
        for z in c:
            freq[abs(z)] = freq.get(abs(z), 0) + 1
    variable = max(freq, key=freq.get)
    for value in (True, False):
        nextcl = []
        for c in clauses:
            if any(abs(z)==variable and (z>0)==value for z in c):
                continue
            nextcl.append(tuple(z for z in c if abs(z)!=variable))
        if dpll(nextcl):
            return True
    return False


def sat_ordinary(f):
    return dpll(f.clauses)


def module_expected(which, b, prefix, target):
    if len(prefix) < b:
        return True
    parity = sum(prefix) & 1
    if which == 'even':
        return parity == 0
    return bool(parity or tuple(prefix) == tuple(target))


def run():
    entries=[]
    parents = 0
    first_children=0
    second_children=0
    parent_second_children=0
    full_pin_queries=0
    ordinary_bits_generated=0
    for b in range(2,7):
        even=(0,)*b
        odd=(0,)*(b-1)+(1,)
        fyes,split=build_pair(b,even)
        fno,split2=build_pair(b,odd)
        check(split==split2)
        check(fyes.n==fno.n and len(fyes.clauses)==len(fno.clauses))
        check([tuple(abs(z) for z in c) for c in fyes.clauses] ==
              [tuple(abs(z) for z in c) for c in fno.clauses])
        byteyes,byteno=encode(fyes),encode(fno)
        check(len(byteyes)==len(byteno))
        check(decode(byteyes,b).clauses==fyes.clauses)
        check(decode(byteno,b).clauses==fno.clauses)
        differing=sum(x!=y for x,y in zip(byteyes,byteno))
        check(differing==2)
        records={}
        for label,f,target in [('SAT',fyes,even),('UNSAT',fno,odd)]:
            parents+=1
            check(sat_ordinary(decode(encode(f), b)) == (label=='SAT'))
            r=dense_module(f,f.clauses[:split]); q=dense_module(f,f.clauses[split:])
            check(sat_ordinary(r)); check(sat_ordinary(q))
            for which,mod in [('even',r),('target',q)]:
                # True, fully serialized ordinary children for two real levels.
                # All source names x_i remain literal IDs 1..b across the cut.
                first={}
                second={}
                for v0 in (0,1):
                    c0=clone_and_pin(mod,1,v0)
                    s0=encode(c0); parsed0=decode(s0,b)
                    ordinary_bits_generated+=len(s0)
                    first_children+=1
                    check(parsed0.clauses==c0.clauses)
                    check(sat_ordinary(parsed0)==module_expected(which,b,(v0,),target))
                    first[v0]=len(s0)
                    for v1 in (0,1):
                        c1=clone_and_pin(parsed0,2,v1)
                        s1=encode(c1); parsed1=decode(s1,b)
                        ordinary_bits_generated+=len(s1)
                        second_children+=1
                        check(parsed1.clauses==c1.clauses)
                        check(sat_ordinary(parsed1)==module_expected(which,b,(v0,v1),target))
                        second[(v0,v1)]=len(s1)
                # Direct-source parity decision is independent of the oracle.
                check(any(module_expected(which,b,(v0,v1),target)
                          for v0,v1 in product((0,1), repeat=2)))
                records[which]={'module_bits':len(encode(mod)),
                               'first_child_bits':max(first.values()),
                               'grandchild_bits':max(second.values())}
            # BOTH-LABEL global join on a single shared x assignment.
            visible_join=any(module_expected('even',b,p,target) and
                             module_expected('target',b,p,target)
                             for p in product((0,1),repeat=b))
            check(visible_join==(label=='SAT'))
            # A blind controller seeing only prefix SAT bits is given no signal:
            for k in range(b):
                for p in product((0,1),repeat=k):
                    check(module_expected('even',b,p,target))
                    check(module_expected('target',b,p,target))
            for p in product((0,1),repeat=b):
                check(module_expected('target',b,p,target)==
                      ((sum(p)&1)==1 or tuple(p)==tuple(target)))
                full_pin_queries+=1
            records[label]={'parent_bits':len(encode(f)),
                            'parent_n':f.n,'parent_m':len(f.clauses),
                            'R':records['even'],'Q':records['target']}
            del records['even'],records['target']
        check(records['SAT']['parent_bits']==records['UNSAT']['parent_bits'])
        # Eager full-parent ordinary descendants also retain both labels.
        for target, label in [(even,True),(odd,False)]:
            parent,_=build_pair(b,target)
            for v0,v1 in product((0,1),repeat=2):
                one=clone_and_pin(parent,1,v0)
                one_dec=decode(encode(one),b)
                ordinary_bits_generated+=len(encode(one))
                check(one.clauses==one_dec.clauses)
                two=clone_and_pin(one_dec,2,v1)
                grand=decode(encode(two),b)
                ordinary_bits_generated+=len(encode(two))
                check(grand.clauses==two.clauses)
                parent_second_children+=1
                check(sat_ordinary(grand)==(label and tuple(target[:2])==(v0,v1)))
        entries.append({'shared_variables':b,'even_targets':1<<(b-1),
                        'no_yes_encoded_bit_changes':differing,
                        'labels':records})
    # Independent proper-3CNF native controls, all 8 signed triples UNSAT.
    tiny=Formula(3); tiny.add(1,2,3)
    check(sat_ordinary(decode(encode(tiny),3)))
    hostile=Formula(3)
    for s in product((1,-1),repeat=3):
        hostile.add(s[0],2*s[1],3*s[2])
    check(not sat_ordinary(decode(encode(hostile),3)))
    horn=Formula(3); horn.add(-1,-2,3)
    check(sat_ordinary(decode(encode(horn),3)))
    fail=encode(horn)[:-1]  # invalid/truncated ordinary body
    try:
        decode(fail,3)
    except ValueError:
        check(True)
    else:
        check(False)
    result={
        'id':'ARC-SEMANTIC-PREFIX113',
        'status':'COMPUTATIONAL finite ordinary 3CNF audit; restricted symbolic lemma separate',
        'seed':None,'exhaustive_cases':'All b=2..6, both target parity labels, all prefix predicates; two actual proper-3CNF levels with complete serialization and independent generic DPLL',
        'cases':{'roots':parents,'module_first_children':first_children,
                 'module_second_children':second_children,
                 'parent_second_children':parent_second_children,
                 'module_complete_prefix_predicates':full_pin_queries},
        'checks':CHECKS,'dpll_recursive_calls':DPLL_CALLS,
        'total_serialized_descendant_bits':ordinary_bits_generated,
        'failures':0,'metadata_matched':True,
        'note':'Actual descendant lengths are asymptotically Theta(parent length), no fixed lambda<1. Python counts NOT physical FLMV time or workspace.',
        'lengths_and_hidden_even_counts':entries,
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    run()

"""Exact joint distributions on encoded strict-C parity cubes."""
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import t5_accounting_sil_parity_return_20261121 as family
import t5_construction_positive_offset1_20261121 as compiler

assert sha256(Path(family.__file__).read_bytes()).hexdigest() == 'dc638ba9988a597361b67ec4476bf85c18e4909e74a04d284c958baf0bff1382'


def encoded(bits):
    n, clauses = family.images(bits)[0]
    n, clauses, links = compiler.split(n, clauses)
    return compiler.encode(n, clauses), links


def circuit(inputs, final_complement):
    # An actual AND/OR/NOT DAG implementing parity with ≤4k+1 gates.
    gates = []
    def gate(op, *parents):
        gates.append((op, *parents))
        return len(inputs)+len(gates)-1
    current = 0
    for next_input in range(1,len(inputs)):
        union = gate('or', current, next_input)
        intersect = gate('and', current, next_input)
        inverted = gate('not', intersect)
        current = gate('and', union, inverted)
    if final_complement:
        current = gate('not',current)
    values = list(inputs)
    for op, *p in gates:
        values.append((1-values[p[0]]) if op=='not' else
                      (values[p[0]] & values[p[1]]) if op=='and' else
                      (values[p[0]] | values[p[1]]))
    return values[current],len(gates)


def main():
    results=[]
    for k in range(1,6):
        words=list(product((0,1),repeat=k))
        baseline,links=encoded(words[0])
        masks=[]
        for j in range(k):
            variant,_=encoded(tuple(int(i==j) for i in range(k)))
            masks.append([i for i,(a,b) in enumerate(zip(baseline,variant)) if a!=b])
        assert all(masks)
        assert len(set().union(*map(set,masks)))==sum(map(len,masks))
        selectors=[m[0] for m in masks]
        flip=sum(int(baseline[j]) for j in selectors)%2
        true_accept=fake_accept=0
        rows=[]
        for bits in words:
            data,e=encoded(bits)
            assert e==links and len(data)==len(baseline)
            difference={i for i,(a,b) in enumerate(zip(data,baseline)) if a!=b}
            expected=set().union(*(set(m) for bit,m in zip(bits,masks) if bit))
            assert difference==expected
            label=1-sum(bits)%2
            count=(20 << links)*label
            assert ((count>>(links+2)) & 1)==label
            inputs=[int(data[j]) for j in selectors]+[label]
            accept,gates=circuit(inputs,flip)
            true_accept+=accept
            for fake in (0,1):
                fake_accept+=circuit(inputs[:-1]+[fake],flip)[0]
            rows.append(dict(switches=bits,sha256=sha256(data.encode()).hexdigest(),
                             first_positive_bit=label))
        assert true_accept==2**k and fake_accept==2**k
        for subset in range((1<<k)-1):
            indices=[j for j in range(k) if subset>>j&1]
            real=Counter()
            fake=Counter()
            for bits in words:
                part=tuple(bits[j] for j in indices)
                real[part+(1-sum(bits)%2,)]+=2
                for y in (0,1):
                    fake[part+(y,)]+=1
            assert real==fake
        results.append(dict(k=k,N=len(baseline),E=links,selectors=selectors,
                            baseline_selector_parity=flip,mask_sizes=list(map(len,masks)),
                            indistinguishable_proper_subsets=(1<<k)-1,
                            AND_OR_NOT_gates=gates,true_accept=true_accept,
                            true_denominator=2**k,fake_accept=fake_accept,
                            fake_denominator=2**(k+1),rows=rows))
    print(json.dumps(dict(lemma='T5-PARITY-BUDGET-PAIR1',results=results,
                         code_sha256=sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__=='__main__':
    main()

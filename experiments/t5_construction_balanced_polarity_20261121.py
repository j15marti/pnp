"""T5-BALANCED-POLARITY1, exact finite tests of a decision reduction."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import t5_construction_positive_offset1_20261121 as c

DEP = '6cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb'
assert sha256(Path(c.__file__).read_bytes()).hexdigest() == DEP


def twins(p, gates, out):
    c.validate(p, gates, out)
    b = p + len(gates)
    augmented = tuple(gates) + (('not', out), ('not', b), ('not', b+1))
    return [c.compile_circuit(p, augmented, target) for target in (b+1, b)]


def main():
    cases = []
    for p in (1, 2):
        for depth in (0, 1):
            for gates in c.enumerate_gates(p, depth):
                for out in range(p + depth):
                    cases.append((p, gates, out))
    cases += [(1, (('not',0),('or',0,1)),2),
              (1, (('not',0),('or',0,1),('not',2)),3),
              (3, (('or',0,1),('or',3,3)),4)]
    rows = []
    for p, gates, out in cases:
        z = c.source_count(p, gates, out)
        b = p + len(gates)
        o = sum(g[0]=='or' for g in gates)
        t = len(gates)-o
        images = twins(p, gates, out)
        assert images[0][1][:-1] == images[1][1][:-1]
        stats = []
        for polarity, (n, clauses) in enumerate(images):
            assert (n,len(clauses)) == (17+4*b+2*o,27+6*b+5*o+t)
            degree = Counter(x for row in clauses for x in row)
            hist = sorted(Counter(degree.values()).items())
            count, calls = c.generic_count(n, clauses)
            expected = z if polarity == 0 else (1<<p)-z
            assert count == 10*expected
            nn, split, e = c.split(n, clauses)
            encoded = c.encode(nn, split)
            assert c.decode(encoded) == (nn, split)
            assert e == 64+14*b+13*o+3*t
            assert (nn,len(split)) == (337+74*b+67*o+15*t,411+90*b+83*o+19*t)
            assert max(Counter(x for row in split for x in row).values()) <= 5
            assert 3*len(split)-nn == 14*e
            stats.append(dict(n=n,m=len(clauses),N=len(c.encode(n,clauses)),n_split=nn,
                              m_split=len(split),N_split=len(encoded),E=e,path_histogram=hist,
                              unsplit_count=count,split_count=count<<e,calls=calls,
                              status='SAT' if count else 'UNSAT',sha256=sha256(encoded.encode()).hexdigest()))
        assert stats[0]['path_histogram'] == stats[1]['path_histogram']
        assert stats[0]['N_split'] == stats[1]['N_split']
        assert stats[0]['split_count']+stats[1]['split_count'] == 10*(1<<(stats[0]['E']+p))
        row = dict(p=p,gates=gates,out=out,source_count=z,images=stats)
        if z in (0,1<<p):
            row['full_unsplit_clauses'] = [x[1] for x in images]
        rows.append(row)
    print(json.dumps(dict(lemma='T5-BALANCED-POLARITY1',cases=rows,case_count=len(rows),
                         dependency_sha256=DEP,code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                         count_method='generic full-domain unsplit; split by proved fiber identity'),indent=2))


if __name__ == '__main__':
    main()

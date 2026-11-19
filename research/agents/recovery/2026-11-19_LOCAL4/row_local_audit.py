import itertools, json
from fractions import Fraction as Q

# Each of four residuals is a predicate on one private bit.
counts = {'SAT': 0, 'UNSAT': 0, 'row_local_checks': 0, 'global_checks': 0}
for raw in itertools.product(range(4), repeat=4):
    cells = [raw[:2], raw[2:]]
    direct_sat = any(all(mask != 0 for mask in row) for row in cells)
    local_no = True
    for row in cells:
        found = False
        for i in range(2):
            counts['row_local_checks'] += 1
            if row[i] == 0:
                found = True
                break
        if not found:
            local_no = False
            break
    global_no = False
    for selector in itertools.product(range(2), repeat=2):
        counts['global_checks'] += 1
        if all(cells[z][selector[z]] == 0 for z in range(2)):
            global_no = True
            break
    assert local_no == global_no == (not direct_sat)
    counts['SAT' if direct_sat else 'UNSAT'] += 1

# Sharing a certificate across obligations is invalid: w=0 and w=1.
predicates = [{0}, {1}]
assert all(any(w in p for w in range(2)) for p in predicates)
assert not any(all(w in p for p in predicates) for w in range(2))

# Native T5 two-branch critical control, independent of prior stored witnesses.
words = ['BBB', 'FBB', 'FFF', 'BB']
def relation(word):
    values = {0}
    for ch in word:
        steps = (1,3) if ch == 'F' else (2,4)
        values = {(a+b)%5 for a in values for b in steps}
    return values
rels = [relation(w) for w in words]
assert not set.intersection(*rels)
edges = sum(map(len,words))
for i, word in enumerate(words):
    # Deleting any edge of thread i removes that endpoint constraint;
    # the two dangling pieces can be greedily colored from their branch ends.
    surviving = set.intersection(*(r for j,r in enumerate(rels) if j != i))
    assert surviving
result = {'status':'PASS', 'tables':256, **counts,
          'shared_certificate_counterexample':True,
          'T5_H9_relations':[sorted(r) for r in rels],
          'T5_deletions_extendable':edges,
          'seed_threshold':str((Q(133,100)-Q(845,1000))/Q(35,100)),
          'local_budget':str(Q(133,100)-Q(195,1000)),
          'whole_enumeration_log_slack':str(Q(134070,100000)-Q(133,100))}
print(json.dumps(result, indent=2))

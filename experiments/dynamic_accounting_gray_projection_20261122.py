"""Exhaustive projection and Gray-update audit. No external dependencies."""
import hashlib
import itertools
import json
from pathlib import Path


def reduced_rows(rows, width):
    rows = list(rows)
    pivots = []
    rank = 0
    for column in range(width):
        found = next((j for j in range(rank, len(rows))
                      if (rows[j] >> column) & 1), None)
        if found is None:
            continue
        rows[rank], rows[found] = rows[found], rows[rank]
        for j in range(len(rows)):
            if j != rank and ((rows[j] >> column) & 1):
                rows[j] ^= rows[rank]
        pivots.append(column)
        rank += 1
    return rows[:rank], pivots


def projected_basis(rows, width, ports):
    reduced, pivots = reduced_rows(rows, width)
    nullspace = []
    for free in range(width):
        if free in pivots:
            continue
        vector = 1 << free
        for row, pivot in zip(reduced, pivots):
            if (row >> free) & 1:
                vector |= 1 << pivot
        nullspace.append(sum(((vector >> p) & 1) << j
                             for j, p in enumerate(ports)))
    return reduced_rows(nullspace, len(ports))[0]


def gray_vectors(basis, width):
    vector = 0
    yield vector, None, 0
    for index in range(1, 1 << len(basis)):
        changed = (index & -index).bit_length() - 1
        # Deliberately update each coordinate to expose the logical bit tariff.
        for bit in range(width):
            vector ^= ((basis[changed] >> bit) & 1) << bit
        yield vector, changed, width


def main():
    records = []
    for rows in itertools.product(range(16), repeat=3):
        basis = projected_basis(rows, 4, (0, 1, 2))
        stream = list(gray_vectors(basis, 3))
        vectors = [v for v, _, _ in stream]
        oracle = {x & 7 for x in range(16)
                  if all((x & row).bit_count() % 2 == 0 for row in rows)}
        assert set(vectors) == oracle and len(vectors) == len(oracle)
        assert sum(cost for _, _, cost in stream) == 3 * ((1 << len(basis)) - 1)
        for j, (vector, changed, _) in enumerate(stream[1:], 1):
            assert vector ^ vectors[j-1] == basis[changed]
        accepted = next((j for j,v in enumerate(vectors) if v.bit_count() == 1), None)
        assert (accepted is not None) == any(v.bit_count() == 1 for v in oracle)
        # A real decision run stops at its first satisfying candidate.
        visited = len(vectors) if accepted is None else accepted + 1
        records.append(dict(rows=rows, rank=len(basis), basis=basis,
                            vectors=vectors, sat=accepted is not None,
                            visited=visited, update_bits=3*(visited-1),
                            factor_read_bits=3*visited))
    controls = []
    for width, rows, ports in [(0, [], ()), (3, [1,2,4], (0,1,2)),
                              (3, [], (0,1,2)), (3, [3,6], ())]:
        basis = projected_basis(rows, width, ports)
        values = [v for v,_,_ in gray_vectors(basis,len(ports))]
        oracle = {sum(((x>>p)&1)<<j for j,p in enumerate(ports))
                  for x in range(1<<width)
                  if all((x&r).bit_count()%2==0 for r in rows)}
        assert set(values)==oracle and len(values)==len(oracle)
        controls.append(dict(width=width, rows=rows, ports=ports, basis=basis, values=values))
    output = dict(mode="4096 ordered 3x4 homogeneous binary matrices; no randomness",
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  SAT=sum(r["sat"] for r in records),
                  UNSAT=sum(not r["sat"] for r in records),
                  record_columns=["packed_matrix", "projected_rank", "candidates_visited", "sat"],
                  records=[[r["rows"][0]+16*r["rows"][1]+256*r["rows"][2],
                            r["rank"],r["visited"],int(r["sat"])] for r in records],
                  representative_traces=records[::512], controls=controls,
                  scope="Logical bit counts only. Physical TM tariff proved in report.")
    destination=Path("results/raw/dynamic_accounting_gray_projection_20261122.json")
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(output,separators=(",",":"))+"\n")
    print(json.dumps({k:v for k,v in output.items() if k not in ("records","controls")}))


if __name__ == "__main__":
    main()

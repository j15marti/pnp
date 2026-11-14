"""Exact DIMACS byte length of a Tseitin CNF on any d-regular graph with n vertices.
Edges are numbered 1..dn/2. Each vertex contributes 2^(d-1) clauses over its d edge
variables; each edge occurs in 2*2^(d-1) clauses, with each sign in exactly half.
Clause line = literals separated by spaces + " 0\n". Header "p cnf V C\n".
The byte count does not depend on graph structure, only on (n, d).
Runs in well under a second; no chunking needed."""
import json, math, sys

def dimacs_bytes(n, d):
    V = d * n // 2; C = (2 ** (d - 1)) * n
    occ = 2 * 2 ** (d - 1)                     # occurrences of each edge variable
    lit = sum(occ * len(str(e)) + (occ // 2) for e in range(1, V + 1))  # digits + '-' signs
    sep = C * (d - 1 + 3)                       # spaces between literals + " 0\n"
    header = len(f"p cnf {V} {C}\n")
    return header + lit + sep

def main():
    rows = []
    for d in (3, 8):
        for n in (10**2, 10**3, 10**4, 10**5, 10**6):
            if d * n % 2:
                continue
            B = 8 * dimacs_bytes(n, d)              # bits
            rows.append({"d": d, "n": n, "N_bits": B, "n_over_N_div_log2N": n / (B / math.log2(B))})
    for r in rows:
        print(r)
    if len(sys.argv) > 1:
        json.dump(rows, open(sys.argv[1], "w"), indent=1)

if __name__ == "__main__":
    main()

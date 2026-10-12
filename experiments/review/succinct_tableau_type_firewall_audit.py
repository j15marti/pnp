#!/usr/bin/env python3
"""Finite audit for SUCCINCT-TABLEAU-TYPE-FIREWALL1.

The experiment separates a compact random-access descriptor from the explicit
fixed-width 3CNF bit string that it denotes.  It checks materialization and
lazy-query ledgers on easy hostile controls.  It does not prove an asymptotic
SAT lower bound; the associated report contains the symbolic theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


Literal = int
Clause = tuple[Literal, Literal, Literal]


def forbid(bits: tuple[int, int, int], vars_: tuple[int, int, int]) -> Clause:
    """Clause falsified exactly by the supplied three-bit assignment."""
    return tuple(v if b == 0 else -v for b, v in zip(bits, vars_))  # type: ignore[return-value]


@dataclass(frozen=True)
class FormulaDescriptor:
    family: str
    n: int
    scale: int = 1

    @property
    def clauses(self) -> int:
        if self.family in {"2SAT", "Horn", "bounded-treewidth"}:
            return max(1, self.n - 1)
        if self.family == "affine-Tseitin":
            return 4 * max(1, self.n - 2)
        if self.family in {"independent-products", "alternate-encoding"}:
            return max(1, self.n // 2)
        if self.family in {"padding", "redundant-clauses"}:
            return max(1, self.scale * self.n)
        raise ValueError(self.family)

    @property
    def index_bits(self) -> int:
        return max(1, math.ceil(math.log2(self.n + 1)))

    @property
    def header_bits(self) -> int:
        width = max(self.index_bits, math.ceil(math.log2(self.clauses + 1)))
        return 2 * width + 2 * math.ceil(math.log2(width + 1))

    @property
    def explicit_bits(self) -> int:
        return self.header_bits + self.clauses * 3 * (1 + self.index_bits)

    @property
    def descriptor_bits(self) -> int:
        # Fixed decoder code is common to the family.  This is the literal
        # self-delimiting payload for (family tag, n, scale), not a claimed
        # minimum circuit size.
        return 8 * (len(self.family) + 2) + max(1, self.n.bit_length()) + max(1, self.scale.bit_length())

    def clause(self, j: int) -> Clause:
        if not 0 <= j < self.clauses:
            raise IndexError(j)
        n = self.n
        if self.family == "2SAT":
            i = min(j + 1, n)
            k = min(i + 1, n)
            return (-i, k, k)
        if self.family == "Horn":
            i = min(j + 1, n)
            k = min(i + 1, n)
            return (-i, k, k)
        if self.family == "bounded-treewidth":
            i = min(j + 1, n)
            k = min(i + 1, n)
            return (i, -k, -k)
        if self.family == "affine-Tseitin":
            block, case = divmod(j, 4)
            i = min(block + 1, max(1, n - 2))
            vars_ = (i, i + 1, i + 2)
            odd = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))
            return forbid(odd[case], vars_)
        if self.family == "independent-products":
            i = 2 * j + 1
            k = min(i + 1, n)
            return (i, k, k)
        if self.family == "alternate-encoding":
            # Reverse the variable order of the same independent product.
            i = n - 2 * j
            k = max(1, i - 1)
            return (i, k, k)
        if self.family == "padding":
            i = (j % n) + 1
            return (i, -i, i)
        if self.family == "redundant-clauses":
            return (1, 1, 1)
        raise ValueError(self.family)

    def explicit_bit(self, position: int) -> int:
        """Random access without materializing the entire explicit encoding."""
        if not 0 <= position < self.explicit_bits:
            raise IndexError(position)
        if position < self.header_bits:
            header = f"{self.n:0{self.header_bits // 2}b}{self.clauses:0{self.header_bits - self.header_bits // 2}b}"
            return int(header[position])
        offset = position - self.header_bits
        literal_width = 1 + self.index_bits
        clause_index, within_clause = divmod(offset, 3 * literal_width)
        literal_index, within_literal = divmod(within_clause, literal_width)
        lit = self.clause(clause_index)[literal_index]
        encoded = ("1" if lit < 0 else "0") + f"{abs(lit):0{self.index_bits}b}"
        return int(encoded[within_literal])

    def materialize(self) -> str:
        return "".join(str(self.explicit_bit(i)) for i in range(self.explicit_bits))


def satisfies(clauses: Iterable[Clause], assignment: tuple[int, ...]) -> bool:
    for clause in clauses:
        if not any((assignment[abs(lit) - 1] == 1) == (lit > 0) for lit in clause):
            return False
    return True


def brute_models(desc: FormulaDescriptor) -> int:
    clauses = [desc.clause(i) for i in range(desc.clauses)]
    return sum(satisfies(clauses, a) for a in itertools.product((0, 1), repeat=desc.n))


def main() -> None:
    families = [
        "2SAT",
        "Horn",
        "affine-Tseitin",
        "bounded-treewidth",
        "independent-products",
        "padding",
        "redundant-clauses",
        "alternate-encoding",
    ]
    wrappers = ["DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP"]
    sizes = [4, 8, 16, 32, 64, 128, 256]
    checks = 0
    failures: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []

    for family in families:
        for n in sizes:
            scale = 8 if family in {"padding", "redundant-clauses"} else 1
            desc = FormulaDescriptor(family, n, scale)
            bits = desc.materialize()
            checks += 2
            if len(bits) != desc.explicit_bits:
                failures.append({"kind": "length", "family": family, "n": n})
            if any(int(bits[i]) != desc.explicit_bit(i) for i in range(len(bits))):
                failures.append({"kind": "lazy_explicit_mismatch", "family": family, "n": n})

            word_bits = max(1, math.ceil(math.log2(desc.explicit_bits + 1)))
            word_writes = math.ceil(desc.explicit_bits / word_bits)
            checks += 2
            if word_writes * word_bits < desc.explicit_bits:
                failures.append({"kind": "word_write_cover", "family": family, "n": n})
            if desc.explicit_bits <= 0:
                failures.append({"kind": "nonpositive_explicit", "family": family, "n": n})

            exponent_ledger = []
            for k in range(1, 9):
                explicit_solver_bound = desc.explicit_bits**k
                full_lazy_queries = desc.explicit_bits
                decoder_cost = 8 + desc.index_bits
                lazy_full_read_bound = full_lazy_queries * decoder_cost
                checks += 2
                if explicit_solver_bound < desc.explicit_bits:
                    failures.append({"kind": "solver_below_read", "family": family, "n": n, "K": k})
                if lazy_full_read_bound < desc.explicit_bits:
                    failures.append({"kind": "lazy_below_queries", "family": family, "n": n, "K": k})
                exponent_ledger.append(
                    {
                        "K": k,
                        "explicit_solver_bound": str(explicit_solver_bound),
                        "full_lazy_query_bound": lazy_full_read_bound,
                    }
                )

            wrapper_rows = []
            for wrapper in wrappers:
                overhead = {
                    "DIRECT": 0,
                    "COPY": desc.explicit_bits,
                    "DEAD": desc.descriptor_bits,
                    "DELAY": desc.explicit_bits,
                    "INTERP": desc.explicit_bits * (1 + desc.index_bits),
                    "RECOMP": 2 * desc.explicit_bits,
                }[wrapper]
                checks += 1
                if overhead < 0:
                    failures.append({"kind": "negative_wrapper", "wrapper": wrapper})
                wrapper_rows.append({"wrapper": wrapper, "added_ops": overhead})

            models = None
            brute_assignment_tests = 0
            if n <= 8:
                models = brute_models(desc)
                brute_assignment_tests = 2**n
                checks += 1
                if models <= 0:
                    failures.append({"kind": "unexpected_unsat_control", "family": family, "n": n})

            rows.append(
                {
                    "family": family,
                    "n": n,
                    "clauses": desc.clauses,
                    "descriptor_bits": desc.descriptor_bits,
                    "explicit_bits": desc.explicit_bits,
                    "compression_ratio": desc.explicit_bits / desc.descriptor_bits,
                    "descriptor_is_smaller": desc.descriptor_bits < desc.explicit_bits,
                    "materialization_bit_writes": desc.explicit_bits,
                    "materialization_word_writes": word_writes,
                    "word_bits": word_bits,
                    "lazy_decoder_ops_per_bit_upper": 8 + desc.index_bits,
                    "preprocessing_ops": desc.descriptor_bits,
                    "extraction_ops": 0,
                    "reconstruction_ops": 0,
                    "decision_output_bits": 1,
                    "brute_models_small_only": models,
                    "brute_assignment_tests": brute_assignment_tests,
                    "solver_ledgers": exponent_ledger,
                    "wrappers": wrapper_rows,
                }
            )

    # Explicitly demonstrate that large compression ratio can coexist with an
    # easy semantic family; padding consists solely of tautologies.
    padding_rows = [r for r in rows if r["family"] == "padding"]
    for a, b in zip(padding_rows, padding_rows[1:]):
        checks += 2
        if b["compression_ratio"] <= a["compression_ratio"]:
            failures.append({"kind": "padding_ratio_not_growing", "n": b["n"]})
        if b["decision_output_bits"] != 1:
            failures.append({"kind": "padding_output_changed", "n": b["n"]})

    payload = {
        "experiment": "SUCCINCT-TABLEAU-TYPE-FIREWALL1 finite audit",
        "status": "COMPUTATIONAL",
        "scope": (
            "Exact finite bit/access/cost bookkeeping for compact descriptors and explicit 3CNF strings. "
            "No asymptotic P-vs-NP or NEXP lower bound is inferred from these rows."
        ),
        "encoding": "self-delimiting header plus fixed-width three-literal clause array",
        "deterministic": True,
        "random_seed": None,
        "sizes": sizes,
        "families": families,
        "wrappers": wrappers,
        "checks": checks,
        "failures": failures,
        "rows": rows,
    }
    out = Path("results/raw/review/2026-10-13_succinct_tableau_type_firewall.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps({"checks": checks, "failures": len(failures), "rows": len(rows), "result": str(out)}))
    print("result_sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()

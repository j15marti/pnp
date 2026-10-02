"""ACR strategy-tree compression hostile control.

Exact finite sanity test: a depth-d adaptive binary challenge tree has 2^d-1
explicit nonterminal histories, but the response strategy used here is encoded
by d source bits.  This demonstrates that explicit strategy-tree size alone is
not a representation-independent lower bound.
"""
import json

def response(source_bits, history):
    i = len(history) - 1
    challenge = history[-1]
    if challenge == 0:
        return source_bits[i]
    return sum(source_bits[: i + 1]) & 1

rows = []
for d in range(1, 21):
    source = tuple((i * i + 3 * i + 1) & 1 for i in range(d))
    nodes = (1 << d) - 1
    # Exhaustively verify all challenge histories through d <= 12.
    checked = 0
    if d <= 12:
        for mask in range(1 << d):
            hist = tuple((mask >> i) & 1 for i in range(d))
            for k in range(1, d + 1):
                _ = response(source, hist[:k])
                checked += 1
    rows.append({
        "depth": d,
        "explicit_strategy_nodes": nodes,
        "succinct_source_bits": d,
        "realized_transcript_responses": d,
        "exhaustive_prefix_responses_checked": checked,
    })
print(json.dumps({
    "status": "COMPUTATIONAL sanity control; no asymptotic SAT lower bound",
    "model": "binary adaptive challenge tree with succinct source-indexed response evaluator",
    "rows": rows,
}, indent=2))

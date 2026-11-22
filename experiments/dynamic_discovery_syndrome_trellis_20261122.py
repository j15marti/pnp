"""Cycle decision with suffix-span pruning. Standard-library semantic audit."""
from itertools import combinations, product
import json


def remainder(value, pivots):
    for index in sorted(pivots, reverse=True):
        if value >> index & 1:
            value ^= pivots[index]
    return value


def basis(values):
    pivots = {}
    for value in values:
        value = remainder(value, pivots)
        if value:
            pivots[value.bit_length()-1] = value
    return pivots


def solve(top, bottom, rows):
    t = len(top)
    columns = [sum(1 << j for j, row in enumerate(rows) if i in row) for i in range(t)]
    full_rank = len(basis(columns))
    live = {(0,0,0), (1,1,0)}
    widths = []
    peak = len(live)
    for i, column in enumerate(columns):
        suffix = basis(columns[i+1:])
        width = len(basis(columns[:i+1])) + len(suffix) - full_rank
        widths.append(width)
        following = set()
        for start, x, syndrome in live:
            new = syndrome ^ (column if x else 0)
            if remainder(new, suffix):
                continue
            for y in range(2):
                if all((x >= y if link == "A" else x != y) for link in (top[i],bottom[i])):
                    following.add((start,y,new))
        live = following
        assert len(live) <= 4 * (1 << width)
        peak = max(peak,len(live))
    return any(start == y and new == 0 for start,y,new in live), max(widths), peak


def oracle(top, bottom, rows):
    for z in product(range(2),repeat=len(top)):
        if any(sum(z[i] for i in row)%2 for row in rows):
            continue
        for i, (a,b) in enumerate(zip(top,bottom)):
            x,y = z[i],z[(i+1)%len(z)]
            if ("A" in (a,b) and (x,y)==(0,1)) or ("C" in (a,b) and x==y):
                break
        else:
            return True
    return False


def main():
    pool = list(combinations(range(4),3))
    cases = sat = 0
    for mask in range(16):
        rows = [r for j,r in enumerate(pool) if mask >> j & 1]
        for words in product("AC",repeat=8):
            a,b = words[:4],words[4:]
            label,_,_ = solve(a,b,rows)
            assert label == oracle(a,b,rows)
            cases += 1
            sat += label
    controls = []
    for q in (1,3,9):
        t = 3*q
        for layout in ("local","spread","shared"):
            rows = ([(3*i,3*i+1,3*i+2) for i in range(q)] if layout=="local" else
                    [(i,i+q,i+2*q) for i in range(q)] if layout=="spread" else
                    [(0,1,2)]*q)
            for link in "AC":
                label,width,peak = solve(link*t,link*t,rows)
                assert label == (link=="A") and width == (q if layout=="spread" else 1)
                controls.append([q,layout,link,width,peak,label])
    print(json.dumps(dict(exhaustive_cases=cases,sat=sat,unsat=cases-sat,
                          controls_q_layout_link_width_peak_sat=controls),indent=2))


if __name__ == "__main__":
    main()

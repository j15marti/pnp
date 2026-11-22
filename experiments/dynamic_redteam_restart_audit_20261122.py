"""Finite read-before-write audit; not a full SAT solver or TM complexity benchmark."""
import hashlib
import itertools
import json
from pathlib import Path

BLANK = "_"
TABLE = {}
for p in "01":
    TABLE["START", p] = ("S" + p, BLANK, 1)
    for q in "01":
        TABLE["S" + p, q] = ("W" + str(int(p) | int(q)), BLANK, -1)
for d in "01":
    TABLE["W" + d, BLANK] = ("READY", d, 0)
    TABLE["READY", d] = ("OUT", d, 1)
TABLE["OUT", BLANK] = ("HALT", "#", 0)


def span(tape, head):
    points = [0, head] + [i for i, s in tape.items() if s != BLANK]
    return max(points) - min(points) + 1


def execute(bits):
    tape = dict(enumerate(bits))
    state, head, seen = "START", 0, set()
    trace, record, events, spans = [], [], [], []
    while state != "HALT":
        symbol = tape.get(head, BLANK)
        t = len(trace) + 1
        first = head in (0, 1) and head not in seen
        if first:
            record.append(symbol)
            events.append(t)
        seen.add(head)
        spans.append(span(tape, head))
        ns, write, move = TABLE[state, symbol]
        trace.append(dict(t=t, state=state, head=head, read=symbol,
                          write=write, move=move, next=ns, first_original=first))
        tape[head] = write
        head += move
        state = ns
    return dict(input=bits, decision=int(tape[0]), output=tape[0] + tape[1],
                trace=trace, record="".join(record), events=events,
                suffix_original_first_events=[t for t in events if t > 3],
                phase_record=trace[3]["read"], phase_events=[4],
                T=len(trace), peak_cell_span=max(spans + [span(tape, head)]),
                pretransition_cell_spans=spans, cell_CM=sum(spans),
                suffix_T=2, suffix_cell_CM=sum(spans[3:]))


def replay(record, unknown, state="START"):
    """No sampled tape is supplied. Unknown checkpoint cells are read from record."""
    tape, head, consumed, trace = {}, 0, 0, []
    while state != "HALT":
        if head not in tape:
            if head in unknown:
                if consumed == len(record):
                    raise ValueError("missing checkpoint symbol")
                tape[head] = record[consumed]
                consumed += 1
            else:
                tape[head] = BLANK
        symbol = tape[head]
        ns, write, move = TABLE[state, symbol]
        trace.append((state, head, symbol, write, move, ns))
        tape[head] = write
        head += move
        state = ns
    assert consumed == len(record)
    return tape[0] + tape[1], trace


def main():
    rows = [execute("".join(p)) for p in itertools.product("01", repeat=2)]
    for row in rows:
        assert row["decision"] == (int(row["input"][0]) | int(row["input"][1]))
        out, trace = replay(row["record"], {0, 1})
        assert out == row["output"]
        assert trace == [(r["state"], r["head"], r["read"], r["write"],
                          r["move"], r["next"]) for r in row["trace"]]
        out, _ = replay(row["phase_record"], {0}, state="READY")
        assert out == row["output"]
        assert row["suffix_original_first_events"] == []
        assert (row["T"], row["peak_cell_span"], row["cell_CM"]) == (5, 2, 8)
    codes = [r["record"] for r in rows]
    assert not any(a != b and b.startswith(a) for a in codes for b in codes)
    try:
        replay("", {0}, state="READY")
    except ValueError:
        missing_checkpoint_detected = True
    else:
        raise AssertionError("empty late transcript unexpectedly decoded")
    raw = dict(scope="Four-input OR transition control; full SAT prefix not executed",
               machine_table=[dict(state=s, read=a, next=v[0], write=v[1], move=v[2])
                              for (s, a), v in sorted(TABLE.items())],
               script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               cases=rows, missing_checkpoint_detected=missing_checkpoint_detected,
               equal_probability_collision=dict(inputs=["00", "10"], outputs=["0#", "1#"],
                    suffix_original_first_records=["", ""], H_decision_bits=1,
                    corrected_phase_records=["0", "1"]),
               checks="PASS: initial replay, phase replay, prefix freedom, omitted-state failure",
               accounting="Cell span excludes fixed finite control; no Kolmogorov complexity measured")
    output = Path(__file__).resolve().parents[1] / "results/raw/dynamic_redteam_restart_audit_20261122.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(raw, indent=2) + "\n")
    print(json.dumps(dict(cases=len(rows), checks=raw["checks"],
                          script_sha256=raw["script_sha256"], output=str(output))))


if __name__ == "__main__":
    main()

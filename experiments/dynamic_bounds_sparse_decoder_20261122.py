"""Finite one-tape suffix and decoder audit. No external dependencies."""
import json

def step(state, head, symbol):
    selected = False
    if state == "cache":
        assert symbol in "01"
        return ("select0" if symbol == "0" else "delay"), symbol, 1, selected
    if state == "delay":
        return "select1", symbol, 1, selected
    if state.startswith("select"):
        return "back" + state[-1], symbol, -1, True
    if state.startswith("back"):
        if symbol == "#":
            return "term", state[-1], 1, selected
        return state, symbol, -1, selected
    assert state == "term"
    return "halt", "!", 0, selected


def execute(bit):
    tape = {0: "#", 3: str(bit), 4: "0", 5: "0"}
    state, head, trace = "cache", 3, []
    while state != "halt":
        old = tape.get(head, "_")
        new_state, written, move, selected = step(state, head, old)
        trace.append(dict(time=len(trace)+1, address=head, read=old, selected=selected))
        tape[head] = written
        head += move
        state = new_state
    assert tape[0] == str(bit) and tape[1] == "!"
    return trace


def decode(reads):
    state, head = "cache", 3
    output = {0: "#", 1: "_"}
    consumed = 0
    for symbol in reads:
        assert state != "halt"
        state, written, move, _ = step(state, head, symbol)
        if head in output:
            output[head] = written
        head += move
        consumed += 1
    assert state == "halt"
    return output[0], consumed


if __name__ == "__main__":
    runs = []
    for bit in (0,1):
        trace = execute(bit)
        reads = "".join(e["read"] for e in trace)
        projected = "".join(e["read"] for e in trace if e["selected"])
        event = next(e for e in trace if e["selected"])
        assert decode(reads) == (str(bit), len(trace))
        assert projected == "0"
        assert event["time"] == bit+2 and event["address"] == bit+4
        runs.append(dict(answer=bit, full_record=reads, projected_record=projected,
                         selected_time=event["time"], selected_address=event["address"],
                         steps=len(trace), trace=trace))
    a,b = [r["full_record"] for r in runs]
    assert not a.startswith(b) and not b.startswith(a)
    assert runs[0]["projected_record"] == runs[1]["projected_record"]
    print(json.dumps(dict(status="COMPUTATIONAL", runs=runs,
                          fair_answer_entropy=1, projected_entropy=0,
                          fair_answer_entropy_given_projection=1,
                          metadata_bit_entropy=1), indent=2))

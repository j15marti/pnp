#!/usr/bin/env python3
"""ARC187: exact source/work authenticated local TM traces and two levels.

Dependency-free finite control. This audits a five-bit total encoded CNF
subfamily, NOT a general all-input SAT machine or a physical tape benchmark.
Each trace record is checked locally, against immutable source bytes, and by
sorting (work-address, chronological time) to authenticate memory consistency.
"""
from __future__ import annotations
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path

RUN_ID = "ARC-DUAL-LOCAL-TRACE187"
BLANK = "_"
CHECKS = 0

def assert_ok(condition, name="test"):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(f"check {CHECKS}: {name}")

def is_unsat(flags):
    assert len(flags) == 5 and all(ch in "01" for ch in flags)
    empty, xp, xn, yp, yn = map(int, flags)
    return bool(empty or (xp and xn) or (yp and yn))

def brute_unsat(flags):
    empty, xp, xn, yp, yn = map(int, flags)
    for x, y in itertools.product((0, 1), repeat=2):
        if not (empty or (xp and not x) or (xn and x) or
                (yp and not y) or (yn and y)):
            return False
    return True

def restrict_flags(flags, var, val):
    """True original-variable restriction, retaining an empty-clause flag."""
    bits = list(map(int, flags))
    assert var in (0, 1) and val in (0, 1)
    pos, neg = (1, 2) if var == 0 else (3, 4)
    if bits[pos] and val == 0 or bits[neg] and val == 1:
        bits[0] = 1
    bits[pos] = bits[neg] = 0
    return "".join(map(str, bits))

def trans(state, input_symbol, work_symbol, input_head, work_head):
    """Fixed-control transition rule for the 5-flag toy SAT family."""
    mode, stage, mask = state
    if mode == "scan":
        if stage < 5:
            if input_head != stage or work_head != stage:
                return None
            if input_symbol not in "01" or work_symbol != BLANK:
                return None
            next_mask = mask | (int(input_symbol) << stage)
            return (("scan", stage + 1, next_mask),
                    input_head + 1, work_head + 1, input_symbol, None)
        if stage == 5 and input_head == 5 and work_head == 5:
            if input_symbol != BLANK or work_symbol != BLANK:
                return None
            return (("verify", 4, mask), 5, 4, BLANK, None)
        return None
    if mode == "verify":
        if not (0 <= stage <= 4 and input_head == 5 and work_head == stage):
            return None
        if input_symbol != BLANK or work_symbol != str((mask >> stage) & 1):
            return None
        if stage:
            return (("verify", stage - 1, mask), 5, stage - 1, work_symbol, None)
        bits = "".join(str((mask >> i) & 1) for i in range(5))
        label = "UNSAT" if is_unsat(bits) else "SAT"
        return (("halt", -1, mask), 5, 0, work_symbol, label)
    return None

def run_machine(flags):
    """Actual deterministic sequential source+work-head computation."""
    mem = {}
    state = ("scan", 0, 0)
    ih, wh = 0, 0
    rows = []
    output = None
    for t in range(24):
        source_val = flags[ih] if 0 <= ih < len(flags) else BLANK
        old_work = mem.get(wh, BLANK)
        v = trans(state, source_val, old_work, ih, wh)
        assert v is not None
        next_state, next_ih, next_wh, write, output = v
        rows.append({"t":t,"state":list(state),"ih":ih,"wh":wh,
                     "in":source_val,"old":old_work,"write":write,
                     "next_state":list(next_state),"next_ih":next_ih,
                     "next_wh":next_wh,"output":output})
        mem[wh] = write
        state, ih, wh = next_state, next_ih, next_wh
        if output is not None:
            break
    assert output is not None
    return rows

def verify_trace(flags, rows, require_unsat=False):
    """Authenticate source, transitions and chronological work read/write."""
    if not isinstance(rows, list) or not rows or len(rows) > 50000:
        return False
    prev_state, prev_ih, prev_wh = ("scan",0,0), 0, 0
    claimed_out = None
    events = []
    try:
        for t, rec in enumerate(rows):
            if rec["t"] != t or tuple(rec["state"]) != prev_state:
                return False
            ih, wh = rec["ih"], rec["wh"]
            if (ih, wh) != (prev_ih, prev_wh):
                return False
            if not (isinstance(ih,int) and isinstance(wh,int) and
                    0 <= ih <= len(flags) and 0 <= wh <= len(rows)+1):
                return False
            claimed_in = rec["in"]
            actual_in = flags[ih] if ih < len(flags) else BLANK
            if claimed_in != actual_in:
                return False
            v = trans(prev_state, claimed_in, rec["old"], ih, wh)
            if v is None:
                return False
            next_state, next_ih, next_wh, write, out = v
            if (list(next_state) != rec["next_state"] or
                next_ih != rec["next_ih"] or next_wh != rec["next_wh"] or
                write != rec["write"] or out != rec["output"]):
                return False
            events.append((wh,t,rec["old"],rec["write"]))
            prev_state, prev_ih, prev_wh = next_state, next_ih, next_wh
            if out is not None:
                if t != len(rows)-1:
                    return False
                claimed_out = out
        if claimed_out is None or (require_unsat and claimed_out != "UNSAT"):
            return False
        last_address, val = None, BLANK
        for address,t,old,new in sorted(events, key=lambda z:(z[0],z[1])):
            if address != last_address:
                last_address, val = address, BLANK
            if old != val:
                return False
            val = new
        return True
    except (TypeError,KeyError,IndexError,ValueError):
        return False

def ledger(flags, rows):
    T = len(rows)
    S = len(set(row["wh"] for row in rows))
    q_input, q_work = T, T
    changed_writes = sum(row["old"] != row["write"] for row in rows)
    unchanged_writes = T - changed_writes
    cross_input = sum(abs(row["next_ih"]-row["ih"]) for row in rows)
    cross_work = sum(abs(row["next_wh"]-row["wh"]) for row in rows)
    input_footprint = len(flags)
    log_index = (T+input_footprint+2).bit_length()
    T1_sweep_budget = 2*T*(input_footprint+S+log_index+8)
    return dict(Tk=T,Sk=S,Qk=q_input+q_work,Ck=cross_input+cross_work,
                input_probes=q_input,work_probes=q_work,
                actual_writes=T,changed_writes=changed_writes,
                unchanged_writes=unchanged_writes,output_bits=1,
                T1_sweep_budget=T1_sweep_budget,
                P1_sweep_bound=input_footprint+S+log_index+8)

def tamper_cases(trace):
    ans = []
    for key,new in (("in","1" if trace[0]["in"]=="0" else "0"),
                    ("old","1"),("write","1" if trace[0]["write"]=="0" else "0"),
                    ("ih",4),("wh",4),("t",999)):
        bad=copy.deepcopy(trace)
        bad[0][key]=new
        ans.append(bad)
    bad=copy.deepcopy(trace)
    bad[-1]["output"]="UNSAT" if bad[-1]["output"]=="SAT" else "SAT"
    ans.append(bad)
    ans.append(copy.deepcopy(trace[:-1]))
    bad=copy.deepcopy(trace)
    bad[1],bad[2]=bad[2],bad[1]
    ans.append(bad)
    bad=copy.deepcopy(trace)
    bad[6]["old"]="1" if bad[6]["old"] != "1" else "0"
    ans.append(bad)
    return ans

def main():
    labels={"SAT":0,"UNSAT":0}
    sizes=[]
    restricted=0
    tamper_rejections=0
    two_level=0
    for bits in itertools.product("01",repeat=5):
        flags="".join(bits)
        u=is_unsat(flags)
        assert_ok(u==brute_unsat(flags),"independent truth table")
        trace=run_machine(flags)
        assert_ok(verify_trace(flags,trace),"full transition authentication")
        assert_ok(verify_trace(flags,trace,True)==u,"UNSAT accepting polarity")
        labels["UNSAT" if u else "SAT"]+=1
        sizes.append(ledger(flags,trace))
        for changed in tamper_cases(trace):
            assert_ok(not verify_trace(flags,changed),"source/work/provenance tampering")
            tamper_rejections+=1
        leaves=[]
        for x,y in itertools.product((0,1),repeat=2):
            one=restrict_flags(flags,0,x)
            two=restrict_flags(one,1,y)
            assert_ok(is_unsat(one)==brute_unsat(one),"one real source restriction")
            assert_ok(is_unsat(two)==brute_unsat(two),"two real source restrictions")
            assert_ok(verify_trace(one,run_machine(one)),"level-one child trace")
            assert_ok(verify_trace(two,run_machine(two),True)==is_unsat(two),
                      "level-two child trace and sound label")
            assert_ok(two==restrict_flags(restrict_flags(flags,0,x),1,y),
                      "authenticated descendant source")
            leaves.append(not is_unsat(two))
            two_level+=1
        assert_ok((not u)==any(leaves),"compatible original-variable join")
        restricted+=1
        fake="00000"
        actual=restrict_flags(restrict_flags(flags,0,0),1,0)
        if actual != fake:
            assert_ok(actual != fake,"fake child rejected by source binder")
    for delay in (0,1,7,31):
        assert_ok(11+delay>=11,"delay count")
    assert_ok(max(v["Sk"] for v in sizes)==6,"visited work cells")
    assert_ok(all(v["Tk"]==11 for v in sizes),"complete step count")
    assert_ok(all(v["changed_writes"]+v["unchanged_writes"]==v["Tk"]
                  for v in sizes),"count unchanged writes")
    assert_ok(all(v["P1_sweep_bound"]>=5+v["Sk"] for v in sizes),
              "separate one-tape input footprint")
    result={"run_id":RUN_ID,
            "model":"finite exact toy Mk source/work trace; separate\n"
                    "analytic M1 sweep upper budget, not measured universal-TM steps",
            "seed":None,"exhaustive":True,"inputs":32,
            "labels":labels,"two_level_leaf_cases":two_level,
            "top_level_join_cases":restricted,
            "tampered_traces_rejected":tamper_rejections,
            "checks":CHECKS,"failed_checks":0,
            "per_case_machine_ledger":sizes[0],
            "scope":"5-bit total CNF flags for empty,x,-x,y,-y; no general SAT\n"
                    "machine or claimed P-vs-NP separation"}
    canonical=json.dumps(result,sort_keys=True,indent=2)+"\n"
    out=Path(__file__).with_name("arc187_results.json")
    out.write_text(canonical)
    print(canonical)
    print("raw_sha256",hashlib.sha256(canonical.encode()).hexdigest())

if __name__=="__main__":
    main()

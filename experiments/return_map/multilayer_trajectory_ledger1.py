"""Multilayer trajectory ledger prototype.

Status: COMPUTATIONAL. Finite accounting experiment only.
Tracks source support, live boundary, representation, derivational history,
and acquire/combine/forget/reacquire accounting across exact mechanisms.
No runtime lower bound is inferred from these coordinates.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class Event:
    step: int
    alg: str
    op: str
    rep: str
    source_support: int
    boundary: int
    rep_width: int
    history: int
    acquire: int
    combine: int
    forget: int
    reacquire: int
    answer_known: bool


def trajectory_summary(events):
    return {
        "steps": len(events),
        "max_source_support": max(e.source_support for e in events),
        "max_boundary": max(e.boundary for e in events),
        "max_rep_width": max(e.rep_width for e in events),
        "max_history": max(e.history for e in events),
        "total_acquire": sum(e.acquire for e in events),
        "total_combine": sum(e.combine for e in events),
        "total_forget": sum(e.forget for e in events),
        "total_reacquire": sum(e.reacquire for e in events),
        "first_global_support_step": next(
            (e.step for e in events if e.source_support == 4), None
        ),
        "first_answer_step": next(
            (e.step for e in events if e.answer_known), None
        ),
    }


def make_trajectories():
    T = {}
    T["DPLL"] = [
        Event(0,"DPLL","READ","CNF",1,3,3,0,1,0,0,0,False),
        Event(1,"DPLL","READ","CNF",2,4,4,0,1,0,0,0,False),
        Event(2,"DPLL","BRANCH","CNF",2,3,4,1,0,1,0,0,False),
        Event(3,"DPLL","UNIT_PROP","CNF",3,2,3,2,0,1,0,0,False),
        Event(4,"DPLL","READ","CNF",4,2,3,2,1,0,0,0,False),
        Event(5,"DPLL","COMBINE_BRANCHES","BOOL",4,1,1,1,0,2,1,0,True),
    ]
    T["RESOLUTION"] = [
        Event(0,"RESOLUTION","SOURCE","CNF",1,3,3,0,0,0,0,0,False),
        Event(1,"RESOLUTION","RESOLVE","CNF",2,3,2,2,0,1,0,0,False),
        Event(2,"RESOLUTION","RESOLVE","CNF",2,3,2,2,0,1,0,0,False),
        Event(3,"RESOLUTION","RESOLVE","CNF",4,1,1,6,0,1,0,0,True),
    ]
    T["2SAT_SCC"] = [
        Event(0,"2SAT_SCC","PARSE","CNF",1,2,2,0,1,0,0,0,False),
        Event(1,"2SAT_SCC","BUILD_IMPLICATIONS","IMPL_GRAPH",4,5,10,0,3,4,0,0,False),
        Event(2,"2SAT_SCC","SCC","SCC_DAG",4,2,5,0,0,5,5,0,True),
    ]
    T["HORN"] = [
        Event(0,"HORN","FACTS","HORN_RULESET",1,1,1,0,1,0,0,0,False),
        Event(1,"HORN","FIRE_RULE","HORN_RULESET",2,2,2,1,0,1,0,0,False),
        Event(2,"HORN","FIRE_RULE","HORN_RULESET",3,2,2,2,0,1,0,0,False),
        Event(3,"HORN","GOAL_CHECK","BOOL",4,1,1,0,0,1,2,0,True),
    ]
    T["GAUSSIAN"] = [
        Event(0,"GAUSSIAN","PARSE","GF2",1,3,5,0,1,0,0,0,False),
        Event(1,"GAUSSIAN","ROW_ADD","GF2",2,2,5,0,0,1,2,0,False),
        Event(2,"GAUSSIAN","ROW_ADD","GF2",4,1,5,0,0,1,2,0,False),
        Event(3,"GAUSSIAN","RANK_CHECK","BOOL",4,1,1,0,0,1,1,0,True),
    ]
    T["SEP_DP"] = [
        Event(0,"SEP_DP","DECOMPOSE","TREE_DECOMP",1,2,2,0,2,0,0,0,False),
        Event(1,"SEP_DP","BAG_TABLE","TABLE",2,2,4,0,0,1,2,0,False),
        Event(2,"SEP_DP","BAG_TABLE","TABLE",2,2,4,0,0,1,2,0,False),
        Event(3,"SEP_DP","JOIN","TABLE",4,2,4,0,0,2,2,0,False),
        Event(4,"SEP_DP","ROOT_DECIDE","BOOL",4,0,1,0,0,1,3,0,True),
    ]
    return T


if __name__ == "__main__":
    trajectories = make_trajectories()
    output = {
        "status": "COMPUTATIONAL",
        "warning": "Finite accounting trajectories are not asymptotic lower bounds.",
        "summaries": {k: trajectory_summary(v) for k, v in trajectories.items()},
        "events": {k: [asdict(e) for e in v] for k, v in trajectories.items()},
    }
    print(json.dumps(output, indent=2, sort_keys=True))

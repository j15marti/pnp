#!/usr/bin/env python3
"""LSPV-2 UTM-CROSS-WRITE-COUNTER175. Python3 stdlib; reproducible finite checks.

Two model variants: INITMARK (permanent *initial* origin marker, D=0),
WRITEONE (initially blank origin; write exactly one marker, D=1).
This is an explicit finite-control two-way-input/one-unary-work-head algorithm
for a ZONE-TAGGED DISJ promise, not a full ordinary-SAT algorithm.
"""
import argparse
import itertools
import json
from collections import Counter

W1 = (
    (-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
    (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
    (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
    (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
    (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14),
)
A_SLOTS = ((6, 0), (11, 0))
B_SLOTS = ((17, 2), (9, 2))
A_INDEX = tuple(sorted({c for c, _ in A_SLOTS}))
B_INDEX = tuple(sorted({c for c, _ in B_SLOTS}))
FIXED_INDEX = tuple(i for i in range(20) if i not in A_INDEX and i not in B_INDEX)
MARK = '@'
class BadInput(Exception):
    pass
MAGIC = '10100110111100000011110010101010'


def gadget(a, b):
    result = [list(c) for c in W1]
    if not a:
        for c, j in A_SLOTS:
            result[c][j] *= -1
    if not b:
        for c, j in B_SLOTS:
            result[c][j] *= -1
    return tuple(tuple(row) for row in result)


def satisfies(clauses, mask):
    return all(any(bool((mask >> (abs(l) - 1)) & 1) == (l > 0)
                   for l in clause) for clause in clauses)


def proper_22(clauses, n):
    pos, neg = Counter(), Counter()
    seen = set()
    for c in clauses:
        if len(c) != 3 or len(set(map(abs, c))) != 3 or c in seen:
            return False
        seen.add(c)
        for v in c:
            (pos if v > 0 else neg)[abs(v)] += 1
    return all(pos[v] == neg[v] == 2 for v in range(1, n + 1))


def fixed_binary(m, a, b):
    assert m >= 1 and len(a) == len(b) == m
    w = (20*m).bit_length()
    modules = [gadget(a[i], b[i]) for i in range(m)]
    clauses = []
    for ix in (A_INDEX, FIXED_INDEX, B_INDEX):
        for i, mod in enumerate(modules):
            clauses += [tuple((abs(l) + 15*i) * (1 if l > 0 else -1)
                              for l in mod[k]) for k in ix]
    # Fixed-width three-field header and 3 fixed-width literals per row.
    header = MAGIC + ''.join(format(v, f'0{w}b') for v in (15*m, 20*m, m))
    literals = ''.join(('1' if l > 0 else '0') + format(abs(l), f'0{w}b')
                       for c in clauses for l in c)
    G = len(FIXED_INDEX)*m*3*(w+1)
    N = len(header)+len(literals)
    assert N == 32 + 3*w + 60*m*(w+1)
    assert G == 16*m*3*(w+1)
    return clauses, header+literals, {'m':m, 'n':15*m, 'clauses':20*m,
                                     'width':w, 'N':N, 'gap':G,
                                     'A_physical_clauses':2*m,
                                     'fixed_physical_clauses':16*m,
                                     'B_physical_clauses':2*m}


def witness_from_A(a):
    return tuple(616 if t == 0 else 4742 for t in a)


def witness_satisfies_formula(clauses, masks):
    assignment = [(mask >> i) & 1 for mask in masks for i in range(15)]
    for clause in clauses:
        if not any(bool(assignment[abs(l)-1]) == (l > 0) for l in clause):
            return False
    return True


class PositionMachine:
    """Finite-control algorithm; no branch consults the Python work coordinate.

    Its *observable* work-cell symbol is @ at the origin and blank elsewhere.
    INITMARK: @ is immutable endmarker supplied in initial work-tape convention.
    WRITEONE: @ is installed by a single symbol-changing initialization step.
    All other work cells are blank. Physical coordinate is accounting ONLY.
    """
    def __init__(self, word, initmark):
        self.N=len(word)
        self.x=word+'~'  # immutable physical right-end sentinel, NOT input data
        self.initmark=initmark
        self.ih=0
        self.wh=0
        self.visited={0}
        self.t=0;self.hm=0;self.wm=0;self.r=0;self.d=0
        self.previous_direction=0
        self.phase='INIT'
        self.abit='?'
        self.output=None
        self.halt=None
        self.cut_events={}
        p=word.find('#')
        p2=word.find('#',p+1) if p>=0 else -1
        if p>=0 and p2>p:
            self.cut_events={c:[] for c in range(p+1,p2-1)}
        if not initmark:
            # An actual work-tape change, performed once. No free sentinel.
            self.t+=1;self.d+=1

    def sym(self):
        return MARK if self.wh==0 else '_'

    def ch(self):
        return self.x[self.ih]

    def step(self, di=0, dw=0):
        assert di in (-1,0,1) and dw in (-1,0,1)
        old=self.ih
        newih=old+di; newwh=self.wh+dw
        if not 0<=newih<len(self.x):raise BadInput
        assert newwh>=0
        self.t+=1
        if di:
            self.hm+=1
            if self.previous_direction and di!=self.previous_direction:
                self.r+=1
            self.previous_direction=di
        if dw:self.wm+=1
        self.ih=newih;self.wh=newwh
        self.visited.add(newwh)
        if di:
            boundary=min(old,newih)
            if boundary in self.cut_events:
                # Complete *visible* finite control and work-head position.
                # Work content is determined by immutable origin mark.
                self.cut_events[boundary].append((self.phase,di,self.wh,self.abit))
        assert self.t < 1000*len(self.x)*(len(self.x)+1)

    def stop(self,answer):
        self.t+=1
        self.output=int(bool(answer))
        self.halt='SAT' if answer else 'UNSAT_OR_INVALID'
        return bool(answer)

    def run(self):
        try:
            return self._run()
        except BadInput:
            return self.stop(False)

    def _run(self):
        if self.N==0 or self.ch()!='^':return self.stop(False)
        self.phase='VALIDATE_A'
        self.step(1,0)
        seen=False
        while self.ch() in '01':
            seen=True
            self.step(1,1)
        if self.ch()!='#' or not seen:return self.stop(False)
        self.phase='VALIDATE_GAP'
        self.step(1,0)
        seen=False
        while self.ch()=='0':
            seen=True
            self.step(1,0)
        if self.ch()!='#' or not seen:return self.stop(False)
        self.phase='VALIDATE_B'
        self.step(1,0)
        seen=False
        while self.ch() in '01':
            seen=True
            if self.sym()==MARK:return self.stop(False)
            self.step(1,-1)
        if self.ch()!='$' or not seen or self.sym()!=MARK:
            return self.stop(False)
        # Prohibit trailing bytes, using the standard immutable right-end sentinel.
        self.step(1,0)
        if self.ch()!='~':return self.stop(False)
        self.step(-1,0)
        self.phase='REWIND_AFTER_VALIDATION'
        while self.ch()!='^':self.step(-1,0)
        while True:
            # Work-head position is the index i, but *only* @ is readable.
            self.phase='FIND_A'
            while self.sym()!=MARK:
                self.step(1,-1)
                if self.ch() not in '01':return self.stop(False)
            self.step(1,0)
            if self.ch()=='#':return self.stop(True)  # reached i=|A|
            if self.ch() not in '01':return self.stop(False)
            self.abit=self.ch()
            self.phase='REWIND_A'
            self.step(-1,0)
            while self.ch()!='^':self.step(-1,1)
            self.phase='SEEK_FIRST_SEPARATOR'
            while self.ch()!='#':self.step(1,0)
            self.phase='SEEK_SECOND_SEPARATOR'
            self.step(1,0)
            while self.ch()!='#':
                if self.ch()!='0':return self.stop(False)
                self.step(1,0)
            self.phase='FIND_B'
            while self.sym()!=MARK:
                self.step(1,-1)
                if self.ch() not in '01':return self.stop(False)
            self.step(1,0)
            if self.ch() not in '01':return self.stop(False)
            if self.abit=='1' and self.ch()=='1':return self.stop(False)
            self.phase='REWIND_B'
            self.step(-1,0)
            while self.ch()!='#':self.step(-1,1)
            self.phase='REWIND_HOME'
            while self.ch()!='^':self.step(-1,0)
            self.phase='INCREMENT_INDEX'
            self.step(0,1)

    def ledger(self):
        return {'T_native_transitions':self.t,'input_head_steps_H':self.hm,
                'work_head_steps':self.wm,'input_reversals_R':self.r,
                'work_visited_cells_S':len(self.visited),
                'actual_work_symbol_changes_D':self.d,
                'work_contents_nonblank_max':1,
                'input_probe_events_with_repeats':self.t,
                'gap_crossings':sum(len(e) for e in self.cut_events.values()),
                'output_bits_L':1,'input_bits_N':self.N,
                'M1_rescan_time_upper_units':self.t*(self.N+len(self.visited)+(self.t+2).bit_length()),
                'M1_rescan_footprint_upper_cells':self.N+len(self.visited)+(self.t+2).bit_length(),
                'status':self.halt}


def zone(a,b,g):
    return '^'+''.join(map(str,a))+'#'+'0'*g+'#'+''.join(map(str,b))+'$'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    args=p.parse_args()
    assert len(W1)==20 and len(A_INDEX)==len(B_INDEX)==2 and len(FIXED_INDEX)==16
    counts={}
    wverify={}
    checked=0
    for a,b in itertools.product((0,1),repeat=2):
        F=gadget(a,b)
        assert proper_22(F,15)
        nmodels=sum(satisfies(F,mask) for mask in range(1<<15))
        assert nmodels=={(0,0):772,(0,1):272,(1,0):272,(1,1):0}[(a,b)]
        counts[f'{a}{b}']=nmodels
        wverify[f'{a}{b}']={'w0_616':satisfies(F,616),'w1_4742':satisfies(F,4742)}
        checked+=32768
    assert wverify['00']['w0_616'] and wverify['01']['w0_616']
    assert wverify['10']['w1_4742'] and not any(wverify['11'].values())
    gadget_cases=0
    machine_cases=0
    g_counts={}
    ledger_examples=[]
    fooling_controls={}
    no_marker_counter_examples=[]
    for m in range(1,6):
        total=0
        seen_crossing={}
        for aa in itertools.product((0,1),repeat=m):
            for bb in itertools.product((0,1),repeat=m):
                clause,physical,measure=fixed_binary(m,aa,bb)
                assert len(physical)==measure['N']
                assert proper_22(clause,15*m)
                expected=not any(x and y for x,y in zip(aa,bb))
                if expected:assert witness_satisfies_formula(clause,witness_from_A(aa))
                # A-only witness printer is deliberately NOT a sound SAT acceptor.
                # For UNSAT it still prints a candidate; at least one clause fails.
                else:assert not witness_satisfies_formula(clause,witness_from_A(aa))
                gadget_cases+=1
                gap=4*m+3
                word=zone(aa,bb,gap)
                for initial_marker in (True,False):
                    z=PositionMachine(word, initial_marker)
                    got=z.run()
                    assert got==expected,(m,aa,bb,got,expected)
                    assert z.d==(0 if initial_marker else 1)
                    assert z.ledger()['work_visited_cells_S']<=m+1
                    assert z.hm<=z.t and z.r<=z.hm
                    assert z.t<=50*(m+1)*len(word)
                    machine_cases+=1
                    if len(ledger_examples)<6 and (aa==tuple(0 for _ in aa) or aa==tuple(1 for _ in aa)):
                        ledger_examples.append({'m':m,'A':aa,'B':bb,'init_mark':initial_marker,'ledger':z.ledger()})
                    if initial_marker and bb==tuple(1-t for t in aa):
                        for cut,seq in z.cut_events.items():
                            key=(cut,tuple(seq))
                            assert key not in seen_crossing,(m,aa,seen_crossing.get(key))
                            seen_crossing[key]=aa
                total+=1
        g_counts[str(m)]={'physical_cases':total,'single_input_native_cases':2*total,
                          'V':15*m,'C':20*m,'w':(20*m).bit_length(),
                          'physical_gap_G':16*m*3*((20*m).bit_length()+1)}
        fooling_controls[str(m)]={'SAT_fooling_inputs':2**m,
                                    'gap_cuts':4*m+2,
                                    'distinct_crossing_histories':len(seen_crossing)}
    # Long physical gaps retain same algorithm but change native input-head costs.
    longgap=[]
    for m in (2,4,8,12):
        w=(20*m).bit_length()
        gap=16*m*3*(w+1)
        for aa,bb in ((tuple([0]*m),tuple([1]*m)),
                       (tuple([1]*m),tuple([1]*m)),
                       (tuple([1]*(m-1)+[0]),tuple([0]*(m-1)+[1]))):
            z=PositionMachine(zone(aa,bb,gap),False)
            result=z.run()
            assert result==(not any(x and y for x,y in zip(aa,bb)))
            longgap.append({'m':m,'gap':gap,'answer':result,'ledger':z.ledger()})
    # Negative: malformed zone words. The machine rejects without relying on the promise.
    malformed=('^01#000#1$', '^01#000#011$', '^01#000#001$', '^01#X00#01$',
               '^01#000#0X$', '^01#00001$', '^#000#01$', '^01#000#01$junk', '^01#000#01', '^01#')
    malformed_results=[]
    for st in malformed:
        z=PositionMachine(st,False)
        assert z.run()==False,(st,z.ledger())
        malformed_results.append({'source':st,'ledger':z.ledger()})
    out={'RUN':'UTM-CROSS-WRITE-COUNTER175','date':'2026-10-27',
         'status':'COMPUTATIONAL controls; restricted symbolic lemmas separate',
         'gadget_counts':counts,'witness_mask_controls':wverify,
         'model_count_evaluations':checked,
         'physical_signed22_formula_controls':gadget_cases,
         'machine_execution_cases':machine_cases,
         'by_m':g_counts,'fooling_transcript_controls':fooling_controls,
         'ledger_examples':ledger_examples,'long_physical_gap_controls':longgap,
         'malformed_controls':malformed_results,
         'total_failures':0,
         'no_marker_D0_note':'On a bi-infinite entirely blank work tape without an origin marker, symbol reads never expose head coordinate: D=0 collapses to 2DFA; no counter is implemented.',
         'M1_vs_Mk_note':'M1 footprint includes input; Mk visited blank work cells counts origin and max unary position; simulated M1 rescan quantities are construction upper estimates, not executed M1 trace.',
         'proof_status':'P vs NP OPEN; ARC-EDGE-90 OPEN'}
    with open(args.output,'w',encoding='utf8') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({'model_count_evaluations':checked,'gadget_cases':gadget_cases,
                      'machine_cases':machine_cases,'fooling':fooling_controls,
                      'long_gap_cases':len(longgap),'malformed_cases':len(malformed)},indent=2))
if __name__=='__main__':main()
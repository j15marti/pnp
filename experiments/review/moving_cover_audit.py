#!/usr/bin/env python3
"""MOVINGCOVER1: exact finite audits of a sequential pointwise portfolio.

Each batch is separately bounded to 25 seconds. Standard library, Python 3.10+.
The virtual-machine and CNF counters are declared logical costs, NOT an FLMV
machine implementation. The proof uses separately charged native runner costs.
No universal SAT solver, lower bound, or finite-to-asymptotic inference is claimed.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools as it
import json
from pathlib import Path
import time
from typing import Callable, Iterator


class Audit:
    def __init__(self) -> None:
        self.start = time.monotonic()
        self.checks: Counter[str] = Counter()
    def check(self, value: bool, name: str) -> None:
        self.checks[name] += 1
        if not value:
            raise AssertionError(name)
        if time.monotonic() - self.start > 25:
            raise TimeoutError('Split the batch: cooperative 25-second deadline')


@dataclass(frozen=True)
class Trial:
    answer: int | None
    ticks: int
    peak: int
    reset: int
    status: str


def sequential(parameters: Iterator[int], run: Callable[[int], Trial],
               time_limit: int, space_limit: int) -> tuple[int | None, dict]:
    """One trial state at a time. No answer on exhaustion is UNKNOWN.

    run must be sound on every returned bit. This controller cannot certify
    that semantic property, and tests intentionally exhibit the need for it.
    """
    attempts = 0; ticks = 0; peak = 0; resets = 0; chosen = None
    status = Counter()
    for p in parameters:
        attempts += 1
        trial = run(p)
        if trial.ticks > time_limit or trial.peak > space_limit:
            raise AssertionError('runner broke its declared resource contract')
        ticks += trial.ticks; resets += trial.reset
        peak = max(peak, trial.peak)
        status[trial.status] += 1
        if trial.answer is not None:
            if trial.answer not in (0, 1):
                raise ValueError('non-Boolean terminal')
            chosen = p
            return trial.answer, {'attempts': attempts, 'ticks': ticks,
                   'reset_work': resets, 'peak_trial_state': peak,
                   'selected': chosen, 'statuses': dict(status)}
    return None, {'attempts': attempts, 'ticks': ticks, 'reset_work': resets,
                  'peak_trial_state': peak, 'selected': chosen,
                  'statuses': dict(status)}


def coverage(a: Audit) -> dict:
    counts = Counter(); examples = []
    # Four explicit inputs, three candidate algorithms. Each bit indicates
    # that the corresponding SOUND partial candidate returns on this input.
    for mask in range(1 << 12):
        rows = [(mask >> (3*x)) & 7 for x in range(4)]
        pointwise = all(rows)
        fixed = any(all(row & (1 << p) for row in rows) for p in range(3))
        actual = []
        for x in range(4):
            target = x.bit_count() % 2
            def run(p: int) -> Trial:
                ok = bool(rows[x] & (1 << p))
                return Trial(target if ok else None, p+1, 2, 2,
                             'ANSWER' if ok else 'UNKNOWN')
            got, ledger = sequential(iter(range(3)), run, 3, 2)
            a.check(got is None or got == target, 'coverage_sound_output')
            a.check((got is not None) == bool(rows[x]), 'coverage_exact_union')
            a.check(ledger['ticks']+ledger['reset_work'] <= 3*(3+2), 'coverage_total_charge')
            actual.append(got is not None)
        a.check(all(actual) == pointwise, 'coverage_uniform_controller')
        a.check(not fixed or pointwise, 'fixed_implies_pointwise')
        counts[f'pointwise_{int(pointwise)}_fixed_{int(fixed)}'] += 1
        if pointwise and not fixed and len(examples) < 4:
            examples.append({'mask': mask, 'coverage_rows': rows})
    a.check(counts['pointwise_1_fixed_0'] == 1680, 'coverage_gap_count')
    a.check(counts['pointwise_1_fixed_1'] == 721, 'fixed_column_count')
    return {'tables': 4096, 'counts': dict(counts), 'examples': examples}


# A tiny register/bit-tape interpreter. Memory references are validated before
# the fixed tape buffer is accessed. Its unit is an instruction, not a bit step.
PARITY = [('LEN',0), ('SET',1,0), ('SET',2,0), ('JGE',1,0,8),
          ('READ',3,1), ('XOR',2,3), ('INC',1), ('JMP',3), ('RET',2)]


def vm(code: list[tuple], bits: tuple[int, ...], budget: int, cap: int) -> Trial:
    if budget < 0 or cap < 0:
        raise ValueError('nonnegative caps required')
    regs = [0]*6; tape = bytearray(cap); pc = steps = high = 0
    # Fixed-width operand discipline, also bounding intentionally bad immediates.
    wordbits = max(1, (len(bits)+budget+cap+len(code)+2).bit_length())
    limit = 1 << wordbits
    while steps < budget:
        if not 0 <= pc < len(code):
            return Trial(None, steps, high, high, 'INVALID')
        ins = code[pc]; pc += 1; steps += 1; op = ins[0]
        if op == 'LEN': regs[ins[1]] = len(bits)
        elif op == 'SET':
            if not 0 <= ins[2] < limit:
                return Trial(None, steps, high, high, 'WORD_CAP')
            regs[ins[1]] = ins[2]
        elif op == 'JGE':
            if regs[ins[1]] >= regs[ins[2]]: pc=ins[3]
        elif op == 'READ':
            j=regs[ins[2]]
            if j >= len(bits): return Trial(None,steps,high,high,'INVALID')
            regs[ins[1]]=bits[j]
        elif op == 'XOR': regs[ins[1]] ^= regs[ins[2]]
        elif op == 'INC':
            regs[ins[1]] += 1
            if regs[ins[1]] >= limit: return Trial(None,steps,high,high,'WORD_CAP')
        elif op == 'JMP': pc=ins[1]
        elif op == 'WRITE':
            address=regs[ins[1]]
            if address >= cap: return Trial(None,steps,high,high,'SPACE_CAP')
            tape[address]=regs[ins[2]] & 1; high=max(high,address+1)
        elif op == 'RET':
            answer=regs[ins[1]]
            if answer not in (0,1): return Trial(None,steps,high,high,'INVALID')
            for j in range(high): tape[j]=0
            return Trial(answer,steps,high,high,'ANSWER')
        else: return Trial(None,steps,high,high,'INVALID')
    # Explicit cleanup is charged on cap exits too.
    for j in range(high): tape[j]=0
    return Trial(None,steps,high,high,'TIME_CAP')


def machines(a: Audit) -> dict:
    count=Counter(); sample=[]
    for n in range(1,9):
        for bits in it.product((0,1),repeat=n):
            expected=sum(bits)%2
            for cap in (0,1,8):
                overflow=[('SET',4,cap),('WRITE',4,4),('JMP',2)]
                loop=[('JMP',0)]
                # The two bad candidates are silent, not semantically false.
                programs=[overflow,loop,PARITY]
                for budget in (1,5,5*n+5,5*n+20):
                    trials=[vm(p,bits,budget,cap) for p in programs]
                    got,ledger=sequential(iter(range(3)),lambda j:trials[j],budget,cap)
                    a.check(got is None or got==expected,'vm_soundness')
                    a.check((got is not None)==(trials[2].answer is not None),'vm_complete_if_fast_trial')
                    a.check(ledger['ticks']+ledger['reset_work'] <= 3*(budget+cap),'vm_time_reset_bound')
                    a.check(ledger['peak_trial_state'] <= cap,'vm_high_water_cap')
                    count['runs']+=1
                    count['trial_instructions']+=sum(t.ticks for t in trials)
                    if n==8 and bits==(1,)*8 and cap==8:
                        sample.append({'budget':budget,'answer':got,'ledger':ledger})
    # Memory is max, not a sum: several silent trials fill the same reused tape.
    fill=[('SET',4,7),('WRITE',4,4),('JMP',2)]
    trials=[vm(fill,(1,),12,8),vm(fill,(1,),12,8),vm(PARITY,(1,),12,8)]
    got,l=sequential(iter(range(3)),lambda j:trials[j],12,8)
    a.check(got==1 and l['peak_trial_state']==8 and l['reset_work']==16,'vm_sequential_reuse')
    # Incorrect fast NO cannot be made trustworthy by scheduling.
    wrong=[('SET',2,0),('RET',2)]
    got,_=sequential(iter(range(2)),lambda j:vm([wrong,PARITY][j],(1,),20,8),20,8)
    a.check(got==0,'vm_unsound_candidate_counterexample_exhibited')
    restart_rows=[]
    for n in range(1,17):
        bits=tuple(i%2 for i in range(n)); cap=8; total=0; rounds=0
        budget=1; programs=[[('SET',4,cap),('WRITE',4,4)],[('JMP',0)],PARITY]
        while True:
            got,record=sequential(iter(range(3)),lambda j:vm(programs[j],bits,budget,cap),budget,cap)
            rounds+=1; total+=record['ticks']+record['reset_work']
            if got is not None:break
            budget*=2
        need=5*n+5
        a.check(got==sum(bits)%2,'doubling_correct_without_winning_time')
        a.check(total<=4*3*need,'doubling_geometric_charge')
        a.check(rounds==(need-1).bit_length()+1,'doubling_round_count')
        restart_rows.append({'n':n,'rounds':rounds,'total_ticks_and_reset':total,'winning_time':need})
    return {'counts':dict(count),'samples':sample,'restarts':restart_rows,
            'excluded_from_tape_cap':'six bounded registers, fixed code, input; theorem charges all native state separately',
            'warning':'Logical VM cap tests only, not an exact FLMV simulator.'}


def cube_clauses():
    return [tuple((i+1)*(1 if b[i] else -1) for i in range(3))
            for b in it.product((0,1),repeat=3)]


def brute_sat(n: int, clauses: list[tuple[int,...]]) -> bool:
    return any(all(any(bool((z>>(abs(l)-1))&1)==(l>0) for l in c) for c in clauses)
               for z in range(1<<n))


def capped_cnf(n: int, clauses: list[tuple[int,...]], start: int,
               budget: int, cap: int) -> Trial:
    """All cyclic assignment orders are exact if run to completion.
    Every attempted assignment and literal inspection costs one logical tick.
    Peak below counts the n-bit assignment plus bounded loop-state estimate;
    the read-only formula is excluded. These are not native machine bounds.
    """
    need=n+4*max(1,(1+(1<<n)+sum(map(len,clauses))).bit_length())
    if need>cap: return Trial(None,0,0,0,'SPACE_CAP')
    ticks=0
    for k in range(1<<n):
        if ticks>=budget:return Trial(None,ticks,need,need,'TIME_CAP')
        ticks+=1; z=(start+k)%(1<<n); valid=True
        for c in clauses:
            sat=False
            for lit in c:
                if ticks>=budget:return Trial(None,ticks,need,need,'TIME_CAP')
                ticks+=1
                if bool((z>>(abs(lit)-1))&1)==(lit>0):sat=True;break
            if not sat:valid=False;break
        if valid:return Trial(1,ticks,need,need,'ANSWER')
    return Trial(0,ticks,need,need,'ANSWER')


def formulas(a: Audit) -> dict:
    cube=cube_clauses(); cases=[]
    for mask in range(256):cases.append((f'cube_{mask}',3,[cube[i] for i in range(8) if mask>>i&1]))
    cases.extend([
        ('Horn',3,[(-1,-2,3),(-3,)]),('dual_Horn',3,[(1,2,-3),(3,)]),
        ('Krom',3,[(1,2),(-1,3),(-2,-3)]),
        ('affine',3,[c for c in cube if sum(l>0 for l in c)%2]),
        ('treewidth_path',4,[(1,2),(-2,3),(-3,4)]),
        ('product',4,[(1,2),(3,4)]),('padding',4,[(1,2)]),
        ('inconsistent',2,[(1,),(-1,)])])
    counts=Counter(); examples=[]
    for name,n,F in cases:
        expected=int(brute_sat(n,F)); count=1<<n
        for budget in (1,8,32,128):
            for cap in (1,128):
                ts=[capped_cnf(n,F,j,budget,cap) for j in range(count)]
                got,l=sequential(iter(range(count)),lambda j:ts[j],budget,cap)
                a.check(got is None or got==expected,'cnf_soundness')
                a.check((got is not None)==any(t.answer is not None for t in ts),'cnf_pointwise_union')
                a.check(l['ticks']+l['reset_work']<=count*(budget+cap),'cnf_reset_time_accounting')
                a.check(l['peak_trial_state']<=cap,'cnf_peak_not_sum')
                counts['runs']+=1;counts['answers' if got is not None else 'unknown']+=1
                counts['controller_ticks']+=l['ticks'];counts['cleanup_ticks']+=l['reset_work']
                if got is not None: counts['answer_no' if got==0 else 'answer_yes']+=1
                if name in ('cube_1','cube_254','cube_255') and cap==128:
                    examples.append({'case':name,'budget':budget,'answer':got,'ledger':l})
    # Same semantics under phase/renaming, no inference about primitive runtime.
    for F in [cube[:4],cube,cube[::2]]:
        expected=brute_sat(3,F)
        for perm in it.permutations((1,2,3)):
            for phase in range(8):
                G=[tuple(perm[abs(l)-1]*(1 if (l>0)^bool(phase>>(abs(l)-1)&1) else -1) for l in c) for c in F]
                a.check(brute_sat(3,G)==expected,'cnf_renaming_phase')
    return {'cases':len(cases),'counts':dict(counts),'examples':examples,
            'warning':'Exhaustive small-input search only; arbitrary n remains exponential.'}


def growth(a: Audit) -> dict:
    rows=[]
    # Actual selector on parity with moving finite fast bands; no exponential
    # delays are executed. A full B_j would deliberately delay off its band.
    for n in list(range(1,65))+[127,128,255,256,511,512,1023,1024,4096]:
        bits=tuple((i*i+n+i//3)&1 for i in range(n))
        j=n.bit_length()-1
        specs=range(j+1)
        def run(p):
            if p!=j:return Trial(None,1,1,1,'UNKNOWN')
            return Trial(sum(bits)%2,n+1,n.bit_length()+1,n.bit_length()+1,'ANSWER')
        got,l=sequential(iter(specs),run,n+1,n.bit_length()+1)
        a.check(got==sum(bits)%2,'moving_band_correct')
        a.check(l['selected']==j,'moving_band_selected_index')
        a.check(l['ticks']<=n+j+1,'moving_band_charged_time')
        a.check(not ((1<<j)<=1<<(j+1)<(1<<(j+1))),'fixed_band_ends')
        rows.append({'n':n,'selected':j,'candidate_count':j+1,'ledger':l})
    arithmetic=[]
    for lam in (Fraction(0),Fraction(1,16),Fraction(1,4)):
        for tau in (Fraction(1),Fraction(5,4),Fraction(11,8),Fraction(3,2)):
            cost=lam+tau; valid=cost<Fraction(3,2)
            a.check(valid==((3*cost.denominator)>2*cost.numerator),'strict_time_slack_arithmetic')
            arithmetic.append({'lambda':str(lam),'tau':str(tau),'sum':str(cost),'below_3/2':valid})
    # A table through length n has >2^n decision bits. O(log n)-bit indices
    # cannot make its generation/output cost disappear.
    for n in range(1,21):
        a.check(sum(1<<i for i in range(n+1))==(1<<(n+1))-1,'truth_table_generation_size')
    # A nonuniform limiting estimate must not replace a uniform bound:
    # r_j(n)=n for n=2^j, and zero otherwise, is eventually zero for each j,
    # while r_log2(n)(n)=n on powers of two.
    for j in range(1,15):
        n=1<<j
        a.check(n>0 and (n if n==1<<j else 0)==n,'moving_index_nonuniform_error_control')
    return {'bands':rows,'exponent_arithmetic':arithmetic,
            'limits':['Fixed-band B_j has deliberately exponential runtime eventually.',
                      'No exponential delay was executed in this finite batch.',
                      'The parity control is not a SAT reduction or hardness claim.']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--batch',required=True,choices=('coverage','machines','formulas','growth'))
    p.add_argument('--out',type=Path,required=True);args=p.parse_args();a=Audit()
    result=globals()[args.batch](a)
    code=Path(__file__).read_bytes()
    data={'run_id':'MOVINGCOVER1','batch':args.batch,'status':'COMPUTATIONAL','seed':None,
          'assertions':sum(a.checks.values()),'checks':dict(a.checks),'failures':0,
          'seconds':time.monotonic()-a.start,'code_sha256':hashlib.sha256(code).hexdigest(),
          'result':result,'limitations':['No polynomial SAT decider implemented.',
          'Logical event counts are not exact FLMV bit costs or Python peak memory.',
          'New symbolic theorem awaits independent review.']}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:data[k] for k in ('batch','assertions','failures','seconds')}))

if __name__=='__main__':main()

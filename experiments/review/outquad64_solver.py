#!/usr/bin/env python3
"""OUTQUAD64 standalone raw quadratic solver.
Exact graph identities affine in input and quadratic in output.
Complete with <=64 candidates on affine-hidden u^3+u^8 maps.
Sound partial solver on arbitrary raw quadratic maps: UNKNOWN is not UNSAT.
No field modulus, hidden affine maps, or cryptographic assumption is used.
Input: {"map":{"schema":"raw-quadratic-v1","dimension":d,"coefficients":[...]},"target":b}
Coefficients: constant, d linear terms, lexicographic i<j quadratic terms;
each coefficient is a nonnegative d-bit integer output vector.
"""
from __future__ import annotations
import argparse,itertools,json,time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable,Iterable
Tick=Callable[[],None]

def noop() -> None:
    pass

class Budget:
    def __init__(self, seconds: float = 25.0) -> None:
        self.deadline = time.monotonic() + seconds
    def __call__(self) -> None:
        if time.monotonic() > self.deadline:
            raise TimeoutError('cooperative experiment deadline exceeded')

def monomials(d: int, degree: int = 2) -> list[int]:
    out = [0]
    for k in range(1, min(d, degree) + 1):
        out += [sum(1 << j for j in js) for js in itertools.combinations(range(d), k)]
    return out

def validate(record: object) -> tuple[int, tuple[int, ...]]:
    if not isinstance(record, dict) or set(record) != {'schema','dimension','coefficients'}:
        raise ValueError('record keys or container are invalid')
    if record['schema'] != 'raw-quadratic-v1':
        raise ValueError('unsupported schema')
    d, cs = record['dimension'], record['coefficients']
    # Bound d by an already present explicit list before d-indexed allocation.
    if type(d) is not int or d < 1 or not isinstance(cs, list) or d >= len(cs):
        raise ValueError('dimension is not supported by explicit coefficient data')
    if len(cs) != 1 + d + d * (d - 1) // 2:
        raise ValueError('coefficient count mismatch')
    if any(type(c) is not int or c < 0 or c.bit_length() > d for c in cs):
        raise ValueError('coefficient is not a d-bit output vector')
    return d, tuple(cs)

def echelon(rows: Iterable[int], tick: Tick = noop) -> dict[int, int]:
    """Row-echelon basis, highest pivot first; integer bitsets are not unit cost."""
    piv: dict[int, int] = {}
    for index, initial in enumerate(rows):
        if index % 64 == 0:
            tick()
        row = initial
        while row:
            p = row.bit_length() - 1
            if p in piv:
                row ^= piv[p]
            else:
                piv[p] = row
                break
    return piv

def kernel(rows: Iterable[int], columns: int, tick: Tick = noop) -> tuple[list[int], int]:
    piv = echelon(rows, tick)
    basis = []
    for f in range(columns):
        if f in piv:
            continue
        v = 1 << f
        for p in sorted(piv):
            if (piv[p] & v).bit_count() & 1:
                v |= 1 << p
        basis.append(v)
        tick()
    return basis, len(piv)

def coefficient_rows(record: dict, tick: Tick = noop) -> tuple[list[int], list[int]]:
    """Matrix for R(x,Q(x))=0, with R bi-affine in x,y.

    Column (a,b) stands for X_a Y_b, where X_0=Y_0=1,
    X_{i+1}=x_i and Y_{j+1}=y_j. Substitution has Boolean degree <=3.
    """
    d, cs = validate(record)
    w = d + 1
    ms = monomials(d, 3)
    rows = {m: 0 for m in ms}
    input_ms = monomials(d)
    for a in range(w):
        tick()
        xmask = 0 if a == 0 else 1 << (a - 1)
        rows[xmask] ^= 1 << (a * w)
        for m, c in zip(input_ms, cs):
            destination = m | xmask  # Boolean reduction, including repeated x_i.
            bits = c
            while bits:
                low = bits & -bits
                b = low.bit_length()  # y_j is column j+1.
                rows[destination] ^= 1 << (a * w + b)
                bits ^= low
    return ms, [rows[m] for m in ms]

def affine_solve(equations: Iterable[tuple[int,int]], d: int) -> tuple[int, list[int]] | None:
    mask = (1 << d)-1
    piv: dict[int,int] = {}
    for a, b in equations:
        row = a | (b << d)
        while row & mask:
            p = (row & mask).bit_length()-1
            if p in piv:
                row ^= piv[p]
            else:
                piv[p] = row
                break
        if not row & mask and row >> d:
            return None
    particular = 0
    for p in sorted(piv):
        if ((piv[p] >> d) ^ (piv[p] & particular).bit_count()) & 1:
            particular |= 1 << p
    basis = []
    for f in range(d):
        if f in piv:
            continue
        v = 1 << f
        for p in sorted(piv):
            if ((piv[p] & mask) & v).bit_count() & 1:
                v |= 1 << p
        basis.append(v)
    return particular, basis

def enumerate_affine(particular: int, basis: list[int]) -> list[int]:
    xs = [particular]
    for v in basis:
        xs += [x ^ v for x in xs]
    return sorted(xs)

def product_support(a: list[int], b: list[int], tick: Tick = noop) -> set[int]:
    out: set[int] = set()
    for i, x in enumerate(a):
        if i % 32 == 0: tick()
        for y in b:
            m = x | y
            if m in out: out.remove(m)
            else: out.add(m)
    return out


def extended_rows(record: dict, tick: Tick = noop) -> tuple[list[int], int]:
    d, cs = validate(record)
    ms3, old_rows = coefficient_rows(record, tick)
    rows = dict(zip(ms3, old_rows))
    ms2 = monomials(d, 2)
    coords = [[m for m, c in zip(ms2, cs) if (c >> j) & 1] for j in range(d)]
    start = (d+1)**2
    for k, (i,j) in enumerate(itertools.combinations(range(d),2)):
        tick()
        bit = 1 << (start+k)
        for m in product_support(coords[i], coords[j], tick):
            rows[m] = rows.get(m,0) ^ bit
    return [rows[m] for m in sorted(rows, key=lambda x:(x.bit_count(),x))], start+d*(d-1)//2


@dataclass(frozen=True)
class ExtendedModel:
    dimension: int
    coefficients: tuple[int,...]
    identities: tuple[int,...]
    coefficient_rank: int
    matrix_rows_present: int
    matrix_columns: int

    def record(self) -> dict:
        return {'schema':'raw-quadratic-v1','dimension':self.dimension,'coefficients':list(self.coefficients)}

    def evaluate(self,x:int) -> int:
        y=0
        for m,c in zip(monomials(self.dimension,2),self.coefficients):
            if x&m==m: y ^= c
        return y

    def to_json(self) -> dict:
        return {'schema':'outquad64-model-v1', 'map':self.record(),
                'identities':list(self.identities),'coefficient_rank':self.coefficient_rank,
                'matrix_rows_present':self.matrix_rows_present,'matrix_columns':self.matrix_columns}


def prepare(record: dict, tick: Tick = noop) -> ExtendedModel:
    d,cs = validate(record)
    rows, columns = extended_rows(record,tick)
    identities,rank=kernel(rows,columns,tick)
    # Full coefficient verification, not test-vector evaluation.
    for i,row in enumerate(rows):
        if i%128==0: tick()
        for r in identities:
            if (row&r).bit_count()&1:
                raise AssertionError('nonzero coefficient in alleged identity')
    return ExtendedModel(d,cs,tuple(identities),rank,len(rows),columns)


def equations(model: ExtendedModel, target: int) -> list[tuple[int,int]]:
    d=model.dimension
    if type(target) is not int or target<0 or target.bit_length()>d:
        raise ValueError('target must be a d-bit nonnegative integer')
    w=d+1; mask=(1<<w)-1; point=1|(target<<1)
    output_pairs=list(itertools.combinations(range(d),2))
    extra=sum(1<<k for k,(i,j) in enumerate(output_pairs) if (target>>i&1) and (target>>j&1))
    eqs=[]
    for rel in model.identities:
        const=((rel&mask)&point).bit_count()&1
        const ^= ((rel>>(w*w))&extra).bit_count()&1
        coeff=0
        for a in range(1,w):
            bit=(((rel>>(a*w))&mask)&point).bit_count()&1
            coeff |= bit<<(a-1)
        eqs.append((coeff,const))
    return eqs


def solve(model: ExtendedModel,target:int,tick:Tick=noop) -> dict:
    tick()
    ans=affine_solve(equations(model,target),model.dimension)
    if ans is None:
        return {'status':'UNSAT','witnesses':[], 'affine_dimension':None,
                'candidates_examined':0,'reason':'inconsistent exact identities'}
    a,basis=ans; dim=len(basis)
    if dim>6:
        return {'status':'UNKNOWN','witnesses':[], 'affine_dimension':dim,
                'candidates_examined':0,'reason':'certified enclosure exceeds 64 points'}
    candidates=enumerate_affine(a,basis)
    roots=[]
    for x in candidates:
        if model.evaluate(x)==target: roots.append(x)
        tick()
    return {'status':'SAT' if roots else 'UNSAT','witnesses':roots,
            'affine_dimension':dim,'candidates_examined':len(candidates),
            'candidate_vectors':candidates,'reason':'entire certified enclosure checked'}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    args=p.parse_args()
    try:
        obj=json.loads(args.input.read_text())
        if not isinstance(obj,dict) or set(obj)!={'map','target'}:
            raise ValueError('input must contain exactly map and target')
        model=prepare(obj['map'])
        result=solve(model,obj['target'])
        result['identities']=len(model.identities)
    except (ValueError,TypeError,KeyError,UnicodeError,RecursionError) as exc:
        result={'status':'INVALID','reason':str(exc)}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()

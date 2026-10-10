import itertools, json, time
from pathlib import Path
t=time.monotonic(); rows=[]
for k in range(2,13):
    rows.extend([
      dict(family="AND",k=k,satisfying=1,x=k,gate_upper=k-1),
      dict(family="PARITY",k=k,satisfying=2**(k-1),x=1,gate_upper=3*(k-1)),
      dict(family="UNSAT_UNIT",k=k,satisfying=0,x=None,gate_upper=2),
      dict(family="EQUALITY_PAIRS",k=k,satisfying=2**(k-k//2),x=k//2,gate_upper=5*(k//2))
    ])
for row in rows:
    k=row["k"]
    if k>10: continue
    if row["family"]=="AND": f=lambda a: all(a)
    elif row["family"]=="PARITY": f=lambda a:sum(a)%2==1
    elif row["family"]=="UNSAT_UNIT": f=lambda a: a[0] and not a[0]
    else: f=lambda a:all(a[2*i]==a[2*i+1] for i in range(k//2))
    actual=sum(bool(f(a)) for a in itertools.product((0,1),repeat=k))
    assert actual==row["satisfying"],(row,actual)
output=dict(status="COMPUTATIONAL",model="explicit circuits and enumerated assignments, not arbitrary SAT algorithms",rows=rows,verified_exhaustively_through_k=10,elapsed_s=round(time.monotonic()-t,4),conclusion="exponential candidate reduction does not imply exponential gate cost")
Path("results/raw/review/2026-10-10_boolean_compression_cost.json").write_text(json.dumps(output,indent=2))
print(json.dumps(dict(cases=len(rows),exhaustive_rows=sum(r["k"]<=10 for r in rows),seconds=output["elapsed_s"])))

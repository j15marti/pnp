"""Separate <25-second repeated-guard replay chunk."""
import runpy,itertools,time,json,pathlib,signal
signal.alarm(24)
p=pathlib.Path(__file__)
m=runpy.run_path(str(p.with_name('2026-10-09_0940_ARC-STRENGTHEN9-test.py'))); a=m['a']; rows=[]; start=time.monotonic()
for d in range(7):
    f=tuple(itertools.product(*[(i,-i) for i in (d+1,d+2,d+3)]))
    for z in range(d,0,-1): f=tuple((s,)+c for c in f for s in (z,-z))
    r=m['solve'](a.encode(f)); assert r['answer'] in (False,None)
    rows.append({'guards':d,'bits':len(a.encode(f))*8,'run':r})
p.with_suffix('.json').write_text(json.dumps({'rows':rows,'runtime_seconds':time.monotonic()-start},indent=2)+'\n')
print(json.dumps(rows[-1]))

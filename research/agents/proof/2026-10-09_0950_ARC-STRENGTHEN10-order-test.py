"""Independent order-sensitivity chunk; bounded at 24 seconds."""
import runpy,pathlib,itertools,json,time,signal
signal.alarm(24)
p=pathlib.Path(__file__)
m=runpy.run_path(str(p.with_name('2026-10-09_0950_ARC-STRENGTHEN10-test.py')))
a=m['a']; start=time.monotonic(); rows=[]
for d in range(6):
    f=tuple(itertools.product(*[(i,-i) for i in (d+1,d+2,d+3)]))
    for z in range(d,0,-1): f=tuple((z,)+c for c in f)+tuple((-z,)+c for c in reversed(f))
    r=m['solve'](a.encode(f)); assert r['answer'] is False
    rows.append({'guards':d,'bits':len(a.encode(f))*8,'run':r})
out={'status':'COMPUTATIONAL','rows':rows,'runtime_seconds':time.monotonic()-start}
p.with_name(p.name.replace('-test.py','-results.json')).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

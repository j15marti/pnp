from pathlib import Path
exec(Path(__file__).with_name('p3r03.py').read_text().split('def parse(s):')[0])
U=[tuple(map(int,t)) for t in '000 003 111 112 221 230 323 332'.split()]
for t in it.product(range(4),repeat=3):
    if t in U:continue
    T=U+[t]
    if planar(4,T) and oracle(4,T):
        a=run(4,T);b=run(4,T,True)
        print('U+ add',t,'close',len(close(4,T)),'raw',a,'guarded',b);break
print('U closure count',len(close(4,U)))

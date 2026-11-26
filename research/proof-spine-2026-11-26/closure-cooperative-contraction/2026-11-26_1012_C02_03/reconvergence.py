import audit as a,itertools as I,json,random
s=a.Solver(1,2);g=((0,0),);pa=s.parent[2][0][0];B=sorted({j for e in a.edges(s.fs[1][pa]) for j in s.ed[1][e]})
statuses=[]
for z in I.product((0,1),repeat=len(B)):
    gg=tuple(zip(B,z));w=s.solve(1,gg)
    if w is not None:a.verify(s.fs[1],w,gg)
    statuses.append([list(z),w is not None])
print('forced contexts',len(statuses),'yes',sum(v for _,v in statuses),s.stats())
r=random.Random(26112603);cones=[]
for h in [1,2,4,8,16,32,64]:
    gg=tuple((j,0) for j in r.sample(range(len(s.fs[2])),h));cones.append([h,s.cone(gg)])
print('cones',cones)
p='/mnt/data/C02_03/results.json';R=json.load(open(p));R['exhaustive_coarse_context_schedule']={'support':B,'statuses':statuses,'stats':s.stats(),'random_seed':26112603,'cone_only':cones};json.dump(R,open(p,'w'),indent=2)

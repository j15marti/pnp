function verify(E,H,compile,B,R,peer){
 const assert=(x,m)=>{if(!x)throw Error(m)},json=x=>JSON.stringify(x)+"\n",hash=x=>H.sha(json(x));let results=[];
 for(let i=0;i<E.results.length;i++){let z=E.results[i],reg=R.instances.find(x=>x.instance_id===z.full),original=B.instances.find(x=>x.id===z.id),G=compile(original);
 assert(H.sha(json(G.network))===reg.sha256&&8*json(G.network).length===reg.N_bits&&H.sha(original.dimacs)===reg.source_cnf.sha256&&H.sha(json(G.source_map))===reg.source_map_sha256,"source");
 let I=H.independentNormalize(G.network),Q=H.verifyTrace(I.fs,z.sourceMap.trace);
 let anchor=z.anchor+1;assert(Q.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"complement");const uniq=a=>[...new Set(a)].sort((a,b)=>a-b);
 let F=Q.fs.map(f=>{let j=f.vs.indexOf(anchor),vs=f.vs.filter(v=>v!==anchor),ok=uniq(f.ok.filter(w=>j<0||!(w>>j&1)).map(w=>vs.reduce((s,v,k)=>s+((w>>f.vs.indexOf(v)&1)<<k),0)));return {...f,vs,ok}});
 // verify semantic factor table and chart artifact separately; extra metadata is preserved in artifact.
 assert(json(F.map(({id,vs,ok})=>({id,vs,ok})))===json(z.sourceChart.factors.map(({id,vs,ok})=>({id,vs,ok}))),"chart");assert(hash(z.sourceChart)===z.chartHash&&hash(z.sourceMap)===z.mapHash,"artifact hash");
 let V=z.sourceChart.variables,C=F.flatMap(f=>Array.from({length:2**f.vs.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.vs.map((v,k)=>w>>k&1?-v:v)));
 let stats={replayLits:0,glueXors:0,peerVisits:0,closureVisits:0,nodes:0,searchVisits:0,checkVisits:0};
 function up(C,g,key){let a=new Map();for(let l of g){let v=Math.abs(l),b=+(l>0);if(a.has(v)&&a.get(v)!==b)return{bad:true,a};a.set(v,b)}while(true){let changed=false;for(let row of C){stats[key]+=row.length;if(stats[key]>3000000)throw Error("cap");let sat=false,unknown=[];for(let l of row){if(!a.has(Math.abs(l)))unknown.push(l);else if(a.get(Math.abs(l))===+(l>0)){sat=true;break}}if(sat)continue;if(!unknown.length)return{bad:true,a};if(unknown.length===1){let l=unknown[0];a.set(Math.abs(l),+(l>0));changed=true;break}}if(!changed)return{bad:false,a}}}
 let paths=[],children=z.delta.map(()=>[]);for(let j=0;j<z.delta.length;j++){let [p,l,v]=z.delta[j];if(j===0){assert(p===-1&&l===0,"root");paths.push([])}else{assert(p>=0&&p<j&&z.delta[p][2]===Math.abs(l)&&V.includes(Math.abs(l))&&!paths[p].some(a=>Math.abs(a)===Math.abs(l)),"edge");paths.push(paths[p].concat(l));children[p].push(l)}if(v===0){let rows=z.hintLists[j];assert(rows&&rows.every(k=>Number.isInteger(k)&&k>=0&&k<C.length),"hints");assert(up(rows.map(k=>C[k]),paths[j],"replayLits").bad,"leaf conflict")}else assert(z.hintLists[j]===null&&V.includes(v),"node")}
 for(let j=0;j<z.delta.length;j++){let v=z.delta[j][2];assert(json(children[j].sort((a,b)=>a-b))===json(v?[-v,v]:[]),"complete tree")}
 // independent sparse polynomial verifier: minimum pivot instead of maximum; indicators by multiplication.
 const flip=(s,m)=>s.has(m)?s.delete(m):s.add(m),deg=m=>m.toString(2).split("1").length-1,bit=v=>1n<<BigInt(V.indexOf(v)),x=bit(z.split),cap=z.degree;
 function poly(c){let a=new Set([0n]);for(let l of c){let q=new Set();for(let m of a){if(l>0)flip(q,m);flip(q,m|bit(Math.abs(l)))}a=q}return a}
 function res(p,b){let q=new Set();for(let m of p){if(!(m&x))flip(q,m);else if(b)flip(q,m^x)}return q}
 function reduce(M,p){let q=new Set(p);while(q.size){let a=[...q].reduce((u,v)=>u<v?u:v);if(!M.has(a))break;for(let m of M.get(a)){stats.glueXors++;flip(q,m)}}return q}
 function add(M,p){let q=reduce(M,p);if(!q.size)return false;M.set([...q].reduce((u,v)=>u<v?u:v),q);return true}
 let A=[new Map(),new Map()],base=new Map(),joint=new Map();for(let row of C){let p=poly(row);if([...p].every(m=>deg(m)<=cap))add(base,p);for(let b=0;b<2;b++){let q=res(p,b);if([...q].every(m=>deg(m)<=cap))add(A[b],q)}}
 let combined=new Map(base);for(let p of z.gluedPolynomials){let q=new Set(p.map(BigInt));assert([...q].every(m=>m>=0n&&m<(1n<<BigInt(V.length))&&deg(m)<=cap),"degree");assert(A.every((M,b)=>reduce(M,res(q,b)).size===0),"membership");assert(add(joint,q),"independence");add(combined,q)}
 assert(A[0].size===z.branchRanks[0]&&A[1].size===z.branchRanks[1]&&base.size===z.originalRank&&joint.size===z.gluedRank&&combined.size-base.size===z.newRank,"ranks");
 // peer candidate admission: exact own chart RUP, not a trusted imported proof of chart equivalence.
 let pc=JSON.parse(peer[i]),peerHash=H.sha(peer[i]);assert(pc.instance_id===z.full&&pc.map.gauge===anchor&&pc.map.carrier.startsWith("min original port+1"),"peer namespace");
 let L=C.slice(),learned=[],forced=[],rejected=0;for(let p of pc.proof){if(!p.c.length)continue;if(!p.c.every(l=>V.includes(Math.abs(l)))||!up(L,p.c.map(l=>-l),"peerVisits").bad){rejected++;continue}L.push(p.c);learned.push(p.c);let cl=up(L,[],"closureVisits");forced.push({after:learned.length,bad:cl.bad,count:cl.a.size});if(cl.bad)break}
 function tree(g){stats.nodes++;if(stats.nodes>10000)throw Error("node cap");let u=up(L,g,"searchVisits");if(u.bad)return {leaf:true};let freq=new Map();for(let c of L){if(c.some(l=>u.a.get(Math.abs(l))===+(l>0)))continue;for(let l of c)if(!u.a.has(Math.abs(l)))freq.set(Math.abs(l),(freq.get(Math.abs(l))||0)+1)}assert(freq.size,"SAT witness");let v=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return {v,L:tree(g.concat(-v)),U:tree(g.concat(v))}}
 let t=tree([]);function check(g,t){if(t.leaf){assert(up(L.slice().reverse(),g,"checkVisits").bad,"hybrid leaf");return}check(g.concat(-t.v),t.L);check(g.concat(t.v),t.U)}check([],t);
 results.push({id:z.id,instance:reg.short_id,instance_id:z.full,N:z.N,chart:z.chart_id,sourceMap:z.sourceMap,sourceChart:z.sourceChart,delta:z.delta,hints:z.hintLists,glued:z.gluedPolynomials,rankGain:z.newRank,peerHash,peerProofCount:pc.proof.length,learned,rejected,forced,hybridTree:t,stats,original_ids:pc.original_ids});
 }
 return results;
}
module.exports=verify;

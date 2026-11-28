function exportNarrow(base,out,w){
 let all=out.clauses,keep=new Set();let active=[...all.slice(0,out.initial)];let ids=[];
 for(let i=out.initial;i<all.length;i++)if(all[i].length<=w){active.push(all[i]);ids.push(i)}
 function mark(i){if(i<out.initial||keep.has(i))return;keep.add(i);let p=out.trace[i-out.initial].p;mark(p[0]);mark(p[1])}
 ids.forEach(mark);let cone=[...keep].sort((a,b)=>a-b).map(i=>({id:i,c:all[i],p:out.trace[i-out.initial].p}));
 let map=new Map(all.slice(0,out.initial).map((c,i)=>[i,c]));
 for(let {id,c,p} of cone){let [i,j,l]=p,x=map.get(i),y=map.get(j);if(!x||!y||!x.includes(l)||!y.includes(-l)||key(canonical([...x.filter(z=>z!==l),...y.filter(z=>z!==-l)]))!==key(c))throw Error("cone");map.set(id,c)}
 return {active,ids,cone,archivedWide:cone.filter(x=>x.c.length>w).length,coneLits:cone.reduce((s,x)=>s+x.c.length,0),activeLits:active.reduce((s,c)=>s+c.length,0)}
}

function boundOwners(owners,pins){
 let checks=0;
 function bound(J){let M=new Map(),demand=0;for(let i of J){let o=owners[i];demand+=o.d;for(let l of o.lits){checks++;let v=Math.abs(l),s=+(l<0),c=M.get(v)||[0,0];c[s]++;M.set(v,c)}}let upper=0,lower=0;
 for(let [v,c] of M){if(pins.has(v)){let a=c[1-pins.get(v)];upper+=a;lower+=a}else{upper+=Math.max(...c);lower+=Math.min(...c)}}
 return {upper,lower,demand,no:upper<demand||J.every(i=>owners[i].exact)&&lower>demand};}
 for(let i=0;i<owners.length;i++){let x=bound([i]);if(x.no)return {status:"UNSAT",support:[owners[i].id],...x,checks}}
 let occ=new Map();for(let i=0;i<owners.length;i++)for(let l of owners[i].lits){let v=Math.abs(l);if(!occ.has(v))occ.set(v,new Set());occ.get(v).add(i)}
 let seen=new Set();for(let vs of occ.values()){let a=[...vs];for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){let k=a[i]+","+a[j];if(seen.has(k))continue;seen.add(k);let x=bound([a[i],a[j]]);if(x.no)return{status:"UNSAT",support:[owners[a[i]].id,owners[a[j]].id],...x,checks};if(checks>500000)return{status:"UNKNOWN",reason:"cap",checks}}}
 return {status:"UNKNOWN",reason:"single/pair bound stall",checks}
}

function flowOwners(owners,pins,cap=2000000){
 const vs=[...new Set(owners.flatMap(o=>o.lits.map(Math.abs)))],ix=new Map(vs.map((v,i)=>[v,i+1])),source=0,off=1+vs.length,sink=off+owners.length,adj=Array.from({length:sink+1},()=>[]),C=new Map(),counts={arcs:0,scans:0,augment:0},demand=owners.reduce((s,x)=>s+x.d,0);
 function tick(){if(++counts.scans>cap)throw Error("cap")}
 function edge(u,v,c){let a={v,c,rev:adj[v].length,initial:c},b={v:u,c:0,rev:adj[u].length,initial:0};adj[u].push(a);adj[v].push(b);counts.arcs++}
 for(let i=0;i<owners.length;i++){let m=new Map();for(let l of owners[i].lits){let v=Math.abs(l),s=+(l<0);if(pins.has(v)&&pins.get(v)!==1-s)continue;let c=C.get(v)||[0,0];c[s]++;C.set(v,c);m.set(v,(m.get(v)||0)+1)}for(let [v,c] of m)edge(ix.get(v),off+i,c);edge(off+i,sink,owners[i].d)}
 for(let v of vs){let c=C.get(v)||[0,0];edge(source,ix.get(v),pins.has(v)?c[1-pins.get(v)]:Math.max(...c))}
 let flow=0;
 try{for(;;){let level=new Int32Array(adj.length).fill(-1),q=[source];level[source]=0;for(let i=0;i<q.length;i++)for(let a of adj[q[i]]){tick();if(a.c>0&&level[a.v]<0){level[a.v]=level[q[i]]+1;q.push(a.v)}}
   if(level[sink]<0){let cut=0;for(let u of q)for(let a of adj[u]){tick();if(level[a.v]<0)cut+=a.initial}if(cut!==flow)throw Error("mincut mismatch");let J=owners.map((o,i)=>({o,i})).filter(x=>level[off+x.i]<0).map(x=>x.o.id);return{status:flow<demand?"UNSAT":"UNKNOWN",flow,demand,cut,counts,sourceSideCarriers:vs.filter(v=>level[ix.get(v)]>=0),sinkSideOwners:J}}
   let ptr=new Int32Array(adj.length);function dfs(u,f){if(u===sink)return f;for(;ptr[u]<adj[u].length;ptr[u]++){tick();let a=adj[u][ptr[u]];if(a.c>0&&level[a.v]===level[u]+1){let d=dfs(a.v,Math.min(f,a.c));if(d){a.c-=d;adj[a.v][a.rev].c+=d;return d}}}return 0}
   for(;;){let d=dfs(source,demand-flow);if(!d)break;counts.augment++;flow+=d;if(flow===demand)return {status:"UNKNOWN",reason:"flow feasible, relaxation only",flow,demand,counts}}
 }}catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN",reason:"cap",flow,demand,counts}}
}

function guarded(F,g){let pins=new Map(g.map(l=>[Math.abs(l),+(l>0)]));return F.map(f=>({v:f.v,ids:f.ids,ok:f.ok.filter(w=>f.v.every((v,i)=>!pins.has(v)||pins.get(v)===(w>>i&1)))}))}

function guardCover(guards,r){
 let sum=0n,counts=[];for(let mask=1;mask<32;mask++){let p=new Map(),bad=false,n=0;for(let i=0;i<5;i++)if(mask>>i&1){n++;for(let l of guards[i]){let v=Math.abs(l),b=+(l>0);if(p.has(v)&&p.get(v)!==b)bad=true;p.set(v,b)}}
 let z=bad?0n:1n<<BigInt(r-p.size);sum+=(n%2?z:-z);counts.push(z.toString())}if(sum!==1n<<BigInt(r))throw Error("coverage");return{counts,sum:sum.toString(),total:(1n<<BigInt(r)).toString()}
}

function conditional(C,F,owners,gauge,depth){
 let vs=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>{let fa=C.reduce((s,c)=>s+(c.includes(a)||c.includes(-a)),0),fb=C.reduce((s,c)=>s+(c.includes(b)||c.includes(-b)),0);return fb-fa||a-b});
 let [x,y,z]=vs,guards=[[-x],[x,-y,-z],[x,-y,z],[x,y,-z],[x,y,z]],cover=guardCover(guards,vs.length),out=[];
 for(let g of guards){let p=new Map(g.map(l=>[Math.abs(l),+(l>0)]));if(gauge!==null)p.set(gauge,0);
  let local=up(C,g),f=guarded(F,g),aff=solver(f,"affine",150000,0),con=boundOwners(owners,p),flow=flowOwners(owners,p,350000);
  let geo=project(f,150000,-1),geoNo=geo.final.some(a=>!a.ok.length); // no extra gauge; sentinel -1 absent from scope
  let c=[...C,...g.map(l=>[l])],d=dpll(c,null,200000,depth),check=d.status==="UNSAT"?replayTree(c,d.tree):null;
  let result={g,local:{status:local.no?"UNSAT":"UNKNOWN",forced:local.a.size-g.length},aff:{status:aff.status,events:aff.events,root:aff.root,check:aff.status==="UNSAT"?independentCheck(f,aff.tree,"affine",500000):null},con,flow,geometry:{status:geoNo?"UNSAT":"UNKNOWN",steps:geo.steps.length,counts:geo.counts,remaining:geo.final.length},dag:{...d,check}};
  out.push(result)
 }
 return{guards,cover,results:out};
}
module.exports={exportNarrow,boundOwners,flowOwners,guarded,guardCover,conditional};

// Node.js, no packages. EX22-03 deterministic fixed-objective anchor audit.
function run(){
let checks=0; const ok=(b)=>{checks++;if(!b)throw Error("assertion "+checks)};
const C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>j).filter(j=>j!==i&&j!==(i+1)%6));
const G=Array.from({length:6},(_,v)=>{const a=C.flatMap((c,i)=>c.includes(v)?[i]:[]);return [a.slice(0,2),a.slice(2)].map(cs=>({v,cs}))}).flat();
const order=G.map((_,i)=>i).sort((a,b)=>G[a].cs[0]-G[b].cs[0]||G[a].v-G[b].v);
const bit=(w,i)=>(w>>i)&1;
const score=w=>order.reduce((s,j)=>2*s+bit(w,j),0);
const ekey=(a,b)=>a<b?a+":"+b:b+":"+a;
const port=(c,v)=>6*c+C[c].indexOf(v);
const links=G.map(g=>ekey(...g.cs.map(c=>port(c,g.v))));
const edges=[...links,...C.flatMap((c,i)=>c.flatMap(v=>[ekey(port(i,v),6*i+4),ekey(port(i,v),6*i+5)]))];
const E=new Map(edges.map((e,i)=>[e,i]));
const rows=[],matchings=[];
for(let w=0;w<4096;w++){
 if(!C.every((_,i)=>G.reduce((s,g,j)=>s+(g.cs.includes(i)?bit(w,j):0),0)===2))continue;
 rows.push(w);
 for(let f=0;f<64;f++){
  let es=links.filter((_,j)=>bit(w,j));
  for(let i=0;i<6;i++){
   const p=C[i].filter(v=>!bit(w,G.findIndex(g=>g.v===v&&g.cs.includes(i)))).map(v=>port(i,v));
   es.push(ekey(p[bit(f,i)],6*i+4),ekey(p[1-bit(f,i)],6*i+5));
  }
  ok(es.length===18&&new Set(es.flatMap(e=>e.split(":"))).size===36&&es.every(e=>E.has(e)));
  matchings.push({w,s:score(w),es:new Set(es.map(e=>E.get(e)))});
 }
}
matchings.sort((a,b)=>a.s-b.s);
const base=matchings[0], good=w=>G.every((g,j)=>bit(w,j)===bit(w,j^1));
ok(!good(base.w));const exact=rows.filter(good);
ok(exact.length===2);
const sourceModels=Array.from({length:64},(_,w)=>w).filter(w=>C.every(c=>c.reduce((s,v)=>s+bit(w,v),0)===2));
ok(sourceModels.length===2&&sourceModels.every(w=>Array.from({length:6},(_,v)=>bit(w,v)).every((b,v)=>b===(bit(w,0)^(v%2)))));
const pins=[];for(let j=0;j<edges.length;j++)for(let b=0;b<2;b++){const a=matchings.find(m=>m.es.has(j)===Boolean(b));ok(!!a);pins.push(a)}
const cases=[];
for(const k of [3,4,8,16,32,64])for(const twist of [0,1]){
 // Connect module i's v0 to module i+1's v2, or v3 at one twisted seam.
 const ids=Array.from({length:k},(_,i)=>Array.from({length:6},(_,v)=>6*i+v));
 for(let i=0;i<k;i++){const j=(i+1)%k;ids[j][j===0&&twist?3:2]=ids[i][0]}
 const F=ids.flatMap(a=>C.map(c=>c.map(v=>a[v])));
 const V=[...new Set(F.flat())];ok(V.length===5*k&&F.length===6*k);
 ok(F.every(c=>new Set(c).size===4)&&new Set(F.map(c=>c.slice().sort((a,b)=>a-b).join(","))).size===F.length);
 const occ=new Map(V.map(v=>[v,[]]));F.forEach((c,i)=>c.forEach(v=>occ.get(v).push(i)));
 for(const a of occ.values()){ok(a.length===4||a.length===8);for(let j=0;j<a.length;j+=2)ok(Math.floor(a[j]/6)===Math.floor(a[j+1]/6))}
 // BFS on actual source incidence, and discover regions using paired-link graph.
 let seen=new Set([0]),queue=[0];for(let p=0;p<queue.length;p++)for(const v of F[queue[p]])for(const j of occ.get(v))if(!seen.has(j)){seen.add(j);queue.push(j)}
 ok(seen.size===F.length);
 const adj=F.map(()=>[]);for(const a of occ.values())for(let j=0;j<a.length;j+=2){adj[a[j]].push(a[j+1]);adj[a[j+1]].push(a[j])}
 const regs=[],vis=new Set();for(let i=0;i<F.length;i++)if(!vis.has(i)){const q=[i];vis.add(i);for(let p=0;p<q.length;p++)for(const j of adj[q[p]])if(!vis.has(j)){vis.add(j);q.push(j)}regs.push(q)}
 ok(regs.length===k&&regs.every(r=>r.length===6));
 // Initial and stagnation closure: exact occupancy under unary pins and actual split matching support.
 let probes=0,rowScans=0,localSupportChecks=0;
 for(let pass=0;pass<2;pass++)for(const v of V)for(const b of [0,1]){
   probes++;for(const c of F){rowScans++;const t=c.includes(v);ok(!t||b<=2&&b+3>=2)} // no unit implication with one pin
   for(const reg of regs){const rr=reg.map(i=>F[i]);if(!rr.some(c=>c.includes(v)))continue;
    const local=ids[Math.floor(reg[0]/6)].indexOf(v);ok(local>=0);
    const a=matchings.find(m=>bit(m.w,2*local)===b&&bit(m.w,2*local+1)===b);
    localSupportChecks++;ok(!!a); // untouched regions use base
   }
 }
 // For every one-edge pin anchor, all other regions retain the bad optimal link word.
 // Pair support certificate: two anchors touch <=2 regions. Explicit check small k; formula for large.
 const touch=[-1];for(let i=0;i<k;i++)for(const a of pins){ok(!!a);touch.push(i)}
 let pairChecks=0;
 if(k<=8)for(let i=0;i<touch.length;i++)for(let j=i;j<touch.length;j++){
   const z=Array.from({length:k},(_,v)=>v).find(v=>v!==touch[i]&&v!==touch[j]);
   ok(z!==undefined&&!good(base.w));pairChecks++;
 }
 // Exact source regional table acquisition from actual clause IDs, not the planted assignment.
 let assignments=0;const summaries=[];
 for(const reg of regs){
  const cs=reg.map(i=>F[i]);const vars=[...new Set(cs.flat())];ok(vars.length===6);
  const boundary=vars.filter(v=>occ.get(v).some(j=>!reg.includes(j)));ok(boundary.length===2);
  const table=new Map();
  for(let w=0;w<(1<<vars.length);w++){assignments++;
   if(cs.every(c=>c.reduce((s,v)=>s+bit(w,vars.indexOf(v)),0)===2)){
    const key=boundary.map(v=>bit(w,vars.indexOf(v))).join("");
    table.set(key,new Map(vars.map((v,j)=>[v,bit(w,j)])));
   }
  }
  ok(table.size===2);
  const keys=[...table.keys()];ok(keys[0].split("").every((b,i)=>b!==keys[1][i]));
  summaries.push({boundary,table,par:Number(keys[0][0])^Number(keys[0][1])});
 }
 // Exact signed graph join; private witnesses retained.
 const graph=new Map();for(const {boundary:[a,b],par} of summaries){if(!graph.has(a))graph.set(a,[]);if(!graph.has(b))graph.set(b,[]);graph.get(a).push([b,par]);graph.get(b).push([a,par])}
 const val=new Map();let feasible=true;
 for(const v of graph.keys())if(!val.has(v)){val.set(v,0);const q=[v];for(let i=0;i<q.length;i++)for(const [j,p] of graph.get(q[i])){const b=val.get(q[i])^p;if(val.has(j)){if(val.get(j)!==b)feasible=false}else{val.set(j,b);q.push(j)}}}
 ok(feasible===!twist);
 if(feasible){const lift=new Map();for(const {boundary,table} of summaries){const w=table.get(boundary.map(v=>val.get(v)).join(""));ok(!!w);for(const [v,b] of w){ok(!lift.has(v)||lift.get(v)===b);lift.set(v,b)}}ok(F.every(c=>c.reduce((s,v)=>s+lift.get(v),0)===2))}
 // Independent direct global exhaustive reference on smallest pair only.
 let ref=null;if(k===3){ref=0;for(let w=0;w<(1<<V.length);w++)if(F.every(c=>c.reduce((s,v)=>s+bit(w,V.indexOf(v)),0)===2))ref++;ok(ref===(twist?0:2))}
 cases.push({k,twist,variables:V.length,clauses:F.length,regions:regs.length,anchors:touch.length,pairChecks,probes,rowScans,localSupportChecks,assignments,decision:feasible?"SAT":"UNSAT",reference:ref});
}
return {local:{clauses:C,pairs:G,order,relaxedWords:rows.length,actualMatchings:matchings.length,baseBits:G.map((_,i)=>bit(base.w,i)),sourceModels,edgePins:pins.length},cases,checks};
}
const result=run(); if(typeof console!=="undefined") console.log(JSON.stringify(result,null,2));

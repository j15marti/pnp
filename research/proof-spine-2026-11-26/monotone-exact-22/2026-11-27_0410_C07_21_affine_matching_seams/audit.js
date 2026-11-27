function audit(){
 const assert=(b,m)=>{if(!b)throw Error(m||"assert")};
 const fp=F=>{let h=2166136261;for(const c of JSON.stringify(F))h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;return h.toString(16).padStart(8,"0")};
 const copy=F=>JSON.parse(JSON.stringify(F));
 function meter(F){return {ticks:0,cap:Math.min(20000000,Math.pow(8*JSON.stringify(F).length,3))}}
 function tick(M,k=1){M.ticks+=k;if(M.ticks>M.cap)throw Error("CAP")}
 function make(k){
  const edges=[];for(let g=0;g<2;g++)for(let i=0;i<k;i++)for(let j=0;j<3;j++)edges.push([2*k*g+i,2*k*g+k+(i+j)%k]);
  const e0=edges.findIndex(e=>e[0]===0&&e[1]===k),e1=edges.findIndex(e=>e[0]===2*k&&e[1]===3*k);
  [edges[e0][1],edges[e1][1]]=[edges[e1][1],edges[e0][1]];
  const ports=Array.from({length:4*k},()=>[]),rows=[],wires=[];let n=2;
  for(const [u,v] of edges){let a=n++,b=n++,h=n++,j=n++;ports[u].push(a);ports[v].push(b);let z=rows.length;
   rows.push([a,h,0,1],[b,h,0,1],[a,j,0,1],[b,j,0,1]);wires.push({u,v,a,b,h,j,eq:[z,z+1,z+2,z+3]});}
  const occ=[];for(let v=0;v<4*k;v++){assert(ports[v].length===3);let b=(v>=k&&v<2*k)||(v>=2*k&&v<3*k)?2:1;occ.push(rows.length);rows.push([...ports[v],b===1?1:0]);}
  return {n,rows,guards:[[0,0],[1,1]],map:{k,wires,occ}};
 }
 function fano(){const t=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];return {n:14,rows:t.map((r,i)=>[...r,7+i]),guards:[],map:{t}}}
 function close(F,M,extra=[]){const d=Array(F.n).fill(-1);for(const [i,b] of [...F.guards,...extra]){if(d[i]>=0&&d[i]!==b)return null;d[i]=b}
  let change=true;while(change){change=false;for(const r of F.rows){tick(M,4);let a=r.filter(i=>d[i]<0),s=r.filter(i=>d[i]===1).length;if(s>2||s+a.length<2)return null;
   if(a.length&&(s===2||s+a.length===2)){for(const i of a)d[i]=s===2?0:1;change=true;}}}return d}
 function prep(F,d,M){let eq=[],occ=[];for(let i=0;i<F.rows.length;i++){tick(M,4);let r=F.rows[i],a=r.filter(x=>d[x]<0),b=2-r.filter(x=>d[x]===1).length;
   if(!a.length){assert(b===0);continue}if(a.length===2&&b===1)eq.push({i,a});else occ.push({i,a,b});}return {eq,occ}}
 // Track A: local occupancy closure and raw degree test, no equality contraction.
 function A(F,M){const d=close(F,M);if(!d)return {status:"UNSAT"};const p=prep(F,d,M),deg=Array(F.n).fill(0);
  for(const r of F.rows)for(const x of r)if(d[x]<0){tick(M);deg[x]++}
  return {status:"UNKNOWN",unpinned:d.filter(x=>x<0).length,rawMaxDegree:Math.max(...deg),affineRows:p.eq.length,occupancyRows:p.occ.length,localNonempty:p.occ.every(r=>r.b>0&&r.b<r.a.length)}}
 // Track B: independent complete GF2 relaxation of every original native row, with all actual guards.
 function B(F,M){const d=close(F,M);if(!d)return {status:"UNSAT"};let piv=new Map();
  for(const r of F.rows){let x=0n,b=0;for(const i of r){tick(M);if(d[i]<0)x^=1n<<BigInt(i);else b^=d[i]}
   while(x){tick(M);const l=x&-x;if(!piv.has(l)){piv.set(l,[x,b]);break}const [y,c]=piv.get(l);x^=y;b^=c}if(!x&&b)return {status:"UNSAT",rank:piv.size}}
  return {status:"UNKNOWN",rank:piv.size,free:d.filter(x=>x<0).length-piv.size,parityConsistent:true}}
 // C: original integer certificate, no quotient graph nor maxflow. Every coefficient is on original row ID.
 function C(F,M){const d=close(F,M);if(!d)return {status:"UNSAT",kind:"closure"};
  if(!F.map.k){let checked=0;for(let t=0;t<128;t++){let a=Array.from({length:7},(_,i)=>(t>>i)&1);let w=[];for(let i=0;i<7;i++){tick(M,4);let b=2-F.rows[i].slice(0,3).reduce((s,j)=>s+a[j],0);w.push(b)}checked++;if(w.every(b=>b===0||b===1)){assert(F.rows.every(r=>r.reduce((s,j)=>s+[...a,...w][j],0)===2));return {status:"SAT",checked}}}return {status:"UNSAT",kind:"native-exhaustive-completions",checked}}
  const {k,occ,wires}=F.map,weights=Array(F.rows.length).fill(0);for(let i=0;i<2*k;i++)weights[occ[i]]=i<k?-1:1;
  for(const e of wires){tick(M);const u=e.u<k?-1:e.u<2*k?1:0;weights[e.eq[0]]-=u;weights[e.eq[1]]+=u;}
  const coef=Array(F.n).fill(0);let rhs=0;for(let i=0;i<F.rows.length;i++){let w=weights[i];if(w)for(const x of F.rows[i]){tick(M);coef[x]+=w}rhs+=2*w}
  for(const [x,v] of F.guards){rhs-=v*coef[x];coef[x]=0}
  const upper=coef.reduce((s,c)=>s+Math.max(c,0),0);assert(rhs>upper,"invalid certificate");return {status:"UNSAT",kind:"integer-linear-cut",rhs,upper,rowsUsed:weights.filter(Boolean).length,nonzero:coef.map((c,i)=>[i,c]).filter(x=>x[1]),weights:weights.map((c,i)=>[i,c]).filter(x=>x[1])}}
 // Hybrid: source-only signed equality contraction. Matching operates on exact common variables, not independent ports.
 function I(F,M){let d=close(F,M);if(!d)return {status:"UNSAT",kind:"closure"};let p=prep(F,d,M);
  let a=Array.from({length:F.n},()=>[]);for(const r of p.eq){let [u,v]=r.a;a[u].push(v);a[v].push(u);tick(M,2)}
  const root=Array(F.n).fill(-1),sign=Array(F.n).fill(-1),classes=new Map();
  for(let i=0;i<F.n;i++)if(d[i]<0&&root[i]<0){let q=[i];root[i]=i;sign[i]=0;classes.set(i,[]);for(let j=0;j<q.length;j++)for(const v of a[q[j]]){tick(M);if(root[v]<0){root[v]=i;sign[v]=sign[q[j]]^1;q.push(v)}else if(sign[v]==sign[q[j]])return {status:"UNSAT",kind:"affine-cycle"}}}
  // The only imported relation is actual pair complement. Recheck all original source rows after import;
  // no new unary pin is implied by a consistent unpinned complement component.
  for(const r of p.eq){tick(M);assert(root[r.a[0]]===root[r.a[1]]&&sign[r.a[0]]!==sign[r.a[1]])}
  let d2=close(F,M);assert(JSON.stringify(d2)===JSON.stringify(d),"closure changed");
  const b=p.occ.map(r=>r.b);for(let j=0;j<p.occ.length;j++)for(const x of p.occ[j].a){tick(M);classes.get(root[x]).push({j,x,s:sign[x]})}
  let edges=[],bad=[],single=0,opposite=0;
  for(const [c,ps] of classes){tick(M);if(ps.length===0)continue;if(ps.length>2){bad.push({c,arity:ps.length});continue}
   if(ps.length===1){single++;continue}if(ps[0].s!==ps[1].s){let j=b.length;b.push(1);edges.push([ps[0].j,j],[ps[1].j,j]);opposite++}else edges.push([ps[0].j,ps[1].j]);}
  if(bad.length||single)return {status:"UNKNOWN",kind:"nonadmitted",bad:bad.length,single,classes:classes.size,maxPorts:Math.max(0,...Array.from(classes.values(),ps=>ps.length))};
  // Exact b-factor on bipartite transformed graph via integral max flow. Nonbipartite branch not implemented here.
  const adj=b.map(()=>[]);for(const [u,v] of edges){adj[u].push(v);adj[v].push(u)}
  const side=b.map(()=>-1);for(let i=0;i<b.length;i++)if(side[i]<0){side[i]=0;let q=[i];for(let z=0;z<q.length;z++)for(const v of adj[q[z]]){tick(M);if(side[v]<0){side[v]=1-side[q[z]];q.push(v)}else if(side[v]===side[q[z]])return {status:"UNKNOWN",kind:"nonbipartite"}}}
  const s=b.length,t=s+1,g=Array.from({length:t+1},()=>[]);function add(u,v,c){const x={v,c,rev:g[v].length},y={v:u,c:0,rev:g[u].length};g[u].push(x);g[v].push(y)}
  let demandL=0,demandR=0;for(let i=0;i<b.length;i++){if(side[i]===0){add(s,i,b[i]);demandL+=b[i]}else{add(i,t,b[i]);demandR+=b[i]}}
  if(demandL!==demandR)return {status:"UNSAT",kind:"total",demandL,demandR};
  for(let [u,v] of edges){if(side[u]) [u,v]=[v,u];add(u,v,1)}
  let flow=0;while(true){const seen=Array(g.length).fill(false),prev=Array(g.length).fill(null),q=[s];seen[s]=true;
   for(let i=0;i<q.length&&!seen[t];i++)for(let j=0;j<g[q[i]].length;j++){tick(M);let e=g[q[i]][j];if(e.c>0&&!seen[e.v]){seen[e.v]=true;prev[e.v]=[q[i],j];q.push(e.v)}}
   if(!seen[t]){let cut=0;for(let i=0;i<b.length;i++){if(side[i]===0&&!seen[i])cut+=b[i];if(side[i]===1&&seen[i])cut+=b[i]}for(let [u,v] of edges){tick(M);if(side[u])[u,v]=[v,u];if(seen[u]&&!seen[v])cut++}
    assert(cut===flow);return {status:flow<demandL?"UNSAT":"FEASIBLE",kind:"flow-cut",flow,demand:demandL,cut,cutVertices:seen.slice(0,b.length).map((x,i)=>x?i:-1).filter(x=>x>=0),classes:classes.size,edges:edges.length,opposite}}
   let f=Infinity;for(let v=t;v!==s;){let [u,j]=prev[v];f=Math.min(f,g[u][j].c);v=u}for(let v=t;v!==s;){let [u,j]=prev[v],e=g[u][j];e.c-=f;g[v][e.rev].c+=f;v=u;tick(M)}flow+=f;
  }
 }
 const jobs=[];for(const F of [4,8,16,32,64,128].map(make).concat([fano()])){
  const h=fp(F);assert(F.rows.every(r=>r.length===4&&new Set(r).size===4&&r.every(x=>x>=0&&x<F.n)));
  const r={fingerprint:h,k:F.map.k||0,n:F.n,m:F.rows.length,N:8*JSON.stringify(F).length,guards:F.guards,tracks:{}};
  for(const [name,f] of [["A",A],["B",B],["C",C],["I",I]]){let G=copy(F),M=meter(F);assert(fp(G)===h);let z;try{z=f(G,M)}catch(e){if(e.message!=="CAP")throw e;z={status:"UNKNOWN",kind:"cap"}}r.tracks[name]={...z,meter:M}}
  assert(r.tracks.C.status==="UNSAT"&&(!r.k||r.tracks.I.status==="UNSAT"));jobs.push(r);
 }
 // Hostile Fano: explicit all-value modulator; native closure is exact on fully fixed seven original IDs.
 let F=fano(),M=meter(F),branches=0;for(let t=0;t<128;t++){tick(M);const g=Array.from({length:7},(_,i)=>[i,(t>>i)&1]);assert(close(F,M,g)===null);branches++}
 return {jobs,hostileModulator:{branches,meter:M},source:"deterministic generators in audit.js, original guards retained; FNV32 noncryptographic"} 
}
console.log(JSON.stringify(audit(),null,2));

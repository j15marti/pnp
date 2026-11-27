function replay(raw){
 const check=(c,m)=>{if(!c)throw Error(m||"check")};
 function make(k){
  const edges=[];for(let g=0;g<2;g++)for(let i=0;i<k;i++)for(let j=0;j<3;j++)edges.push([2*k*g+i,2*k*g+k+(i+j)%k]);
  const e0=edges.findIndex(e=>e[0]===0&&e[1]===k),e1=edges.findIndex(e=>e[0]===2*k&&e[1]===3*k);
  [edges[e0][1],edges[e1][1]]=[edges[e1][1],edges[e0][1]];
  const ports=Array.from({length:4*k},()=>[]),rows=[],wires=[];let n=2;
  for(const [u,v] of edges){let a=n++,b=n++,h=n++,j=n++;ports[u].push(a);ports[v].push(b);let z=rows.length;
   rows.push([a,h,0,1],[b,h,0,1],[a,j,0,1],[b,j,0,1]);wires.push({u,v,a,b,h,j,eq:[z,z+1,z+2,z+3]});}
  const occ=[];for(let v=0;v<4*k;v++){let b=(v>=k&&v<2*k)||(v>=2*k&&v<3*k)?2:1;occ.push(rows.length);rows.push([...ports[v],b===1?1:0]);}
  return {n,rows,guards:[[0,0],[1,1]],map:{k,wires,occ}};
 }
 function fp(F){let h=2166136261;for(const c of JSON.stringify(F))h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;return h.toString(16).padStart(8,"0")}
 const out=[];
 for(const job of raw.jobs.filter(j=>j.k)){
  const F=make(job.k),t=job.tracks.I;check(fp(F)===job.fingerprint);const cap=job.tracks.I.meter.cap;let ticks=0;const tick=(n=1)=>{ticks+=n;check(ticks<=cap,"CAP")};let guards=new Map(F.guards),occ=[],eq=Array.from({length:F.n},()=>[]),weights=Array(F.rows.length).fill(0);
  for(let i=0;i<F.rows.length;i++){let r=F.rows[i],b=2-r.reduce((s,x)=>s+(guards.get(x)||0),0),a=r.filter(x=>!guards.has(x));tick(4);
   if(a.length===2&&b===1){eq[a[0]].push([a[1],i]);eq[a[1]].push([a[0],i])}else occ.push({i,b,a})}
  const ports=Array.from({length:F.n},()=>[]);occ.forEach((r,i)=>r.a.forEach(x=>ports[x].push(i)));
  let seen=new Set(),connections=[];
  for(let v=0;v<F.n;v++)if(!guards.has(v)&&!seen.has(v)){
   const q=[v],prev=new Map([[v,null]]);seen.add(v);for(let i=0;i<q.length;i++)for(const [x,r] of eq[q[i]]){tick();if(!seen.has(x)){seen.add(x);prev.set(x,[q[i],r]);q.push(x)}}
   const hits=q.flatMap(x=>ports[x].map(j=>({x,j})));check(hits.length===2,"two ports");
   const [a,b]=hits;const search=[a.x],pp=new Map([[a.x,null]]);for(let i=0;i<search.length&&!pp.has(b.x);i++)for(const [x,r] of eq[search[i]]){tick();if(!pp.has(x)){pp.set(x,[search[i],r]);search.push(x)}}
   check(pp.has(b.x));let path=[];for(let x=b.x;x!==a.x;){let [y,r]=pp.get(x);path.push(r);x=y}path.reverse();check(path.length%2===0,"same sign");
   connections.push({a,b,path});
  }
  let adj=occ.map(()=>[]);for(const {a,b} of connections){adj[a.j].push(b.j);adj[b.j].push(a.j)}
  let side=occ.map(()=>-1);for(let i=0;i<side.length;i++)if(side[i]===-1){side[i]=0;let q=[i];for(let j=0;j<q.length;j++)for(let x of adj[q[j]]){tick();if(side[x]===-1){side[x]=side[q[j]]^1;q.push(x)}else check(side[x]!==side[q[j]])}}
  const S=new Set(t.cutVertices);for(let i=0;i<occ.length;i++)if(S.has(i))weights[occ[i].i]=side[i]===0?1:-1;
  for(const {a,b,path} of connections){let w=weights[occ[a.j].i];for(let i=0;i<path.length;i++){tick();weights[path[i]]-=w*(i%2===0?1:-1)}}
  // Verifier below knows ONLY original rows, actual pins and multipliers, no flow, no quotient.
  function verify(w){
   let c=Array(F.n).fill(0),rhs=0;for(let i=0;i<F.rows.length;i++){check(Number.isSafeInteger(w[i]));rhs+=2*w[i];if(w[i])for(const x of F.rows[i]){tick();c[x]+=w[i]}}
   for(const [x,b] of F.guards){rhs-=b*c[x];c[x]=0}
   let ub=c.reduce((s,z)=>s+Math.max(z,0),0);return {rhs,ub,margin:rhs-ub,nonzero:c.map((a,i)=>[i,a]).filter(x=>x[1])}
  }
  let v=verify(weights);check(v.margin===t.demand-t.flow&&v.margin>0,"cut mismatch");check(verify(weights.map(()=>0)).margin===0,"zero falsifier");
  out.push({k:job.k,fingerprint:job.fingerprint,flowMargin:t.demand-t.flow,rowsUsed:weights.filter(Boolean).length,certificate:weights.map((w,i)=>[i,w]).filter(x=>x[1]),verification:v,ticks,cap});
 }
 return out;
}
const fs=require('fs'); console.log(JSON.stringify(replay(JSON.parse(fs.readFileSync(process.argv[2]||'results.json','utf8'))),null,2));

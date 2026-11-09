#!/usr/bin/env node
// LSPV-3/522 source-indexed mod-3 Tseitin finite pair-flow control.
// NOT a historical mixed checker or unrestricted proof-size theorem.
function run() {
 const cases={
  K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
  K33:[6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])],
  cube:[8,Array.from({length:8},(_,v)=>[0,1,2].map(b=>[v,v^(1<<b)]).filter(p=>p[0]<p[1])).flat()],
  Petersen:[10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,((i+2)%5)+5]),...Array.from({length:5},(_,i)=>[i,i+5])]]
 };
 const mod=x=>((x%3)+3)%3,result=[];
 for(const [name,[h,raw]] of Object.entries(cases)) {
  const edges=raw.map(e=>e.slice().sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),m=edges.length;
  if(m*2!==3*h)throw Error("not cubic");
  const incident=Array.from({length:h},()=>[]);
  edges.forEach(([a,b],i)=>{incident[a].push(i);incident[b].push(i)});
  const sign=(v,i)=>edges[i][0]===v?1:-1;
  const parent=Array(h).fill(-1),pe=Array(h).fill(-1),order=[0];parent[0]=0;
  for(let k=0;k<order.length;k++){let v=order[k];for(let i of incident[v]){
    let w=edges[i][0]===v?edges[i][1]:edges[i][0];
    if(parent[w]===-1){parent[w]=v;pe[w]=i;order.push(w)}
  }}
  if(order.length!==h)throw Error("disconnected");
  const tree=new Set(pe.slice(1)),free=edges.map((_,i)=>i).filter(i=>!tree.has(i));
  function flow(d,vals) {
   const z=Array(m).fill(0),r=d.slice();
   free.forEach((ei,j)=>{let v=vals[j],[a,b]=edges[ei];z[ei]=v;r[a]=mod(r[a]-v);r[b]=mod(r[b]+v)});
   for(let k=order.length-1;k>=1;k--){let v=order[k],ei=pe[v],x=mod(sign(v,ei)*r[v]),[a,b]=edges[ei];
    z[ei]=x;r[a]=mod(r[a]-x);r[b]=mod(r[b]+x)}
   if(r.some(x=>x!==0))throw Error("flow fails");
   return z;
  }
  const b=Array(h).fill(0);b[0]=1;
  const counts=[];let tested=0,checks=0;
  for(let u=0;u<h;u++)for(let v=u+1;v<h;v++) {
    const d=b.slice();d[u]=mod(d[u]+1);d[v]=mod(d[v]+1);
    const seen=new Set(),samples=3**free.length;
    for(let j=0;j<samples;j++){
      let x=j,vals=free.map(()=>{let r=x%3;x=Math.floor(x/3);return r});
      const z=flow(d,vals);
      for(let w=0;w<h;w++){
       const div=mod(incident[w].reduce((s,ei)=>s+sign(w,ei)*z[ei],0));
       if(div!==d[w])throw Error("bad divergence");checks++;
      }
      const a=incident[u].map(i=>z[i]).join(""),c=incident[v].map(i=>z[i]).join("");
      seen.add(a+":"+c);tested++;
    }
    const adjacent=edges.some(e=>e[0]===u&&e[1]===v),want=adjacent?27:81;
    if(seen.size!==want)throw Error(name+" pair "+u+","+v+": "+seen.size+" expected "+want);
    counts.push({u,v,adjacent,reachable_pair_patterns:seen.size});
  }
  result.push({graph:name,h,edge_count:m,cycle_dimension:free.length,source_clauses:39*h/2,
    exact_min_unsat_source_core:39*h/2-9,unit_binary_source_work_lower_bound:39*h/2-10,
    pair_flow_assignments_tested:tested,divergence_assertions:checks,
    distinct_pair_flow_patterns:counts.reduce((s,x)=>s+x.reachable_pair_patterns,0),
    pair_counts:counts});
 }
 return {status:"COMPUTATIONAL pair-flow checks; symbolic theorem separately proved",models:result,
    total_pair_flow_assignments:result.reduce((s,x)=>s+x.pair_flow_assignments_tested,0),
    total_divergence_assertions:result.reduce((s,x)=>s+x.divergence_assertions,0)};
}
if(typeof module!=="undefined"&&module.exports){module.exports={run};if(require.main===module)console.log(JSON.stringify(run(),null,2))}

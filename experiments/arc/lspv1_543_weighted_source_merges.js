// LSPV-1/543 independent JavaScript partition-domain CEGAR ceiling verifier.
// Exports run() for deterministic replay; no native R_mix341 rule is implemented.
function canon(parts) { return parts.map(p=>[...p].sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]); }
function key(parts) { return parts.map(p=>p.join(',')).join('|'); }
function merge(parts, idx) {
  const keep=[], all=[];
  for(let i=0;i<parts.length;i++) (idx.includes(i) ? all : keep).push(...(idx.includes(i)?parts[i]:[parts[i]]));
  keep.push(all.sort((a,b)=>a-b));
  return canon(keep);
}
function choose(n,k,fn,prefix=[],start=0) {
  if(prefix.length===k) { fn(prefix); return; }
  for(let i=start;i<n;i++) choose(n,k,fn,[...prefix,i],i+1);
}
function exactGraph(m,types){
  const init=canon(Array.from({length:m},(_,i)=>[i]));
  let states=new Map([[key(init),{parts:init,d:0}]]);
  let queue=[{parts:init,d:0}], processed=0;
  while(queue.length){
    queue.sort((a,b)=>a.d-b.d);
    const s=queue.shift(),sk=key(s.parts);
    if(s.d!==states.get(sk).d) continue;
    processed++;
    if(s.parts.length===1) return {cost:s.d,states:states.size,processed};
    for(const [arity,cost] of types){
      for(let k=2;k<=Math.min(arity,s.parts.length);k++){
        choose(s.parts.length,k,indices=>{
          const p=merge(s.parts,indices),ky=key(p),d=s.d+cost;
          if(!states.has(ky)||d<states.get(ky).d){
            states.set(ky,{parts:p,d});queue.push({parts:p,d});
          }
        });
      }
    }
  }
  throw new Error('no goal; an allowed arity >=2 is required');
}
function exactKnapsack(m,types) {
  const D=Array(m).fill(Infinity);D[0]=0;
  for(let p=1;p<m;p++) for(const [r,c] of types)
    if(r>=2) D[p]=Math.min(D[p],c+D[Math.max(0,p-(r-1))]);
  return D[m-1];
}
function run(){
  const typesList=[
    [[2,1]],[[2,1],[3,2]],[[2,1],[4,1]],[[3,2]],
    [[4,0],[2,1]],[[2,3],[3,1]],[[2,2],[3,4],[4,3]]
  ];
  const results=[];let assertions=0;
  for(const types of typesList)for(let m=2;m<=6;m++){
    const g=exactGraph(m,types),dp=exactKnapsack(m,types);
    if(g.cost!==dp)throw Error(JSON.stringify({m,types,g,dp}));assertions++;
    const rho=Math.min(...types.map(([r,w])=>w/(r-1)));
    if(dp+1e-9<(m-1)*rho)throw Error('potential lower bound violated');assertions++;
    const witness=types.filter(([r,w])=>w/(r-1)===rho);
    if(dp>(m-1)*rho+Math.min(...witness.map(x=>x[1]))+1e-9)throw Error('ceiling violated');assertions++;
    results.push({m,types,dp,partitionsSeen:g.states,processed:g.processed});
  }
  const macro=exactKnapsack(16,[[2,1],[16,1]]);
  if(macro!==1)throw Error('macro control');assertions++;
  const binary=exactKnapsack(16,[[2,1]]);
  if(binary!==15)throw Error('binary control');assertions++;
  const zero=exactKnapsack(32,[[2,1],[32,0]]);
  if(zero!==0)throw Error('zero-cost closure control');assertions++;
  return {run:'LSPV-1/543',mode:'explicit partition-state Dijkstra plus independent integer knapsack DP',status:'COMPUTATIONAL',cases:results.length,assertions,macro,binary,zero,results};
}

if (typeof console !== 'undefined') console.log(JSON.stringify(run(),null,2));

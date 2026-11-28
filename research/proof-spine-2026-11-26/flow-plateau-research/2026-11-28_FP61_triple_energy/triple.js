function triple(ctx, E, guard=[], maxEvents=2600000) {
 const F=ctx.chart, P=new Map(guard), m=F.length;
 let ledger={},total=0;function tick(k,n=1){if(total+n>maxEvents)throw Error("CAP");ledger[k]=(ledger[k]||0)+n;total+=n}
 const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const scope=fs=>[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b);
 const valid=(f,w)=>f.vs.every((v,i)=>!P.has(v)||P.get(v)===((w>>i)&1));
 const init=F.map(f=>f.cost.map((z,w)=>valid(f,w)?z:Infinity));
 const B=init.map(r=>r.slice()),proofs=[],pair=[],trips=[],adj=F.map(()=>new Set());let stage="pair",stopped=null,stages=[],global=0;
 function compute(ids,compressed=true){
  let fs=ids.map(i=>F[i]),U=scope(fs),W=U.filter(v=>!P.has(v)), maps=fs.map(f=>f.vs.map(v=>W.indexOf(v)));
  let rows=fs.map(f=>Array(f.cost.length).fill(Infinity)),min=Infinity;
  for(let a=0;a<2**W.length;a++){
   let ws=fs.map((f,i)=>f.vs.reduce((w,v,j)=>w|((P.has(v)?P.get(v):(a>>maps[i][j])&1)<<j),0));
   let z=0;for(let i=0;i<fs.length;i++){tick("joinReads");z+=fs[i].cost[ws[i]]}
   if(compressed)z=Math.min(4,z);
   min=Math.min(min,z);for(let i=0;i<fs.length;i++){tick("projectionWrites");rows[i][ws[i]]=Math.min(rows[i][ws[i]],z)}
  }
  return {rows,min,U};
 }
 function merge(ids){
  const a=compute(ids);let changed=[];
  for(let j=0;j<ids.length;j++){let i=ids[j];for(let w=0;w<B[i].length;w++){tick("compare");if(Number.isFinite(B[i][w])&&a.rows[j][w]>B[i][w]){B[i][w]=a.rows[j][w];changed.push([i,w,B[i][w]])}}}
  global=Math.max(global,a.min);if(changed.length)proofs.push({ids,changed,min:a.min,U:a.U});return a.min;
 }
 function stats(name){return {name,global:Math.max(global,...B.map(r=>Math.min(...r))),zeroExcluded:B.reduce((n,r,i)=>n+r.filter((z,w)=>init[i][w]===0&&z>0).length,0),threshold2Excluded:B.reduce((n,r,i)=>n+r.filter((z,w)=>init[i][w]<=2&&z>2).length,0),total,proofs:proofs.length}}
 try{
  for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){tick("pairScan");if(F[i].vs.some(v=>F[j].vs.includes(v))){adj[i].add(j);adj[j].add(i);if(scope([F[i],F[j]]).filter(v=>!P.has(v)).length<=5)pair.push([i,j])}}
  for(const p of pair)merge(p);
  stages.push(stats("pairs"));stage="triples";
  // enumerate connected triples by a center; dedup; fixed width5. Charge candidate-generation even if discarded.
  const seen=new Set();for(let j=0;j<m;j++){let ns=[...adj[j]].sort((a,b)=>a-b);for(let a=0;a<ns.length;a++)for(let k=a+1;k<ns.length;k++){tick("tripleScan");let t=[j,ns[a],ns[k]].sort((a,b)=>a-b),key=t.join(",");if(seen.has(key))continue;seen.add(key);if(scope(t.map(i=>F[i])).filter(v=>!P.has(v)).length<=5)trips.push(t)}}
  for(const t of trips)merge(t);
  stages.push(stats("triples"));
 }catch(e){stopped=String(e);stages.push(stats(stage+" partial"))}
 // Independent scalar verification, uncompressed, using Cartesian product of factor rows compatible on shared variable bits.
 // Verify every strict improvement (including positive-energy thresholds); no inferred energy sums across overlapping clusters.
 let verifyReads=0,verifyJoins=0,verifyRows=0;let replay=init.map(r=>r.slice());
 for(const p of proofs){let fs=p.ids.map(i=>F[i]),exact=fs.map(f=>Array(f.cost.length).fill(Infinity)),best=Infinity;
  function rec(j,A,W,z){if(j===fs.length){verifyJoins++;best=Math.min(best,z);W.forEach((w,k)=>exact[k][w]=Math.min(exact[k][w],z));return}
   let f=fs[j];for(let w=0;w<f.cost.length;w++){verifyRows++;let M=new Map(A),ok=true;for(let k=0;k<f.vs.length;k++){verifyReads++;let v=f.vs[k],b=(w>>k)&1;if(M.has(v)&&M.get(v)!==b){ok=false;break}M.set(v,b)}if(ok)rec(j+1,M,[...W,w],z+f.cost[w])}
  }
  rec(0,P,[],0);if(Math.min(4,best)!==p.min)throw Error("bad join minimum");for(let [i,w,z] of p.changed){if(Math.min(4,exact[p.ids.indexOf(i)][w])!==z||z<=replay[i][w])throw Error("invalid row");replay[i][w]=z}
 }
 // Check all committed row updates (a cap can interrupt a join's update loop; don't credit unfinished updates)
 if(!stopped&&!same(B,replay))throw Error("replay mismatch");
 let reduced=F.map((f,i)=>({...f,cost:f.cost.map((z,w)=>replay[i][w]>0&&z===0?2:z)}));
 // guard-incompatible rows removed only under explicit guard, used for zero-energy decision only.
 const zero=ctx.support(F,guard),hybrid=ctx.support(reduced,guard);
 return {guard,stages,pairCount:pair.length,tripleCount:trips.length,stopped,ledger,total,maxEvents,proofs,verify:{reads:verifyReads,joins:verifyJoins,rows:verifyRows},zero,hybrid,final:replay.map(r=>r.map(x=>Number.isFinite(x)?x:null)),reduced};
}
function feedback(C,V,residue,init){
 let A=new Map(V.map(v=>[v,init])),visits=0,flips=[],ties=0;const mod=x=>((x%3)+3)%3;
 function evalA(){let u=0,z=0,table=[];for(let c of C){let k=0,s=0;for(let l of c){visits++;let b=A.get(Math.abs(l)-1)||0,t=l>0?b:b-1;k+=t*t;s+=t}u+=k===0;z+=k>0&&mod(s)===0;table.push([k,mod(k),mod(s)])}return {u,z,table}}
 let q=evalA(),start=q.u;for(let step=0;step<Math.min(4*V.length,100);step++){let best=q.u,options=[];for(let v of V){A.set(v,1-A.get(v));let t=evalA();A.set(v,1-A.get(v));if(t.u<best){best=t.u;options=[]}if(t.u===best&&best<q.u)options.push([v,t])}if(!options.length)break;options.sort((a,b)=>a[0]-b[0]);let normal=options[0],chosen=residue?options.slice().sort((a,b)=>a[1].z-b[1].z||a[0]-b[0])[0]:normal;ties+=chosen[0]!==normal[0];A.set(chosen[0],1-A.get(chosen[0]));q=chosen[1];flips.push([chosen[0],q.u,q.z])}
 return {init,residue,start,end:q.u,visits,ties,flips,assignment:[...A],table:q.table};
}
if(typeof module!=="undefined")module.exports={triple,feedback};

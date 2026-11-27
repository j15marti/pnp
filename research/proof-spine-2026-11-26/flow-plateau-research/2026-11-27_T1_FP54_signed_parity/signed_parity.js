function parityExperiment(ctx,E,G,prior,instance,sha){
 const {chart,F,V,gauge,n,trace}=ctx;
 if(!F.every(f=>f.cost.every(c=>c>=0&&Number.isInteger(c)&&c%2===0)))throw Error("non-even chart");
 const all=prior.eligible;
 // Signed scores for every original native B-port: sign +1 if root positive, -1 if negative; truth square = actual occupancy.
 let signedChecks=0;
 for(const f of n.factors){const v=f.ids[0];for(let w=0;w<f.cost.length;w++){let Q=0,D=0;for(let j=0;j<4;j++){let p=4*v+j,r=n.roots[p],s=n.sg[p],x=r===gauge?0:(w>>f.vs.indexOf(r))&1;let t=s?x-1:x;Q+=t*t;D+=t;signedChecks++}if(Number(Q!==2)!==f.cost[w]||(Q+D)%2||(Q-D)%2)throw Error("signed occupancy mismatch")}}
 // Local exact degree-d Boolean polynomial annihilators, by column-dependence of evaluation vectors.
 // Variables represented by BigInt squarefree masks. A row is XOR of distinct monomials.
 const pop=x=>{let k=0;while(x){x&=x-1n;k++}return k};
 const hi=x=>{const s=x.toString(16);return 4*(s.length-1)+Math.floor(Math.log2(parseInt(s[0],16)))};
 const counters={localEvaluations:0,localXors:0,multipliedTerms:0,globalXors:0,checkEvaluations:0,checkTerms:0,generated:0};
 const cap=6000000;
 const tick=()=>{if(Object.values(counters).reduce((s,v)=>s+v,0)>cap)throw Error("parity cap")};
 function monomials(vs,d){const A=[0n];function rec(start,left,m){if(!left)return;for(let j=start;j<vs.length;j++){let q=m|(1n<<BigInt(vs[j]));A.push(q);rec(j+1,left-1,q)}}rec(0,d,0n);return A}
 function makeRows(pins,d,allowedId=-1){
  const P=new Map(pins),free=V.filter(v=>!P.has(v)),at=new Map(free.map((v,i)=>[v,i])),M=monomials(free.map((_,i)=>i),d),mi=new Map(M.map((v,i)=>[v,i])),rows=[];
  for(const f of chart){
   let ids=f.vs.filter(v=>at.has(v)).map(v=>at.get(v)),localM=monomials(ids,d);
   let good=[];
   for(let w=0;w<f.cost.length;w++){counters.localEvaluations++;if((allowedId===f.i?f.cost[w]===2:f.cost[w]===0)&&f.vs.every((v,j)=>!P.has(v)||P.get(v)===((w>>j)&1))){let word=0n;f.vs.forEach((v,j)=>{if(at.has(v)&&((w>>j)&1))word|=1n<<BigInt(at.get(v))});good.push(word)}}
   // If there are no allowed words, polynomial 1 valid (empty relation).
   let B=new Map(),basis=[];
   for(let j=0;j<localM.length;j++){
    let col=0n;for(let i=0;i<good.length;i++){counters.localEvaluations++;if((localM[j]&good[i])===localM[j])col|=1n<<BigInt(i)}
    let proof=1n<<BigInt(j);
    while(col){let p=hi(col);if(!B.has(p)){B.set(p,[col,proof]);break}let b=B.get(p);col^=b[0];proof^=b[1];counters.localXors++}
    if(!col){let poly=localM.filter((_,i)=>Boolean((proof>>BigInt(i))&1n));basis.push(poly)}
   }
   for(const poly of basis){
    let degree=Math.max(...poly.map(pop));
    for(const mult of monomials(free.map((_,i)=>i),d-degree)){
     let row=0n;for(const m of poly){counters.multipliedTerms++;row^=1n<<BigInt(mi.get(m|mult))}
     if(row){rows.push({row,owner:f.i,poly:poly.map(String),mult:String(mult)});counters.generated++}
    }
   }
   tick();
  }
  return {pins,d,free,M,rows,allowedId};
 }
 function solve(rowsObj,drop,reverse=false){
  const B=new Map(),rows=rowsObj.rows,ds=new Set(drop);
  let order=rows.map((_,i)=>i);if(reverse)order.reverse();
  for(const i of order){let r=rows[i];if(ds.has(r.owner))continue;let x=r.row,z=1n<<BigInt(i);
   while(x){let k=hi(x);if(!B.has(k)){if(k===0){let ids=[];for(let t=0;t<rows.length;t++)if((z>>BigInt(t))&1n)ids.push(t);const owners=[...new Set(ids.map(t=>rows[t].owner))];return {status:"UNSAT",rank:B.size,ids,owners}}B.set(k,[x,z]);break}let b=B.get(k);x^=b[0];z^=b[1];counters.globalXors++;if((counters.globalXors&1023)===0)tick();}
  }
  return {status:"UNKNOWN",rank:B.size};
 }
 // Independent certificate checker: verify each original polynomial on allowed local rows; multiply directly and XOR monomial strings.
 function verify(R,s,drop){
  if(s.status!=="UNSAT")return null;
  const out=new Set(),P=new Map(R.pins),at=new Map(R.free.map((v,i)=>[v,i]));
  for(const id of s.ids){let row=R.rows[id],f=chart[row.owner];if(drop.includes(f.i))throw Error("dropped factor used");let poly=row.poly.map(BigInt),mult=BigInt(row.mult);
   for(let w=0;w<f.cost.length;w++)if((R.allowedId===f.i?f.cost[w]===2:f.cost[w]===0)&&f.vs.every((v,j)=>!P.has(v)||P.get(v)===((w>>j)&1))){let word=0n;f.vs.forEach((v,j)=>{if(at.has(v)&&((w>>j)&1))word|=1n<<BigInt(at.get(v))});let val=0;for(const p of poly){counters.checkEvaluations++;val^=Number((p&word)===p)}if(val)throw Error("invalid vanishing identity")}
   for(const p of poly){let m=String(p|mult);counters.checkTerms++;if(out.has(m))out.delete(m);else out.add(m)}
  }
  if(out.size!==1||!out.has("0"))throw Error("bad polynomial identity");
  tick();return s.ids.map(i=>({owner:R.rows[i].owner,poly:R.rows[i].poly,mult:R.rows[i].mult}));
 }
 // Root and guarded parity algebra, independent of imported proof trees.
 let root=[],cells=[],unknownReason=null;
 try{
 for(const d of [1,2,3]){const R=makeRows([],d);let s=solve(R,[]);root.push({d,rows:R.rows.length,cols:R.M.length,rank:s.rank,status:s.status,owners:s.owners,certificate:verify(R,s,[])});}
 // each exact FP53 guard-coordinate cell; use all parity certs to exclude single-defect support outside cores.
 const guardVars=prior.guardProjection.vs, candidates=new Set(all);
 for(let mask=0;mask<2**guardVars.length;mask++){
  const pins=guardVars.map((v,j)=>[v,(mask>>j)&1]);
  let start=all.slice(),live=new Set(start),attempts=[],R=makeRows(pins,3),q=solve(R,[]);
  if(q.status==="UNSAT"){
    const cert=verify(R,q,[]);for(const i of live)if(!q.owners.includes(i))live.delete(i);
    attempts.push({drop:[],status:q.status,rank:q.rank,owners:q.owners,certificate:cert,removed:start.length-live.size});
  }else attempts.push({drop:[],status:q.status,rank:q.rank});
  // Independent row eligibility under exact pins; no imported core screen used until after this lane.
  for(const i of live){let f=chart[i];if(!f.cost.some((z,w)=>z===2&&f.vs.every((v,j)=>!guardVars.includes(v)||((mask>>guardVars.indexOf(v))&1)===((w>>j)&1))))live.delete(i)}
  const beforeBlocks=live.size;
  let queue=[[...live]],probeLimit=15,probe=0;
  while(queue.length&&live.size&&probe<probeLimit){let D=queue.shift().filter(i=>live.has(i));if(!D.length)continue;probe++;const s=solve(R,D);
   if(s.status==="UNSAT"){let cert=verify(R,s,D),before=live.size;for(const i of live)if(!s.owners.includes(i))live.delete(i);attempts.push({drop:D,status:s.status,rank:s.rank,owners:s.owners,certificate:cert,removed:before-live.size});}
   else{attempts.push({drop:D,status:"UNKNOWN",rank:s.rank});if(D.length>1){let mid=Math.ceil(D.length/2);queue.unshift(D.slice(0,mid),D.slice(mid));}}
  }
  cells.push({mask,pins,rows:R.rows.length,cols:R.M.length,start:start.length,beforeBlocks,remaining:[...live],attempts});
 }
 }catch(e){unknownReason=String(e)}
 // Replay FP53 acquired conditional cores independently before comparing. Root proof and guard-projected support domains.
 let importChecks=0;
 for(const x of prior.local){const sub=chart.filter(f=>x.core.includes(f.i));importChecks+=ctx.replayTree(sub,x.pins,x.tree,500000).rows;}
 for(const x of prior.peer){const sub=chart.filter(f=>x.core.includes(f.i));importChecks+=ctx.replayTree(sub,x.pins,x.tree,500000).rows;}
 importChecks+=ctx.replayTree(chart.filter(f=>prior.root.tree.core.includes(f.i)),[],prior.root.tree.s.tree,500000).rows;
 let union=new Set(),combined=new Set(),visits=0,combinedVisits=0;
 for(const c of cells){for(const i of c.remaining)union.add(i);visits+=c.remaining.length;let old=prior.guardProjection.cells.find(x=>x.mask===c.mask).hit;let now=c.remaining.filter(i=>old.includes(i));c.combined=now;now.forEach(i=>combined.add(i));combinedVisits+=now.length;}
 if(cells.length!==2**prior.guardProjection.vs.length){for(let mask=0;mask<2**prior.guardProjection.vs.length;mask++)if(!cells.some(c=>c.mask===mask)){all.forEach(i=>union.add(i));prior.guardProjection.cells.find(c=>c.mask===mask).hit.forEach(i=>combined.add(i));}}
 // Signed CNF all-true/all-false counts, strict feedback using exact score. No negative inference from local stall.
 const C=instance.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1));
 const score=A=>C.map(c=>c.reduce((q,l)=>{let x=A[Math.abs(l)-1],t=l>0?x:x-1;return q+t*t},0));
 const feedback=[];
 for(let init of [0,1]){let A=Array(instance.nvars).fill(init),Q=score(A),steps=0,evals=1,trajectory=[{unsat:Q.filter(v=>v===0).length,odd:Q.filter(v=>v%2).length}];
 while(steps<instance.nvars*4){let old=Q.filter(v=>v===0).length,best=old,bj=-1,bq;for(let j=0;j<A.length;j++){A[j]^=1;let q=score(A),u=q.filter(v=>v===0).length;evals++;A[j]^=1;if(u<best){best=u;bj=j;bq=q}}
 if(bj<0)break;A[bj]^=1;Q=bq;steps++;trajectory.push({unsat:best,odd:Q.filter(v=>v%2).length});}
 feedback.push({init,steps,evals,trajectory,assignment:A});
 }
 // Independently verify lift of prior positive witness and root zero proof before using result.
 const W=E.lift(G,n,trace,prior.witness);if(W.defects.length!==prior.witness.best)throw Error("witness mismatch");
 return {signedChecks,root,cells,unknownReason,counters,cap,importChecks,standalone:{unique:union.size,visits},combined:{unique:combined.size,visits:combinedVisits,candidates:[...combined].sort((a,b)=>a-b)},oldGuard:{unique:prior.guardProjection.projected.length,visits:prior.guardProjection.cells.reduce((s,c)=>s+c.hit.length,0)},feedback,witness:{best:prior.witness.best,defects:W.defects},normalCost:ctx.normalCost,chartHash:ctx.chartHash,mapHash:ctx.mapHash};
}
if(typeof module!=="undefined")module.exports={parityExperiment};

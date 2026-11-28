/* node count-merge.js evidence.json benchmarks.json ID */
function exactMerge(q,inst){
 let C=q.chart?q.chart.flatMap(f=>Array.from({length:2**f.v.length},(_,m)=>m).filter(m=>!f.r.includes(m)).map(m=>f.v.map((x,j)=>(m>>j)&1?-x:x))):inst.dimacs.trimEnd().split("\n").slice(1).map(x=>x.split(/\s+/).map(Number).slice(0,-1));
 let fixed=new Map(q.experiment.early.a);C=C.filter(c=>!c.some(l=>fixed.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!fixed.has(Math.abs(l))));
 let inc=new Map();for(let j=0;j<C.length;j++)for(let l of C[j]){let x=Math.abs(l);if(!inc.has(x))inc.set(x,[]);inc.get(x).push([j,l])}
 let totals={baseReads:0,deltaOccurrenceReads:0,mergeAdds:0,mergeInputs:0,mergeOutputs:0,scoreRows:0,fullCheckReads:0,overlapControls:0,overlapWrong:0};let proofs=[];
 for(let r of q.experiment.records){
  let a=new Map(r.base),T=C.map(c=>{let k=0,h=0;for(let l of c){totals.baseReads++;if(a.get(Math.abs(l))===+(l>0)){k++;h+=l>0?1:-1}}return [k,h]});
  function leaf(d){let z=new Map();for(let x of d)for(let [i,l] of inc.get(x)){totals.deltaOccurrenceReads++;let dk=a.get(x)===+(l>0)?-1:1,dh=dk*(l>0?1:-1),old=z.get(i)||[0,0];z.set(i,[old[0]+dk,old[1]+dh]);}return z}
  function merge(L,R){totals.mergeInputs+=L.size+R.size;let Z=new Map(L);for(let [i,v] of R){let a=Z.get(i);if(a){totals.mergeAdds+=2;Z.set(i,[a[0]+v[0],a[1]+v[1]])}else Z.set(i,v)}totals.mergeOutputs+=Z.size;return Z}
  let L=r.deltas.map(leaf),Z=merge(merge(L[0],L[1]),merge(L[2],L[3]));let D=new Set(r.deltas.flat());if(D.size!==r.deltas.flat().length)throw Error("not disjoint");let E=r.e,rows=[];
  for(let [i,[dk,dh]] of Z){totals.scoreRows++;let [k,h]=T[i],K=k+dk,H=h+dh;E+=+(K===0)-+(k===0);rows.push([i,dk,dh,K,K%3,(H%3+3)%3]);}
  let a1=new Map(a);for(let x of D)a1.set(x,1-a1.get(x));let exact=0;for(let i=0;i<C.length;i++){let k=0,h=0;for(let l of C[i]){totals.fullCheckReads++;if(a1.get(Math.abs(l))===+(l>0)){k++;h+=l>0?1:-1}}exact+=+(k===0);let [dk,dh]=Z.get(i)||[0,0];if(k!==T[i][0]+dk||h!==T[i][1]+dh)throw Error("count mismatch")}
  if(E!==exact||E!==r.ef)throw Error("energy mismatch");
  // Adversarial repeated flip: exact XOR cancels, unnormalized additive sum does not.
  let x=r.deltas[0][0];if(x!==undefined){let p=leaf([x]),bad=merge(p,p);totals.overlapControls++;if([...bad.values()].some(z=>z[0]!==0||z[1]!==0))totals.overlapWrong++}
  proofs.push({seed:r.seed,leafSupport:L.map(m=>m.size),jointSupport:Z.size,rows,E,full:exact});
 }
 return {totals,proofs,verified:true};
}
const fs=require('node:fs');let q=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),b=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));console.log(JSON.stringify(exactMerge(q,b.instances.find(x=>x.id===process.argv[4])),null,2));

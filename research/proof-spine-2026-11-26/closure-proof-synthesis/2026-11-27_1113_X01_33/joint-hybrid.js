function jointHybrid(G,own,chart,threshold,continuation,normalized,auditOwnerCertificate,verifyNative,cap=3000000){
 const same=x=>x.instance_id===own.instance_id&&x.guard_id==="EMPTY"&&x.residual_id==="ROOT";
 if(![chart,threshold,continuation].every(same))throw Error("parent scope");
 const ownerAudit=auditOwnerCertificate(G,own,verifyNative),n=normalized(G),g=n.gauge-1;
 if(g!==chart.r.gauge)throw Error("gauge mismatch");
 const sort=a=>a.sort((a,b)=>a-b),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let F=[],initialRows=0,bids=[];
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){
   bids.push(v);let p=[0,1,2,3].map(j=>4*v+j),vs=sort([...new Set(p.map(i=>n.root[i]).filter(r=>r!==g))]);
   let cost=Array.from({length:2**vs.length},(_,w)=>{initialRows++;return Number(p.reduce((a,i)=>a+(n.phase[i]^(n.root[i]===g?0:(w>>vs.indexOf(n.root[i]))&1)),0)!==2)});
   F.push({vs,cost,ids:[v]})
 }
 function group(F){const M=new Map();for(const f of F){let k=f.vs.join(",");if(!M.has(k))M.set(k,{vs:f.vs.slice(),cost:f.cost.slice(),ids:f.ids.slice()});else{let q=M.get(k);q.cost=q.cost.map((a,i)=>a+f.cost[i]);q.ids.push(...f.ids)}}return [...M.values()]}
 F=group(F);let factorReads=0,traceScans=0;
 for(const t of chart.r.chart.trace){traceScans+=F.length;let bucket=F.filter(f=>f.vs.includes(t.v)),U=sort([...new Set(bucket.flatMap(f=>f.vs))]),S=U.filter(v=>v!==t.v);
   if(!bucket.length||!eq(S,t.S)||!eq(sort(bucket.flatMap(f=>f.ids)),t.ids))throw Error("trace scope");
   let c=[],arg=[];
   for(let w=0;w<2**S.length;w++){let q=[0,1].map(b=>bucket.reduce((a,f)=>{factorReads++;let k=f.vs.reduce((k,r,i)=>k|((r===t.v?b:(w>>S.indexOf(r))&1)<<i),0);return a+f.cost[k]},0));c.push(Math.min(...q));arg.push(Number(q[1]<q[0]))}
   if(!eq(c,t.cost)||!eq(arg,t.arg))throw Error("min/argmin");
   F=group([...F.filter(f=>!bucket.includes(f)),{vs:S,cost:c,ids:t.ids}]);
 }
 if(!eq(F,chart.r.chart.F)||!eq(sort(F.flatMap(f=>f.ids)),bids)||!F.every(f=>f.cost.every(x=>Number.isInteger(x)&&x>=0&&x%2===0)))throw Error("chart partition/evenness");
 const pairs=own.intersection.map(s=>s.split(",").map(Number)),eligible=F.map((f,i)=>i).filter(i=>F[i].cost.includes(2)),needed=eligible.filter(i=>{let B=new Set(F[i].ids);return pairs.some(([u,v])=>B.has(u)&&B.has(v))});
 const trees=new Map();for(let a of [...threshold.result.cases,...continuation.cases]){if(trees.has(a.i))throw Error("duplicate tree");trees.set(a.i,a.tree)}
 let rowChecks=0,nodes=0,caseCounts=[];
 function check(i,t){let f=F.map((f,j)=>({vs:f.vs,words:f.cost.map((x,w)=>x<=(i===j?2:0)?w:-1).filter(w=>w>=0)}));let before=rowChecks,bn=nodes;
   function close(A){let changed=true;while(changed){changed=false;for(let q of f){let live=[];for(let w of q.words){if(++rowChecks>cap)throw Error("support cap");if(q.vs.every((v,k)=>!A.has(v)||A.get(v)===((w>>k)&1)))live.push(w)}if(!live.length)return false;
      let or=live.reduce((a,b)=>a|b,0),and=live.reduce((a,b)=>a&b,(1<<q.vs.length)-1);
      for(let [k,v] of q.vs.entries())if(!A.has(v)&&(((or^and)>>k)&1)===0){A.set(v,(and>>k)&1);changed=true}
   }}return true}
   function walk(A,t){nodes++;A=new Map(A);if(!close(A))return;if(t===null||!Array.isArray(t)||t.length!==3)throw Error("false leaf");
     let v=t[0]-1;if(!Number.isInteger(v)||v<0)throw Error("split");if(A.has(v)){walk(A,t[1+A.get(v)]);return}
     for(let b of [0,1]){let B=new Map(A);B.set(v,b);walk(B,t[1+b])}
   }
   walk(new Map(),t);caseCounts.push({i,rows:rowChecks-before,nodes:nodes-bn})
 }
 for(let i of needed){if(!trees.has(i))throw Error("uncovered eligible");check(i,trees.get(i))}
 // Direct physical witness; the chart proof is independent of its truth.
 let A=new Map(chart.r.lift.assignment),bit=i=>(A.get(n.root[i])??0)^n.phase[i],defects=[];
 for(const [i,j,s] of G.edges)if((bit(i)^bit(j))!==s)throw Error("wire");
 for(let v=0;v<G.types.length;v++){let a=[0,1,2,3].map(j=>bit(4*v+j));if(G.types[v]==="E"&&a.some(x=>x!==a[0]))throw Error("E");if(G.types[v]==="B"&&a.reduce((a,b)=>a+b,0)!==2)defects.push(v)}
 if(defects.length!==4||!eq(defects,chart.r.lift.defects))throw Error("witness");
 return {claim:"Exact native minimum B-violation energy 4",gauge:g,ownerAudit,initialRows,traceScans,factorReads,eliminations:chart.r.chart.trace.length,factors:F.length,eligible,needed,caseCounts,rowChecks,nodes,defects,witnessChecks:{vertices:G.types.length,edges:G.edges.length}}
}
// Node usage: node joint-hybrid.js compile.js discovery.js independent_checker.js runner.js benchmarks.json registry.json owner.json chart.json threshold.json continuation.json
const fs=require("node:fs"),crypto=require("node:crypto");const [cp,dp,kp,rp,bp,gp,op,pp,tp,up]=process.argv.slice(2),read=p=>fs.readFileSync(p,"utf8"),hash=s=>crypto.createHash("sha256").update(s).digest("hex");const cs=read(cp),ds=read(dp),ck=read(kp),rs=read(rp),compile=new Function(cs.slice(cs.indexOf("function compile("),cs.indexOf("function auditLocal("))+";return compile")(),normalized=new Function(ds.slice(ds.indexOf("function normalized("),ds.indexOf("function run("))+";return normalized")(),verifyNative=new Function(ck.slice(ck.indexOf("function verifyNative("),ck.indexOf("function replayTree("))+";return verifyNative")(),auditOwnerCertificate=new Function(rs.slice(0,rs.indexOf("// Usage:"))+";return auditOwnerCertificate")();const src=JSON.parse(read(bp)).instances.find(x=>x.id==="JOINT-24"),reg=JSON.parse(read(gp)).instances.find(x=>x.alias==="EB-JOINT-24"),C=compile(src),s=JSON.stringify(C.network)+"\n";if(hash(s)!==reg.sha256||Buffer.byteLength(s)*8!==reg.N_bits||hash(src.dimacs)!==reg.source_cnf.sha256||hash(JSON.stringify(C.source_map)+"\n")!==reg.source_map_sha256)throw Error("source ID");const inputs=[op,pp,tp,up].map(read);if(JSON.stringify(inputs.map(hash))!==JSON.stringify(["c7764d7f45198d9b30789c5abe30f25199f6d4eda27fb752dfbe2e685f007abb","eea1bbdefdd1db76adcbe73c68ba93cf07e7f39d29d07ef18ba88c953dbb96d0","8370f251cf3ad9912a2c802312a70105356c85398ecac295fd8d4e077c2ba63c","80ef6a64a485c17b1e6200e0a8a6796eb71fb8f679c3e8889147eff52e9856a7"]))throw Error("parent digests");console.log(JSON.stringify(jointHybrid(C.network,...inputs.map(JSON.parse),normalized,auditOwnerCertificate,verifyNative),null,2));

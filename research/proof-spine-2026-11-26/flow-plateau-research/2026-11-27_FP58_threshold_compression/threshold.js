function threshold(ctx,sha,entry){
 const {chart,V,gauge}=ctx,join=F=>[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),idx=(vs,U,w)=>vs.reduce((a,v,j)=>a|(((w>>U.indexOf(v))&1)<<j),0);
 const ledger={planIncidence:0,planUnionEntries:0,restrictionReads:0,guardChecks:0,coverage:0,earlyRows:0,stochasticRows:0,stochasticCandidateWeights:0,peerRows:0};
 function plan(F,width){
   let Q=F.map(f=>({id:f.i,vs:f.vs})),next=F.length,steps=[];
   while(Q.some(f=>f.vs.length)){
     const occ=new Map();for(const f of Q)for(const v of f.vs){ledger.planIncidence++;if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
     let opts=[...occ].map(([v,fs])=>{ledger.planUnionEntries+=fs.reduce((s,f)=>s+f.vs.length,0);return {v,fs,k:join(fs).length}}).sort((a,b)=>a.k-b.k||a.v-b.v);
     let {v,fs}=opts[0];fs.sort((a,b)=>b.vs.length-a.vs.length||a.id-b.id);
     let groups=[];for(const f of fs){let g=groups.find(g=>{ledger.planUnionEntries+=g.reduce((s,q)=>s+q.vs.length,0)+f.vs.length;return join([...g,f]).length<=width});if(!g)groups.push([f]);else g.push(f)}
     Q=Q.filter(f=>!fs.includes(f));for(const g of groups){let U=join(g),S=U.filter(x=>x!==v),id=next++;if(U.length>width)throw Error("factor wider than cap");steps.push({v,in:g.map(f=>f.id),U,S,id});Q.push({id,vs:S})}
   }
   return {width,steps,final:Q.map(f=>f.id)};
 }
 function restrict(pins){
   let P=new Map(pins);return chart.map(f=>{let vs=f.vs.filter(v=>!P.has(v)),cost=Array.from({length:2**vs.length},(_,w)=>{ledger.restrictionReads++;return f.cost[f.vs.reduce((a,v,j)=>a|((P.has(v)?P.get(v):((w>>vs.indexOf(v))&1))<<j),0)]/2});return {i:f.i,vs,cost}});
 }
 function run(F,pl,K,check=false){
   let events={reads:0,bitReads:0,writes:0,bitWrites:0,indexBits:0,skipped:0,peakValueBits:0,peakAllocatedPayloadBits:0,createdRows:0,cumulativeValueBits:0,steps:0};
   const Q=new Map(),cap=K===null?Infinity:K,bits=K===null?0:Math.ceil(Math.log2(K+1));
   function put(id,vs,cost){
     const m=cost.length,w=bits||Math.max(1,Math.ceil(Math.log2(Math.max(...cost)+1)));
     let a=K===null||check?cost:new Uint8Array(Math.ceil(m*w/8));
     if(K!==null&&!check)for(let j=0;j<m;j++)for(let k=0;k<w;k++){let b=j*w+k;a[b>>3]|=((cost[j]>>k)&1)<<(b&7);events.bitWrites++}
     Q.set(id,{vs,a,w,m,logical:m*w,allocated:(K===null||check)?64*m:8*a.length});events.writes+=m;events.createdRows+=m;events.cumulativeValueBits+=m*w;
     events.peakValueBits=Math.max(events.peakValueBits,[...Q.values()].reduce((s,f)=>s+f.logical,0));events.peakAllocatedPayloadBits=Math.max(events.peakAllocatedPayloadBits,[...Q.values()].reduce((s,f)=>s+f.allocated,0));
   }
   function val(f,j){events.reads++;if(K===null||check)return f.a[j];let x=0;for(let k=0;k<f.w;k++){let b=j*f.w+k;x|=((f.a[b>>3]>>(b&7))&1)<<k;events.bitReads++}return x}
   for(const f of F)put(f.i,f.vs,f.cost.map(x=>Math.min(cap,x)));
   let hashes=[];
   for(const s of pl.steps){
     events.steps++;let fs=s.in.map(i=>Q.get(i));if(fs.some(x=>!x))throw Error("bad dependency");
     if(JSON.stringify(join(fs))!==JSON.stringify(s.U)||JSON.stringify(s.U.filter(v=>v!==s.v))!==JSON.stringify(s.S))throw Error("bad scope");
     let cost=Array(2**s.S.length).fill(Infinity);
     if(check){for(let w=0;w<2**s.U.length;w++){let z=0;for(const f of fs){events.indexBits+=f.vs.length;z+=val(f,idx(f.vs,s.U,w))}let j=idx(s.S,s.U,w);cost[j]=Math.min(cost[j],cap,z)}}
     else {let U=[...s.S,s.v];for(let w=0;w<cost.length;w++){let best=Infinity;for(let b=0;b<2;b++){let z=0;for(let j=0;j<fs.length;j++){let f=fs[j];events.indexBits+=f.vs.length;z+=val(f,idx(f.vs,U,w|(b<<s.S.length)));if(z>=cap){events.skipped+=fs.length-j-1;z=cap;break}}best=Math.min(best,z);if(best===0){if(b===0)events.skipped+=fs.length;break}}cost[w]=best}}
     // Retain values in proof hash, not a free semantic hash equality; checker compares exact per-row data from separately computed execution via caller.
     hashes.push({id:s.id,cost});
     for(const i of s.in)Q.delete(i);put(s.id,s.S,cost);
   }
   if(Q.size!==pl.final.length||pl.final.some(i=>!Q.has(i)||Q.get(i).vs.length))throw Error("nonconstant terminal");
   let bound=0;for(let i of pl.final){bound+=val(Q.get(i),0);bound=Math.min(cap,bound)}
   return {bound,events,rows:hashes};
 }
 function test(F,pins,width){
   let pl=plan(F,width),exact=run(F,pl,null),coarse=run(F,pl,1),compressed=run(F,pl,2),check=run(F,pl,2,true);
   if(compressed.bound!==Math.min(2,exact.bound)||coarse.bound!==Math.min(1,exact.bound)||check.bound!==compressed.bound)throw Error("saturation bound mismatch");
   for(let i=0;i<pl.steps.length;i++){let a=exact.rows[i],b=coarse.rows[i],c=compressed.rows[i],d=check.rows[i];for(let j=0;j<a.cost.length;j++)if(Math.min(1,a.cost[j])!==b.cost[j]||Math.min(2,a.cost[j])!==c.cost[j]||c.cost[j]!==d.cost[j])throw Error("saturation row mismatch")}
   // Coarse zero implies cap2 zero for THIS PLAN. If coarse positive, selective threshold-2 refinement runs exactly once.
   let hybrid={bound:coarse.bound?compressed.bound:0,refined:!!coarse.bound,reads:coarse.events.reads+(coarse.bound?compressed.events.reads:0),bitReads:coarse.events.bitReads+(coarse.bound?compressed.events.bitReads:0),writes:coarse.events.writes+(coarse.bound?compressed.events.writes:0)};
   const by=new Map();for(const f of F){let k=f.vs.join(",");if(!by.has(k))by.set(k,f.cost.slice());else by.set(k,by.get(k).map((v,i)=>v+f.cost[i]))}
   let same=[...by.values()].reduce((s,c)=>s+Math.min(...c),0);
   const strip=({bound,events})=>({bound,events});
   return {pins,width,same,plan:pl,exact:strip(exact),coarse:strip(coarse),compressed:strip(compressed),check:strip(check),hybrid,compressedRows:compressed.rows};
 }
 function closure(pins){const o=ctx.support(chart,pins),a=ctx.affine(chart,o.pins||pins),m=ctx.matching(chart,o.pins||pins);ledger.earlyRows+=o.rows+a.rows;return {occupancy:o,affine:a,matching:m}}
 const root=closure([]),lanes=[],tests=[];
 // All guards on same exact chart; zero-only forces must never be hard-pinned in positive-energy relaxation.
 for(const pins of ctx.guards){
   let early=closure(pins),sep=ctx.bucket(chart,pins,100000),tree=ctx.core(chart,pins,100000);
   let ps=early.occupancy.pins||pins;
   let eligible=V.filter(v=>!ps.some(([w])=>w===v)),weights=eligible.map(v=>chart.reduce((s,f)=>{ledger.stochasticCandidateWeights++;return s+Number(f.vs.includes(v))},1)),pool=eligible.flatMap((v,i)=>[[v,0,weights[i]],[v,1,weights[i]]]);
   let stochastic=[];for(const mode of ["deterministic","uniform","adaptive"]){let R=12345,random=()=>{R=(Math.imul(1664525,R)+1013904223)>>>0;return R},draws=[];for(let t=0;t<Math.min(2,pool.length)&&early.occupancy.status!=="UNSAT";t++){
     let j;if(mode==="deterministic")j=pool.map((x,i)=>[x[2],i]).sort((a,b)=>b[0]-a[0]||a[1]-b[1])[t][1];else if(mode==="uniform"||random()%4===0)j=random()%pool.length;else{let w=random()%pool.reduce((s,q)=>s+q[2],0);j=0;while(w>=pool[j][2])w-=pool[j++][2]}
     let [v,b]=pool[j],G=[...ps,[v,b]],o=ctx.support(chart,G,30000);ledger.stochasticRows+=o.rows;let replay=null;if(o.status==="UNSAT"){replay=ctx.support(chart.slice().reverse(),G,30000);ledger.stochasticRows+=replay.rows;if(replay.status!=="UNSAT")throw Error("stochastic replay mismatch")}draws.push({v,b,weight:pool[j][2],o,replay});}stochastic.push({mode,seed:12345,pool,draws})}
   lanes.push({pins,early,separator:sep,tree,stochastic});
   const F=restrict(pins);tests.push(test(F,pins,8));
 }
 // Root control and exact five-guard coverage.
 tests.unshift(test(restrict([]),[],8));
 const counts=[];for(let mask=1;mask<32;mask++){let A=new Map(),bad=false;for(let j=0;j<5;j++)if(mask>>j&1)for(const [v,b] of ctx.guards[j]){ledger.guardChecks++;if(A.has(v)&&A.get(v)!==b)bad=true;A.set(v,b)}counts.push(bad?0n:1n<<BigInt(V.length-A.size))}
 const covered=counts.reduce((s,v,i)=>s+((i+1).toString(2).split("1").length%2===0?v:-v),0n);if(covered!==(1n<<BigInt(V.length)))throw Error("guard coverage");
 const guards=ctx.guards.map(p=>{let pins=[[gauge,0],...p].sort((a,b)=>a[0]-b[0]),h=sha(JSON.stringify(pins)+"\n"),guard_id="GUARD-v1:sha256:"+sha(JSON.stringify(["PNP-GUARD-v1",entry.instance_id,"EB-PORT-PINS-v1",h])+"\n");return {pins,guard_id,residual_id:"RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",entry.instance_id,guard_id,"FP51-ENERGY-TABLE-v1",ctx.chartHash,ctx.mapHash])+"\n")}});
 // Independently replay relative port equality from T2, restricted to zero energy only.
 let peer=null;if(entry.alias==="EB-JOINT-24"){
  let r=ctx.n.roots[593],s=ctx.n.sg[593]^ctx.n.sg[10];if(ctx.n.roots[10]===gauge&&V.includes(r)){
   let bad=ctx.support(chart,[[r,s^1]]),rev=ctx.support(chart.slice().reverse(),[[r,s^1]]);ledger.peerRows+=bad.rows+rev.rows;
   if(bad.status==="UNSAT"&&rev.status==="UNSAT"){let good=closure([[r,s]]);peer={r,s,bad,rev,good,scope:"zero energy only",parent:"CERT-v1:sha256:72c1f458755954fb2b6561cfc3bd12cda7e0bff1b7429479e5395effab9a5bb4"}}
  }
 }
 return {root,lanes,tests,guards,coverage:{counts:counts.map(String),total:String(covered)},ledger,peer,chartHash:ctx.chartHash,mapHash:ctx.mapHash,gauge,variables:V,normalCost:ctx.normalCost,originalOwners:chart.map(f=>({i:f.i,ids:f.ids,vs:f.vs}))};
}
if(typeof module!=="undefined")module.exports={threshold};

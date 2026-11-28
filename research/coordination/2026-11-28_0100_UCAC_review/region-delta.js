function experiment(d,pins){
 const sha=new Function(d.hash.slice(d.hash.indexOf("function sha("),d.hash.indexOf("if(require.main"))+";return sha")(),enc=x=>JSON.stringify(x)+"\n";
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
 const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")();
 const {project,verifyProjection,adapter,up,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,up,solve,replay}")();
 const results=[];
 function check(F,P){let A=F.slice(),visits=0;for(let i=0;i<P.length;i++){let u=up(A,P[i].map(l=>[Math.abs(l),+(l<0)]));visits+=u.work;if(!u.conflict)throw Error("RUP "+i);A.push(P[i]);}if(P.at(-1)?.length!==0)throw Error("not refutation");return visits;}
 for(const [name,id,expected] of [["joint","JOINT-24","3835d700e05d955e2e92efdc941cffe31d1a9f4f88856fd25566ffbf6d61ef13"],["random","RANDOM-3CNF-40","72431a7be9f694f687cd74bf80d66e2ed2a841cc1b686a7e6114db1028342bcf"]]){
  const x=JSON.parse(d.corpus).instances.find(q=>q.id===id),r=JSON.parse(d.reg).instances.find(q=>q.alias==="EB-"+id),G=compile(x),s=enc(G.network);
  if(sha(s)!==r.sha256||s.length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256||sha(d[name])!==expected)throw Error("auth");
  const p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,early=up(F);if(early.conflict||early.a.size)throw Error("unexpected early UP");
  const c=JSON.parse(d[name]),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
  if(gid!==c.internal_guard||rid!==c.internal_residual||chartHash!==c.chartHash||mapHash!==c.mapHash)throw Error("ids");
  // Choose scopes before reading seed rows, sorted by size and original carrier ID.
  const vars=[...new Set(F.flat().map(Math.abs))], candidates=vars.map(v=>({v,scope:[v,...[...new Set(F.filter(q=>q.some(l=>Math.abs(l)===v)).flat().map(Math.abs))].filter(u=>u!==v).sort((a,b)=>a-b)]})).sort((a,b)=>a.scope.length-b.scope.length||a.v-b.v);
  const selected=candidates.filter(q=>q.scope.length<=12).slice(0,3);
  const baseline=solve(F),baseReplay=replay(F,baseline.tree);
  const P=c.proof.filter(q=>q[0]===c.anchor).map(q=>q.slice(1)),gaugeVisits=check(F,P),S=[...F.map(q=>[c.anchor,...q]),...F.map(q=>[-c.anchor,...q.map(l=>-l)])];if(sha(enc(S))!==c.symmetricChartHash)throw Error("sym");
  const rootVisits=check(S,c.proof),ad=adapter(p,G,x.dimacs,x.nvars),M=new Map(ad.mapping.map(([i,v,s])=>[v,[i,s]])),Q=P.map(q=>q.map(l=>{let [i,s]=M.get(Math.abs(l));return i*(l>0?1:-1)*(s?-1:1)})),companionVisits=check(ad.orig,Q);
  const regions=[];let work={freshLiteral:0,deltaLiteral:0,hybridLiteralMaskBuild:0,hybridBigIntOps:0,hybridBitSpanUpper:0,comparisonCells:0,scopeTests:0,initLiteral:0,ablationLiteral:0};
  for(const {v,scope} of selected){
   const w=scope.length,Z=2**w,B=Z/2,idx=new Map(scope.map((v,i)=>[v,i]));
   const included=q=>{work.scopeTests+=q.length;return q.every(l=>idx.has(Math.abs(l)))};
   const ids=F.flatMap((q,i)=>included(q)?[i]:[]),R=ids.map(i=>F[i]),seeds=P.flatMap((q,i)=>q.length&&included(q)?[{i,q}]:[]);
   function sat(q,m,k){for(let l of q){work[k]++;if(Boolean(m&(1<<idx.get(Math.abs(l))))===(l>0))return true;}return false;}
   function fresh(rows,k){let a=[];for(let m=0;m<Z;m++)if(rows.every(q=>sat(q,m,k)))a.push(m);return a;}
   function response(a){let counts=Array(B).fill(0);for(let m of a)counts[m>>1]++;return counts;}
   const initial=fresh(R,"initLiteral");let live=initial.slice(),rows=R.slice(),cnt=response(live),bits=0n;const masks=new Map();for(let i=0;i<w;i++)for(let sign of [-1,1]){let mask=0n;for(let m of initial){work.hybridLiteralMaskBuild++;if(Boolean(m&(1<<i))===(sign>0)){mask|=1n<<BigInt(m);work.hybridBigIntOps+=2;work.hybridBitSpanUpper+=2*Z;}}masks.set(sign*scope[i],mask)}for(let m of initial){bits|=1n<<BigInt(m);work.hybridBigIntOps+=2;work.hybridBitSpanUpper+=2*Z;}
   let steps=[];for(let {i,q} of seeds){rows.push(q);let next=[];let before=live.length,old=cnt.filter(x=>x>0).length;for(let m of live){if(sat(q,m,"deltaLiteral"))next.push(m);else cnt[m>>1]--;}live=next;
    let allowed=0n;for(let l of q){allowed|=masks.get(l);work.hybridBigIntOps++;work.hybridBitSpanUpper+=Z;}bits&=allowed;work.hybridBigIntOps++;work.hybridBitSpanUpper+=Z;
    let a=fresh(rows,"freshLiteral"),b=response(a),decoded=[];for(let m=0;m<Z;m++){work.comparisonCells++;if((bits>>BigInt(m))&1n)decoded.push(m);}work.hybridBitSpanUpper+=2*Z*Z;work.hybridBigIntOps+=2*Z;
    work.comparisonCells+=B;if(a.join()!==live.join()||a.join()!==decoded.join()||b.join()!==cnt.join())throw Error("delta discrepancy");steps.push({parentRow:i,clause:q,tuplesBefore:before,tuplesAfter:live.length,boundaryBefore:old,boundaryAfter:cnt.filter(x=>x>0).length});
   }
   let ablations=seeds.slice(0,3).map(({i})=>({removed:i,support:response(fresh([...R,...seeds.filter(s=>s.i!==i).map(s=>s.q)],"ablationLiteral")).filter(x=>x>0).length}));
   // Exact one-interior replacement: omit all other imported rows, retain all exterior source rows. The locally admitted rows are global consequences, so replacement is equisatisfiable.
   let full=[...F.filter((q,i)=>!ids.includes(i)),...cnt.flatMap((a,m)=>a?[]:[scope.slice(1).map((u,j)=>(m&(1<<j))?-u:u)])];
   if(full.some(q=>q.some(l=>Math.abs(l)===v)))throw Error("interior escaped");let hybrid=solve(full),hybridReplay=replay(full,hybrid.tree);
   regions.push({interior:v,scope,sourceRows:ids,seedRows:seeds,initialTuples:initial.length,initialBoundary:response(initial).filter(x=>x>0).length,finalTuples:live.length,finalBoundary:cnt.filter(x=>x>0).length,finalCounts:cnt,finalWitnesses:live,steps,ablations,hybrid:{rows:full.length,nodes:hybrid.nodes,work:hybrid.work,replay:hybridReplay,tree:hybrid.tree}});
  }
  const cert={format:"T4-REGIONAL-DELTA-v1",problem_id:"STRICT-EB4-v1",instance:r.short_id,instance_id:r.instance_id,original_N_bits:r.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:c.original_ids,parent_certificate_id:"CERT-v1:sha256:"+expected,source_cnf:r.source_cnf,projection,early:{pins:early.a.size,visits:early.work},gaugeVisits,rootVisits,companionVisits,sourceBaseline:{nodes:baseline.nodes,work:baseline.work,replay:baseReplay},regions,work,candidateScopes:candidates.map(q=>({v:q.v,width:q.scope.length})),scope:"Exact fixed-scope witness deletion and response counts; imports independently replayed; no universal coverage or bit-time claim."};
  results.push({certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),cert});
 }
 return results;
}
const fs=require('node:fs');const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"reg":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"hash":["research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js","4a42c99a37a2a22c1ac36ed204eadce7dfa77908"],"joint":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/JOINT-24.cert.json","eb3eb5f2098fbfa73cd11540ba270ac997438f78"],"random":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/RANDOM-3CNF-40.cert.json","f96bea02c40c7545eb32c7fd5ac37afac7e436e8"]};const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(experiment(d,pins),null,2));

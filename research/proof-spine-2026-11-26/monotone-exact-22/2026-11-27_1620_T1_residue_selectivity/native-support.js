// Node: node native-support.js DIR; fetch input files from pins.
const fs=require('node:fs');const files={"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"support":["research/proof-spine-2026-11-26/monotone-exact-22/2026-11-27_1620_T1_residue_selectivity/support.js","a2e6fe81060dae7f5f2463aa492a8ef9ac2521b1"]};const d=Object.fromEntries(Object.keys(files).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function run(d){
 const {sha,canon}=new Function(d.native+";return {sha,canon};")(),b=JSON.parse(d.corpus),reg=JSON.parse(d.registry),A=(x,m)=>{if(!x)throw Error(m)},out=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const started=Date.now(),x=b.instances.find(x=>x.id===alias),ent=reg.instances.find(x=>x.alias==="EB-"+alias);
  const enc=x=>JSON.stringify(x)+"\n",compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile("),d.compiler.indexOf("function auditLocal"))+"\nreturn compile")(),G=compile(x);
  A(sha(enc(G.network))===ent.sha256&&enc(G.network).length*8===ent.N_bits&&sha(x.dimacs)===ent.source_cnf.sha256&&sha(enc(G.source_map))===ent.source_map_sha256,"auth");
  const {project,verifyProjection}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function up("))+";return {project,verifyProjection};")();
  const p=project(G.network),replay=verifyProjection(G.network,p),C=p.clauses.map(c=>canon(c)),n=Math.max(0,...C.flat().map(Math.abs)),guard=[[p.anchor,0]],guard_id="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ent.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))]));
  const chart={anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final},maps={root:p.root,phase:p.phase},chartHash=sha(enc(chart)),mapHash=sha(enc(maps)),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ent.instance_id,guard_id,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
  const counts={indexReads:0,exactRowChecks:0,terms:0,coefficientVisits:0,neighborTests:0,closureVisits:0,unitReplayChecks:0,terminalReplayChecks:0},index=new Map(),nbr=Array.from({length:n+1},()=>new Map());
  for(let [i,c] of C.entries()){counts.indexReads+=c.length;index.set(c.join(),i+1);if(c.length===2&&c.every(l=>l<0)){const [u,v]=c.map(Math.abs);nbr[u].set(v,i+1);nbr[v].set(u,i+1)}}
  const rows=[];for(let [i,c] of C.entries()){if(!c.length||!c.every(l=>l>0))continue;let ok=true,ids=[i+1];for(let j=0;j<c.length;j++)for(let k=j+1;k<c.length;k++){counts.exactRowChecks++;const id=nbr[c[j]].get(c[k]);if(id===undefined)ok=false;else ids.push(id)}if(ok)rows.push({v:c,ids})}
  const units=new Map(),supportSeen=new Set();let stage="root";
  function up(){
   let live=new Map([...units.keys()].map(l=>[-l,0])),trace=[];
   for(;;){let change=false;for(let [i,c] of C.entries()){let sat=false,free=[];for(let l of c){counts.closureVisits++;const v=live.get(Math.abs(l));if(v===undefined)free.push(l);else if(v===+(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return {conflict:i+1,trace};if(free.length===1){let l=free[0];live.set(Math.abs(l),+(l>0));trace.push([l,i+1]);change=true}}if(!change)return null}
  }
  let terminal=up(),stageStats=[];
  function acquire(terms){
   counts.terms++;const coef=new Map();let rhs=0;
   for(let [r,s] of terms){rhs+=s;for(let v of r.v){counts.coefficientVisits++;coef.set(v,(coef.get(v)||0)+s)}}
   if(rhs<=0)return;
   const P=[...coef].filter(([v,c])=>c>0).map(([v])=>v).sort((a,b)=>a-b),key=P.join(",");
   if(supportSeen.has(key))return;supportSeen.add(key);
   if(!P.length){terminal={direct:{terms,rhs,P}};return}
   // Choose the shortest exclusion adjacency. Every surviving candidate must exclude all positive terms.
   const v=P.slice().sort((u,v)=>nbr[u].size-nbr[v].size||u-v)[0];
   for(let [w] of nbr[v]){
    if(units.has(-w))continue;let ids=[],ok=true;
    for(let u of P){counts.neighborTests++;let id=nbr[u].get(w);if(id===undefined){ok=false;break}ids.push([u,id])}
    if(ok){units.set(-w,{terms,rhs,P,guard:[w,1],zeroReasons:ids,unit:-w});terminal=up();if(terminal)return}
   }
  }
  if(!terminal){stage="single";for(let r of rows){acquire([[r,1]]);if(terminal)break}stageStats.push({stage,units:units.size,terms:counts.terms});}
  if(!terminal){stage="three";outer:for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++)for(let k=0;k<rows.length;k++){if(k===i||k===j)continue;acquire([[rows[i],1],[rows[j],1],[rows[k],-1]]);if(terminal)break outer}stageStats.push({stage,units:units.size,terms:counts.terms})}
  // Independent replay exact original-clause support, positive-coefficient bound and every UP reason.
  const equal=(a,b)=>a.length===b.length&&a.every(l=>b.includes(l));
  function verifyTerms(terms,rhs,P){
   let a=new Map(),r=0;for(let [row,s] of terms){A(s===1||s===-1,"sign");const need=[row.v,...row.v.flatMap((u,i)=>row.v.slice(i+1).map(v=>[-u,-v]))];for(let c of need){counts.unitReplayChecks+=row.ids.length;A(row.ids.some(id=>equal(C[id-1],c)),"exact-one")};r+=s;for(let v of row.v){counts.unitReplayChecks++;a.set(v,(a.get(v)||0)+s)}}
   const q=[...a].filter(([v,c])=>c>0).map(([v])=>v);A(r===rhs&&rhs>0&&equal(P,q),"support");
  }
  for(let [u,p] of units){verifyTerms(p.terms,p.rhs,p.P);A(p.unit===u&&p.guard[0]===-u&&p.guard[1]===1,"guard");A(equal(p.P,p.zeroReasons.map(r=>r[0])),"guard coverage");for(let [v,id] of p.zeroReasons){counts.unitReplayChecks++;A(equal(C[id-1],[u,-v]),"source exclusion")}}
  if(terminal?.direct){verifyTerms(terminal.direct.terms,terminal.direct.rhs,terminal.direct.P);A(!terminal.direct.P.length,"direct")}
  else if(terminal){const live=new Map([...units.keys()].map(u=>[-u,0]));for(let [l,id] of terminal.trace){let c=C[id-1];counts.terminalReplayChecks+=c.length;A(c.includes(l)&&!live.has(Math.abs(l))&&c.filter(x=>x!==l).every(x=>live.get(Math.abs(x))===+(x<0)),"UP");live.set(Math.abs(l),+(l>0))}let c=C[terminal.conflict-1];counts.terminalReplayChecks+=c.length;A(c.every(x=>live.get(Math.abs(x))===+(x<0)),"terminal")}
  out.push({problem_id:"STRICT-EB4-v1",instance:ent.short_id,instance_id:ent.instance_id,original_N_bits:ent.N_bits,source_pin:files,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1],chartClauseIds:[1,C.length],chartVariables:[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b)},parents:[],claim:terminal?"checked contradiction by sparse integer row support, exclusion intersection and unit closure":"no terminal under named positive exact-one source scan",alias,chart:{guard_id,guard,residual_id:rid,chartHash,mapHash,chartArtifact:chart,projectionCosts:p.cost,projectionReplay:replay,carrierCount:p.carriers,eliminated:p.steps.length},rows,stageStats,units:[...units.values()],terminal,status:terminal?"UNSAT":"UNKNOWN",counts,ms:Date.now()-started,scope:"native source-only after exact projection; no compiler-map advice; port literals are original port ID+1; chart row IDs in exact artifact, gauge discharged by global complement; fixed one/three-row scan; not universal."})
 }
 return out
}

console.log(JSON.stringify(run(d),null,2));

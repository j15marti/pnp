const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"runner":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_predictive_refinement/run.js","f6ba5a235ddc8fb5fe1dae7621e406370c51a6d2"],"results":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_predictive_refinement/results.json","f5c72c5e74707ae5890f87a3967fd90adfe9bbbc"],"peer":["research/proof-spine-2026-11-26/four-partition-nae/2026-11-27_T2_orientation_guard_cover/JOINT-24-direct-conservation.json","a6e8108a11830101e72ecbaac87bcf677f29ad41"],"prior":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_compression_refinement/run.js",null]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const sliceAudit=function sliceAudit(data,pins){
  const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
  const {sha,norm,replay,canon,key,up}=new Function(data.native+";return {sha,norm,replay,canon,key,up};")();
  const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n",V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),meter=(cap=10000000)=>({scans:0,lits:0,nodes:0,cap});
  const expr=data.runner.slice(data.runner.indexOf("const run=")+10,data.runner.lastIndexOf(";\nconsole.log(")).replace("let out=[];","return {independent,index,conflict}; let out=[];");
  const {independent,index,conflict}=new Function("return ("+expr+")")()(data,pins);
  const corpus=JSON.parse(data.corpus),registry=JSON.parse(data.registry);
  let out=[];
  for(let r of JSON.parse(data.results)){
   const s=corpus.instances.find(x=>x.id===r.alias),reg=registry.instances.find(x=>x.alias==="EB-"+r.alias),g0=compile({nvars:s.nvars,dimacs:s.dimacs}),g=g0.network;
   A(sha(enc(g))===reg.sha256&&enc(g).length*8===reg.N_bits&&sha(s.dimacs)===reg.source_cnf.sha256&&s.dimacs.length*8===reg.source_cnf.N_bits&&sha(enc(g0.source_map))===reg.source_map_sha256,"auth");
   const b=norm(g),p=replay(b.C,r.projection.trace);A(sha(enc(p.C))===r.projection.projectedSha,"projection");
   const cnf=s.dimacs.trim().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)));
   for(let [kind,C0] of [["native",p.C],["cnf",cnf]]){
    const e=r[kind],u=up(C0,[],meter()),C=C0.filter(c=>!c.some(l=>u.A.get(Math.abs(l))===+(l>0))).map(c=>canon(c.filter(l=>!u.A.has(Math.abs(l)))));
    A(sha(enc(C))===e.residualSha,"chart");const I=index(C),leaves=[],tree=e.baseline.tree,work={init:0,occ:0,lits:0,assignments:0,reasonVisits:0,pins:0,checkScans:0,checkLits:0};
    function go(t,g){if(t===null){const k=conflict(C,I,g);A(k.conflict&&k.guard.every(l=>g.includes(l)),"guard subset");leaves.push({path:g,core:k.support,guard:k.guard,proof:k.check});for(let k0 of ["init","occ","lits","assignments","reasonVisits","pins"])work[k0]+=k.m[k0];work.checkScans+=k.check.scans;work.checkLits+=k.check.lits;return}A(!g.some(l=>Math.abs(l)===t[0]),"repeat pivot");go(t[1],[...g,-t[0]]);go(t[2],[...g,t[0]])}
    go(tree,[]);
    let unique=new Map(),comparisons=0;
    for(let l of leaves){let k=key(l.guard);if(!unique.has(k)||l.core.length<unique.get(k).core.length)unique.set(k,l)}
    let minimal=[...unique.values()].filter(l=>![...unique.values()].some(m=>{comparisons++;return m.guard.length<l.guard.length&&m.guard.every(x=>l.guard.includes(x))}));
    let map=leaves.map(l=>{let j=minimal.findIndex(m=>{comparisons++;return m.guard.every(x=>l.path.includes(x))});A(j>=0,"coverage");return j});
    let originalCore=[...new Set(minimal.flatMap(l=>l.core))].sort((a,b)=>a-b),F=originalCore.map(i=>C[i]),guardClauses=minimal.map(l=>canon(l.guard.map(x=>-x)));
    let ck=independent(F,[],tree),gck=independent(guardClauses,[],tree);
    // exact independent source-subset proof and guard coverage using the same tree, no SAT solver in either checker.
    let peer=null;if(r.alias==="JOINT-24"&&kind==="native"){let raw=data.peer,peer0=JSON.parse(raw);A(sha(raw)==="e1f3c884142546ba67b979cc00003f7e7ff3c595377f79e58301eba3dc55b7e0","peer digest");
     let pins0=peer0.excluded_guard.guard.map(([i,v])=>[b.root[i],v^b.sign[i]]),cnt=new Map(),f=new Map(pins0);
     for(let j of peer0.original_ids.B_vertices){A(g.types[j]==="B","owner");for(let t=0;t<4;t++){let i=4*j+t,v=b.root[i];if(!cnt.has(v))cnt.set(v,[0,0]);cnt.get(v)[b.sign[i]]++}}
     let max=0;for(let [v,[a,z]] of cnt)max+=f.has(v)?(f.get(v)?a:z):Math.max(a,z);
     A(max<2*peer0.original_ids.B_vertices.length,"peer conservation");
     let C1=canon(pins0.map(([v,z])=>z?-v:v)),root=new Map(e.rootUnits);let satisfied=C1.some(l=>root.get(Math.abs(l))===+(l>0)),clause=C1.filter(l=>!root.has(Math.abs(l)));
     peer={digest:sha(raw),ports:peer0.excluded_guard.guard,owners:peer0.original_ids.B_vertices,max,required:2*peer0.original_ids.B_vertices.length,clause,satisfied,alreadyPresent:C.some(c=>key(c)===key(clause)),bytes:raw.length};}
    out.push({alias:r.alias,kind,source:e.source,residualSha:e.residualSha,rootUnits:e.rootUnits,tree,leaves,minimal,coverMap:map,originalCore,guardClauses,work,comparisons,coreCheck:ck,guardCheck:gck,baseline:e.baseline.m,baselineCheck:e.baseCheck,priorSize:C.length,projection:kind==="native"?r.projection:null,peer});
   }
  }
  return out;
 };
console.log(JSON.stringify(sliceAudit(data,pins),null,2));

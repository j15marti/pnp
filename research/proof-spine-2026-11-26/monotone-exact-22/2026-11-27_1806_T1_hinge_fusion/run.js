// Reproduce: node run.js DIR (fetch all pinned files by key).
const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"peer":["research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_1800_T3_cross_scope/owner-cert.js","faf453592a9c63182fe941dd79d4ef62ba606cef"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function(data,pins){
 const {sha,canon}=new Function(data.native+"\n;return {sha,canon};")();
 const compile=new Function(data.compiler.slice(data.compiler.indexOf("function compile("),data.compiler.indexOf("function auditLocal"))+"\n;return compile")();
 const {project,verifyProjection}=new Function(data.chart.slice(data.chart.indexOf("const key="),data.chart.indexOf("function up("))+"\n;return {project,verifyProjection};")();
 const L=new Function(data.peer.slice(0,data.peer.indexOf("function compile("))+"\n;return {quotient,gauge,project,clauses,canon,up,tree,replay,importPrefix};")();
 const i=data.peer.indexOf("function study("),j=data.peer.indexOf("\nfunction ",i+15);
 const study=new Function(data.peer.slice(i,j)+"\n;return study;")();
 const enc=x=>JSON.stringify(x)+"\n", A=(ok,m)=>{if(!ok)throw Error(m)},key=c=>canon(c).join(),vars=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
 const reg=JSON.parse(data.registry),corpus=JSON.parse(data.corpus);
 A(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
 function experiment(C,mode,limit=2500000,imports=[]){
  const start=Date.now(),V=vars(C),F=C.slice(),seen=new Set(F.map(key)),proof=[],stats={queryReads:0,scans:0,candidatePairs:0,clausePairs:0,hinges:0,failedQueries:0,successfulQueries:0,verify:0,imported:0,duplicateQueries:0,peakLits:F.reduce((z,c)=>z+c.length,0)},trace=[];
  const K=(a,b)=>[Math.min(a,b),Math.max(a,b)].join(","),co=new Map(),hinge=new Map(),occ=new Map(),support=new Map();
  for(let i=0;i<C.length;i++){let c=C[i];for(let l of c){if(!occ.has(l))occ.set(l,[]);occ.get(l).push(i)}for(let a=0;a<c.length;a++)for(let b=a+1;b<c.length;b++){let k=K(Math.abs(c[a]),Math.abs(c[b]));co.set(k,(co.get(k)||0)+1)}}
  for(let v of V)for(let i of occ.get(v)||[])for(let j of occ.get(-v)||[]){stats.clausePairs++;for(let a of C[i])for(let b of C[j]){a=Math.abs(a);b=Math.abs(b);stats.hinges++;if(a===b||a===v||b===v)continue;let k=K(a,b);hinge.set(k,(hinge.get(k)||0)+1);if(!support.has(k))support.set(k,[i+1,j+1,v])}}
  let pairs=[...new Set([...co.keys(),...hinge.keys()])].filter(k=>mode==="same"?co.has(k):mode==="cross"?!co.has(k)&&hinge.has(k):true).sort((a,b)=>((mode==="same"?co.get(b):hinge.get(b))||0)-((mode==="same"?co.get(a):hinge.get(a))||0)||a.localeCompare(b)).map(k=>k.split(",").map(Number));
  if(mode==="random"){let s=19771127;for(let i=pairs.length-1;i>0;i--){s=(Math.imul(1664525,s)+1013904223)>>>0;let j=s%(i+1);[pairs[i],pairs[j]]=[pairs[j],pairs[i]]}}
  function prop(ass){let P=new Set(ass),changed=true;while(changed){changed=false;for(let i=0;i<F.length;i++){stats.scans++;let sat=false,free=[];for(let l of F[i]){if(++stats.queryReads>limit)return {cap:true,P};if(P.has(l)){sat=true;break}if(!P.has(-l))free.push(l)}if(sat)continue;if(!free.length)return {bad:true,P,conflict:i+1};if(free.length===1){P.add(free[0]);changed=true}}}return {bad:false,P}}
  let initial=prop([]),status=initial.bad?"UNSAT":"UNKNOWN",root=initial,stopped="candidate exhaustion";
  function admit(c,kind,guard,parents=[]){c=canon(c);if(seen.has(key(c)))return false;let r=prop(c.map(l=>-l));if(r.cap){stopped="cap";return false}if(!r.bad){stats.failedQueries++;return false}
   stats.successfulQueries++;F.push(c);seen.add(key(c));proof.push(c);trace.push({kind,c,guard,parents,conflict:r.conflict});stats.peakLits+=c.length;if(kind==="import")stats.imported++;
   root=prop([]);if(root.cap)stopped="cap";else if(root.bad){if(c.length){F.push([]);proof.push([]);trace.push({kind:"closure",c:[],guard:[],parents:[],conflict:root.conflict})}status="UNSAT"}return true}
  if(initial.bad){proof.push([]);trace.push({kind:"early",c:[],guard:[],parents:[]})}
  for(let c of imports){if(status==="UNSAT"||stopped==="cap")break;admit(c,"import",c.map(l=>-l))}
  const probe=(v)=>{if(root.P.has(v)||root.P.has(-v))return;for(let b of [v,-v]){if(status==="UNSAT"||stopped==="cap")break;admit([-b],"unit",[b])}};
  for(let pass=0;pass<2&&status!=="UNSAT"&&stopped!=="cap";pass++){let prev=proof.length;
   outer:for(let [a,b] of pairs){stats.candidatePairs++;if(root.P.has(a)||root.P.has(-a)||root.P.has(b)||root.P.has(-b))continue;
    for(let x of [a,-a])for(let y of [b,-b]){
     if(status==="UNSAT"||stopped==="cap")break outer;
     let c=[-x,-y];if(seen.has(key(c))){stats.duplicateQueries++;continue}
     if(admit(c,"pair",[x,y],support.get(K(a,b))||[])){probe(a);probe(b)}
    }
   }if(prev===proof.length)break;
  }
  const replay=L.replay(C,proof);stats.verify=replay.visits;A((status==="UNSAT")===replay.unsat,"terminal replay");
  return {mode,limit,status,stopped,initialUnits:[...initial.P],rootUnits:[...root.P],candidatePairUniverse:pairs.length,proof,trace,stats,ms:Date.now()-start,peakRows:F.length};
 }
 const out=[];
 for(let name of ["JOINT-24","RANDOM-3CNF-40"]){
  const start=Date.now(),x=corpus.instances.find(q=>q.id===name),r=reg.instances.find(q=>q.alias==="EB-"+name),G=compile(x);
  A(sha(enc(G.network))===r.sha256&&enc(G.network).length*8===r.N_bits&&sha(x.dimacs)===r.source_cnf.sha256&&x.dimacs.length*8===r.source_cnf.N_bits&&sha(enc(G.source_map))===r.source_map_sha256,"auth "+name);
  const p=project(G.network),vr=verifyProjection(G.network,p),C=p.clauses.map(c=>canon(c)),S=x.dimacs.trimEnd().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)));
  const chart={anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final},mapping={root:p.root,phase:p.phase},guard=[[p.anchor,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",sha(enc(chart)),sha(enc(mapping))]));
  const native=[],comp=[];
  for(let [F,T] of [[C,native],[S,comp]]){for(let mode of ["same","cross","random"])T.push(experiment(F,mode));let prefix=T[1].proof.filter(c=>c.length).slice(0,8);T.push(experiment(F,"hybrid",2500000,prefix))}
  const q=L.quotient(G.network),g=L.gauge(q.F),p2={F:p.final.map(f=>({s:f.s.map(v=>v+1),a:f.a}))};
  A(g.g===p.anchor+1,"gauge match");
  const five=study(L,G.network,q,g,p2,C,[],[],S,name);
  A(five.covered>=0&&five.covered<=16,"coverage");
  const original_ids={vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1],chart_clauses:[1,C.length],cnf_clauses:[1,S.length]};
  out.push({name,registry:r,source_pin:pins,original_ids,guard_id:"EMPTY",residual_id:"ROOT",chart:{guard,gid,rid,chartHash:sha(enc(chart)),mapHash:sha(enc(mapping)),projectionCosts:p.cost,replay:vr,carriers:p.carriers,raw:p.raw.length,eliminated:p.steps.length,clauses:C},native,comp,five,elapsed:Date.now()-start});
 }
 return out
};
console.log(JSON.stringify(run(data,pins)));

const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"prior":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_compression_refinement/run.js","6d558074c29cb6b7b3a5295e3cfc7cb3f3c1c9b6"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data,pins){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,up,canon,key}=new Function(data.native+";return {sha,norm,project,replay,up,canon,key};")();
 const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n",V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),meter=(cap=10000000)=>({scans:0,lits:0,nodes:0,cap});
 const start=data.prior.indexOf("const run=function"),end=data.prior.indexOf(" function process(C,source)");
 const lib=new Function("return ("+data.prior.slice(start+10,end)+"\nreturn {dpll,verify,compress,relax,checkRelax,refine};})")()(data,pins);
 const {dpll,verify,compress,relax,checkRelax,refine}=lib;
 function independent(C,ass,tree){
  const m={scans:0,lits:0,nodes:0};
  function prop(g){let p=new Map();for(let l of g){let v=Math.abs(l);if(p.has(v)&&p.get(v)!==l)return {conflict:true,p};p.set(v,l)}
   for(;;){let change=false;for(let i=C.length-1;i>=0;i--){m.scans++;let c=C[i],n=0,last=0,sat=false;for(let l of c){m.lits++;let x=p.get(Math.abs(l));if(x===l)sat=true;else if(x===undefined){n++;last=l}}if(sat)continue;if(!n)return {conflict:true,p};if(n===1){p.set(Math.abs(last),last);change=true}}
    if(!change)return {conflict:false,p}}
  }
  function walk(t,g){m.nodes++;let r=prop(g);if(r.conflict)return;if(t===null)throw Error("nonconflict leaf");A(Array.isArray(t)&&t.length===3,"tree");let v=t[0];if(r.p.has(v)){walk(t[r.p.get(v)>0?2:1],g);return}walk(t[1],[...g,-v]);walk(t[2],[...g,v])}
  if(tree===undefined){let r=prop(ass);return {...m,conflict:r.conflict}}
  walk(tree,ass);return {...m,conflict:true};
 }
 function index(C){let occ=new Map(),lits=0;for(let i=0;i<C.length;i++)for(let l of C[i]){lits++;if(!occ.has(l))occ.set(l,[]);occ.get(l).push(i)}return {occ,lits}}
 // A causal support for a failed sequence of candidate pins. Each pin is a decision, not a forced fact.
 function conflict(C,I,pins){
  let P=new Map(),reason=new Map(),Q=[],head=0,counts=new Int32Array(C.length),m={init:C.length,occ:0,lits:0,assignments:0,reasonVisits:0,pins:0},bad=null;
  function assign(l,why){let v=Math.abs(l);if(P.has(v)){if(P.get(v)!==l){bad={opposite:l,why};return false}return true}P.set(v,l);reason.set(v,why);Q.push(l);m.assignments++;return true}
  function propagate(){while(head<Q.length&&!bad){let l=Q[head++];for(let ci of I.occ.get(-l)||[]){m.occ++;let c=C[ci],n=++counts[ci];if(n<c.length-1)continue;let sat=false,free=[];for(let z of c){m.lits++;let y=P.get(Math.abs(z));if(y===z)sat=true;else if(y===undefined)free.push(z)}if(sat)continue;if(!free.length){bad={clause:ci};break}if(free.length===1&&!assign(free[0],ci))break}}}
  for(let i=0;i<C.length&&!bad;i++){if(!C[i].length)bad={clause:i};else if(C[i].length===1)assign(C[i][0],i)}propagate();
  for(let l of pins){if(bad)break;m.pins++;assign(l,-1);propagate()}
  if(!bad)return {conflict:false,m,assigned:P.size};
  let support=new Set(),guards=new Set(),todo=[],seen=new Set();
  function clause(ci){if(support.has(ci))return;support.add(ci);for(let l of C[ci])if(P.get(Math.abs(l))===-l)todo.push(-l)}
  if(bad.clause!==undefined)clause(bad.clause);else{todo.push(-bad.opposite);if(bad.why===-1)guards.add(bad.opposite);else clause(bad.why)}
  while(todo.length){let l=todo.pop(),v=Math.abs(l);if(seen.has(v))continue;seen.add(v);m.reasonVisits++;let ci=reason.get(v);A(ci!==undefined,"reason");if(ci===-1)guards.add(l);else clause(ci)}
  // If a requested assumption contradicts another assumption, this is a tautological guard; our callers never do this.
  let G=canon([...guards]),S=[...support].sort((a,b)=>a-b);A(!G.some(l=>G.includes(-l)),"guard consistency");
  let ck=independent(S.map(i=>C[i]),G);A(ck.conflict,"core replay");
  return {conflict:true,m,support:S,guard:G,clause:canon(G.map(l=>-l)),check:ck,assigned:P.size};
 }
 function test(C0,source){
  let m=meter(),u=up(C0,[],m);A(!u.conflict,"unexpected root");
  let C=C0.filter(c=>!c.some(l=>u.A.get(Math.abs(l))===+(l>0))).map(c=>canon(c.filter(l=>!u.A.has(Math.abs(l)))));
  let vs=V(C),cmp=compress(C),R=relax(cmp.G),relaxCheck=checkRelax(cmp.G,R),I=index(C),byScope=new Map(cmp.G.map((g,i)=>[key(g.s),i])),gid=C.map(c=>byScope.get(key(c.map(Math.abs))));
  A(gid.every(i=>i!==undefined),"group IDs");
  let groupClauses=cmp.G.map(()=>[]);C.forEach((c,i)=>groupClauses[gid[i]].push(i));
  const degree=new Map(vs.map(v=>[v,(I.occ.get(v)||[]).length+(I.occ.get(-v)||[]).length]));
  const order=vs.slice().sort((a,b)=>degree.get(b)-degree.get(a)||a-b);
  let baseline=dpll(C,vs),baseCheck=independent(C,[],baseline.tree);A(baseline.status==="UNSAT","baseline");
  function experiment(mode){
   let db=R.C.map(c=>c.slice()),seen=new Set(db.map(key)),active=new Set(),epochs=[],proofs=[],search=0,lits=0,nodes=0,checkScans=0,checkLits=0,validation=0,selection=0,coreWork={init:0,occ:0,lits:0,assignments:0,reasonVisits:0,pins:0},seeded=0,seedTrials=0,learned=0,peak=db.length,term=null;
   function add(c){let k=key(c);if(seen.has(k))return false;seen.add(k);db.push(c);peak=Math.max(peak,db.length);return true}
   function restore(ids){let fresh=[];for(let i of ids){if(active.has(i))continue;active.add(i);fresh.push(i);for(let j of groupClauses[i])add(C[j])}return fresh}
   function account(p){for(let k of Object.keys(coreWork))coreWork[k]+=p.m[k];if(p.conflict){checkScans+=p.check.scans;checkLits+=p.check.lits;proofs.push(p)}}
   function use(p){account(p);if(!p.conflict)return [];let fresh=restore([...new Set(p.support.map(i=>gid[i]))]);if(mode.includes("guard")&&p.clause.length<=4&&add(p.clause))learned++;return fresh}
   if(mode.includes("seed"))for(let v of order.slice(0,8))for(let l of [-v,v]){seedTrials++;seeded+=use(conflict(C,I,[l])).length}
   for(let t=0;t<=cmp.G.length;t++){
    let r=dpll(db,vs,[],Math.max(1,2000000-search));search+=r.m.scans;lits+=r.m.lits;nodes+=r.m.nodes;
    if(r.status!=="SAT"){term=r;if(r.status==="UNSAT"){let ck=independent(db,[],r.tree);checkScans+=ck.scans;checkLits+=ck.lits}break}
    let a=new Map(r.witness);for(let c of db){validation+=c.length;A(c.some(l=>a.get(Math.abs(l))===+(l>0)),"coarse witness")}
    let violated=[];for(let i=0;i<C.length;i++){validation+=C[i].length;if(!C[i].some(l=>a.get(Math.abs(l))===+(l>0)))violated.push(i)}
    if(!violated.length){term=r;break}
    let old=active.size,ids=[...new Set(violated.map(i=>gid[i]))],fresh,guard=null;
    if(mode==="one")fresh=restore(ids.slice(0,1));else if(mode==="batch")fresh=restore(ids);else{
     let pins=order.map(v=>a.get(v)?v:-v);selection+=pins.length;let p=conflict(C,I,pins);A(p.conflict,"full candidate must conflict");fresh=use(p);guard=p.guard;
     A(p.support.some(i=>violated.includes(i)),"core must reject candidate");
    }
    A(active.size>old,"strict refinement credit");
    epochs.push({fresh,violated:ids.length,guard,active:active.size,clauses:db.length,search:r.m.scans});
   }
   return {mode,status:term?.status||"UNKNOWN",epochs,restored:[...active],finalDB:db,proofs,tree:term?.tree??null,work:{search,lits,nodes,checkScans,checkLits,validation,selection,coreWork,seeded,seedTrials,learned,peak,terminalNodes:term?.m?.nodes,terminalScans:term?.m?.scans}}
  }
  let arms=["one","batch","core","core-guard","seed-core-guard"].map(experiment);
  // Verify all final clauses are from the original projected CNF, an independently checked local relaxation, or a checked guard.
  for(let a of arms){let ok=new Set([...C,...R.C,...a.proofs.map(p=>p.clause)].map(key));A(a.finalDB.every(c=>ok.has(key(c))),"DB provenance");A(a.status==="UNSAT","arm not solved")}
  // Independent conditional guard replay. Compare contradiction-support sets, not their intersection as a proof.
  let [x,y,z]=order,guards=[[-x,-y],[-x,y],[x,-y],[x,y,-z],[x,y,z]],guardTrials=guards.map(g=>conflict(C,I,g));
  let cover=Array.from({length:8},(_,w)=>guards.filter(g=>g.every(l=>{let j=[x,y,z].indexOf(Math.abs(l));return ((w>>j)&1)===+(l>0)})).length);A(cover.every(k=>k===1),"guard partition");
  return {source,rootUnits:[...u.A],early:m,vars:vs,clauses:C.length,residualSha:sha(enc(C)),baseline,baseCheck,groupCount:cmp.G.length,relaxation:{clauses:R.C.length,proof:R.proof,setupTests:R.tests,checkTests:relaxCheck,indexLits:I.lits},arms,guards:{guards,guardTrials,cover}};
 }
 let out=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){let s=JSON.parse(data.corpus).instances.find(x=>x.id===alias),reg=JSON.parse(data.registry).instances.find(x=>x.alias==="EB-"+alias),g=compile({nvars:s.nvars,dimacs:s.dimacs});
  A(sha(enc(g.network))===reg.sha256&&enc(g.network).length*8===reg.N_bits&&sha(s.dimacs)===reg.source_cnf.sha256&&s.dimacs.length*8===reg.source_cnf.N_bits&&sha(enc(g.source_map))===reg.source_map_sha256,"auth");
  let b=norm(g.network),early=meter(),eu=up(b.C,[],early),p=project(b.C,128),q=replay(b.C,p.trace);A(enc(p.C)===enc(q.C),"projection");
  let cnf=s.dimacs.trim().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)));
  out.push({alias,native:test(p.C,reg),cnf:test(cnf,reg.source_cnf),projection:{trace:p.trace,scans:p.scans,pairs:p.pairs,replayScans:q.scans,replayPairs:q.pairs,gauge:b.gauge,normalizationVisits:b.vis,localWords:b.rows,early,earlyUnits:[...eu.A],normalizedSha:sha(enc(b.C)),projectedSha:sha(enc(p.C))}});
 }
 return out;
};
console.log(JSON.stringify(run(data,pins),null,2));

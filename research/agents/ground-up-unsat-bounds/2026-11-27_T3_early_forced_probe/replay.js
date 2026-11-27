/* node replay.js: read pinned dependencies into data object, then call experiment(data,pin). */
const fs=require('node:fs');
const pin={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};
const data=Object.fromEntries(Object.keys(pin).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const experiment=function experiment(data,pin){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,canon,key,solve,check}=new Function(data.native+";return {sha,norm,project,replay,canon,key,solve,check};")();
 const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n";
 A(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
 const corpus=JSON.parse(data.corpus),registry=JSON.parse(data.registry);
 const V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
 function up(C,pins,ctr){
  let P=new Map(); for(const l of pins){let v=Math.abs(l),b=l>0;if(P.has(v)&&P.get(v)!==b)return {conflict:true,P};P.set(v,b)}
  for(;;){let change=false;for(const c of C){ctr.scans++;if(ctr.scans>ctr.cap)throw Error("cap");let free=0,last=0,sat=false;for(let l of c){ctr.lits++;let x=P.get(Math.abs(l));if(x===undefined){free++;last=l}else if(x===(l>0)){sat=true;break}}
   if(sat)continue;if(free===0)return {conflict:true,P};if(free===1){P.set(Math.abs(last),last>0);change=true}
  }if(!change)return {conflict:false,P}}
 }
 function stats(cap=3000000){return {scans:0,lits:0,cap,probes:0,passes:0,learned:0,units:0,binaries:0,rootFixed:0,rootClauses:null}}
 function reduce(C,P){return C.filter(c=>!c.some(l=>P.get(Math.abs(l))===(l>0))).map(c=>c.filter(l=>!P.has(Math.abs(l))))}
 function learn(base,mode,cap=3000000){
  let C=base.map(c=>c.slice()), seen=new Set(C.map(key)), tr=[],m=stats(cap),pair=false;
  function add(c){c=canon(c);let k=key(c);if(seen.has(k))return false;seen.add(k);C.push(c);tr.push(c);m.learned++;if(c.length===1)m.units++;if(c.length===2)m.binaries++;return true}
  try{for(;;){
   m.passes++;let root=up(C,[],m);m.rootFixed=root.P.size;m.rootClauses=reduce(C,root.P).length;
   if(root.conflict){add([]);return {status:"UNSAT",m,tr}}
   let old=tr.length,vs=V(C).filter(v=>!root.P.has(v));
   for(let v of vs){
    let curr=up(C,[],m);if(curr.conflict){add([]);return {status:"UNSAT",m,tr}}if(curr.P.has(v))continue;
    let out=[];
    for(let l of [v,-v]){m.probes++;let u=up(C,[l],m);out.push(u);
     if(u.conflict){add([-l]);break}
     if(mode!=="unit"){for(let [w,b] of u.P){if(w===v||curr.P.has(w))continue;add([-l,b?w:-w])}}
    }
    if(out.length===2&&!out[0].conflict&&!out[1].conflict&&mode!=="unit"){
      for(let [w,b] of out[0].P)if(w!==v&&!curr.P.has(w)&&out[1].P.get(w)===b)add([b?w:-w]);
    }
    if(tr.length>old&&mode==="unit")break;
   }
   if(tr.length>old)continue;
   if(mode==="pair"){
    pair=true;let found=false;
    outer:for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)for(let a of [vs[i],-vs[i]])for(let b of [vs[j],-vs[j]]){m.probes++;if(up(C,[a,b],m).conflict&&add([-a,-b])){found=true;break outer}}
    if(found)continue;
   }
   return {status:"UNKNOWN_FIXED_POINT",m,tr,pair};
  }}catch(e){if(String(e.message)!=="cap")throw e;return {status:"UNKNOWN_CAP",m,tr,pair}}
 }
 function verify(base,tr){let C=base.map(c=>c.slice()),m=stats(50000000);
  for(let c of tr){if(!up(C,c.map(l=>-l),m).conflict)throw Error("invalid learned "+key(c));C.push(c)}
  return {clauses:tr.length,scans:m.scans,lits:m.lits,contradiction:tr.some(c=>!c.length)};
 }
 function affine(C){let vars=V(C),idx=new Map(vars.map((v,i)=>[v,i])),groups=new Map(),work=0,rank=0,eq=0,B=new Map();
  for(let c of C){let v=V([c]),k=key(v);if(!groups.has(k))groups.set(k,{v,cs:[]});groups.get(k).cs.push(c)}
  for(let {v,cs} of groups.values()){if(v.length>8)continue;let words=[];for(let w=0;w<2**v.length;w++){work+=cs.length;if(cs.every(c=>c.some(l=>Boolean((w>>v.indexOf(Math.abs(l)))&1)===(l>0))))words.push(w)}
   if(!words.length)return {status:"UNSAT",work,rank,eq};
   let parity=x=>{let b=0;while(x){x&=x-1;b^=1}return b};
   for(let mask=1;mask<2**v.length;mask++){let b=parity(mask&words[0]);work+=words.length;if(!words.every(w=>parity(mask&w)===b))continue;
    eq++;let x=0n;v.forEach((l,i)=>{if(mask>>i&1)x|=1n<<BigInt(idx.get(l))});
    while(x){work++;let j=x.toString(2).length-1;if(!B.has(j)){B.set(j,[x,b]);rank++;break}let [z,t]=B.get(j);x^=z;b^=t}
    if(!x&&b)return {status:"UNSAT",work,rank,eq};
   }
  }return {status:"UNKNOWN",work,rank,eq}
 }
 function hall(C){let work=0,best=0;for(let order of [C,[...C].reverse(),[...C].sort((a,b)=>a.length-b.length)]){let seen=new Set(),groups=[];
   for(let c of order){work+=c.length;if(c.some(l=>seen.has(l)))continue;c.forEach(l=>seen.add(l));groups.push(V([c]))}
   let M=new Map();function aug(i,S){for(let v of groups[i]){work++;if(S.has(v))continue;S.add(v);if(!M.has(v)||aug(M.get(v),S)){M.set(v,i);return true}}return false}
   let count=0;for(let i=0;i<groups.length;i++)if(aug(i,new Set()))count++;best=Math.max(best,groups.length-count);if(count<groups.length)return {status:"UNSAT",work,deficiency:best};
  }return {status:"UNKNOWN",work,deficiency:best};
 }
 function test(C){
  let m=stats();let u=up(C,[],m);let D=reduce(C,u.P);
  let unit=learn(C,"unit"), imp=learn(C,"imp"), hybrid=learn(C,"pair");
  let au=verify(C,unit.tr),ai=verify(C,imp.tr),ah=verify(C,hybrid.tr);
  const dpll=solve(C,3000000);const dpllCheck=dpll.status==="UNSAT"?check(C,dpll.tree):null;
  let al=affine(D),ha=hall(D),sep=project(D,16);
  return {root:{scans:m.scans,lits:m.lits,fixed:u.P.size,varsBefore:V(C).length,varsAfter:V(D).length,clausesBefore:C.length,clausesAfter:D.length},unit,imp,hybrid,checks:{unit:au,imp:ai,hybrid:ah},affine:al,hall:ha,separator:{status:sep.C.some(c=>!c.length)?"UNSAT":"UNKNOWN",scans:sep.scans,pairs:sep.pairs,eliminations:sep.trace.length},dpll,dpllCheck}
 }
 let results=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const src=corpus.instances.find(x=>x.id===alias), reg=registry.instances.find(x=>x.alias==="EB-"+alias);
  A(sha(src.dimacs)===reg.source_cnf.sha256&&src.dimacs.length*8===reg.source_cnf.N_bits,"CNF fingerprint");
  const built=compile({nvars:src.nvars,dimacs:src.dimacs}), bytes=enc(built.network);
  A(sha(bytes)===reg.sha256&&bytes.length*8===reg.N_bits,"native fingerprint");
  A(sha(enc(built.source_map))===reg.source_map_sha256,"map fingerprint");
  let b=norm(built.network),early=stats(),initial=up(b.C,[],early);
  let p=project(b.C,128),q=replay(b.C,p.trace);
  A(p.C.map(key).sort().join(";")===q.C.map(key).sort().join(";"),"projection replay");
  let native=test(p.C);
  let clauses=src.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
  let cnf=test(clauses);
  let proof={schema:"T3-PROBE-RUP-v1",problem_id:"STRICT-EB4-v1",instance:reg.short_id,instance_id:reg.instance_id,original_N_bits:reg.N_bits,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,built.network.types.length-1],ports:[0,built.network.types.length*4-1],edges:[0,built.network.edges.length-1]},parents:[],gauge:{root_port:b.gauge-1,value:0,justification:"global complement preserves E4/B4 and signed edges"},projection_trace:p.trace,projected_sha:sha(enc(p.C)),rup_trace:native.imp.status==="UNSAT"?native.imp.tr:native.hybrid.tr,checker:"pinned norm, independent exact replay of DP projection, then RUP each learned clause via negated assumptions; empty clause is terminal",scope:"native zero-energy feasibility, not all-input coverage",pin};
  let cproof={schema:"T3-PROBE-RUP-v1",problem_id:"DIMACS-CNF-v1",instance:reg.source_cnf.short_id,instance_id:reg.source_cnf.instance_id,original_N_bits:reg.source_cnf.N_bits,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[1,src.nvars],clauses:[1,src.nclauses]},parents:[],rup_trace:cnf.imp.status==="UNSAT"?cnf.imp.tr:cnf.hybrid.tr,checker:"sequential RUP by UP on exact ordered CNF",pin};
  results.push({alias,reg,norm:{vis:b.vis,rows:b.rows,components:b.components,clauses:b.C.length,gauge:b.gauge,early:{fixed:initial.P.size,scans:early.scans,lits:early.lits}},projection:{pairs:p.pairs,scans:p.scans,steps:p.trace.length,replayPairs:q.pairs,replayScans:q.scans},native,cnf,proof,cproof,proofHash:sha(enc(proof)),cproofHash:sha(enc(cproof))});
 }
 let cube=Array.from({length:16},(_,w)=>Array.from({length:4},(_,i)=>w>>i&1?-(i+1):i+1));
 let control=learn(cube,"pair");A(control.status==="UNKNOWN_FIXED_POINT"&&control.tr.length===0,"control");
 let tiny=[[1,2],[-1,2],[1,-2,3],[-1,-2,3]];
 let tc=learn(tiny,"imp");verify(tiny,tc.tr);
 return {results,controls:{cube:control,tiny:tc}};
};
console.log(JSON.stringify(experiment(data,pin),null,2));

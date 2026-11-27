const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,solve,check,up,key,canon}=new Function(data.native+";return {sha,norm,project,replay,solve,check,up,key,canon};")();
 const A=(x,m)=>{if(!x)throw Error(m)},enc=o=>JSON.stringify(o)+"\n",V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),mod=x=>(x%3+3)%3;
 function arm(C,mode,width,native){
  let start=Date.now(),m={scans:0,lits:0,cap:10000000},u=up(C,[],m);A(!u.conflict,"root");
  let D=C.slice(),seen=new Set(D.map(key)),proof=[],pairs=0,score=0,changes=[],flips=0,states=[],verification=0,stop="DONE";
  function descend(initial){
   let vs=V(D),val=new Map(vs.map(v=>[v,u.A.has(v)?u.A.get(v):initial])),inc=new Map(vs.map(v=>[v,[]]));
   const fields=c=>{let k=0,s=0;for(let l of c){score++;if(val.get(Math.abs(l))===+(l>0)){k++;s+=l>0?1:-1}}return [k,k%3,mod(s)]};
   let F=D.map((c,i)=>{for(let l of c)inc.get(Math.abs(l)).push([i,l]);return fields(c)}),bad=F.filter(f=>!f[0]).length,initialBad=bad,moves=[];
   while(bad&&score<2000000){
    let best=-1,plain=-1,gain=0,bz=Infinity;
    for(let v of vs){if(u.A.has(v))continue;let g=0,dz=0;for(let [i,l] of inc.get(v)){score++;let [k,_,s]=F[i],d=val.get(v)===+(l>0)?-1:1,nk=k+d,ns=mod(s+d*(l>0?1:-1));g+=+(k===0)-+(nk===0);dz+=+(nk>0&&ns===0)-+(k>0&&s===0)}
     if(g>gain){gain=g;plain=best=v;bz=dz}else if(g===gain&&g>0&&mode==="residue"&&dz<bz){best=v;bz=dz}}
    if(gain<=0)break;if(best!==plain)changes.push({initial,step:moves.length,plain,best,gain});
    for(let [i,l] of inc.get(best)){let [k,_,s]=F[i],d=val.get(best)===+(l>0)?-1:1;F[i]=[k+d,(k+d)%3,mod(s+d*(l>0?1:-1))]}
    val.set(best,1-val.get(best));bad-=gain;flips++;moves.push([best,gain,bad,F.filter(f=>f[0]&&f[2]===0).length])
   }
   A(F.every((f,i)=>f.join()===fields(D[i]).join()),"residue replay");A(D.filter(c=>!c.some(l=>val.get(Math.abs(l))===+(l>0))).length===bad,"score replay");
   states.push({initial,initialBad,moves,bad,cap:score>=2000000,assignmentSha:sha(enc([...val]))})
  }
  if(["flip","table","residue"].includes(mode)){descend(0);descend(1)}
  if(["deduction","table","residue"].includes(mode)){
   for(let round=0;round<4;round++){
    let before=D.length,inc=new Map();for(let i=0;i<before;i++)for(let l of D[i]){if(!inc.has(l))inc.set(l,[]);inc.get(l).push(i)}
    outer:for(let v of V(D))for(let i of inc.get(v)||[])for(let j of inc.get(-v)||[]){
     if(pairs>=40000||proof.length>=2000){stop="DEDUCTION_CAP";break outer}pairs++;
     let a=D[i],b=D[j],r=canon([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);if(r.length>width||r.some(l=>r.includes(-l))||seen.has(key(r)))continue;
     seen.add(key(r));proof.push({i,j,v,r});D.push(r)}
    if(D.length===before||stop!=="DONE")break;
   }
   if(["table","residue"].includes(mode)){descend(0);descend(1)}
  }
  let E=C.slice();for(let {i,j,v,r} of proof){A(i<E.length&&j<E.length&&E[i].includes(v)&&E[j].includes(-v),"parent");let a=new Set([...E[i],...E[j]]);a.delete(v);a.delete(-v);A(![...a].some(l=>a.has(-l))&&a.size===r.length&&r.every(l=>a.has(l)),"resolvent");verification+=E[i].length+E[j].length+r.length;E.push(r)}
  let p=native?project(D,128):{C:D,trace:[],pairs:0,scans:0,peak:D.length},rp=native?replay(E,p.trace):{C:E,pairs:0,scans:0};
  A([...new Set(p.C.map(key))].sort().join(";")===[...new Set(rp.C.map(key))].sort().join(";"),"projection");
  let s=solve(p.C,500000),ck=s.status==="UNSAT"?check(rp.C,s.tree):null;
  return {mode,width,status:s.status,early:m,initialUnits:[...u.A],initialVars:V(C).length,initialClauses:C.length,finalVars:V(p.C).length,finalClauses:p.C.length,proof,pairs,score,changes,flips,states,verification,stop,peakRows:D.length,projection:{trace:p.trace,pairs:p.pairs,scans:p.scans,peak:p.peak,replayPairs:rp.pairs,replayScans:rp.scans},terminal:s,check:ck,ms:Date.now()-start};
 }
 let out=[],corpus=JSON.parse(data.corpus),reg=JSON.parse(data.registry);
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const s=corpus.instances.find(x=>x.id===alias),g=compile({nvars:s.nvars,dimacs:s.dimacs}),R=reg.instances.find(x=>x.alias==="EB-"+alias);
  A(sha(enc(g.network))===R.sha256&&enc(g.network).length*8===R.N_bits&&sha(s.dimacs)===R.source_cnf.sha256&&s.dimacs.length*8===R.source_cnf.N_bits&&sha(enc(g.source_map))===R.source_map_sha256,"authentication");
  let b=norm(g.network),cnf=s.dimacs.trimEnd().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)));
  let nat=[],comp=[];for(let mode of ["base","flip","deduction","table","residue"])nat.push(arm(b.C,mode,2,true));
  for(let w of [2,4])for(let mode of ["base","flip","deduction","table","residue"])comp.push(arm(cnf,mode,w,false));
  out.push({alias,R,normalization:{gauge:b.gauge,components:b.components,vis:b.vis,rows:b.rows,clauses:b.C.length},nat,comp})
 }
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(l=>-l)]);
 return {out,control:[2,4].map(w=>arm(fano,"residue",w,false))};
};
console.log(JSON.stringify(run(data),null,2));

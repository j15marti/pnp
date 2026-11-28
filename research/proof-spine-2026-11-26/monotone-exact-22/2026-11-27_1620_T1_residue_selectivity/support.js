// Node: node support.js DIR; files named corpus,registry,native from pins.
const fs=require('node:fs');const files={"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};const d=Object.fromEntries(Object.keys(files).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function run(d){
 const {sha,canon}=new Function(d.native+";return {sha,canon};")(),b=JSON.parse(d.corpus),reg=JSON.parse(d.registry),A=(x,m)=>{if(!x)throw Error(m)},out=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const started=Date.now(),x=b.instances.find(x=>x.id===alias),ent=reg.instances.find(x=>x.alias==="EB-"+alias).source_cnf,n=x.nvars,C=x.dimacs.trimEnd().split("\n").slice(1).map(s=>canon(s.trim().split(/\s+/).map(Number).slice(0,-1)));
  A(sha(x.dimacs)===ent.sha256&&x.dimacs.length*8===ent.N_bits,"auth");
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
  out.push({problem_id:"DIMACS-CNF-v1",instance:ent.short_id,instance_id:ent.instance_id,original_N_bits:ent.N_bits,source_pin:files,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,C.length],variables:[1,n]},parents:[],claim:terminal?"checked contradiction by sparse integer row support, exclusion intersection and unit closure":"no terminal under named positive exact-one source scan",alias,rows,stageStats,units:[...units.values()],terminal,status:terminal?"UNSAT":"UNKNOWN",counts,ms:Date.now()-started,scope:"no provenance; no peer proof advice; fixed one/three row scan, signed positive exact-one rows only. Not universal."})
 }
 return out
}
console.log(JSON.stringify(run(d),null,2));

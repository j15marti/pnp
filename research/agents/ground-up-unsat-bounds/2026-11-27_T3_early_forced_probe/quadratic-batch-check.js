const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"results":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_early_forced_probe/results.json","1d0dc7becd25027a2e6b2f2d28ce93ffb63ff047"],"scope":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_early_forced_probe/scope-audit-results.json","5aa377092eb1101e94cf7af2a44de24ba050be00"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data,pins){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,replay,key,canon}=new Function(data.native+";return {sha,norm,replay,key,canon};")();
 const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n",V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
 const reg=JSON.parse(data.registry),corp=JSON.parse(data.corpus),old=JSON.parse(data.results),sc=JSON.parse(data.scope);
 const parity=a=>{let b=0;while(a){a&=a-1n;b^=1}return b};
 function up(C,ass,m){
  let a=new Map();for(let l of ass){let v=Math.abs(l);if(a.has(v)&&a.get(v)!==l)return {a,conflict:true};a.set(v,l)}
  for(;;){let change=false;for(let c of C){m.scans++;if(m.scans>m.cap)throw Error("cap");let free=0,last=0,sat=false;for(let l of c){m.lits++;let v=a.get(Math.abs(l));if(v===l){sat=true;break}if(v===undefined){free++;last=l}}
   if(sat)continue;if(!free)return {a,conflict:true};if(free===1){a.set(Math.abs(last),last);change=true}}
   if(!change)return {a,conflict:false}}
 }
 const meter=(cap=8000000)=>({scans:0,lits:0,cap,probes:0,rounds:0,candidateGuards:0,skip:0});
 function simplify(C,a){return C.filter(c=>!c.some(l=>a.get(Math.abs(l))===l)).map(c=>c.filter(l=>!a.has(Math.abs(l))))}
 function batch(base,guard=[]){
  let C=[...base,...guard.map(l=>[l])], seen=new Set(C.map(key)),trace=[],m=meter(),rounds=[],status="UNKNOWN_FIXED_POINT";
  function learn(c){let k=key(c);if(seen.has(k))return;seen.add(k);trace.push(c);C.push(c)}
  try{for(;;){m.rounds++;let u=up(C,[],m);if(u.conflict){learn([]);status="UNSAT";break}
   let D=simplify(C,u.a);if(!D.length){status="SAT";break}
   let vs=V(D),prev=trace.length, pending=new Map(),known=new Set(D.map(key));const add=c=>{c=canon(c);let k=key(c);if(!known.has(k))pending.set(k,c)};
   for(let v of vs)for(let l of [v,-v]){m.probes++;let r=up(D,[l],m);if(r.conflict)add([-l]);else for(let w of r.a.values())if(Math.abs(w)!==v)add([-l,w])}
   if(!pending.size){for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)for(let a of [vs[i],-vs[i]])for(let b of [vs[j],-vs[j]]){m.candidateGuards++;let c=canon([-a,-b]);if(known.has(key(c))){m.skip++;continue}m.probes++;if(up(D,[a,b],m).conflict)add(c)}}
   for(let c of pending.values())learn(c);
   rounds.push({vars:vs.length,clauses:D.length,learned:trace.length-prev,scans:m.scans});
   if(prev===trace.length)break;
  }}catch(e){if(e.message!=="cap")throw e;status="UNKNOWN_CAP"}
  return {status,guard,trace,m,rounds};
 }
 function checkRup(base,res){let C=[...base,...res.guard.map(l=>[l])],m=meter(50000000);for(let c of res.trace){A(up(C,c.map(l=>-l),m).conflict,"RUP check");C.push(c)}return {scans:m.scans,lits:m.lits,clauses:res.trace.length}}
 function checkQuadratic(C,certificate){
  const vs=certificate.variables,n=vs.length,one=1n<<BigInt(n),mask=one-1n,idx=new Map(vs.map((v,i)=>[v,i])),rows=[],work={scopeWords:0,clauseTests:0,rankOps:0,coefficientEvaluations:0,failureTests:0};
  for(let e of certificate.certificate){let reason=e.reason,S=reason.scope,local=reason.local,row=BigInt("0x"+e.row),derived=0n;
   A(local.every(i=>i>=0&&i<C.length&&C[i].every(l=>S.includes(Math.abs(l)))),"scope support");
   for(let i=0;i<S.length;i++)if(reason.mask>>i&1)derived|=1n<<BigInt(idx.get(S[i]));if(reason.b)derived|=one;
   A(row===derived,"row derivation");let allowed=0;
   for(let w=0;w<2**S.length;w++){work.scopeWords++;let ok=true;for(let i of local){work.clauseTests++;if(!C[i].some(l=>+(l>0)===(w>>S.indexOf(Math.abs(l))&1))){ok=false;break}}if(ok){allowed++;A(parity(BigInt(w&reason.mask))===reason.b,"row not forced")}}
   A(allowed>0,"empty scope");rows.push(row);
  }
  function echelon(rs){let M=new Map();for(let row of rs){let a=row;while(a&mask){let j=(a&mask).toString(2).length-1;if(!M.has(j)){M.set(j,a);break}a^=M.get(j);work.rankOps++}if(!(a&mask))A(a===0n,"linear contradiction")}return M}
  const claimed=certificate.basis.map(([p,a])=>BigInt("0x"+a)),M=echelon(rows),B=echelon(claimed);A(M.size===B.size&&M.size===certificate.rank,"rank");
  for(let row of claimed){let a=row;while(a&mask){let j=(a&mask).toString(2).length-1;A(M.has(j),"basis span");a^=M.get(j);work.rankOps++}A(a===0n,"basis constant")}
  const free=vs.map((v,i)=>i).filter(i=>!B.has(i)),k=free.length;
  const q=certificate.quadratic.clauseIndices;A(q.every(i=>C[i].length<=2),"degree");
  function lift(w){let x=0n;free.forEach((p,i)=>{if(w>>BigInt(i)&1n)x|=1n<<BigInt(p)});for(let p of [...B.keys()].sort((a,b)=>a-b)){let row=B.get(p),z=parity(row&mask&x)^+(Boolean(row&one));if(z)x|=1n<<BigInt(p)}for(let row of rows)A(parity(row&mask&x)===+(Boolean(row&one)),"lift");return x}
  function evalAt(w){let x=lift(w),sum=0;work.coefficientEvaluations++;for(let i of q){work.failureTests++;sum^=+C[i].every(l=>Boolean(x&(1n<<BigInt(idx.get(Math.abs(l)))))!==(l>0))}A(sum===1,"quadratic identity")}
  evalAt(0n);for(let i=0;i<k;i++)evalAt(1n<<BigInt(i));for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)evalAt((1n<<BigInt(i))|(1n<<BigInt(j)));
  return {rank:M.size,free:k,terms:q.length,work,verified:true};
 }
 let out=[];
 for(let r of old.results){
  let s=corp.instances.find(x=>x.id===r.alias),g0=compile({nvars:s.nvars,dimacs:s.dimacs}),R=reg.instances.find(x=>x.alias==="EB-"+r.alias);
  A(sha(enc(g0.network))===R.sha256&&enc(g0.network).length*8===R.N_bits&&sha(s.dimacs)===R.source_cnf.sha256&&sha(enc(g0.source_map))===R.source_map_sha256,"source");
  let b=norm(g0.network),p=replay(b.C,r.proof.projection_trace);A(sha(enc(p.C))===r.proof.projected_sha,"chart");
  let m=meter(),u=up(p.C,[],m),D=simplify(p.C,u.a),scope=sc.results.find(x=>x.alias===r.alias);
  let cnf=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
  let algebra=null;if(r.alias==="JOINT-24")algebra={native:checkQuadratic(D,scope.pair.native),cnf:checkQuadratic(cnf,scope.pair.cnf),nativeSingle:checkQuadratic(D,scope.local.native),cnfSingle:checkQuadratic(cnf,scope.local.cnf)};
  let nat=batch(D),nc=checkRup(D,nat),comp=batch(cnf),cc=checkRup(cnf,comp);
  // Partition on source-only occurrence scores, excluding gauge; five exhaustive disjoint cells.
  let degree=new Map();for(let c of D)for(let l of c){let v=Math.abs(l);degree.set(v,(degree.get(v)||0)+1)}
  let [x,y,z]=[...degree].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(a=>a[0]);
  let guards=[[-x,-y],[-x,y],[x,-y],[x,y,-z],[x,y,z]],coverage=[];
  for(let w=0;w<8;w++){let a=new Map([[x,!!(w&1)],[y,!!(w&2)],[z,!!(w&4)]]);coverage.push(guards.filter(g=>g.every(l=>a.get(Math.abs(l))===(l>0))).length)}A(coverage.every(v=>v===1),"guard coverage");
  let gr=[];for(let guard of guards){let gm=meter(1000000),u=up(D,guard,gm);gr.push({guard,rootConflict:u.conflict,rootFixed:u.a.size,free:V(simplify(D,u.a)).length,work:gm})}
  out.push({alias:r.alias,instance_id:R.instance_id,original_N_bits:R.N_bits,source_pin:pins,algebra,native:{...nat,check:nc},cnf:{...comp,check:cc},initial:{work:m,units:[...u.a.values()],clauses:D.length,variables:V(D)},guards:{partition:guards,coverage,root:gr},chart:{gauge:b.gauge,root_units:[...u.a.values()],projection_trace:r.proof.projection_trace,normalized_sha:sha(enc(b.C)),projected_sha:sha(enc(p.C)),simplified_sha:sha(enc(D))}});
 }
 return out;
};
console.log(JSON.stringify(run(data,pins),null,2));

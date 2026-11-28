// Node: node syzygy.js DIR; files named corpus,registry,native,peer.
const fs=require('node:fs');
const pins={"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"peer":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/JOINT-24.singleton-hall.json","b923e2b97b9c6cc6d789168847f2ab9f6a6287f9"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function experiment(data,pins){
 const {sha,canon,up}=new Function(data.native+";return {sha,canon,up};")();
 const reg=JSON.parse(data.registry),corpus=JSON.parse(data.corpus),peer=JSON.parse(data.peer);
 const A=(a,m)=>{if(!a)throw Error(m)},eq=(a,b)=>canon(a).join()===canon(b).join(),out=[];
 for(const alias of ["JOINT-24","RANDOM-3CNF-40"]){
  const start=Date.now(),s=corpus.instances.find(x=>x.id===alias),ent=reg.instances.find(x=>x.alias==="EB-"+alias).source_cnf,n=s.nvars;
  A(sha(s.dimacs)===ent.sha256&&s.dimacs.length*8===ent.N_bits,"auth");
  const C=s.dimacs.trimEnd().split("\n").slice(1).map(x=>canon(x.trim().split(/\s+/).map(Number).slice(0,-1))),index=new Map(C.map((c,i)=>[c.join(),i+1]));
  let counts={rowLookups:0,combos:0,guardTests:0,coefficientOps:0,verifyClauseReads:0,verifyCoefficientOps:0,upVisits:0,geXors:0};
  const get=c=>{counts.rowLookups++;return index.get(canon(c).join())};
  const rows=[];
  for(let i=0;i<C.length;i++){let v=C[i];if(!v.length||!v.every(l=>l>0))continue;let ids=[i+1],ok=true;
   for(let a=0;a<v.length;a++)for(let b=a+1;b<v.length;b++){let z=get([-v[a],-v[b]]);if(!z)ok=false;else ids.push(z)}
   if(ok)rows.push({v,ids});
  }
  function verifyRow(r){
   let expected=[r.v,...r.v.flatMap((v,i)=>r.v.slice(i+1).map(w=>[-v,-w]))];
   for(let c of expected){counts.verifyClauseReads+=r.ids.length;A(r.ids.some(id=>eq(C[id-1],c)),"exact-one row");}
  }
  function verifySyzygy(p){
   const b=new Int32Array(n+1);let rhs=0;
   for(let [r,sign] of p.terms){verifyRow(r);rhs+=sign;for(let v of r.v){b[v]+=sign;counts.verifyCoefficientOps++}}
   A(rhs===p.rhs,"rhs");
   const [v,z]=p.guard,forced=new Map([[v,z]]);
   for(let [w,id] of p.zeroReasons){counts.verifyClauseReads++;A(z===1&&eq(C[id-1],[-v,-w]),"bad pair");forced.set(w,0)}
   let upper=0;for(let i=1;i<=n;i++){counts.verifyCoefficientOps++;upper+=forced.has(i)?b[i]*forced.get(i):Math.max(0,b[i]);}
   A(upper<rhs&&upper===p.upper,"not a contradiction");return z===1?-v:v;
  }
  const peerAudit=[];
  if(alias==="JOINT-24"){
   A("CERT-v1:sha256:"+sha(data.peer)==="CERT-v1:sha256:3f669411797c44b34514243c32334e7d3acd0a486ec285124e6b81d8ba23f3ca","peer hash");
   for(let p of peer.certs){let terms=[...p.rowsPlus.map(r=>[r,1]),...p.rowsMinus.map(r=>[r,-1])];let q={terms,rhs:p.rhs,guard:p.guard[0],zeroReasons:p.zeroReasons,upper:0};A(verifySyzygy(q)===p.unit,"unit");peerAudit.push(p.unit)}
  }
  // From original clauses only: all singleton guard states; no Hall partition assumptions.
  const guards=[];for(let v=1;v<=n;v++)for(let z=0;z<=1;z++){const zero=[];if(z)for(let w=1;w<=n;w++)if(w!==v){let id=get([-v,-w]);if(id)zero.push([w,id])}guards.push({v,z,zero,zeroSet:new Set(zero.map(a=>a[0]))})}
  const found=new Map(),b=new Int32Array(n+1),chosen=[],LIMIT=2000000;
  function check(rhs){
   counts.combos++;let nz=[],ub=0;for(let v=1;v<=n;v++){counts.coefficientOps++;if(b[v])nz.push(v);if(b[v]>0)ub+=b[v]}
   if(rhs<=0)return; // Multiplication by -1 is separately enumerated.
   for(let g of guards){if(counts.guardTests>=LIMIT)return;counts.guardTests++;let unit=g.z?-g.v:g.v;if(found.has(unit))continue;
    let u=ub;for(let v of nz){counts.coefficientOps++;if(v===g.v)u+=b[v]*g.z-Math.max(0,b[v]);else if(b[v]>0&&g.zeroSet.has(v))u-=b[v];}
    if(u<rhs){const p={terms:chosen.map(([i,sign])=>[rows[i],sign]),rhs,guard:[g.v,g.z],zeroReasons:g.zero.filter(([v])=>b[v]>0),upper:u};
     A(verifySyzygy(p)===unit,"discovery verification");found.set(unit,p)}
   }
  }
  function rec(from,left,rhs){if(counts.guardTests>=LIMIT)return;if(!left){check(rhs);return}for(let i=from;i<=rows.length-left;i++){for(let sign of [1,-1]){chosen.push([i,sign]);for(let v of rows[i].v){b[v]+=sign;counts.coefficientOps++}rec(i+1,left-1,rhs+sign);for(let v of rows[i].v){b[v]-=sign;counts.coefficientOps++}chosen.pop()}}}
  let depths=[];for(let k=1;k<=4;k++){const prev=found.size;rec(0,k,0);depths.push({k,added:found.size-prev,total:found.size});if(counts.guardTests>=LIMIT)break}
  // Independent parity certificate: RREF over GF(2), track exact source-row and unit parents.
  function closure(units){
   let live=new Map(units.map(l=>[Math.abs(l),+(l>0)])),trace=[],u0={scans:0,lits:0,cap:1000000};
   if(live.size!==units.length)return {status:"opposite certified units",trace};
   for(let iteration=0;iteration<=n;iteration++){
    let r=up(C,[...live],u0);if(r.conflict){counts.upVisits+=u0.lits;return {status:"UNSAT",trace,units:[...live],up:u0}}
    for(let [v,z] of r.A)if(!live.has(v)){live.set(v,z);trace.push({type:"UP",v,z})}
    const eqs=[...rows.map((r,i)=>({m:r.v.reduce((m,v)=>m|(1n<<BigInt(v)),1n),parents:1n<<BigInt(i)})),...[...live].map(([v,z],i)=>({m:(1n<<BigInt(v))|BigInt(z),parents:1n<<BigInt(rows.length+i)}))];
    let B=new Map();
    for(let q of eqs){let {m,parents}=q;while(m>1n){let v=m.toString(2).length-1;if(!B.has(v)){B.set(v,{m,parents});break}let a=B.get(v);m^=a.m;parents^=a.parents;counts.geXors++}if(m===1n){counts.upVisits+=u0.lits;return {status:"UNSAT parity",trace,parents:parents.toString(),live:[...live],up:u0}}}
    // RREF remove lower pivots from all higher rows.
    let keys=[...B.keys()].sort((a,b)=>a-b);for(let v of keys)for(let w of keys)if(w>v&&((B.get(w).m>>BigInt(v))&1n)){B.get(w).m^=B.get(v).m;B.get(w).parents^=B.get(v).parents;counts.geXors++}
    let newFacts=[];for(let [v,q] of B)if((q.m>>1n)===(1n<<BigInt(v-1))&&!live.has(v)){const p={v,z:Number(q.m&1n),parents:q.parents.toString(),unitOrder:[...live]};let mm=0n;for(let i=0;i<eqs.length;i++)if((q.parents>>BigInt(i))&1n)mm^=eqs[i].m;A(mm===q.m,"parity replay");newFacts.push(p)}
    if(!newFacts.length){counts.upVisits+=u0.lits;return {status:"UNKNOWN",trace,units:[...live],up:u0}}
    for(let q of newFacts){trace.push({type:"GF2",...q});live.set(q.v,q.z)}
   }throw Error("loop")
  }
  const discovery=closure([...found.keys()]),cooperative=peerAudit.length?closure(peerAudit):null;
  const meta={problem_id:"DIMACS-CNF-v1",instance:ent.short_id,instance_id:ent.instance_id,original_N_bits:ent.N_bits,source_pin:pins,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,C.length],variables:[1,n]},parents:[],claim:"bounded exact-one signed-syzygy singleton discovery, conditional scoped closure only"};
  out.push({...meta,alias,rows,depths,certs:[...found].map(([unit,p])=>({unit,...p})),discovery,peerAudit,peerParent:peerAudit.length?"CERT-v1:sha256:"+sha(data.peer):null,cooperative,counts,ms:Date.now()-start,scope:"source-only bounded four-row search; separate peer-replay arm, no map to native; root propagation and parity closure; no universal coverage."})
 }
 return out
}
console.log(JSON.stringify(experiment(data,pins),null,2));

const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"reg":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"hash":["research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js","4a42c99a37a2a22c1ac36ed204eadce7dfa77908"],"joint":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/JOINT-24.cert.json","eb3eb5f2098fbfa73cd11540ba270ac997438f78"],"random":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/RANDOM-3CNF-40.cert.json","f96bea02c40c7545eb32c7fd5ac37afac7e436e8"]};
function run(d,pins){
 const enc=x=>JSON.stringify(x)+"\n",sha=new Function(d.hash.slice(d.hash.indexOf("function sha("),d.hash.indexOf("if(require.main"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,up,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,up,solve,replay}")();
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
 const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=c=>canon(c).join(","),abs=c=>c.map(Math.abs),degree=3,results=[];
 for(const id of ["JOINT-24","RANDOM-3CNF-40"]){
  const name=id==="JOINT-24"?"joint":"random",x=JSON.parse(d.corpus).instances.find(q=>q.id===id),r=JSON.parse(d.reg).instances.find(q=>q.alias==="EB-"+id),G=compile(x),s=enc(G.network);
  if(sha(s)!==r.sha256||s.length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth");
  const p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,early=up(F),ad=adapter(p,G,x.dimacs,x.nvars),ce=up(ad.orig),S=solve(F),C=solve(ad.orig),baseReplay=replay(F,S.tree),compReplay=replay(ad.orig,C.tree);
  const ch=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mh=sha(enc({root:p.root,phase:p.phase})),guard="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,guard,"EB-CHART-SYZYGY-v1",ch,mh]));
  let peer=JSON.parse(d[name]);if(ch!==peer.chartHash||mh!==peer.mapHash||guard!==peer.internal_guard||rid!==peer.internal_residual)throw Error("peer chart");
  let P=peer.proof.filter(q=>q[0]===peer.anchor).map(q=>q.slice(1)),learned=F.slice(),rupVisits=0;
  for(let q of P){let u=up(learned,q.map(l=>[Math.abs(l),+(l<0)]));rupVisits+=u.work;if(!u.conflict)throw Error("RUP");learned.push(q)}
  let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),candidates=[],selection=0;
  for(let v of vars){let inc=F.filter(c=>{selection+=c.length;return abs(c).includes(v)}),scope=[v,...[...new Set(inc.flat().map(Math.abs))].filter(u=>u!==v).sort((a,b)=>a-b)];if(scope.length<=12)candidates.push({v,scope})}
  candidates.sort((a,b)=>a.scope.length-b.scope.length||a.v-b.v);
  let regions=[];
  for(let {v,scope} of candidates.slice(0,3)){
   let sourceRows=F.map((c,i)=>[c,i]).filter(([c])=>abs(c).every(u=>scope.includes(u))).map(([c,i])=>i),src=sourceRows.map(i=>F[i]),seeds=P.filter(c=>c.length&&abs(c).every(u=>scope.includes(u))),idx=new Map(scope.map((u,i)=>[u,i])),masks=[];
   function gen(start,m,k){masks.push(m);if(k)for(let i=start;i<scope.length;i++)gen(i+1,m|(1<<i),k-1)}gen(0,0,degree);
   let D=masks.length,mi=new Map(masks.map((m,i)=>[m,i])),pop=m=>{let n=0;while(m){m&=m-1;n++}return n};
   function poly(c){let a=new Set([0]);for(let l of c){let b=1<<idx.get(Math.abs(l)),z=new Set();let flip=m=>z.has(m)?z.delete(m):z.add(m);for(let m of a){if(l>0)flip(m);flip(m|b)}a=z}return a}
   function times(a,m){let z=new Set();for(let t of a){let n=t|m;if(z.has(n))z.delete(n);else z.add(n)}return z}
   function vec(a){let z=0n;for(let m of a){if(!mi.has(m))throw Error("degree");z^=1n<<BigInt(mi.get(m))}return z}
   function rank(rows,order){let B=new Map(),tests=0,xors=0;for(let row of rows){for(let i of order){tests++;let b=1n<<BigInt(i);if(!(row&b))continue;if(B.has(i)){row^=B.get(i);xors++}else{B.set(i,row);break}}}return {B,tests,xors}}
   let order=masks.map((m,i)=>i).sort((a,b)=>((masks[b]&1)-(masks[a]&1))||b-a),reverse=order.slice().reverse();
   function span(rows){let out=[],products=0,terms=0;for(let c of rows){if(c.length>degree)continue;let a=poly(c),s=c.reduce((m,l)=>m|(1<<idx.get(Math.abs(l))),0);for(let m of masks)if(!(m&s)&&pop(m)+c.length<=degree){let t=times(a,m);products++;terms+=t.size;out.push(vec(t))}}return {out,products,terms}}
   let modes=[];
   for(let mode of ["source","seeded","remove-first"]){
    let ss=mode==="source"?[]:mode==="seeded"?seeds:seeds.slice(1),R=[...src,...ss],pos=R.map((c,i)=>[c,i]).filter(([c])=>c.includes(v)),neg=R.map((c,i)=>[c,i]).filter(([c])=>c.includes(-v)),other=R.filter(c=>!abs(c).includes(v)),res=[],pairs=0,checks=0;
    for(let [a,i] of pos)for(let [b,j] of neg){pairs++;let q=canon([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);if(q.some(l=>q.includes(-l)))continue;
     // independently validate clause resolution with symbolic Boolean product identity: p_R=(p_missing_A*p_a)+(p_missing_B*p_b).
     const A=a.filter(l=>l!==v),B=b.filter(l=>l!==-v),u=poly(a),w=poly(b);
     function mult(t,ls){for(let l of ls){let z=new Set(),bit=1<<idx.get(Math.abs(l)),flip=m=>z.has(m)?z.delete(m):z.add(m);for(let m of t){checks++;if(l>0)flip(m);flip(m|bit)}t=z}return t}
     let z=mult(u,q.filter(l=>!A.includes(l))),y=mult(w,q.filter(l=>!B.includes(l)));for(let m of y)z.has(m)?z.delete(m):z.add(m);
     let expected=poly(q);if(z.size!==expected.size||[...z].some(m=>!expected.has(m)))throw Error("algebraic lift");res.push({q,i,j});
    }
    let L=span(R),A=rank(L.out,order),boundary=[...A.B].filter(([i])=>!(masks[i]&1)).map(([i,z])=>z);
    let projected=[...other,...res.map(t=>t.q)],Q=span(projected),hy=rank([...boundary,...Q.out],order),direct=rank(Q.out,order),check=rank([...boundary,...Q.out],reverse);
    if(check.B.size!==hy.B.size)throw Error("rank");
    let K=new Set(projected.map(key)),unique=[...K],signs=new Map(),unate=true;for(let c of projected)for(let l of c){let u=Math.abs(l);if(signs.has(u)&&signs.get(u)!==Math.sign(l))unate=false;signs.set(u,Math.sign(l))}
    let exactUnateRank=null;if(unate){let cm=projected.map(c=>c.reduce((m,l)=>m|(1<<idx.get(Math.abs(l))),0));exactUnateRank=masks.filter(m=>!(m&1)&&cm.some(q=>(m&q)===q)).length;if(exactUnateRank!==direct.B.size||hy.B.size!==direct.B.size)throw Error("unate theorem");}
    // Witness for one novel boundary identity relative to original bounded-multiple span; exact row source, not semantic independence.
    let novel=null;for(let t of res){if(t.q.length>degree)continue;let row=vec(poly(t.q));if(rank([...boundary,row],order).B.size>boundary.length){novel=t;break}}
    let H=[...F.filter((c,i)=>!sourceRows.includes(i)),...projected.filter((c,i)=>projected.findIndex(t=>key(t)===key(c))===i)],T=solve(H),V=replay(H,T.tree);
    modes.push({mode,seedCount:ss.length,pairs,resolvents:res,projectedUnique:unique.length,rawRank:A.B.size,rawBoundaryRank:boundary.length,directRank:direct.B.size,hybridRank:hy.B.size,novel,unate,exactUnateRank,counters:{liftTermVisits:checks,rawProducts:L.products,rawTerms:L.terms,projectedProducts:Q.products,projectedTerms:Q.terms,rankTests:A.tests+hy.tests+direct.tests+check.tests,rankXors:A.xors+hy.xors+direct.xors+check.xors},tree:T.tree,terminal:{nodes:T.nodes,work:T.work,replay:V}})
   }
   regions.push({v,scope,sourceRows,seeds,features:D,modes})
  }
  const cert={format:"T2-COMPACT-RESOLVENT-ANF-v1",problem_id:"STRICT-EB4-v1",instance:r.short_id,instance_id:r.instance_id,original_N_bits:r.N_bits,source_pin:pins,guard_id:guard,residual_id:rid,original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},parents:["CERT-v1:sha256:"+sha(d[name])],chartHash:ch,mapHash:mh,claim:"Exact complete single-carrier elimination by all non-tautological resolvents; verify each polynomial lift by symbolic GF2 multiplication, no whole boundary enumeration. Compare bounded degree3 monomial-multiple subspaces (not full PC), and exact degree3 vanishing rank only when response is unate. Recompose and replay DPLL.",degree,projection,projectionCost:p.cost,carriers:p.carriers,eliminated:p.steps.length,early:[early.a.size,early.work],companionEarly:[ce.a.size,ce.work],base:{nodes:S.nodes,work:S.work,replay:baseReplay},companion:{id:r.source_cnf,nodes:C.nodes,work:C.work,replay:compReplay},rupVisits,selection,candidateCount:candidates.length,regions};
  results.push({certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),cert})
 }
 return results
}
const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(d,pins)));

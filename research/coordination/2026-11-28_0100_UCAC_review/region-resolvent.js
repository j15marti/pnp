function compact(d,ev,pins){
 const enc=x=>JSON.stringify(x)+"\n",sha=new Function(d.hash.slice(d.hash.indexOf("function sha("),d.hash.indexOf("if(require.main"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,up,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,up,solve,replay}")();
 const result=[];
 for(let {certificate_id,cert} of JSON.parse(ev)){
  if("CERT-v1:sha256:"+sha(enc(cert))!==certificate_id)throw Error("parent");
  let name=cert.instance.includes("JOINT")?"joint":"random",id=cert.instance.includes("JOINT")?"JOINT-24":"RANDOM-3CNF-40",x=JSON.parse(d.corpus).instances.find(q=>q.id===id),r=JSON.parse(d.reg).instances.find(q=>q.alias==="EB-"+id),G=compile(x);
  if(sha(enc(G.network))!==r.sha256||enc(G.network).length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth");
  let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses;if(sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final}))!==cert.chartHash||sha(enc({root:p.root,phase:p.phase}))!==cert.mapHash)throw Error("chart");
  if("CERT-v1:sha256:"+sha(d[name])!==cert.parent_certificate_id)throw Error("producer");let c=JSON.parse(d[name]),P=c.proof.filter(q=>q[0]===c.anchor).map(q=>q.slice(1)),learned=F.slice(),rupVisits=0;for(let q of P){let u=up(learned,q.map(l=>[Math.abs(l),+(l<0)]));rupVisits+=u.work;if(!u.conflict)throw Error("RUP");learned.push(q);}
  const regions=[];
  for(let a of cert.regions){
   let v=a.interior,scope=a.scope,idx=new Map(scope.map((u,i)=>[u,i])),source=a.sourceRows.map(i=>F[i]);if(F.some((q,i)=>q.some(l=>Math.abs(l)===v)&&!a.sourceRows.includes(i)))throw Error("incident");
   if(a.seedRows.some(s=>JSON.stringify(s.q)!==JSON.stringify(P[s.i])))throw Error("seed");
   let modes=[];
   for(let mode of ["source-only","seeded","leave-first-out"]){
    let seeds=mode==="source-only"?[]:a.seedRows.filter((s,i)=>mode==="seeded"||i>0).map(s=>s.q),R=[...source,...seeds],A=R.filter(q=>q.includes(v)),B=R.filter(q=>q.includes(-v)),C=R.filter(q=>!q.includes(v)&&!q.includes(-v));let pairs=0,mergeLiteral=0,subsumption=0,checks=0;
    for(let f of A)for(let g of B){pairs++;let q=new Set([...f.filter(l=>l!==v),...g.filter(l=>l!==-v)]);mergeLiteral+=f.length+g.length;if([...q].some(l=>q.has(-l)))continue;C.push([...q].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));}
    const sorted=C.sort((a,b)=>a.length-b.length||a.join(",").localeCompare(b.join(","))),D=[];for(let q of sorted){let found=false;for(let u of D){subsumption+=u.length+q.length;if(u.every(l=>q.includes(l))){found=true;break}}if(!found)D.push(q)}
    function sat(q,m){for(let l of q){checks++;if(Boolean(m&(1<<idx.get(Math.abs(l))))===(l>0))return true;}return false;}
    let support=0;for(let b=0;b<2**(scope.length-1);b++){let yes=[0,1].some(t=>R.every(q=>sat(q,2*b+t))),out=D.every(q=>sat(q,2*b));if(yes!==out)throw Error("projection");if(yes)support++;if(mode==="seeded"&&yes!==Boolean(a.finalCounts[b]))throw Error("parent response");}
    let H=[...F.filter((q,i)=>!a.sourceRows.includes(i)),...D];if(H.some(q=>q.some(l=>Math.abs(l)===v)))throw Error("interior");
    let U=up(H),T=solve(H),V=replay(H,T.tree);
    modes.push({mode,localRows:R.length,pairs,mergeLiteral,subsumption,checks,support,projectedRows:D,globalRows:H.length,nodes:T.nodes,work:T.work,replay:V,earlyPins:U.a.size,earlyVisits:U.work,tree:T.tree});
   }
   regions.push({interior:v,scope,sourceRows:a.sourceRows,modes,denseSeeded:{rows:a.hybrid.rows,nodes:a.hybrid.nodes,work:a.hybrid.work}});
  }
  const q={format:"T4-REGIONAL-RESOLVENT-v1",instance:cert.instance,instance_id:cert.instance_id,problem_id:cert.problem_id,original_N_bits:cert.original_N_bits,source_pins:pins,guard_id:cert.guard_id,residual_id:cert.residual_id,chartHash:cert.chartHash,mapHash:cert.mapHash,original_ids:cert.original_ids,parent_certificate_ids:[certificate_id,cert.parent_certificate_id],projection,rupVisits,regions};result.push({certificate_id:"CERT-v1:sha256:"+sha(enc(q)),cert:q});
 }return result;
}
const fs=require('node:fs');const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"reg":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"hash":["research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js","4a42c99a37a2a22c1ac36ed204eadce7dfa77908"],"joint":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/JOINT-24.cert.json","eb3eb5f2098fbfa73cd11540ba270ac997438f78"],"random":["research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/RANDOM-3CNF-40.cert.json","f96bea02c40c7545eb32c7fd5ac37afac7e436e8"]};const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+3],'utf8')]));console.log(JSON.stringify(compact(d,fs.readFileSync(process.argv[2],'utf8'),pins),null,2));

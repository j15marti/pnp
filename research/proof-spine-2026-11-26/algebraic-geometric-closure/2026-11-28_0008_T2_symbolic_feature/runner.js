const fs=require('node:fs');
const paths={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"reg":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"hash":["research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js","4a42c99a37a2a22c1ac36ed204eadce7dfa77908"],"peer":["research/proof-spine-2026-11-26/affine-bijunctive-sat/2026-11-27_2347_T2_interface/JOINT-interface.certificate.json","f35905e4f2823611d44e10b9709f751697eaf77a"]};
function run(d,paths){
 const sha=new Function(d.hash.slice(d.hash.indexOf("function sha("),d.hash.indexOf("if(require.main"))+";return sha")(),enc=x=>JSON.stringify(x)+"\n";
 const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")();
 const {project,verifyProjection,adapter,up,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,up,solve,replay}")();
 let common=[],charts={};
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
  let x=JSON.parse(d.corpus).instances.find(x=>x.id===id),r=JSON.parse(d.reg).instances.find(x=>x.alias==="EB-"+id),G=compile(x);
  if(sha(enc(G.network))!==r.sha256||enc(G.network).length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth "+id);
  let p=project(G.network),v=verifyProjection(G.network,p),a=adapter(p,G,x.dimacs,x.nvars),early=up(p.clauses),ce=up(a.orig),s=solve(p.clauses),c=solve(a.orig),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),guard="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,guard,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
  charts[id]={p,r,chartHash,mapHash,guard,rid};
  let F=p.clauses,vars=[...new Set(F.flat().map(Math.abs))],binary=F.filter(c=>c.length<=2),rest=F.filter(c=>c.length>2),A=new Set(binary.flat().map(Math.abs)),B=new Set(rest.flat().map(Math.abs)),boundary=vars.filter(v=>A.has(v)&&B.has(v)),matched=new Set(),matching=[],covered=new Set(),packing=[];
  for(let c of binary){if(c.length===2&&c.every(l=>l<0)&&!matched.has(-c[0])&&!matched.has(-c[1])){matched.add(-c[0]);matched.add(-c[1]);matching.push(c)}}
  for(let c of F){if(c.length&&c.every(l=>l>0&&!covered.has(l))){c.forEach(l=>covered.add(l));packing.push(c)}}
  common.push({id,instance_id:r.instance_id,N:r.N_bits,cnf:r.source_cnf,carriers:p.carriers,eliminated:p.steps.length,rows:F.length,variables:vars.length,early:[early.a.size,early.work],companionEarly:[ce.a.size,ce.work],projection:p.cost,verification:v,chartHash,mapHash,guard,rid,base:{nodes:s.nodes,work:s.work,replay:replay(F,s.tree)},companion:{nodes:c.nodes,work:c.work,replay:replay(a.orig,c.tree)},sourceOnlyCut:{binary:binary.length,other:rest.length,boundary:boundary.length,leftInterior:A.size-boundary.length,rightInterior:B.size-boundary.length},packing:{matching,packing,upper:vars.length-matching.length,lower:packing.length}})
 }
 let j=charts["JOINT-24"],q=JSON.parse(d.peer);
 if(sha(d.peer)!=="5572c6e3da6d3eaf4cd935f3616e6c180b28bda1bdf09ced541f642a70bcf9b2"||j.chartHash!==q.chartHash||j.mapHash!==q.mapHash||j.guard!==q.internal_guard||j.rid!==q.internal_residual)throw Error("peer auth");
 let F=j.p.clauses,L=q.leftRows.map(i=>F[i-1]),R=q.rightRows.map(i=>F[i-1]),B=q.boundary;
 if(new Set([...q.leftRows,...q.rightRows]).size!==F.length||B.join()!==[...new Set(L.flat().map(Math.abs))].filter(x=>R.flat().map(Math.abs).includes(x)).sort((a,b)=>a-b).join())throw Error("partition");
 function features(b,d){let out=[];function gen(start,m,k){out.push(m);if(k)for(let i=start;i<b;i++)gen(i+1,m|(1<<i),k-1)}gen(0,0,d);return out}
 let M=features(B.length,3),D=M.length,rows=new Map(),work={nodes:0,visits:0,scans:0,cubes:0,coefficientTests:0,coefficientRows:0,pivotTests:0,xors:0,rightChecks:0,rightRows:0};
 function add(x,y){for(let i=D-1;i>=0;i--){work.pivotTests++;let bit=1n<<BigInt(i);if(!(x&bit))continue;let r=rows.get(i);if(r){x^=r[0];y^=r[1];work.xors++}else{rows.set(i,[x,y]);return true}}if(y)throw Error("inconsistent separation");return false}
 let cubes=[];
 function addCube(A,y){let one=0,zero=0;for(let i=0;i<B.length;i++){let b=A.get(B[i]);if(b===0)zero|=1<<i;else if(b===1)one|=1<<i}let coeff=new Map();for(let i=0;i<D;i++){work.coefficientTests++;let m=M[i];if(m&zero)continue;let free=m&~one;coeff.set(free,(coeff.get(free)||0n)|(1n<<BigInt(i)))}if(!coeff.has(0)&&y)throw Error("constant");for(let [m,v] of coeff){work.coefficientRows++;add(v,+(m===0&&y===1))}return [one,zero]}
 function dfs(g){if(work.nodes>20000||work.pivotTests>10000000)throw Error("cap");work.nodes++;let U=up(L,g);work.visits+=U.work;if(U.conflict)return;let freq=new Map();for(let c of L){let sat=false;for(let l of c){work.scans++;if(U.a.get(Math.abs(l))===+(l>0)){sat=true;break}}if(!sat)for(let l of c)if(!U.a.has(Math.abs(l)))freq.set(Math.abs(l),(freq.get(Math.abs(l))||0)+1)}
 if(!freq.size){work.cubes++;cubes.push(addCube(U.a,0));return}
 let v=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];dfs([...U.a,[v,0]]);dfs([...U.a,[v,1]])}
 dfs([]);let leftRank=rows.size;
 if(!R.every(c=>c.length<=2&&c.every(l=>l<0)&&c.every(l=>B.includes(-l))))throw Error("right not downset");
 // Since right is a downset, h=1 exactly iff its constant is 1 and coefficients on feasible nonempty monomials vanish.
 let rightBasis=[];
 for(let i=0;i<D;i++){let w=M[i],ok=true;for(let c of R){let sat=false;for(let l of c){work.rightChecks++;if(!(w&(1<<B.indexOf(-l)))){sat=true;break}}if(!sat){ok=false;break}}if(ok){rightBasis.push(w);work.rightRows++;add(1n<<BigInt(i),+(w===0))}}
 let sol=0n;for(let i=0;i<D;i++){let r=rows.get(i);if(r){let z=r[0]&sol,par=0;while(z){z&=z-1n;par^=1}if(par!==r[1])sol|=1n<<BigInt(i)}}
 let terms=M.filter((m,i)=>Boolean(sol&(1n<<BigInt(i))));
 // Separate verifier uses direct restriction and branches over the remaining polynomial support.
 function checkRegion(F,y){let nodes=0,visits=0,scans=0,pruned=0;function go(g){nodes++;let U=up(F,g);visits+=U.work;if(U.conflict)return;let polys=new Set();for(let m of terms){let t=m,zero=false;for(let i=0;i<B.length;i++)if(t&(1<<i)){scans++;let b=U.a.get(B[i]);if(b===0){zero=true;break}if(b===1)t^=1<<i}if(!zero){if(polys.has(t))polys.delete(t);else polys.add(t)}}
 if(polys.size===y&&(!y||polys.has(0))){pruned++;return}if([...polys].every(m=>m===0)){let v=[...new Set(F.flat().map(Math.abs))].find(v=>!U.a.has(v));if(v===undefined)throw Error("separator counterexample");go([...U.a,[v,0]]);go([...U.a,[v,1]]);return}
 let m=[...polys].find(x=>x),i=31-Math.clz32(m&-m),v=B[i];go([...U.a,[v,0]]);go([...U.a,[v,1]])}
 go([]);return {nodes,visits,scans,pruned}}
 let checks=[checkRegion(L,0),checkRegion(R,1)];
 let result={format:"T2-SYMBOLIC-FEATURE-COEFFICIENT-v1",problem_id:"STRICT-EB4-v1",instance:q.instance,instance_id:q.instance_id,original_N_bits:q.original_N_bits,source_pin:q.source_pin,guard_id:"EMPTY",residual_id:"ROOT",internal_guard:j.guard,internal_residual:j.rid,chartHash:j.chartHash,mapHash:j.mapHash,original_ids:q.original_ids,parents:["CERT-v1:sha256:"+sha(d.peer)],parent_scope:"partition only; no support or separator used as advice",boundary:B,leftRows:q.leftRows,rightRows:q.rightRows,claim:"Symbolic coefficient equations from satisfying cubes and negative-only right downset give a degree<=3 separator. Independent recursive restriction verifier proves left h=0 and right h=1; complement symmetry discharges anchor.",degree:3,featureCount:D,leftRank,rightRank:rightBasis.length,combinedRank:rows.size,terms,cubes,rightBasis,work,checks,common,source_pins:paths};
 return {result,certificate_id:"CERT-v1:sha256:"+sha(enc(result))}
}
const d=Object.fromEntries(Object.keys(paths).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));process.stdout.write(JSON.stringify(run(d,paths).result)+'\n');

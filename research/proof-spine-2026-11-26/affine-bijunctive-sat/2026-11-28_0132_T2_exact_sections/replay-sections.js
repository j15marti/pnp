// Node.js: node replay-sections.js compile.js benchmarks.json native-chart.js gauge-lift.js instance-registry-v1.json
// Inputs must be the exact pinned files listed below. Fixed candidate replay, NOT blind discovery.
const pins={
  "compiler": [
    "research/coordination/shared-eb-2026-11-27/compile.js",
    "21b9d53fb8166c819b24e708656c742cd3c24f10"
  ],
  "corpus": [
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json",
    "e315349cd6c1fe3fa696504859f28312f6aab69a"
  ],
  "chart": [
    "research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js",
    "52cae4a54513a67dd9468c7e3ee597cf317d67a3"
  ],
  "hash": [
    "research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js",
    "4a42c99a37a2a22c1ac36ed204eadce7dfa77908"
  ],
  "registry": [
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json",
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c"
  ]
};
function run(d,pins){
 const extract=(s,a,b,r)=>new Function(s.slice(s.indexOf(a),s.indexOf(b))+";return "+r)();
 const compile=extract(d.compiler,"function compile","function auditLocal","compile"),sha=extract(d.hash,"function sha(","if(require.main","sha"),{project,verifyProjection,up,solve,replay}=extract(d.chart,"const key=","function checkHall","{project,verifyProjection,up,solve,replay}");
 const enc=x=>JSON.stringify(x)+"\n";
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")throw Error("sha");
 let results=[];
 for(let [id,targets] of [["JOINT-24",[[1,[-417,-961],"and"],[42,[-1,-18,-242],"and"],[961,[-1,-417],"and"]]],["RANDOM-3CNF-40",[[1,[-82,497],"or"]]]]){
  let x=JSON.parse(d.corpus).instances.find(q=>q.id===id),reg=JSON.parse(d.registry).instances.find(q=>q.alias==="EB-"+id),G=compile(x);
  if(sha(enc(G.network))!==reg.sha256||enc(G.network).length*8!==reg.N_bits||sha(x.dimacs)!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits||sha(enc(G.source_map))!==reg.source_map_sha256)throw Error("auth");
  let p=project(G.network),vr=verifyProjection(G.network,p),F=p.clauses,early=up(F),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",reg.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",reg.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
  for(let [v,lits,mode] of targets){
   let B=F.map((c,i)=>({c,i:i+1})).filter(q=>q.c.some(l=>Math.abs(l)===v)),X=F.filter(c=>!c.some(l=>Math.abs(l)===v)),s=[...new Set(B.flatMap(q=>q.c.map(Math.abs)))].filter(x=>x!==v).sort((a,b)=>a-b);
   let pcnf=mode==="and"?lits.map(l=>[l]):[lits],ncnf=mode==="and"?[lits.map(l=>-l)]:lits.map(l=>[-l]),Y=[],seen=new Set();
   // Independent syntactic check: functional AND definition or single-negative-row section.
   const key=c=>[...c].sort((a,b)=>a-b).join(","),K=new Set(B.map(q=>key(q.c)));
   if(mode==="and"&&(!K.has(key([v,...lits.map(l=>-l)]))||!lits.every(l=>K.has(key([-v,l])))))throw Error("gate");
   if(mode==="or"&&(B.filter(q=>q.c.includes(-v)).length!==1||!K.has(key([-v,...lits]))))throw Error("section");
   for(let c of B.map(q=>q.c)){let vSign=c.includes(v),a=c.filter(l=>Math.abs(l)!==v);for(let row of (vSign?pcnf:ncnf)){let z=[...new Set([...a,...row])].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=z.join(",");if(!z.some(l=>z.includes(-l))&&!seen.has(key)){seen.add(key);Y.push(z)}}}
   let checks=0,support=0,amb=0;for(let a=0;a<2**s.length;a++){let M=new Map(s.map((z,i)=>[z,(a>>i)&1]));let sat=C=>C.every(c=>c.some(l=>{checks++;return M.get(Math.abs(l))===+(l>0)}));M.set(v,0);let p0=sat(B.map(q=>q.c));M.set(v,1);let p1=sat(B.map(q=>q.c));let y=sat(Y);if(y!==(p0||p1))throw Error("sub");support+=+y;amb+=+(p0&&p1)}
   let Q=[...X,...Y],t=solve(Q),r=replay(Q,t.tree);
   let cert={format:"T2-EXACT-SECTION-SUBSTITUTION-v1",instance_id:reg.instance_id,anchor:p.anchor,chartHash,mapHash,v,lits,mode,B,Y,tree:t.tree};
   results.push({instance:reg.short_id,instance_id:reg.instance_id,original_N_bits:reg.N_bits,source_pin:pins,guard_id:gid,residual_id:rid,original_ids:{vertices:[0,reg.vertices-1],ports:[0,4*reg.vertices-1],edges:[0,reg.edges-1],interior_port:v-1,boundary_ports:s.map(v=>v-1)},parents:[],certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),certificate:cert,support,amb,checks,rows:Q.length,nodes:t.nodes,visits:t.work,replay:r.work,projectionReplay:vr,projectionDiscovery:p.cost,early:{pins:early.a.size,work:early.work}});
  }
 }
 return results;
}
const fs=require('node:fs');const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(d,pins),null,2));

// Node CLI: node verify.js compile.js benchmarks.json registry.json independent_checker.js lanes.js batch.js persistent.js root.certificate.json [two-demand.js guarded-exports.json]
// Independent root replay; no discovery search, no reference UNSAT tree.
const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
const [cp,bp,rp,hp,lp,up,sp,qp,tp,gp]=process.argv.slice(2),read=p=>fs.readFileSync(p,"utf8"),sha=s=>crypto.createHash("sha256").update(s).digest("hex"),hash=x=>sha(JSON.stringify(x)+"\n"),cc=read(cp),hh=read(hp);
const compile=Function(cc.slice(cc.indexOf("function compile"),cc.indexOf("function auditLocal"))+";return compile")();
const L=Function(hh.slice(0,hh.indexOf('const fs=require("node:fs"),[compiler'))+";return {independentNormalize,verifyTrace}")(),A=require(path.resolve(lp)),U=require(path.resolve(up)),S=require(path.resolve(sp)),B=JSON.parse(read(bp)),R=JSON.parse(read(rp)),raw=read(qp),q=JSON.parse(raw),e=R.instances.find(e=>e.instance_id===q.instance_id),x=B.instances.find(x=>"EB-"+x.id===e.alias),g=compile(x),s=JSON.stringify(g.network)+"\n";
if(sha(s)!==e.sha256||s.length*8!==e.N_bits||q.original_N_bits!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(JSON.stringify(g.source_map)+"\n")!==e.source_map_sha256||q.guard_id!=="EMPTY"||q.residual_id!=="ROOT")throw Error("identity");
const D=L.independentNormalize(g.network),V=L.verifyTrace(D.fs,q.map.trace),inv=f=>f.ok.length>0&&f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)));
if(!D.fs.every(inv)||!V.fs.every(inv)||!V.fs.some(f=>f.vs.includes(q.map.gauge)))throw Error("complement gauge");
const F=A.specialize(V.fs,q.map.gauge),C=U.cnf(F),artifact={F,C};
if(JSON.stringify(artifact)!==JSON.stringify(q.artifact)||hash(artifact)!==q.chart.artifact_sha256||hash(q.map)!==q.chart.map_sha256||"RESIDUAL-v1:sha256:"+hash(["PNP-RESIDUAL-v1",q.instance_id,"EMPTY",q.chart.schema,hash(artifact),hash(q.map)])!==q.chart.id)throw Error("chart");
const z=S.verifyProof(C,q.proof,U,{replay:(C,t)=>({D:C,work:0})});if(!z.ok)throw Error("root proof");
let guarded=null;
if(tp&&gp){const T=require(path.resolve(tp)),a=JSON.parse(read(gp)),gid="GUARD-v1:sha256:"+hash(["PNP-GUARD-v1",q.instance_id,"EB-PORT-PINS-v1",hash([[q.map.gauge-1,0]])]);
if(a.instance_id!==q.instance_id||a.guard_id!==gid||hash(a.guardArtifact)!==a.guard_artifact_sha256||a.residual_id!=="RESIDUAL-v1:sha256:"+hash(["PNP-RESIDUAL-v1",q.instance_id,gid,q.chart.schema,hash(artifact),hash(q.map)]))throw Error("guard identity");guarded=a.cuts.map(c=>T.verifyCut(C,c))}
console.log(JSON.stringify({verified:true,certificate_id:"CERT-v1:sha256:"+sha(raw),root:z,projection:V.tests,guarded}));

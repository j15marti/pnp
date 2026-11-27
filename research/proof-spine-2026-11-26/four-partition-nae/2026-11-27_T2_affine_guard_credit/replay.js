// Run: node replay.js /path/compile.js /path/benchmarks.json /path/instance-registry-v1.json /path/certificate.json
const fs=require("node:fs"), crypto=require("node:crypto");
const {normalize,project,independentCheck}=require("./affine-closure.js");
const sha=x=>crypto.createHash("sha256").update(x).digest("hex");
const [compiler,corpusText,registryText,certificateText]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));
const cert=JSON.parse(certificateText), corpus=JSON.parse(corpusText), registry=JSON.parse(registryText);
const ent=registry.instances.find(e=>e.instance_id===cert.instance_id);
if(!ent||cert.guard_id!=="EMPTY"||cert.residual_id!=="ROOT"||ent.N_bits!==cert.original_N_bits)throw Error("registry/guard");
const x=corpus.instances.find(e=>e.id===ent.source_cnf.alias);
if(!x||sha(x.dimacs)!==ent.source_cnf.sha256||8*Buffer.byteLength(x.dimacs)!==ent.source_cnf.N_bits)throw Error("CNF bytes");
const compile=new Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+"\nreturn compile")();
const g=compile(x), b=JSON.stringify(g.network)+"\n", m=JSON.stringify(g.source_map)+"\n";
if(sha(b)!==ent.sha256||8*Buffer.byteLength(b)!==ent.N_bits||sha(m)!==ent.source_map_sha256)throw Error("native/map bytes");
const a=normalize(g.network), p=project(a.F);
if(p.status!=="COMPLETE"||p.gauge!==cert.proof.gauge||JSON.stringify(p.steps)!==JSON.stringify(cert.proof.projection_steps)||JSON.stringify(p.final)!==JSON.stringify(cert.proof.final_factors))throw Error("projection mismatch");
const r=independentCheck(p.final,cert.proof.tree,cert.proof.leaf_mode);
if(!r.verified)throw Error("leaf verification incomplete");
console.log(JSON.stringify({status:"VERIFIED",instance:ent.instance_id,N_bits:ent.N_bits,certificate_sha256:sha(certificateText),normalization:a.counts,projection:p.counts,replay:r}));

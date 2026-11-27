// Usage: node verify-row.js compile.js benchmarks.json registry.json own-certificate.json [parent-certificate.json]
// Requires adjacent experiment.js and row-shadow.js at report pins.
const fs=require("node:fs"),crypto=require("node:crypto"),{projection,localRows}=require("./row-shadow.js");
const hash=s=>crypto.createHash("sha256").update(s).digest("hex");
const [cp,bp,rp,certp,parentp]=process.argv.slice(2);
const read=p=>fs.readFileSync(p,"utf8"),src=read(cp),compile=Function(src.slice(src.indexOf("function compile"),src.indexOf("function auditLocal"))+"return compile")();
const es=read(__dirname+"/experiment.js"),{root,cnf,rup}=Function(es.slice(0,es.indexOf("// Node invocation:"))+"return {root,cnf,rup}")();
const B=JSON.parse(read(bp)),R=JSON.parse(read(rp)),cert=JSON.parse(read(certp)),e=R.instances.find(x=>x.instance_id===cert.instance_id),x=B.instances.find(x=>"EB-"+x.id===e.alias),G=compile(x),raw=JSON.stringify(G.network)+"\n";
if(hash(raw)!==e.sha256||raw.length*8!==e.N_bits||hash(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||hash(JSON.stringify(G.source_map)+"\n")!==e.source_map_sha256||cert.original_N_bits!==e.N_bits||cert.guard_id!=="EMPTY"||cert.residual_id!=="ROOT")throw Error("identity");
const S=root(G.network);let trace=cert.projection,imp=[];
if(cert.parents.length){const s=read(parentp),p=JSON.parse(s);if("CERT-v1:sha256:"+hash(s)!==cert.parents[0].certificate_id||p.instance_id!==cert.instance_id||p.gauge!==cert.gauge||p.guard_id!=="EMPTY"||p.residual_id!=="ROOT")throw Error("parent identity");trace=p.trace;const Q=projection(S.fs,cert.gauge,trace),P=p.proof.map(x=>{if(x.kind!=="UP")throw Error("parent rule");return x.clause});if(!rup(cnf(Q.fs),P).valid||JSON.stringify(P.slice(0,cert.imported.length))!==JSON.stringify(cert.imported))throw Error("parent proof");imp=cert.imported}
const Q=projection(S.fs,cert.gauge,trace),d=localRows(Q.fs,imp,1,cert.deletions,50000000);if(d.status!=="UNSAT")throw Error("proof failed "+JSON.stringify(d));console.log(JSON.stringify({valid:true,certificate_id:"CERT-v1:sha256:"+hash(read(certp)),projectionTests:Q.tests,projectionScans:Q.scans,replay:d}));

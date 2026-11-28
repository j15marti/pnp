// node replay.js compile.js benchmarks.json registry.json affine-closure.js reverse.js certificate.json
const fs=require('node:fs'),crypto=require('node:crypto');
const [compiler,corpus,reg,old,rev,ct]=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex'),c=JSON.parse(ct),e=JSON.parse(reg).instances.find(x=>x.instance_id===c.instance_id),x=JSON.parse(corpus).instances.find(x=>x.id===e.source_cnf.alias);
const compile=new Function(compiler.slice(compiler.indexOf('function compile('),compiler.indexOf('function auditLocal'))+'\nreturn compile')(),{normalize,project}=new Function(old.replace(/module\.exports=/,'return '))(),{replay}=new Function(rev.replace(/module\.exports=/,'return '))();
if(c.guard_id!=='EMPTY'||c.residual_id!=='ROOT'||c.original_N_bits!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||8*Buffer.byteLength(x.dimacs)!==e.source_cnf.N_bits)throw Error('IDs');
const g=compile(x),b=JSON.stringify(g.network)+'\n',m=JSON.stringify(g.source_map)+'\n';
if(sha(b)!==e.sha256||8*Buffer.byteLength(b)!==e.N_bits||sha(m)!==e.source_map_sha256)throw Error('bytes');
const n=normalize(g.network),p=project(n.F);
if(p.status!=='COMPLETE'||p.gauge!==c.proof.gauge||JSON.stringify(p.steps)!==JSON.stringify(c.proof.steps)||JSON.stringify(p.final)!==JSON.stringify(c.proof.finalFactors))throw Error('projection');
const C=p.final.flatMap(f=>Array.from({length:2**f.v.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.v.map((v,i)=>w>>i&1?-v:v)));
if(JSON.stringify(C)!==JSON.stringify(c.proof.base))throw Error('base');
const z=replay(C,c.proof.trace);if(!z.unsat)throw Error('no empty clause');
console.log(JSON.stringify({status:'VERIFIED',instance_id:c.instance_id,N:e.N_bits,sha256:sha(ct),steps:z.steps,visits:z.visits,reasonRows:z.reasonRows,projection:p.counts}));

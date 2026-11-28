// Usage: node replay.js compile.js benchmarks.json registry.json affine-closure.js agenda.js certificate.json
const fs=require('node:fs'),crypto=require('node:crypto');
const [compiler,corpusText,regText,ac,ag,ct]=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const compile=new Function(compiler.slice(compiler.indexOf('function compile('),compiler.indexOf('function auditLocal'))+'\nreturn compile')();
const {normalize,project}=new Function(ac.replace(/module\.exports=/,'return '))();
const {canonical,key,replayTree}=new Function(ag.replace(/module\.exports=/,'return '))();
const c=JSON.parse(ct),reg=JSON.parse(regText),corpus=JSON.parse(corpusText),e=reg.instances.find(z=>z.instance_id===c.instance_id),x=corpus.instances.find(z=>z.id===e.source_cnf.alias);
if(c.guard_id!=='EMPTY'||c.residual_id!=='ROOT'||c.original_N_bits!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256)throw Error('IDs');
const g=compile(x),b=JSON.stringify(g.network)+'\n',m=JSON.stringify(g.source_map)+'\n';
if(sha(b)!==e.sha256||8*Buffer.byteLength(b)!==e.N_bits||sha(m)!==e.source_map_sha256||8*Buffer.byteLength(x.dimacs)!==e.source_cnf.N_bits)throw Error('bytes');
const n=normalize(g.network),p=project(n.F);
if(p.status!=='COMPLETE'||p.gauge!==c.proof.gauge||JSON.stringify(p.steps)!==JSON.stringify(c.proof.projection)||JSON.stringify(p.final)!==JSON.stringify(c.proof.finalFactors))throw Error('projection');
const chart=p.final.flatMap(f=>Array.from({length:2**f.v.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.v.map((v,i)=>w>>i&1?-v:v)));
let base=[],seen=new Set();for(let q of chart){q=canonical(q);let k=key(q);if(!q.some(l=>q.includes(-l))&&!seen.has(k)){seen.add(k);base.push(q)}}
if(JSON.stringify(base)!==JSON.stringify(c.proof.baseClauses))throw Error('base');
const M=new Map(base.map((q,i)=>[i,q]));for(const {id,c:q,p:[i,j,l]} of c.proof.cone){const a=M.get(i),b=M.get(j);if(!a||!b||id<=i||id<=j||M.has(id)||!a.includes(l)||!b.includes(-l)||q.length>4||key(canonical([...a.filter(z=>z!==l),...b.filter(z=>z!==-l)]))!==key(q))throw Error('cone');M.set(id,q)}
const A=[...base,...c.proof.exportIDs.map(i=>{const q=M.get(i);if(!q||q.length>c.proof.exportWidth)throw Error('export');return q})];
console.log(JSON.stringify({instance_id:c.instance_id,N:e.N_bits,certificate_sha256:sha(ct),cone:c.proof.cone.length,leafReplay:replayTree(A,c.proof.tree),normalization:n.counts,projection:p.counts}));

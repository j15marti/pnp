// Node.js: node check.js corpus.json registry.json JOINT-24.solo.json RANDOM-3CNF-40.solo.json
const fs=require("node:fs"),crypto=require("node:crypto"),{compile,normalize,makeFactors,clauses,replayProjection,replayLearn,batch,up,run,learnBatch}=require("./batch2.js");
const sha=s=>crypto.createHash("sha256").update(s).digest("hex");
function controls(){
 let seed=12937,rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n},probes=0,systems=0,sat=0,unsat=0;
 for(let t=0;t<128;t++){let n=3+rand(4),C=[];for(let i=0;i<4+rand(12);i++){let a=[];let k=1+rand(3);while(a.length<k){let v=1+((rand(65536)>>>5)%n);if(!a.some(l=>Math.abs(l)===v))a.push((rand(65536)&256)?v:-v)}C.push(a)}let guards=[[]];for(let i=1;i<=n;i++)for(let s of [-1,1]){guards.push([s*i]);for(let j=i+1;j<=n;j++)for(let q of [-1,1])guards.push([s*i,q*j])}
 let b=batch(C,guards,10000000);if(b.capped)throw Error("small cap");for(let j=0;j<guards.length;j++){probes++;if(Boolean(b.dead&(1n<<BigInt(j)))!==up(C,guards[j]).bad)throw Error("scalar mismatch")}
 let truth=false;for(let w=0;w<2**n;w++)if(C.every(c=>c.some(l=>Boolean(w>>(Math.abs(l)-1)&1)===(l>0))))truth=true;truth?sat++:unsat++;
 let a=learnBatch(C);if(a.status==="UNSAT"&&truth)throw Error("false UNSAT");if(replayLearn(C,a.learn).unsat!==(a.status==="UNSAT"))throw Error("replay");systems++;
 }
 const C=Array.from({length:16},(_,w)=>[1,2,3,4].map((v,i)=>(w>>i)&1?-v:v));let a=run(C.map(c=>c.slice())),b=learnBatch(C);if(a.status!=="UNKNOWN"||b.status!=="UNKNOWN"||a.learn.length||b.learn.length)throw Error("width refusal");
 let corrupt=false;try{replayLearn([[1,2]],[[1]])}catch(e){corrupt=true}if(!corrupt)throw Error("accepted false RUP");
 return {systems,scalarGuardComparisons:probes,satisfiableControls:sat,unsatisfiableControls:unsat,all16ForbiddenAssignments:{status:a.status,learned:a.learn.length},invalidRUPRejected:corrupt};
}
console.log(JSON.stringify(controls()));
const [cor,reg,...raw]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));for(let z of raw){let a=JSON.parse(z),e=JSON.parse(reg).instances.find(x=>x.instance_id===a.instance_id),s=JSON.parse(cor).instances.find(x=>x.id===e.source_cnf.alias),G=compile(s),bytes=JSON.stringify(G.network)+"\n",map=JSON.stringify(G.source_map)+"\n";if(sha(bytes)!==e.sha256||bytes.length*8!==e.N_bits||sha(s.dimacs)!==e.source_cnf.sha256||s.dimacs.length*8!==e.source_cnf.N_bits||sha(map)!==e.source_map_sha256||a.original_N_bits!==e.N_bits||a.guard_id!=="EMPTY"||a.residual_id!=="ROOT")throw Error("identity");let {P,Q}=normalize(G.network);if(P[a.gauge-1]!==a.gauge-1)throw Error("gauge");let F=makeFactors(G.network,P,Q).concat({s:[a.gauge],a:[0]}),pr=replayProjection(F,a.projection_order),check=replayLearn(clauses(pr.F),a.learned);if(!check.unsat)throw Error("not UNSAT");console.log(JSON.stringify({instance:a.instance,certificate_id:"CERT-v1:sha256:"+sha(z),projectionRows:pr.calls,check}));}

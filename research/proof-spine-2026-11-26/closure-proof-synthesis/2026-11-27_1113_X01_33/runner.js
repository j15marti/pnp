function auditOwnerCertificate(G, cert, verifyNative){
 const m=4*G.types.length,par=Array.from({length:m},(_,i)=>i),ph=Array(m).fill(0);
 let ufSteps=0,truthChecks=0,implications=0;
 function find(a){let s=0,b=a;while(par[b]!==b){s^=ph[b];b=par[b];ufSteps++}return [b,s]}
 function join(a,b,s){let [r,p]=find(a),[t,q]=find(b);if(r===t){if((p^q)!==s)throw Error("inconsistent wire");return}if(r>t)[r,t]=[t,r];par[t]=r;ph[t]=p^q^s}
 for(const [a,b,s] of G.edges)join(a,b,s);
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="E")for(let k=1;k<4;k++)join(4*v,4*v+k,0);
 function implies(v,c){if(!Number.isInteger(v)||G.types[v]!=="B")return false;
   let p=[0,1,2,3].map(j=>find(4*v+j)),R=[...new Set(p.map(q=>q[0]))];
   if(c.some(l=>!R.includes(Math.abs(l)-1)))return false;
   for(let w=0;w<2**R.length;w++){truthChecks++;const val=r=>(w>>R.indexOf(r))&1;
     if(p.reduce((t,[r,s])=>t+(val(r)^s),0)===2&&!c.some(l=>val(Math.abs(l)-1)===Number(l>0)))return false;
   }return true
 }
 if(cert.guard_id!=="EMPTY"||cert.residual_id!=="ROOT"||cert.proofs.length!==cert.supports.length||!cert.proofs.length)throw Error("scope");
 let allowed=null,proofMetrics=[],minSizes=[];
 for(let k=0;k<cert.proofs.length;k++){let p=cert.proofs[k],s=cert.supports[k];proofMetrics.push(verifyNative(G,{proof:p}));
   let D=new Map(),pairs=new Set(),min=Infinity;
   for(let z of s.supports){if(D.has(z.id)||new Set(z.owners).size!==z.owners.length||z.owners.length<2)throw Error("invalid support");D.set(z.id,z.owners)}
   for(let [id,r] of p.records){if(!r.src||typeof r.src[0]!=="number")continue;
      if(!D.has(id))throw Error("missing leaf");let O=D.get(id);D.delete(id);min=Math.min(min,O.length);
      for(let v of O){implications++;if(!implies(v,r.c))throw Error("unsupported owner")}
      if(O.length===2)pairs.add(O.slice().sort((a,b)=>a-b).join(","))
   }
   if(D.size||min!==s.min||JSON.stringify([...pairs].sort())!==JSON.stringify(s.pairs.slice().sort()))throw Error("support summary");
   minSizes.push(min);allowed=allowed===null?pairs:new Set([...allowed].filter(q=>pairs.has(q)))
 }
 if(JSON.stringify([...allowed].sort())!==JSON.stringify(cert.intersection.slice().sort()))throw Error("intersection");
 return {minSizes,remainingPairs:allowed.size,truthChecks,implications,ufSteps,proofMetrics}
}
function checkEnergy(G,cert,ownerCert,verifyNative){
 const checked=auditOwnerCertificate(G,ownerCert,verifyNative);
 if(cert.instance_id!==ownerCert.instance_id||cert.guard_id!=="EMPTY"||cert.residual_id!=="ROOT")throw Error("energy scope");
 let n=G.types.length*4,adj=Array.from({length:n},()=>[]);const edge=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s])};
 for(let [a,b,s] of G.edges)edge(a,b,s);for(let v=0;v<G.types.length;v++)if(G.types[v]==="E")for(let j=1;j<4;j++)edge(4*v,4*v+j,0);
 let A=new Map(cert.assignment),values=new Array(n).fill(-1);
 if(A.size!==cert.assignment.length||cert.assignment.some(([r,b])=>!Number.isInteger(r)||r<0||r>=n||![0,1].includes(b)))throw Error("assignment");
 for(let r=0;r<n;r++)if(values[r]<0){values[r]=A.get(r)??0;let Q=[r];for(let i=0;i<Q.length;i++)for(let [b,s] of adj[Q[i]]){let v=values[Q[i]]^s;if(values[b]<0){values[b]=v;Q.push(b)}else if(values[b]!==v)throw Error("wire contradiction")}}
 let defects=[];for(let v=0;v<G.types.length;v++){let z=values.slice(v*4,v*4+4);if(G.types[v]==="E"&&z.some(x=>x!==z[0]))throw Error("E");if(G.types[v]==="B"&&z.reduce((a,b)=>a+b,0)!==2)defects.push(v)}
 for(let [a,b,s] of G.edges)if((values[a]^values[b])!==s)throw Error("wire");
 if(defects.length!==2||JSON.stringify(defects)!==JSON.stringify(cert.defects)||!ownerCert.intersection.includes(defects.join(",")))throw Error("energy witness");
 return {energy:2,defects,checked}
}
// Usage: node runner.js compile.js discovery.js independent_checker.js benchmarks.json registry.json INSTANCE owner-certificate.json [energy-certificate.json]
// Use the exact pinned source files listed in report.md. Discovery mode is optional: set REPLAY_DISCOVERY=1.
const fs=require("node:fs"),crypto=require("node:crypto");
const [compiler,discovery,checker,corpus,registry,id,certpath,energyPath]=process.argv.slice(2);
const read=p=>fs.readFileSync(p,"utf8"),hash=s=>crypto.createHash("sha256").update(s).digest("hex");
const cs=read(compiler),ds=read(discovery),ck=read(checker);
const compile=new Function(cs.slice(cs.indexOf("function compile("),cs.indexOf("function auditLocal("))+";return compile")();
const verifyNative=new Function(ck.slice(ck.indexOf("function verifyNative("),ck.indexOf("function replayTree("))+";return verifyNative")();
const src=JSON.parse(read(corpus)).instances.find(x=>x.id===id),reg=JSON.parse(read(registry)).instances.find(x=>x.alias==="EB-"+id),G=compile(src),bytes=JSON.stringify(G.network)+"\n",cert=JSON.parse(read(certpath));
if(hash(bytes)!==reg.sha256||Buffer.byteLength(bytes)*8!==reg.N_bits||hash(src.dimacs)!==reg.source_cnf.sha256||Buffer.byteLength(src.dimacs)*8!==reg.source_cnf.N_bits||hash(JSON.stringify(G.source_map)+"\n")!==reg.source_map_sha256||cert.instance_id!==reg.instance_id||cert.original_N_bits!==reg.N_bits)throw Error("authentication");
let out={certificate_id:"CERT-v1:sha256:"+hash(read(certpath)),verification:auditOwnerCertificate(G.network,cert,verifyNative)};
if(energyPath){let e=JSON.parse(read(energyPath));if(!e.parents.includes(out.certificate_id))throw Error("parent");out.energy=checkEnergy(G.network,e,cert,verifyNative);out.energy_certificate_id="CERT-v1:sha256:"+hash(read(energyPath))}
if(process.env.REPLAY_DISCOVERY==="1"){const {normalized,run,proof}=new Function(ds.slice(ds.indexOf("function normalized("),ds.indexOf("function checkMap("))+";return {normalized,run,proof}")();let n=normalized(G.network),A=run(n.rows,false),B=run(n.rows,true),C=run(n.rows.slice().reverse(),true);out.discovery=[A,B,C].map(x=>({status:x.status,ev:x.ev}));let proofs=[B,C].filter(x=>x.status==="UNSAT").map(proof);if(JSON.stringify(proofs)!==JSON.stringify(cert.proofs))throw Error("discovery proof mismatch")}
console.log(JSON.stringify(out,null,2));

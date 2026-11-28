function run(inputs){
 const {raw,peer,compiler,corp,reg,chart}=inputs;
 const sha=new Function(peer.slice(0,peer.indexOf("function quotient"))+";return sha")(),compile=new Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection}=new Function(chart.slice(chart.indexOf("const key="),chart.indexOf("function up("))+";return {project,verifyProjection}")();
 const enc=x=>JSON.stringify(x)+"\n"; if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
 function verify(F,proof){
 const rows=F.map(c=>c.slice()),idx=new Map(),units=[];let work=0,steps=0;function add(c,j){for(let l of c){if(!idx.has(l))idx.set(l,[]);idx.get(l).push(j)}if(c.length<=1)units.push(j)}
 rows.forEach(add);
 function rup(p){let A=new Set(),queue=[];function set(l){if(A.has(-l))return false;if(!A.has(l)){A.add(l);queue.push(l)}return true}
 for(let l of p)if(!set(-l))return true;
 for(let j of units){work++;let c=rows[j];if(!c.length||!set(c[0]))return true}
 for(let k=0;k<queue.length;k++){for(let j of idx.get(-queue[k])||[]){let c=rows[j],u=0,n=0,sat=false;for(let l of c){work++;if(A.has(l)){sat=true;break}if(!A.has(-l)){n++;u=l}}if(sat)continue;if(n===0||n===1&&!set(u))return true}}
 return false}
 for(let c of proof){if(!rup(c))throw Error("RUP "+steps);add(c,rows.length);rows.push(c);steps++}
 if(!proof.length||proof.at(-1).length)throw Error("no empty clause");return{steps,work,proofSHA256:sha(enc(proof))}
 }
 let out=[];for(let row of JSON.parse(raw)){let r=JSON.parse(reg).instances.find(z=>z.alias==="EB-"+row.name),x=JSON.parse(corp).instances.find(z=>z.id===row.name),G=compile(x);if(sha(enc(G.network))!==r.sha256||enc(G.network).length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("source mismatch");
 let p=project(G.network),projectOps=verifyProjection(G.network,p),guard=[[p.anchor,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),sha(enc({root:p.root,phase:p.phase}))]));
 let native=verify(p.clauses,row.native.proof),cnf=verify(x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)),row.cnf.proof);
 if(native.proofSHA256!==row.native.proofHash||cnf.proofSHA256!==row.cnf.proofHash)throw Error("proof hash");
 out.push({name:row.name,registry:r,guard,gid,rid,projectOps,native,cnf,projectionCost:p.cost})}
 return out
}

if(typeof require!=="undefined"&&require.main===module){const fs=require("node:fs");const keys=["raw","peer","compiler","corp","reg","chart"];console.log(JSON.stringify(run(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],"utf8")]))),null,2))}

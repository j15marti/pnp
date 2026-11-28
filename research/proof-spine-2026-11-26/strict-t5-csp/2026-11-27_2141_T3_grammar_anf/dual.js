function dual(P,sha){
 const A=(p,s)=>{if(!p)throw Error(s)},enc=x=>JSON.stringify(x)+"\n",par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p},result=[];
 for(let [id,bytes] of Object.entries(P)){let p=JSON.parse(bytes),rows=p.groupedRows,mon=new Map([["",0]]),a=rows.map(r=>r.terms.reduce((x,t)=>{let k=t.join(",");if(!mon.has(k))mon.set(k,mon.size);return x^(1n<<BigInt(mon.get(k)))},0n));let M=a.concat(1n),basis=new Map(),deps=[],xors=0;
  for(let i=0;i<M.length;i++){let v=M[i],u=1n<<BigInt(i);while(v){let k=v&-v;if(!basis.has(k)){basis.set(k,{v,u});break}let b=basis.get(k);v^=b.v;u^=b.u;xors++}if(!v)deps.push(u)}
  let order=[...basis].sort((a,b)=>a[0]>b[0]?-1:1),outputs=[],verification=0,solves=0,blocked=0;
  let targets=p.proof?p.proof:[-1];
  for(let i of targets){let rhs=(1n<<BigInt(a.length))|(i<0?0n:1n<<BigInt(i));if(deps.some(u=>par(u&rhs))){blocked++;continue}
   let lambda=0n;for(let [k,{v,u}] of order){solves++;if(par(v&lambda)!==par(u&rhs))lambda^=k}
   for(let j=0;j<M.length;j++){verification++;A(par(M[j]&lambda)===Number(j===a.length||j===i),"dual check")}
   outputs.push({omittedOwner:i,ones:[...mon].filter(([k,j])=>Boolean(lambda>>BigInt(j)&1n)).map(([k])=>k===""?[]:k.split(",").map(Number))})
  }
  let guard=[[p.gauge-1,0]],guardSchema="EB-PORT-PINS-v1",guardHash=sha(enc(guard)),guardId="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",p.instance_id,guardSchema,guardHash]));
  let residualSchema="T3-GROUPED-VIOLATION-ANF-v1",residualHash=sha(enc(rows)),mapArtifact={normalizer:"08f5d87b1534442cf0b8225761ba1a954a455e6c",projection:p.projection,gauge:p.gauge,rootPins:p.rootPins,clauseOrder:"verify.js exact table-to-CNF then canonical insertion-order dedup; group ids zero-based"};
  let mapHash=sha(enc(mapArtifact)),residualId="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",p.instance_id,guardId,residualSchema,residualHash,mapHash]));
  let c={schema:"T3-DUAL-ANF-REFUSAL-v1",problem_id:p.problem_id,instance_id:p.instance_id,original_N_bits:p.original_N_bits,guard_id:guardId,residual_id:residualId,guardArtifact:guard,guardSchema,guardHash,residualSchema,residualHash,mapHash,original_ids:p.original_ids,parents:["CERT-v1:sha256:"+sha(bytes)],claim:p.proof?"Listed owner deletions destroy constant-one membership in this fixed linear span; not a claim about satisfiability or other proof systems":"Constant one is not in the span of these verified grouped violation rows; no claim about PC multiplication or feasibility",proofs:outputs,counts:{factorizationXors:xors,backsolveRows:solves,verificationDots:verification,blockedTargets:blocked,monomials:mon.size,rank:basis.size}};
  result.push({id,certificate_id:"CERT-v1:sha256:"+sha(enc(c)),cert:c});
 }return result
}
if(typeof require==='function'){const fs=require('fs'),h=fs.readFileSync(process.argv[2],'utf8'),sha=Function(h.split('if(typeof require==="function"')[0]+';return sha')();let ids=['JOINT-24','RANDOM-3CNF-40','MIXED-3-NO','MIXED-MANY-3-NO'],P=Object.fromEntries(ids.map((k,i)=>[k,fs.readFileSync(process.argv[i+3],'utf8')]));console.log(JSON.stringify(dual(P,sha),null,2));}

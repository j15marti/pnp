"use strict";
/* LSPV-1/615: parameter-scalable source-SAT false-acceptance counterfamily.
 * Mathematical graph construction is indexed by k>=0. Literal native JavaScript
 * execution is bounded by Array/string/index limits and available memory;
 * ONLY finite k actually replayed may be called operationally verified.
 * This is a defect demonstration, not a valid UNSAT proof or the full R_mix341 calculus.
 * Usage from a complete checkout: node experiments/arc/lspv1_615_infinite_false_acceptance.cjs [raw-output.json]
 * Node >=18, only standard library. Every generated packet is deterministically rebuilt.
 */
const BASE=[[5,9],[5,10],[0,2],[0,3],[1,2],[1,3],[2,3],[0,4],[1,4],[6,8],[5,11],[6,9],[6,10],[7,8],[7,9],[7,10],[8,11],[4,11]];
const bit=(mask,e)=>Number((mask>>BigInt(e))&1n);
function gauss(eqs,E){
  const A=eqs.map(([mask,rhs])=>[BigInt(mask),rhs]);let at=0;const piv=[];
  for(let e=0;e<E&&at<A.length;e++){
    let j=at;while(j<A.length&&!bit(A[j][0],e))j++;
    if(j===A.length)continue;
    [A[at],A[j]]=[A[j],A[at]];
    for(let k=0;k<A.length;k++)if(k!==at&&bit(A[k][0],e)){A[k][0]^=A[at][0];A[k][1]^=A[at][1];}
    piv.push(e);at++;
  }
  if(A.some(([m,r])=>m===0n&&r))return null;
  const sol=Array(E).fill(0);
  for(let j=0;j<piv.length;j++)sol[piv[j]]=A[j][1];
  return {sol,rank:piv.length};
}
function graph(K){
  if(!Number.isInteger(K)||K<0)throw Error("nonnegative expansion count required");
  let n=12,edges=BASE.map(x=>x.slice());
  function connectedExcept(skip){
    const adj=Array.from({length:n},()=>[]);
    edges.forEach(([u,v],i)=>{if(i!==skip){adj[u].push(v);adj[v].push(u);}});
    const seen=new Set([0]),queue=[0];
    for(let k=0;k<queue.length;k++)for(const v of adj[queue[k]])if(!seen.has(v)){seen.add(v);queue.push(v);}
    return seen.size===n;
  }
  for(let k=0;k<K;k++){
    // Never reindex the three selected source edges 0,1,10.
    // Every expansion leaves an internal K4 cycle edge eligible for the next step.
    const idx=edges.findIndex(([u,v],i)=>i>=12&&u!==5&&v!==5&&connectedExcept(i));
    if(idx<0)throw Error("no nonbridge expansion edge");
    const [u,v]=edges[idx];edges.splice(idx,1);
    const [a,b,c,d,s,t]=Array.from({length:6},(_,i)=>n+i);n+=6;
    // A K4 with edges (a,b) and (c,d) subdivided, joined to u and v.
    edges.push([a,c],[a,d],[b,c],[b,d],[a,s],[s,b],[c,t],[t,d],[u,s],[v,t]);
  }
  const inc=Array.from({length:n},()=>[]);
  edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e);});
  if(inc[5].join(",")!=="0,1,10"||edges.length*2!==3*n||inc.some(x=>x.length!==3))
    throw Error("cubic graph/source-coordinate invariant");
  if(!edges.some((_,i)=>!connectedExcept(i)))throw Error("required bridge absent");
  if(!connectedExcept(10))throw Error("the shadow edge is a bridge");
  return {n,edges,inc};
}
function produce(K){
  const {n,edges,inc}=graph(K),E=edges.length,t=5;
  const q=Array(n).fill(0);q[0]=1;
  const charges=q.slice();charges[t]="0"; // JS bitwise-XOR coercion and strict-inequality divergence.
  const constraints=inc.map((sup,v)=>{
    const selected=v===t?[0,1]:sup;
    return [selected.reduce((x,e)=>x^(1n<<BigInt(e)),0n),q[v]];
  });
  const solution=gauss(constraints,E);
  if(!solution||solution.rank!==n)throw Error("modified incidence rows not independent");
  const clauses=[];
  for(let v=0;v<n;v++)for(let m=0;m<8;m++){
    const b=[m&1,(m>>1)&1,(m>>2)&1];
    const forbidden=v===t?(b[0]!==b[1]):((b[0]^b[1]^b[2])!==q[v]);
    if(forbidden)clauses.push({id:"s"+clauses.length,vertex:v,
      literals:inc[v].map((e,j)=>b[j]?-(e+1):(e+1))});
  }
  if(clauses.length!==4*n)throw Error("source clause count");
  const csat=(c,b)=>c.literals.some(lit=>lit>0?b[lit-1]===1:b[-lit-1]===0);
  if(!clauses.every(c=>csat(c,solution.sol)))throw Error("SAT witness does not satisfy source");
  const factor=new Map();
  for(const c of clauses){
    const sup=inc[c.vertex];let table=0;
    for(let m=0;m<8;m++){
      const bits=Array(E).fill(0);
      sup.forEach((e,j)=>bits[e]=(m>>j)&1);
      if(csat(c,bits))table|=1<<m;
    }
    factor.set(c.id,{kind:"factor",support:sup,table});
  }
  const evalFactor=(p,b)=>{let m=0;for(let j=0;j<p.support.length;j++)m|=Number(b[p.support[j]]??0)<<j;return (p.table>>m)&1;};
  const proof=[],rows=[];
  for(let v=0;v<n;v++){
    let left="s"+4*v;
    for(let j=1;j<=3;j++){
      const right="s"+(4*v+j),A=factor.get(left),B=factor.get(right);
      const support=v===t&&j===3?"102":inc[v].slice();
      let table=0;
      for(let m=0;m<8;m++){
        const bits=Array(E).fill(0);
        for(let i=0;i<support.length;i++)bits[support[i]]=(m>>i)&1;
        if(evalFactor(A,bits)&&evalFactor(B,bits))table|=1<<m;
      }
      const id="d"+proof.length,p={id,kind:"factor",rule:"AND3",parents:[left,right],support,table};
      if(j===3){
        const mask=inc[v].reduce((b,e)=>b|(1n<<BigInt(e)),0n);
        p.row={mask:"0x"+mask.toString(16),rhs:q[v]};rows.push(id);
      }
      factor.set(id,p);proof.push(p);left=id;
    }
  }
  let prev=rows[0],mask=BigInt(factor.get(prev).row.mask),rhs=factor.get(prev).row.rhs;
  for(let v=1;v<n;v++){
    const right=rows[v],id="d"+proof.length,row=factor.get(right).row;
    mask^=BigInt(row.mask);rhs^=row.rhs;
    proof.push({id,kind:"affine",rule:"XOR",parents:[prev,right],row:{mask:"0x"+mask.toString(16),rhs}});
    prev=id;
  }
  if(proof.length!==4*n-1||mask!==0n||rhs!==1)throw Error("terminal GF2 invalid");
  const deleted=clauses.map(c=>{
    const eqs=constraints.filter((_,v)=>v!==c.vertex).map(([m,r])=>[m,r]);
    for(let j=0;j<3;j++){
      const e=Math.abs(c.literals[j])-1,val=c.literals[j]<0?1:0;
      eqs.push([1n<<BigInt(e),val]);
    }
    const s=gauss(eqs,E);
    if(!s)return {sourceId:c.id,assignment:null};
    if(csat(c,s.sol)||clauses.some(d=>d.id!==c.id&&!csat(d,s.sol)))
      throw Error("deletion witness false");
    return {sourceId:c.id,assignment:s.sol.join("")};
  });
  const essential=deleted.filter(d=>d.assignment!==null).length;
  const packet={version:"LSPV1-615-INFINITE-FALSE-ACCEPTANCE",
    definition:"Archived /341 fixture checker only, not sound R_mix341",
    fixtures:[{graph:{name:"BRIDGE_341_FAMILY_"+K,n,edges},
      charges,clauses,proof,deleted,evenWitness:"0".repeat(E),properties:{essential}}],
    summary:[{}]};
  return {packet,K,vertices:n,variables:E,originalClauses:clauses.length,paidNodes:proof.length,
    essential,modelCount:"2^"+(E-n),modelCountDecimal:(1n<<BigInt(E-n)).toString(),
    sourceSatWitness:solution.sol.join("")};
}
function adversaries(pkt){
  const clone=()=>JSON.parse(JSON.stringify(pkt));
  const out=[];
  let x=clone();x.fixtures[0].proof[17].support=[0,1,10];out.push(["array_support_repair",x,false]);
  x=clone();x.fixtures[0].charges[5]=0;out.push(["numeric_charge_repair",x,false]);
  x=clone();x.fixtures[0].proof[17].parents[0]="missing";out.push(["bad_parent",x,false]);
  x=clone();x.fixtures[0].proof.at(-1).row.rhs=0;out.push(["bad_terminal",x,false]);
  x=clone();x.fixtures[0].clauses[20].literals[0]=999999;out.push(["bad_signed_source",x,false]);
  x=clone();const d=x.fixtures[0].deleted.find(y=>y.assignment!==null);
  d.assignment="2".repeat(x.fixtures[0].graph.edges.length);
  out.push(["bad_deleted_witness",x,false]);
  return out;
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("node:fs"),os=require("node:os"),path=require("node:path"),
    cp=require("node:child_process"),crypto=require("node:crypto"),assert=require("node:assert/strict");
  const repo=path.resolve(__dirname,"../.."),
    checker=path.join(repo,"experiments/arc/lspv2_341_independent_verify.js"),
    cb=fs.readFileSync(checker),
    gitblob=crypto.createHash("sha1").update("blob "+cb.length+"\0").update(cb).digest("hex");
  assert.equal(gitblob,"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","native checker identity");
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-615-")),results=[];
  try{
    for(let K=0;K<=4;K++){
      const {packet,...meta}=produce(K);
      const tests=[["accepted_sat",packet,true],...(K===0?adversaries(packet):[])],trial=[];
      for(const [name,pkt,want]of tests){
        const filename=path.join(dir,K+"_"+name+".json");
        fs.writeFileSync(filename,JSON.stringify(pkt));
        const r=cp.spawnSync(process.execPath,[checker,filename],
          {encoding:"utf8",timeout:30000,maxBuffer:5_000_000});
        assert.equal(r.status===0,want,"unexpected native verdict "+K+" "+name+" "+r.stderr);
        trial.push({name,accepted:r.status===0,checks:r.status===0?JSON.parse(r.stdout).checks:null,
          error:r.status===0?null:(r.stderr.match(/Error: [^\r\n]*/)||[])[0]||"REJECT"});
      }
      results.push({...meta,tests:trial,sha256:crypto.createHash("sha256").update(JSON.stringify(packet)).digest("hex")});
    }
    const raw={report:"LSPV-1/615",checkerGitBlob:gitblob,nativeOS:true,
      exhaustiveSearch:false,method:"symbolic GF(2) constructive infinite family, finite original-checker OS controls",
      model:"archived fixture /341 checker ONLY",results};
    const data=JSON.stringify(raw,null,2)+"\n";
    if(process.argv[2])fs.writeFileSync(process.argv[2],data);
    process.stdout.write(data);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
}

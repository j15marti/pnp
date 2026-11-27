// node audit.js compile.js corpus.json registry.json affine-closure.js JOINT.native.json JOINT.cnf.json JOINT.peer.json RANDOM.native.json RANDOM.cnf.json RANDOM.peer.json
const fs=require("node:fs"); const [compiler,corpus,registry,projection,...f]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));
function sha256(s) {
  // All canonical bytes in this run are ASCII.
  const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19], n=s.length, len=Math.ceil((n+9)/64)*64, a=new Uint8Array(len);
  for(let i=0;i<n;i++){const c=s.charCodeAt(i);if(c>127)throw Error("non ASCII");a[i]=c}a[n]=128;
  let bits=BigInt(n)*8n;for(let i=0;i<8;i++){a[len-1-i]=Number(bits&255n);bits>>=8n}
  const r=(x,k)=>(x>>>k)|(x<<(32-k)),w=new Int32Array(64);
  for(let o=0;o<len;o+=64){
    for(let i=0;i<16;i++)w[i]=(a[o+4*i]<<24)|(a[o+4*i+1]<<16)|(a[o+4*i+2]<<8)|a[o+4*i+3];
    for(let i=16;i<64;i++){const x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(r(x,7)^r(x,18)^(x>>>3))+w[i-7]+(r(y,17)^r(y,19)^(y>>>10)))|0}
    let [A,B,C,D,E,F,G,J]=H;
    for(let i=0;i<64;i++){let t=(J+(r(E,6)^r(E,11)^r(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((r(A,2)^r(A,13)^r(A,22))+((A&B)^(A&C)^(B&C)))|0;J=G;G=F;F=E;E=(D+t)|0;D=C;C=B;B=A;A=(t+u)|0}
    [A,B,C,D,E,F,G,J].forEach((v,i)=>H[i]=(H[i]+v)|0);
  }return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")
}

function audit(src,inputs,sha){
 const compile=new Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal"))+"\nreturn compile")();const module={exports:{}};new Function("module",src.projection)(module);const {normalize,project,cnfFactors}=module.exports,reg=JSON.parse(src.registry),corpus=JSON.parse(src.corpus),J=x=>JSON.stringify(x)+"\n",uniq=a=>[...new Set(a)].sort((a,b)=>a-b);
 const assert=(x,s)=>{if(!x)throw Error(s)},eq=(a,b)=>J(a)===J(b);
 function dsu(net){let n=4*net.types.length,P=Int32Array.from({length:n},(_,i)=>i),S=new Uint8Array(n),ops=0;function find(x){let b=0,y=x;while(P[y]!==y){b^=S[y];y=P[y];ops++}while(P[x]!==x){let j=P[x],a=S[x];P[x]=y;S[x]=b;b^=a;x=j;ops++}return [y,S[x]]}
  // A separate noncompressing read for signs; merge larger root into smaller root.
  function get(x){let b=0;while(P[x]!==x){b^=S[x];x=P[x];ops++}return [x,b]}
  function join(a,b,s){let [u,x]=get(a),[v,y]=get(b);if(u===v){assert((x^y)===s,"dsu cycle");return}if(u>v)[u,v]=[v,u];P[v]=u;S[v]=x^y^s;ops++}
  for(let [a,b,s] of net.edges)join(a,b,s);for(let [v,t] of net.types.entries())if(t==="E")for(let j=1;j<4;j++)join(4*v,4*v+j,0);let roots=[],signs=[];for(let i=0;i<n;i++){let [r,b]=get(i);roots.push(r);signs.push(b)}return {roots,signs,ops}}
 // Independent domain-set closure and branch replay; no proof search when checking submitted trees.
 function checkTree(F,tree,g=[],cap=3000000,build=false){
  let work=0,nodes=0;function tick(n=1){work+=n;if(work>cap)throw Error("cap")}
  const vars=uniq(F.flatMap(a=>a.v)),index=new Map(vars.map((x,i)=>[x,i]));
  function closure(g){let dom=new Uint8Array(vars.length).fill(3);for(let [x,b] of g){if(!index.has(x))continue;dom[index.get(x)]&=1<<b;if(!dom[index.get(x)])return null}
   let change=true;while(change){change=false;for(let t of F){let support=new Uint8Array(t.v.length),has=false,ii=t.v.map(x=>index.get(x));for(let w of t.ok){tick(t.v.length+1);if(ii.every((v,i)=>dom[v]&(1<<(w>>i&1)))){has=true;ii.forEach((_,i)=>support[i]|=1<<(w>>i&1))}}if(!has)return null;for(let i=0;i<ii.length;i++){let d=dom[ii[i]]&support[i];if(!d)return null;if(d!==dom[ii[i]]){dom[ii[i]]=d;change=true}}}}return dom}
  function replay(t,g){nodes++;if(t===0)return closure(g)===null;return Array.isArray(t)&&t.length===3&&index.has(t[0])&&!g.some(([v])=>v===t[0])&&replay(t[1],[...g,[t[0],0]])&&replay(t[2],[...g,[t[0],1]])}
  function search(g){if(++nodes>192)throw Error("node cap");let d=closure(g);if(!d)return 0;let f=new Map();for(let a of F)for(let v of a.v){tick();if(d[index.get(v)]===3)f.set(v,(f.get(v)||0)+1)}if(!f.size)return null;let v=[...f].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let l=search([...g,[v,0]]);if(l===null)return null;let r=search([...g,[v,1]]);return r===null?null:[v,l,r]}
  try{let t=build?search(g):tree,n=nodes,w=work;let ok=t!==null&&replay(t,g);return {ok,tree:t,nodes,work,discovery:build?w:0,verification:build?work-w:work,searchNodes:build?n:0}}catch(e){if(!["cap","node cap"].includes(e.message))throw e;return {ok:false,reason:e.message,work,nodes}}
 }
 function checkCert(F,cert,gauge=null){
  const R=cert.proof.result;let count=0,work=0;assert(R.hybrid.length===0,"unexpected prior hybrid");
  for(let p of R.proofs){assert(p.k.every(i=>Number.isInteger(i)&&i>=0&&i<F.length),"factor index");assert(eq(uniq(p.k.flatMap(i=>F[i].ids)),p.original_B_or_clause_ids),"support");
   let pins=gauge===null?p.guard:[[gauge-1,0],...p.guard.map(([v,b])=>[v-1,b])].sort((a,b)=>a[0]-b[0]);let schema=gauge===null?"CNF-VAR-PINS-v1":"EB-PORT-PINS-v1";assert(eq(pins,p.guard_artifact.pins),"guard map");assert(p.guard_artifact.id==="GUARD-v1:sha256:"+sha(J(["PNP-GUARD-v1",cert.instance_id,schema,sha(J(pins))])),"guard id");
   let q=checkTree(p.k.map(i=>F[i]),p.tree,p.guard);assert(q.ok,"invalid submitted tree "+p.mode);count++;work+=q.work;
  }
  let G=R.best.map((i,k)=>{assert(i!==null&&eq(R.proofs[i].guard,R.guards[k]),"chosen guard");return R.guards[k]});
  let V=uniq(G.flatMap(g=>g.map(x=>x[0]))),coverage=0;for(let w=0;w<2**V.length;w++)if(G.some(g=>g.every(([v,b])=>(w>>V.indexOf(v)&1)===b)))coverage++;
  assert(coverage===2**V.length&&R.full,"cover");assert(eq(uniq(R.best.flatMap(i=>R.proofs[i].original_B_or_clause_ids)),R.support),"union");
  // Import only independently checked non-resolution guards, NOT the completed five-guard cover.
  let inds=R.rows.flatMap(r=>{let m=r.methods.find(m=>m.mode==="cardinality"&&m.proofIndex!==undefined);return m?[m.proofIndex]:[]});
  let imported=inds.map(i=>{let p=R.proofs[i],v=p.guard.map(a=>a[0]),b=p.guard.reduce((w,a,j)=>w|(a[1]<<j),0);return {v,ok:Array.from({length:2**v.length},(_,w)=>w).filter(w=>w!==b),ids:p.original_B_or_clause_ids,parent:i}});
  let baseline=checkTree(F,null,[],1500000,true),hybrid=checkTree([...F,...imported],null,[],1500000,true);
  // Same fixed seed tests extra two-pin guards at the stalled methods; local table closure only, exact check.
  let random=[],seed=20261127,Vall=uniq(F.flatMap(t=>t.v));function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
  for(let j=0;j<12;j++){let x=Vall[rand()%Vall.length],y=Vall[rand()%Vall.length],b=rand()&1,c=rand()&1;if(x===y){random.push({status:"duplicate variable"});continue}let g=[[x,b],[y,c]].sort((a,b)=>a[0]-b[0]),q=checkTree(F,0,g,150000);random.push({g,status:q.ok?"verified local conflict (not imported)":"UNKNOWN",work:q.work})}
  // Exact 5-guard logical terminal, with four explicitly checked binary resolution operations.
  let clauses=G.map(g=>g.map(([v,b])=>b?-v:v).sort((a,b)=>a-b)),live=clauses.map(a=>a.slice()),steps=[];
  while(!live.some(c=>!c.length)){let done=false;for(let i=0;i<live.length&&!done;i++)for(let j=i+1;j<live.length&&!done;j++){for(let l of live[i])if(live[j].includes(-l)){let res=uniq([...live[i].filter(x=>x!==l),...live[j].filter(x=>x!==-l)]);if(res.some(x=>res.includes(-x))||res.length>=Math.max(live[i].length,live[j].length))continue;if(live.some(c=>eq(c,res)))continue;steps.push({i,j,pivot:Math.abs(l),res});live.push(res);done=true;break}}if(!done)throw Error("resolution merge failed")}
  return {verified:true,proofCount:count,independentReplayEvents:work,guardAssignmentCount:2**V.length,covered:coverage,nonResolutionImports:inds,baseline,hybrid,random,merge:{clauses,steps}};
 }
 let out=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){let e=reg.instances.find(x=>x.alias==="EB-"+alias),x=corpus.instances.find(x=>x.id===alias),g=compile(x);
  assert(sha(J(g.network))===e.sha256&&J(g.network).length*8===e.N_bits&&sha(J(g.source_map))===e.source_map_sha256&&sha(x.dimacs)===e.source_cnf.sha256,"input");
  let n=normalize(g.network),ds=dsu(g.network);assert(eq(ds.roots,Array.from(n.root))&&eq(ds.signs,Array.from(n.par)),"independent DSU");
  let p=project(n.F,1500000),N=JSON.parse(inputs[alias].native),C=JSON.parse(inputs[alias].cnf),T=JSON.parse(inputs[alias].peer);let chart=N.proof.chart;
  assert(p.status==="COMPLETE"&&sha(J(p.final))===chart.residualHash&&sha(J({gauge:p.gauge,root:Array.from(n.root),par:Array.from(n.par),projection_steps:p.steps}))===chart.mapHash,"chart");
  assert(chart.residual_id==="RESIDUAL-v1:sha256:"+sha(J(["PNP-RESIDUAL-v1",e.instance_id,chart.gId,"EB-TABLE-ROOTPLUS1-v1",chart.residualHash,chart.mapHash])),"residual id");
  let a=checkCert(p.final,N,p.gauge),b=checkCert(cnfFactors(x.dimacs),C),peer=null;
  assert(T.instance_id===e.instance_id&&T.proof.gauge===p.gauge&&eq(T.proof.projection_steps,p.steps)&&eq(T.proof.final_factors,p.final),"peer mapping");
  let q=checkTree(p.final,T.proof.tree);assert(q.ok,"peer tree");peer={certificate_id:"CERT-v1:sha256:"+sha(inputs[alias].peer),nodes:q.nodes,work:q.work,verified:true,usedAsAdvice:false};
  out.push({alias,native:a,cnf:b,peer,dsuOps:ds.ops,nativeCert:"CERT-v1:sha256:"+sha(inputs[alias].native),cnfCert:"CERT-v1:sha256:"+sha(inputs[alias].cnf)});
 }
 return out;
}
console.log(JSON.stringify(audit({compiler,corpus,registry,projection},{"JOINT-24":{native:f[0],cnf:f[1],peer:f[2]},"RANDOM-3CNF-40":{native:f[3],cnf:f[4],peer:f[5]}},sha256)));

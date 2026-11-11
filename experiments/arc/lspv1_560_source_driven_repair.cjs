"use strict";
/* LSPV-1/560. Run from repository root:
   node experiments/arc/lspv1_560_source_driven_repair.cjs
   Exact upstream Git blobs: producer 4081022e8a3841d79f751a3d3a7a10decbb026da,
   recovered checker fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
   This is a recovered-fixture adapter, NOT an R_mix341 full-calculus checker.
*/
const fs=require("fs"),os=require("os"),path=require("path"),cp=require("child_process"),crypto=require("crypto");
const root=path.resolve(__dirname,"../..");
const producer=path.join(root,"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js");
const checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const rawPath=path.join(root,"results/raw/arc/2026-11-10_1755_LSPV1_560_SOURCE_DRIVEN_REPAIR_RAW.json");
function gitSHA(p){const b=fs.readFileSync(p);return crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");}
function assert(x,m){if(!x)throw Error(m)}
assert(gitSHA(producer)==="4081022e8a3841d79f751a3d3a7a10decbb026da","producer Git SHA changed");
assert(gitSHA(checker)==="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","checker Git SHA changed");
const original=JSON.parse(cp.execFileSync(process.execPath,[producer],{encoding:"utf8",maxBuffer:25000000}));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-l1-560-"));
function check(packet){const file=path.join(tmp,"packet.json");fs.writeFileSync(file,JSON.stringify(packet));
 try{const x=JSON.parse(cp.execFileSync(process.execPath,[checker,file],{encoding:"utf8",maxBuffer:25000000,stdio:["ignore","pipe","pipe"]}));return {accepted:true,checks:x.checks};}
 catch(e){return {accepted:false,reason:String((e.stderr||"").toString()||e.message).slice(0,250)};}}
function clone(x){return JSON.parse(JSON.stringify(x))}
function repairFixture(f, externalClauses){
 const g=f.graph,V=g.n,E=g.edges.length; assert(Number.isSafeInteger(V)&&V>=4&&E*2===3*V,"cubic dimensions");
 const incid=Array.from({length:V},()=>[]);
 const seenEdges=new Set(),deg=Array(V).fill(0);
 g.edges.forEach(([u,v],i)=>{assert(Number.isSafeInteger(u)&&Number.isSafeInteger(v)&&u>=0&&v>=0&&u<V&&v<V&&u!==v,"bad edge");
  const key=Math.min(u,v)+":"+Math.max(u,v);assert(!seenEdges.has(key),"duplicate edge");seenEdges.add(key);
  incid[u].push(i);incid[v].push(i);deg[u]++;deg[v]++;});
 assert(deg.every(d=>d===3),"noncubic");
 assert(Array.isArray(f.charges)&&f.charges.length===V&&f.charges.every(x=>typeof x==="number"&&(x===0||x===1))&&f.charges.reduce((a,b)=>a^b,0)===1,"G2 numeric odd charges");
 assert(Array.isArray(f.clauses)&&f.clauses.length===4*V&&Array.isArray(externalClauses)&&externalClauses.length===4*V,"G1 source count");
 const byV=Array.from({length:V},()=>[]),ids=new Set();
 f.clauses.forEach((c,i)=>{
  assert(Array.isArray(c.literals)&&c.literals.length===3&&c.literals.every(x=>Number.isSafeInteger(x)&&x!==0),"G1 primitive literals");
  assert(JSON.stringify(c.literals)===JSON.stringify(externalClauses[i]),"G1 external signed-source mismatch");
  assert(Number.isSafeInteger(c.vertex)&&c.vertex>=0&&c.vertex<V,"source vertex");
  assert(!ids.has(c.id),"source IDs not distinct in parsed semantics");ids.add(c.id);
  const v=c.vertex,loc=incid[v].map(e=>c.literals.find(x=>Math.abs(x)===e+1));
  assert(loc.every(x=>x!==undefined)&&new Set(c.literals.map(x=>Math.abs(x))).size===3,"source signed incidence");
  const bits=loc.map(x=>Number(x<0));
  assert(bits.reduce((a,b)=>a^b,0)!==f.charges[v],"not forbidden charge parity");
  assert(!byV[v].some(x=>x.bits.join("")===bits.join("")),"duplicate forbidden pattern");
  let table=0;for(let m=0;m<8;m++)if(bits.some((x,j)=>x!==((m>>j)&1)))table|=1<<m;
  byV[v].push({id:c.id,bits,table});
 });
 assert(byV.every(a=>a.length===4),"four parity clauses per vertex");
 let prefix="REPAIR";while([...ids].some(x=>typeof x==="string"&&x.startsWith(prefix)))prefix+="_";
 const proof=[],vertexRows=[];
 for(let v=0;v<V;v++){
   let prior=byV[v][0];
   for(let j=1;j<4;j++){
     const p={id:prefix+proof.length,kind:"factor",rule:"AND3",parents:[prior.id,byV[v][j].id],support:incid[v].slice(),table:prior.table&byV[v][j].table};
     proof.push(p);prior={id:p.id,table:p.table};
   }
   const row=proof[proof.length-1];
   row.row={mask:"0x"+incid[v].reduce((s,e)=>s^(1n<<BigInt(e)),0n).toString(16),rhs:f.charges[v]};
   vertexRows.push(row);
 }
 let acc=vertexRows[0],mask=BigInt(acc.row.mask),rhs=acc.row.rhs;
 for(let v=1;v<V;v++){
  mask^=BigInt(vertexRows[v].row.mask);rhs^=vertexRows[v].row.rhs;
  const p={id:prefix+proof.length,kind:"affine",rule:"XOR",parents:[acc.id,vertexRows[v].id],row:{mask:"0x"+mask.toString(16),rhs}};
  proof.push(p);acc=p;
 }
 assert(mask===0n&&rhs===1&&proof.length===4*V-1,"invalid repaired contradiction or tariff");
 return {...f,proof};
}
function repairPacket(p, external){assert(p.fixtures.length===external.length,"source fixture mismatch");return {...p,fixtures:p.fixtures.map((f,i)=>repairFixture(f,external[i]))};}
// External source is a frozen source *snapshot* generated before test mutations.
// A production source binder must separately parse and authenticate independently supplied DIMACS bytes.
const external=original.fixtures.map(f=>f.clauses.map(c=>c.literals.slice()));
function mutate(name){const p=clone(original),f=p.fixtures[0];
 if(name==="paired_ghost")for(const i of [2,5])f.proof[i].row.mask="0x"+(BigInt(f.proof[i].row.mask)^(1n<<128n)).toString(16);
 if(name==="string_terminal_support")f.proof[2].support=f.proof[2].support.join("");
 if(name==="coercible_string_charge")f.charges[0]="1";
 if(name==="wrong_signed_source")f.clauses[0].literals[0]=999;
 if(name==="bad_sink")f.proof[f.proof.length-1].row.rhs=0;
 return p;
}
const cases=[];
try{
 for(const name of ["baseline","paired_ghost","string_terminal_support","coercible_string_charge","wrong_signed_source","bad_sink"]){
  const packet=mutate(name),before=check(packet);let after;
  try{after=check(repairPacket(packet,external));}catch(e){after={accepted:false,guardFailure:String(e.message)};}
  cases.push({name,before,after});
 }
 assert(cases[0].before.accepted&&cases[0].after.accepted,"baseline");
 for(const i of [1,2])assert(cases[i].before.accepted&&cases[i].after.accepted,"accepted hostile repair "+cases[i].name);
 assert(cases[3].before.accepted&&!cases[3].after.accepted,"G2 false accept");
 assert(!cases[4].after.accepted,"G1 invalid source");
 assert(!cases[5].before.accepted&&cases[5].after.accepted,"reverse direction is not a theorem");
 const raw={date:"2026-11-10 17:55 PST",status:"PROVED/RESTRICTED mathematical source reconstruction; COMPUTATIONAL OS-Node only when actually run",producer_git_blob:gitSHA(producer),checker_git_blob:gitSHA(checker),
  trust:"external is an independent-by-copy signed clause snapshot from the original producer; production external DIMACS binder NOT tested",cases,
  fixtures:original.fixtures.map(f=>({name:f.graph.name,V:f.graph.n,W:4*f.graph.n-1})),nonclaims:["no full historical R_mix341 grammar","no arbitrary CNF sound retraction","no machine-time or space lower bound"]};
 fs.writeFileSync(rawPath,JSON.stringify(raw,null,2)+"\n");console.log(JSON.stringify(raw,null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}

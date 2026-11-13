#!/usr/bin/env node
'use strict';
/* LSPV-5/518. Independent native-OS and source-semantics validation of
 * LSPV-1/609. This concerns only the recovered /341 fixture checker. It does
 * not authenticate the missing complete historical R_mix341 dispatcher.
 *
 * Run from repository root:
 *   node experiments/review/lspv5_518_native341_minimal_sat_os_validation.cjs [raw.json]
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const rel={
 checker:'experiments/arc/lspv2_341_independent_verify.js',
 peer:'experiments/arc/lspv1_609_bridge_slice_forge.cjs',
 packet:'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json',
 hosted:'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_HOSTED_RAW.json'
};
const pins={
 checker:{git:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',sha256:'0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae'},
 peer:{git:'001fc1934e22adb9d26a917ca044b3beaff41664',sha256:'65334658ac3dd3f623076cd98f1efaa376fab2678eb6f35da3724771b378340b'},
 packet:{git:'8d6d9bc7f2940a77edf2a07fcb72af111ba5b928',sha256:'b1cd6c51b34502801319c47f9c1617cdb53f265c49b09867e3176d262bb8a3a2'},
 hosted:{git:'84e3690a1d6b00cc86e4e6393b1a5220849cccb2',sha256:'1e2132dde5616299780a37ed61822d1e239002b2ae7fdbebf28ed9f7f2390269'}
};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const git=b=>crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
const bytes={};
for(const [k,p] of Object.entries(rel)){
 bytes[k]=fs.readFileSync(path.join(root,p));
 assert.equal(git(bytes[k]),pins[k].git,`${k} Git blob drift`);
 assert.equal(sha(bytes[k]),pins[k].sha256,`${k} SHA-256 drift`);
}
const packet=JSON.parse(bytes.packet),hosted=JSON.parse(bytes.hosted),f=packet.fixtures[0];
assert.equal(packet.fixtures.length,1);assert.equal(f.graph.n,12);assert.equal(f.graph.edges.length,18);
assert.equal(f.clauses.length,48);assert.equal(f.proof.length,47);
assert.equal(f.charges[5],'0');assert.equal(typeof f.charges[5],'string');
assert.equal(f.proof[17].support,'102');assert.equal(typeof f.proof[17].support,'string');
assert.equal(f.proof[17].row.mask,'0x403');assert.equal(f.proof[17].row.rhs,0);

// Independent graph audit.
const V=f.graph.n,E=f.graph.edges.length,degree=Array(V).fill(0),pairs=new Set();
for(const [u,v] of f.graph.edges){
 assert(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<V&&v<V&&u!==v);
 const key=`${Math.min(u,v)}:${Math.max(u,v)}`;assert(!pairs.has(key));pairs.add(key);degree[u]++;degree[v]++;
}
assert(degree.every(x=>x===3));assert.equal(2*E,3*V);
function connected(skip=-1){
 const seen=new Set([0]),todo=[0];
 for(let i=0;i<todo.length;i++)for(let e=0;e<E;e++)if(e!==skip){
  const [a,b]=f.graph.edges[e],w=a===todo[i]?b:b===todo[i]?a:-1;
  if(w>=0&&!seen.has(w)){seen.add(w);todo.push(w);}
 }
 return seen.size===V;
}
assert(connected());assert.equal(connected(17),false);assert.equal(connected(10),true);

// Independent source semantics and model distribution.
const sat=(c,bits)=>c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0);
let models=0,modelsX10One=0,fakeAliasViolations=0,first=null,firstFakeViolation=null;
for(let x=0;x<(1<<E);x++){
 const bits=Array.from({length:E},(_,i)=>(x>>i)&1);
 if(f.clauses.every(c=>sat(c,bits))){
  models++;const s=bits.join('');if(first===null)first=s;
  if(bits[10]===1)modelsX10One++;
  if((bits[0]^bits[1]^bits[10])!==0){fakeAliasViolations++;if(firstFakeViolation===null)firstFakeViolation=s;}
 }
}
assert.equal(models,64);assert.equal(modelsX10One,64);assert.equal(fakeAliasViolations,64);
assert.equal(first,'000000010010000001');
const target=f.clauses.filter(c=>c.vertex===5);assert.equal(target.length,4);
for(let a=0;a<8;a++){
 const bits=Array(E).fill(0);bits[0]=a&1;bits[1]=(a>>1)&1;bits[10]=(a>>2)&1;
 assert.equal(target.every(c=>sat(c,bits)),bits[0]===bits[1]);
}

// All 48 SOURCE definitions are ancestors of the final paid node.
const byId=new Map([...f.clauses,...f.proof].map(x=>[x.id,x])),used=new Set(),stack=[f.proof.at(-1).id];
while(stack.length){const id=stack.pop();if(used.has(id))continue;used.add(id);const x=byId.get(id);assert(x);for(const q of x.parents||[])stack.push(q);}
assert(f.clauses.every(c=>used.has(c.id)));

// The source-code threshold premise is pinned, not inferred from a reimplementation.
const checkerText=bytes.checker.toString('utf8');
assert(checkerText.includes('if(E<=15){ // independent exhaustive truth-table count'));
assert(checkerText.includes('assert(oddCount===0,"UNSAT brute-force failure")'));
assert.equal(Math.floor(3*10/2),15);

function run(label,args){
 const t0=process.hrtime.bigint();
 const r=cp.spawnSync(process.execPath,args,{cwd:root,encoding:'utf8',timeout:30000,maxBuffer:5e6});
 assert.ifError(r.error);assert.equal(r.status,0,`${label}: ${r.stderr.slice(0,800)}`);
 return {json:JSON.parse(r.stdout),elapsedMs:Number(process.hrtime.bigint()-t0)/1e6};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-518-'));
try{
 const peer=run('exact /609 runner',[path.join(root,rel.peer),path.join(tmp,'peer.json')]);
 assert.equal(peer.json.native_os,true);assert.equal(peer.json.model_count,64);assert.equal(peer.json.essential,39);
 assert.equal(peer.json.signed_original_clauses,48);assert.equal(peer.json.paid_nodes,47);
 assert.deepEqual(peer.json.runs.map(x=>x.accepted),[true,false,false,false,false,false]);
 assert.equal(peer.json.runs[0].checks,5155);
 const direct=run('published packet direct checker',[path.join(root,rel.checker),path.join(root,rel.packet)]);
 assert.equal(direct.json.checks,5155);assert.equal(direct.json.cases[0].proofNodes,47);
 assert.equal(hosted.checker_output_assertions,5155);assert.equal(hosted.source_models,64);
 const ledger={
  schema:'LSPV5-518-NATIVE341-MINIMAL-SAT-OS-VALIDATION/v1',
  timestamp_pst:'2026-11-12T21:48:00-08:00',node:process.version,
  status:'PROVED/RESTRICTED threshold validation + COMPUTATIONAL native OS replay; full R_mix341 OPEN',
  scope:'Pinned recovered /341 fixture checker only',pins,
  graph:{vertices:V,edges:E,cubic:true,connected:true,bridgeEdge17:true,edge10Nonbridge:true},
  source:{signedClauses:f.clauses.length,models,modelsWithEdge10One:modelsX10One,
   modelsViolatingFalseClaimedAlias:fakeAliasViolations,firstModel:first,firstFalseAliasModel:firstFakeViolation,
   targetVertex:5,targetActualEquation:'x0 XOR x1 = 0',falseClaimedEquation:'x0 XOR x1 XOR x10 = 0'},
  proof:{paidNodes:f.proof.length,allSourcesInTerminalCone:true,essentialWitnesses:f.properties.essential,
   spoofCharge:{value:f.charges[5],type:typeof f.charges[5]},spoofSupport:{value:f.proof[17].support,type:typeof f.proof[17].support},falseMask:f.proof[17].row.mask},
  native:{peerRunnerAccepted:1,peerRunnerRejected:5,peerRunnerChecks:5155,directPublishedPacketChecks:5155,
   peerElapsedMs:peer.elapsedMs,directElapsedMs:direct.elapsedMs},
  threshold:{statement:'For this checker sublanguage, any accepted satisfiable-source connected simple cubic fixture has V>=12; /609 attains V=12.',
   proof:'Cubic implies V even and E=3V/2. For V<12, V<=10 and E<=15; pinned checker exhaustively rejects any source with a model. The pinned V=12 packet directly accepts and has 64 models.'},
  cegar:'The accepted checker execution is genuine and cannot be refined away from a checker-language abstraction; it is not a valid refutation in a sound source-bound calculus.',
  affected:['P2-D1 remains OPEN','P2-C3 remains OPEN','P2-B1 remains OPEN','P2-B2/B3 remain separate OPEN'],
  nonClaims:['No complete historical mixed dispatcher recovered','No sound refutation of the satisfiable source','No all-rule cost abstraction','No SAT lower bound or P versus NP result']
 };
 const out=JSON.stringify(ledger,null,2)+'\n';
 if(process.argv[2]){fs.mkdirSync(path.dirname(process.argv[2]),{recursive:true});fs.writeFileSync(process.argv[2],out);}
 process.stdout.write(out);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}

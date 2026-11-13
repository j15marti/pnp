'use strict';
// LSPV-4/573. Run from the j15marti/pnp repository root with Node.js >=18.
// Exact fixed-DAG serialized-record retention proxy, NOT historical full R_mix341 or physical RAM.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
 crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const SOURCE='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const CHECK='experiments/arc/lspv2_341_independent_verify.js';
function gitblob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
function pinned(file,sha){const b=fs.readFileSync(file);assert.equal(gitblob(b),sha,'changed: '+file);return b.toString('utf8');}
const original=JSON.parse(pinned(SOURCE,'fe27fe1011d0021e721ccaeb747ed58da65d7464'));
pinned(CHECK,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const clone=x=>JSON.parse(JSON.stringify(x));
function analyze(f){
 const p=f.proof,n=p.length,indices=new Map(p.map((x,i)=>[x.id,i]));
 const predecessors=p.map(x=>x.parents.reduce((v,z)=>indices.has(z)?v|(1n<<BigInt(indices.get(z))):v,0n));
 const consumers=Array(n).fill(0n);
 p.forEach((x,i)=>x.parents.forEach(z=>{if(indices.has(z))consumers[indices.get(z)]|=1n<<BigInt(i);}));
 // All original proof-node records are ASCII. This is a byte-size of a chosen
 // representation, NOT a lower bound on necessary semantic-object storage.
 const w=p.map(x=>Buffer.byteLength(JSON.stringify(x),'utf8'));
 const live=mask=>{let bytes=0,slots=0;for(let i=0;i<n;i++){
  const bit=1n<<BigInt(i);
  if((mask&bit)&&(consumers[i]===0n || (consumers[i]&mask)!==consumers[i])){
   bytes+=w[i];slots++;
  }
 }return {bytes,slots};};
 const score=order=>{let m=0n,area=0,slotArea=0,freshPeak=0,atomicPeak=0;
  for(const i of order){
   const bit=1n<<BigInt(i);assert(!(m&bit)&&((predecessors[i]&m)===predecessors[i]));
   const before=live(m);freshPeak=Math.max(freshPeak,before.bytes+w[i]);
   m|=bit;const after=live(m);area+=after.bytes;slotArea+=after.slots;atomicPeak=Math.max(atomicPeak,before.slots,after.slots);
  }
  assert.equal(m,(1n<<BigInt(n))-1n);return {byte_area:area,slot_area:slotArea,fresh_output_peak_bytes:freshPeak,atomic_live_peak:atomicPeak};
 };
 const zero={mask:0n,cost:0,order:[]},states=new Map([['0',zero]]),queue=[zero];let edges=0;
 for(let head=0;head<queue.length;head++){
  const s=queue[head];
  for(let i=0;i<n;i++){
   const bit=1n<<BigInt(i);
   if((s.mask&bit)||((predecessors[i]&s.mask)!==predecessors[i]))continue;
   const mask=s.mask|bit,after=live(mask);if(after.slots>2)continue;
   edges++;const cost=s.cost+after.bytes,key=mask.toString(),prior=states.get(key);
   if(!prior){const t={mask,cost,order:[...s.order,i]};states.set(key,t);queue.push(t);}
   else if(cost<prior.cost){prior.cost=cost;prior.order=[...s.order,i];}
  }
 }
 const best=states.get(((1n<<BigInt(n))-1n).toString());assert(best);
 let dfs=[];function visit(i){for(const q of p[i].parents)if(indices.has(q))visit(indices.get(q));dfs.push(i);}visit(n-1);
 const before=score(p.map((_,i)=>i)),depthFirst=score(dfs),optimal=score(best.order);
 assert.equal(optimal.byte_area,best.cost);
 assert.equal(optimal.slot_area,7*f.graph.n-4);
 assert.equal(before.slot_area,2*f.graph.n*f.graph.n+f.graph.n);
 return {graph:f.graph.name,vertices:f.graph.n,paid_nodes:n,states:states.size,legal_transitions:edges,
  original:before,depth_first:depthFirst,optimal,improvement_over_DFS:depthFirst.byte_area-optimal.byte_area,
  optimal_original_proof_ids:best.order.map(i=>p[i].id)};
}
const rows=original.fixtures.map(analyze),out=clone(original);
out.fixtures.forEach((f,i)=>{const lookup=new Map(f.proof.map(p=>[p.id,p]));f.proof=rows[i].optimal_original_proof_ids.map(id=>lookup.get(id));});
assert.equal(Buffer.byteLength(JSON.stringify(original)+'\n'),77714);
assert.equal(Buffer.byteLength(JSON.stringify(out)+'\n'),77714);
assert.deepEqual(rows.map(x=>x.optimal.byte_area),[2452,3862,5272,6751,8211,23836,6724]);
assert.deepEqual(rows.map(x=>x.improvement_over_DFS),[0,0,0,9,9,33,0]);
assert.deepEqual(rows.map(x=>x.states),[79,189,347,553,807,5987,553]);
function originalCLI(packet){
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-573-')),file=path.join(tmp,'packet.json');
 try{
  fs.writeFileSync(file,JSON.stringify(packet)+'\n');
  const proc=cp.spawnSync(process.execPath,[path.resolve(CHECK),file],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
  if(proc.status!==0)return {accept:false,stderr:String(proc.stderr||proc.error||'').slice(0,250)};
  return {accept:true,checks:JSON.parse(proc.stdout).checks};
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
const base=originalCLI(original),optimized=originalCLI(out);
assert(base.accept&&optimized.accept);
assert.equal(base.checks,30714);assert.equal(optimized.checks,30714);
const hostiles=[];
let x=clone(out);[x.fixtures[0].proof[0],x.fixtures[0].proof[1]]=[x.fixtures[0].proof[1],x.fixtures[0].proof[0]];
hostiles.push({test:'child_before_parent',...originalCLI(x)});
x=clone(out);x.fixtures[0].proof[0].parents[0]='not-a-source';
hostiles.push({test:'forged_parent',...originalCLI(x)});
x=clone(out);x.fixtures[0].proof.at(-1).row.rhs^=1;
hostiles.push({test:'forged_terminal',...originalCLI(x)});
assert(hostiles.every(x=>!x.accept));
console.log(JSON.stringify({tag:'LSPV-4/573',date_local:'2026-11-12 17:36 PST',
 scope:'seven separate archived /341 SOURCE/AND3/XOR fixed proof trees; two atomic paid-result slots, read-only SOURCE, no recomputation',
 cost:'byte length of compact JSON.stringify(original paid inference record), after-step retained-weight area',
 warning:'NOT physical RAM, NOT historical complete R_mix341, NOT all-proof lower bound',
 original_cli:base,reordered_cli:optimized,hostiles,compact_packet_bytes:77714,
 rows,P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',P2_B2_B3:'OPEN',P_vs_NP:'OPEN'},null,2));

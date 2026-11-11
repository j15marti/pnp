'use strict';
/* LSPV-4/548. Exact fixed-62-RES-DAG in-place last-use resource audit.
 * Run at j15marti/pnp checkout root:
 * node experiments/arc/lspv4_548_inplace_register_exact.cjs
 * Or without checkout, using embedded independently checked incidence:
 * node experiments/arc/lspv4_548_inplace_register_exact.cjs --incidence-only
 * Authoritative /386 checker is invoked as an OS subprocess in checkout mode.
 * Slots hold complete signed clause values, NOT physical bit-addressed RAM.
 */
const fs = require('fs');
const crypto = require('crypto');
const cp = require('child_process');
const path = require('path');
const os = require('os');
const assert = require('assert').strict;
const DEP = [[],[0],[0],[1],[2],[],[5],[5],[6],[4,8],[9],[7],[3,11],[12],[],[14],[15],[14],[17],[],[19],[19],[21],[22,18],[23],[13,24],[20],[26,16],[27],[28,10],[25,29],[],[31],[],[33],[34,32],[35],[],[37],[],[39],[40,38],[41],[42,36],[43],[],[45],[],[47],[46,48],[49],[],[51],[],[53],[54,52],[55],[50,56],[57],[44,58],[59,30],[60]];
const ORDER = [...Array.from({length:21},(_,i)=>i),26,27,21,22,23,24,25,...Array.from({length:34},(_,i)=>28+i)];
const SEED = 'results/raw/arc/2026-11-11_0936_LSPV4_546_AREA_SCHEDULE_ACCEPTED.json';
const NEW = 'results/raw/arc/2026-11-11_1136_LSPV4_548_INPLACE_BYTE_SAFE_ACCEPTED.json';
const CHECKER = 'experiments/arc/lspv2_386_independent_verify.js';
const SHA_SEED = '0a428dc5afa7154cad3ae9a1f7816eb285d7a6b9';
const SHA_CHECKER = '338305c0ce101704205e57543756b8127074a986';
const shaGit = b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const n=DEP.length, bits=DEP.map((_,i)=>1n<<BigInt(i)), all=(1n<<BigInt(n))-1n;
const pred=DEP.map(v=>v.reduce((m,i)=>m|bits[i],0n));
const succ=Array(n).fill(0n);
for (let i=0;i<n;i++)for (const j of DEP[i])succ[j]|=bits[i];
function live(mask) {
  const un=all^mask;let c=0;
  for (let i=0;i<n;i++)if ((mask&bits[i]) && (succ[i]&un))c++;
  return c;
}
function overwritable(mask,i,rows,byteLimit) {
  const remaining=all^mask;
  return DEP[i].filter(j=>(succ[j]&remaining)===bits[i] &&
     (!byteLimit || JSON.stringify(rows[j].c).length>=JSON.stringify(rows[i].c).length));
}
function plan(order, rows) {
  let mask=0n,peakFresh=0,peakInPlace=0,peakByteSafe=0,any=0,nonexp=0;
  const trace=[];
  for (const i of order) {
    assert(!(pred[i]&~mask),'forward paid dependency at '+i);
    const l=live(mask), reusable=overwritable(mask,i,rows,false);
    const safe=overwritable(mask,i,rows,true);
    const freshness=l+1, inplace=l+(reusable.length?0:1), noExpand=l+(safe.length?0:1);
    peakFresh=Math.max(peakFresh,freshness);
    peakInPlace=Math.max(peakInPlace,inplace);
    peakByteSafe=Math.max(peakByteSafe,noExpand);
    any+=Number(reusable.length>0);nonexp+=Number(safe.length>0);
    trace.push({id:i,liveBefore:l,reuseLastParent:safe.length?safe[0]:null,
      temporaryPeakByteSafe:noExpand});
    mask|=bits[i];
  }
  assert(mask===all);
  return {peakFresh,peakInPlace,peakByteSafe,any,nonexp,trace};
}
function bfs(cap) {
  const q=[0n],seen=new Set(q);let head=0,edges=0,maxCompleted=0;
  while(head<q.length){
    const m=q[head++],p=m.toString(2).replace(/0/g,'').length;
    maxCompleted=Math.max(maxCompleted,p);
    if(m===all)return {cap,reached:true,visited:seen.size,edges,maxCompleted};
    const l=live(m);
    for(let i=0;i<n;i++){
      if((m&bits[i])||(pred[i]&~m)||l+Number(!overwritable(m,i,null,false).length)>cap)continue;
      const next=m|bits[i];edges++;
      if(!seen.has(next)){seen.add(next);q.push(next);}
    }
  }
  return {cap,reached:false,visited:seen.size,edges,maxCompleted};
}
function readPinned(file,sha){
  const b=fs.readFileSync(file);assert.equal(shaGit(b),sha,'Git blob mismatch: '+file);
  return JSON.parse(b.toString('utf8'));
}
function checkPacket(p){
  assert.equal(p.records.length,103);
  assert.equal(p.summary.source,41);assert.equal(p.summary.resolution,62);
  assert.equal(p.gate_defs.length,1);assert.equal(p.summary.paid_total,63);
  const clause=a=>[...new Set(a)].sort((u,v)=>Math.abs(u)-Math.abs(v)||u-v);
  for(let i=0;i<p.records.length;i++){
    const r=p.records[i];if(i<41){assert.equal(r.kind,'SOURCE');continue;}
    assert.equal(r.kind,'RES');assert.equal(r.parents.length,2);
    const [j,k]=r.parents;assert(j<i&&k<i,'chronology '+i);
    const A=p.records[j].c,B=p.records[k].c,v=r.pivot;
    assert(A.includes(v)&&B.includes(-v),'signed pivot '+i);
    const out=clause([...A.filter(z=>z!==v),...B.filter(z=>z!==-v)]);
    assert.deepEqual(out,r.c,'resolvent '+i);assert(!out.some(z=>out.includes(-z)));
  }
  assert.deepEqual(p.records.at(-1).c,[]);
  return p.records.slice(41);
}
function main(){
  const none=Array.from({length:n},()=>({c:[]}));
  assert.equal(n,62);assert.equal(new Set(ORDER).size,62);
  const exact=bfs(5);
  assert.deepEqual({reached:exact.reached,visited:exact.visited,edges:exact.edges,maxCompleted:exact.maxCompleted},
      {reached:false,visited:185340,edges:725941,maxCompleted:48});
  const base={version:'LSPV-4/548',claim:'Exact six whole-clause slots for fixed 62-RES DAG, last-use in-place with no recomputation',
    status:'PROVED/RESTRICTED + COMPUTATIONAL',nativeWork:63,RES:62,SOURCE:41,
    certifiedNoFiveAnyReuse:exact,thereforeNoFiveByteSafe:true};
  if(process.argv.includes('--incidence-only')){
    console.log(JSON.stringify({...base,note:'No original packet or original checker OS replay in incidence-only mode'},null,2));
    return;
  }
  const seed=readPinned(SEED,SHA_SEED);
  const witness=JSON.parse(fs.readFileSync(NEW,'utf8'));
  const source=checkPacket(seed),target=checkPacket(witness);
  const dep=source.map(r=>r.parents.filter(j=>j>=41).map(j=>j-41));
  assert.deepEqual(dep,DEP,'incidence changed');
  const ordIndex=new Map(ORDER.map((v,i)=>[v,41+i]));
  assert.deepEqual(target,ORDER.map(i=>({...source[i],parents:source[i].parents.map(j=>j<41?j:ordIndex.get(j-41))})));
  assert.deepEqual(witness.records.slice(0,41),seed.records.slice(0,41));
  assert.deepEqual(witness.spec,seed.spec);assert.deepEqual(witness.gate_defs,seed.gate_defs);
  const area=plan([...Array(n).keys()],source),newPlan=plan(ORDER,source);
  assert.equal(area.peakFresh,7);assert.equal(area.peakByteSafe,7);
  assert.equal(newPlan.peakFresh,7);assert.equal(newPlan.peakInPlace,6);
  assert.equal(newPlan.peakByteSafe,6);
  assert.equal(newPlan.nonexp,36);
  const checkerRaw=fs.readFileSync(CHECKER);
  assert.equal(shaGit(checkerRaw),SHA_CHECKER,'original checker altered');
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-548-'));
  let checkerSummary=[];
  try {
    const f=path.join(temp,'witness.json');fs.writeFileSync(f,JSON.stringify(witness)+'\n');
    const stdout=cp.execFileSync(process.execPath,[CHECKER,f],{encoding:'utf8'});
    checkerSummary=stdout.trim().split('\n').map(s=>JSON.parse(s));
    assert.equal(checkerSummary[0].paid,63);assert.equal(checkerSummary[0].negativeTests,11);
  } finally {fs.rmSync(temp,{recursive:true,force:true});}
  console.log(JSON.stringify({...base,area:{fresh:area.peakFresh,byteSafe:area.peakByteSafe},
    reordered:{fresh:newPlan.peakFresh,any:newPlan.peakInPlace,byteSafe:newPlan.peakByteSafe,
      lastUseReuses:newPlan.any,byteSafeLastUseReuses:newPlan.nonexp,order:ORDER},
    originalCheckerOS:checkerSummary},null,2));
}
main();

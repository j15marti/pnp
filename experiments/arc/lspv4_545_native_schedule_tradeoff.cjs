'use strict';
/*
 * LSPV-4/545: exact /386 accepted native DAG rescheduling and recomputation audit.
 * Run in the j15marti/pnp checkout:
 *     node experiments/arc/lspv4_545_native_schedule_tradeoff.cjs
 *     node experiments/arc/lspv4_545_native_schedule_tradeoff.cjs --write
 * No dependencies beyond Node.js >=18. Read-only original checker subprocess.
 */
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto'),cp=require('child_process'),assert=require('assert');
const ROOT=path.resolve(__dirname,'../..');
const ORIGINAL='results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_PACKET.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const EXPECTED_ORIGINAL='1efb525f0c84dfffb626c00e592f4952cc796c69';
const EXPECTED_CHECKER='338305c0ce101704205e57543756b8127074a986';
const OUT_REORDER='results/raw/arc/2026-11-11_0836_LSPV4_545_REORDERED_BRIDGE_ACCEPTED.json';
const OUT_UNFOLD='results/raw/arc/2026-11-11_0836_LSPV4_545_UNFOLDED_BRIDGE_ACCEPTED.json';
const OUT_SUMMARY='results/raw/arc/2026-11-11_0836_LSPV4_545_NATIVE_SCHEDULE_TRADEOFF_RAW.json';
function blobSha(s){const b=Buffer.from(s,'utf8');return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');}
function clone(x){return JSON.parse(JSON.stringify(x));}
function resource(rows) {
 const uses=rows.map(()=>0);
 for(const row of rows)for(const p of row.parents)uses[p]++;
 const live=new Set(); let peak=0,literals=0,area=0,postPeak=0;
 for(let i=0;i<rows.length;i++){
  const row=rows[i];
  if(row.kind==='RES'){
   peak=Math.max(peak,live.size+1);
   let k=row.c.length;
   for(const j of live)k+=rows[j].c.length;
   literals=Math.max(literals,k);
  }
  if(row.kind==='RES'&&uses[i]>0)live.add(i);
  for(const p of row.parents){uses[p]--;if(uses[p]===0)live.delete(p);}
  area+=live.size;postPeak=Math.max(postPeak,live.size);
 }
 return {freshPeakPaidSlots:peak,peakLiteralSlots:literals,retainedSlotSteps:area,maxPostStepPaidSlots:postPeak};
}
function schedule(base){
 const R=base.records,n=R.length,S=[],P=[],children=R.map(()=>[]);
 for(let i=0;i<n;i++){if(R[i].kind==='SOURCE')S.push(i);else if(R[i].kind==='RES')P.push(i);for(const p of R[i].parents)children[p].push(i);}
 let seed=424242;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
 function attempt(wa,wb,wc,noise){
  const rem=R.map(r=>r.kind==='RES'?r.parents.filter(j=>R[j].kind==='RES').length:0);
  const use=children.map(c=>c.length),ready=P.filter(i=>rem[i]===0),live=new Set(),order=[...S];
  while(ready.length){
   let bj=-1,best=Infinity;
   for(let j=0;j<ready.length;j++){
    const i=ready[j],pars=R[i].parents.filter(p=>R[p].kind==='RES');
    const free=pars.filter(p=>use[p]===1).length,degree=children[i].length;
    const price=live.size+1-free+(degree?1:0);
    const score=wa*price+wb*degree+wc*(i/R.length)+(noise?noise*(rand()-.5):0);
    if(score<best){best=score;bj=j;}
   }
   const i=ready.splice(bj,1)[0];order.push(i);
   if(children[i].length)live.add(i);
   for(const p of R[i].parents){use[p]--;if(!use[p])live.delete(p);}
   for(const c of children[i])if(R[c].kind==='RES'&&--rem[c]===0)ready.push(c);
  }
  return order;
 }
 let bestOrder=null,best={freshPeakPaidSlots:Infinity,retainedSlotSteps:Infinity},bestTrial=-1;
 for(let t=0;t<20000;t++){
  const order=attempt(.1+5*rand(),-3+6*rand(),-5+10*rand(),8*rand());
  assert.equal(order.length,n);
  assert.equal(order[order.length-1],n-1);
  const inv=new Map(order.map((i,j)=>[i,j]));
  const rows=order.map(i=>({...R[i],parents:R[i].parents.map(p=>inv.get(p))}));
  for(let k=0;k<rows.length;k++)for(const p of rows[k].parents)assert(p<k);
  const m=resource(rows);
  if(m.freshPeakPaidSlots<best.freshPeakPaidSlots||(m.freshPeakPaidSlots===best.freshPeakPaidSlots&&m.retainedSlotSteps<best.retainedSlotSteps)){
   best=m;bestOrder=order;bestTrial=t;
  }
 }
 const inv=new Map(bestOrder.map((i,j)=>[i,j]));
 return {packet:{...base,records:bestOrder.map(i=>({...R[i],parents:R[i].parents.map(p=>inv.get(p))}))},bestTrial,bestOrder};
}
function unfold(base){
 const old=base.records,n=old.length,dp=[];
 for(let i=0;i<n;i++){
  const row=old[i];if(row.kind!=='RES'){dp.push({min:0,first:0});continue;}
  const [a,b]=row.parents,cA=old[a].kind==='RES'?1:0,cB=old[b].kind==='RES'?1:0;
  const opPeak=1+cA+cB;
  const ab=Math.max(dp[a].min,cA+dp[b].min,opPeak),ba=Math.max(dp[b].min,cB+dp[a].min,opPeak);
  dp.push({min:Math.min(ab,ba),first:ab<=ba?0:1});
 }
 const rows=old.filter(r=>r.kind==='SOURCE').map(r=>({...r,parents:[]}));
 function emit(i){
  const r=old[i];if(r.kind!=='RES')return i; const order=dp[i].first?[1,0]:[0,1],pars=[];
  for(const k of order)pars[k]=emit(r.parents[k]);
  const j=rows.length;rows.push({...r,parents:pars});return j;
 }
 emit(n-1);
 const resolution=rows.filter(r=>r.kind==='RES').length;
 const packet={...base,records:rows,summary:{...base.summary,resolution,paid_total:resolution+base.gate_defs.length,live_records:rows.length}};
 return {packet,expressionMinPeak:dp[n-1].min};
}
function runChecker(checker,bytes,name){
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-545-'));
 try{
  const f=path.join(tmp,name+'.json');fs.writeFileSync(f,bytes);
  const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',maxBuffer:8*1024*1024});
  return {accept:r.status===0,status:r.status,stdout:r.stdout,stderr:r.stderr};
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
function main(){
 const text=fs.readFileSync(path.join(ROOT,ORIGINAL),'utf8');
 const checker=path.join(ROOT,CHECKER),source=fs.readFileSync(checker,'utf8');
 assert.strictEqual(blobSha(text),EXPECTED_ORIGINAL,'original packet was modified');
 assert.strictEqual(blobSha(source),EXPECTED_CHECKER,'original checker was modified');
 const base=JSON.parse(text),opt=schedule(base),unfolded=unfold(base);
 const packets=[base,opt.packet,unfolded.packet],names=['original','reordered','unfolded'];
 const nativeChecks=[];
 for(let i=0;i<3;i++){
  const result=runChecker(checker,JSON.stringify(packets[i]),names[i]);
  assert(result.accept,names[i]+' native checker rejected: '+result.stderr);
  nativeChecks.push(JSON.parse(result.stdout.trim().split('\n').at(-1)));
 }
 const bad=[];
 function reject(label,mutated){
  const r=runChecker(checker,JSON.stringify(mutated),label);
  assert(!r.accept,'false acceptance of '+label);bad.push(label);
 }
 let v=clone(opt.packet);v.summary.paid_total++;reject('wrong-paid-total',v);
 v=clone(opt.packet);v.records.at(-1).pivot=999999;reject('wrong-terminal-pivot',v);
 v=clone(opt.packet);v.records[0].c=[0];reject('invalid-signed-SOURCE',v);
 v=clone(opt.packet);v.records.at(-1).parents[0]=v.records.length+1;reject('forward-parent',v);
 v={...base,records:opt.bestOrder.map(i=>({...base.records[i]}))};reject('unmapped-topological-parents',v);
 const sourceUnchanged=JSON.stringify(base.records.filter(x=>x.kind==='SOURCE'))===JSON.stringify(opt.packet.records.filter(x=>x.kind==='SOURCE'));
 assert(sourceUnchanged,'original signed source modified');
 for(const p of packets){assert.equal(p.records.at(-1).c.length,0);assert.equal(p.summary.paid_total,p.summary.resolution+p.summary.paid_gates);}
 const res=base.records,visits=Array(res.length).fill(0n);visits.at(-1);visits[visits.length-1]=1n;
 for(let i=res.length-1;i>=0;i--)for(const j of res[i].parents)visits[j]+=visits[i];
 const resVisits=visits.reduce((s,x,i)=>s+(res[i].kind==='RES'?x:0n),0n);
 const srcVisits=visits.reduce((s,x,i)=>s+(res[i].kind==='SOURCE'?x:0n),0n);
 assert.equal(Number(resVisits),unfolded.packet.summary.resolution);
 const entries=packets.map((p,i)=>({name:names[i],work:p.summary.paid_total,source:p.summary.source,resolution:p.summary.resolution,owners:p.summary.paid_gates,records:p.records.length,parentReferences:2*p.summary.resolution,compactBytes:Buffer.byteLength(JSON.stringify(p)),resource:resource(p.records),checker:{paid:nativeChecks[i].paid,assertions:nativeChecks[i].assertions,negativeTests:nativeChecks[i].negativeTests}}));
 assert.equal(entries[0].resource.freshPeakPaidSlots,33);assert.equal(entries[1].resource.freshPeakPaidSlots,14);assert.equal(entries[2].resource.freshPeakPaidSlots,8);
 const summary={scope:'archived /386 only; not historical R_mix341',proofStatus:'PROVED/RESTRICTED+COMPUTATIONAL',datePST:'2026-11-11 08:36',pinnedBlobs:{originalPacket:EXPECTED_ORIGINAL,originalChecker:EXPECTED_CHECKER},search:{trials:20000,seed:424242,bestTrial:opt.bestTrial,bestOrderOriginalRecordIDs:opt.bestOrder},unfolding:{expressionMinPeak:unfolded.expressionMinPeak,resolutionOccurrences:resVisits.toString(),sourceRetrievals:srcVisits.toString()},entries,hostileRejections:bad,hostedV8Note:'Separate hosted-V8 original-body replay in role report; this Node runner uses real OS subprocesses.'};
 if(process.argv.includes('--write')){fs.writeFileSync(path.join(ROOT,OUT_REORDER),JSON.stringify(opt.packet));fs.writeFileSync(path.join(ROOT,OUT_UNFOLD),JSON.stringify(unfolded.packet));fs.writeFileSync(path.join(ROOT,OUT_SUMMARY),JSON.stringify(summary,null,2)+'\n');}
 process.stdout.write(JSON.stringify(summary,null,2)+'\n');
}
main();

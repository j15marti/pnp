'use strict';
/* LSPV-4/547. Exact fixed-DAG, one-shot fresh-result register peak.
 * This executable reads the *unchanged* published original-/386-accepted
 * certificates in a checkout. It does not reconstruct missing R_mix341 rules.
 * Run: node experiments/arc/lspv4_547_exact_bridge_fresh_slot.cjs
 */
function analyze(base,area,lit) {
  function checkPacket(p,label) {
    const R=p.records; if(R.length!==103||p.gate_defs.length!==1)throw Error(label+': record/owner count');
    if(p.summary.source!==41||p.summary.resolution!==62||p.summary.paid_total!==63)throw Error(label+': incorrect tariff');
    const canonical=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
    let src=0,res=0;const depths=[];
    for(let i=0;i<R.length;i++){
      const r=R[i];if(r.kind==='SOURCE'){src++;if(r.parents.length)throw Error('source parents');depths.push(0);continue;}
      if(r.kind!=='RES'||r.parents.length!==2)throw Error(label+': non RES');
      res++;
      const [j,k]=r.parents;if(j>=i||k>=i||j<0||k<0)throw Error('parent chronology');
      const [a,b]=[R[j].c,R[k].c];
      if(!a.includes(r.pivot)||!b.includes(-r.pivot))throw Error('oriented pivot');
      const out=canonical([...a.filter(v=>v!==r.pivot),...b.filter(v=>v!==-r.pivot)]);
      if(out.length!==r.c.length||out.some((v,t)=>v!==r.c[t]))throw Error('resolvent');
      depths.push(1+Math.max(depths[j],depths[k]));
    }
    if(src!==41||res!==62||R.at(-1).kind!=='RES'||R.at(-1).c.length)throw Error('terminal/source counts');
    const resRows=R.map((r,i)=>({r,i})).filter(v=>v.r.kind==='RES');
    const local=new Map(resRows.map((v,i)=>[v.i,i])),n=resRows.length;
    const dep=resRows.map(v=>v.r.parents.filter(j=>local.has(j)).map(j=>local.get(j)));
    const bits=dep.map((_,i)=>1n<<BigInt(i)),full=(1n<<BigInt(n))-1n;
    const pre=dep.map(d=>d.reduce((m,j)=>m|bits[j],0n));
    const succ=Array(n).fill(0n);
    for(let i=0;i<n;i++)for(const j of dep[i])succ[j]|=bits[i];
    const live=mask=>{let q=0,missing=full^mask;for(let i=0;i<n;i++)if((mask&bits[i])&&(succ[i]&missing))q++;return q;};
    let mask=0n,peak=0,post=0;
    for(let i=0;i<n;i++){
      if(pre[i]&~mask)throw Error('internal topological index');
      peak=Math.max(peak,1+live(mask));
      mask|=bits[i];post=Math.max(post,live(mask));
    }
    return {label,peakFreshPaidSlots:peak,peakAfterOnlySlots:post,span:depths.at(-1),dep,pre,succ,bits,full,live};
  }
  const a=checkPacket(area,'area546'),b=checkPacket(base,'base575'),c=checkPacket(lit,'literal546');
  if(a.peakFreshPaidSlots!==7||b.peakFreshPaidSlots!==10||c.peakFreshPaidSlots!==7)
    throw Error('published schedule mismatch');
  const src=p=>JSON.stringify(p.records.filter(r=>r.kind==='SOURCE').map(r=>[r.source,r.c]).sort((u,v)=>JSON.stringify(u).localeCompare(JSON.stringify(v))));
  if(src(base)!==src(area)||src(area)!==src(lit))throw Error('signed SOURCE mismatch');
  if(JSON.stringify(base.spec)!==JSON.stringify(area.spec)||JSON.stringify(base.gate_defs)!==JSON.stringify(area.gate_defs))throw Error('spec/owner mismatch');
  const {pre,succ,bits,full,live}=a,n=bits.length;
  function enumerateBreadthFirst(maxPeak) {
    const seen=new Set([0n]),q=[0n],levels=Array(n+1).fill(0);
    let transitions=0,dead=0,reached=false;
    for(let head=0;head<q.length;head++){
      const mask=q[head];levels[mask.toString(2).replace(/0/g,'').length]++;
      if(mask===full){reached=true;break;}
      if(1+live(mask)>maxPeak){dead++;continue;}
      for(let i=0;i<n;i++){
        if((mask&bits[i])||(pre[i]&~mask))continue;
        const next=mask|bits[i];transitions++;
        if(!seen.has(next)){seen.add(next);q.push(next);}
      }
    }
    return {maxPeak,reached,visited:seen.size,legalTransitionTraversals:transitions,unextendableAtPeak:dead,maxCompletedNodes:levels.findLastIndex(v=>v>0),levels};
  }
  function enumerateDepthFirst(maxPeak) {
    const seen=new Set(),path=[];let found=false;
    function dfs(mask){
      if(mask===full){found=true;return;}
      if(seen.has(mask))return;seen.add(mask);
      const l=live(mask);if(1+l>maxPeak)return;
      for(let i=0;i<n&&!found;i++){
        if((mask&bits[i])||(pre[i]&~mask))continue;
        const next=mask|bits[i];if(next!==full&&1+live(next)>maxPeak)continue;
        dfs(next);
      }
    }
    dfs(0n);return {maxPeak,reached:found,visited:seen.size};
  }
  const bfs6=enumerateBreadthFirst(6),dfs6=enumerateDepthFirst(6);
  if(bfs6.reached||dfs6.reached||bfs6.visited!==770940||bfs6.maxCompletedNodes!==49)
    throw Error('6-slot exhaustion differs from independently established control');
  const cap5=enumerateDepthFirst(5);if(cap5.reached)throw Error('5-slot path found');
  // A deliberately wrong after-only ledger misses the fresh output slot.
  if(a.peakAfterOnlySlots!==6)throw Error('fresh-before-release falsifier changed');
  return {claim:'Exact optimum peak=7 for permutations of THIS 62-RES DAG only',
    status:'PROVED/RESTRICTED + COMPUTATIONAL',
    scopedModel:'read-only 41 SOURCE; one globally paid dead AND2 owner; 62 RES; fresh non-overwriting paid result before last-use release; no recompute',
    nodeCount:n,sourceCount:41,gateOwners:1,nativeWork:63,
    base575:{freshPeak:b.peakFreshPaidSlots,afterOnlyPeak:b.peakAfterOnlySlots,span:b.span},
    area546:{freshPeak:a.peakFreshPaidSlots,afterOnlyPeak:a.peakAfterOnlySlots,span:a.span},
    literal546:{freshPeak:c.peakFreshPaidSlots,afterOnlyPeak:c.peakAfterOnlySlots,span:c.span},
    completeNo6:bfs6,independentNo6:dfs6,independentNo5:cap5,
    lowerBoundFreshSlots:7,upperBoundAcceptedSchedule:7,
    auditedBoundary:['The original /386 checker previously ACCEPTED the exact published packets; this script independently rechecks strict oriented Resolution, not the original executable.',
    'The lower bound is fixed DAG and fixed allocation/retrieval rules only, not the minimum across different legal proofs or R_mix341.',
    'The source is an authenticated internal signed SOURCE packet, not independently bound to an external DIMACS input.',
    'GF(2), AND3, LOCAL-CONVERT, branching, contexts and discharge are not recognized by this archived checker.']
  };
}
if(typeof require==='function'&&typeof module==='object'&&require.main===module){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'../..');
 const paths={
 base:'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json',
 area:'results/raw/arc/2026-11-11_0936_LSPV4_546_AREA_SCHEDULE_ACCEPTED.json',
 lit:'results/raw/arc/2026-11-11_0936_LSPV4_546_LITERAL_SCHEDULE_ACCEPTED.json'};
 const pins={base:'d5de0f477cd736ec5fd7b01be18350f9cb594fd2',
 area:'0a428dc5afa7154cad3ae9a1f7816eb285d7a6b9'};
 const read=(k)=>{const bytes=fs.readFileSync(path.join(root,paths[k]));
 const digest=crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'),bytes])).digest('hex');
 if(pins[k]&&digest!==pins[k])throw Error(k+': mismatched Git blob SHA '+digest);
 return JSON.parse(bytes.toString('utf8'));};
 console.log(JSON.stringify(analyze(read('base'),read('area'),read('lit')),null,2));
}

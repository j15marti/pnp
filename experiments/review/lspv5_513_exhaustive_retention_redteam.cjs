'use strict';
// LSPV-5/513 red team: exhaustive downset DP over ALL no-recomputation topological
// orders of each original /341 fixture tree with V<=VMAX. Independent of LSPV-4/572's
// Sethi-Ullman construction: it does not use the claimed schedule or proof.
// Usage (repo root): node experiments/review/lspv5_513_exhaustive_retention_redteam.cjs [fixtureIndex]
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const BASE='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const buf=fs.readFileSync(BASE);
const sha=crypto.createHash('sha1').update('blob '+buf.length+'\0').update(buf).digest('hex');
assert.equal(sha,'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const packet=JSON.parse(buf.toString('utf8'));
const VMAX=10;
const only=process.argv[2]===undefined?null:Number(process.argv[2]);
function dp(f){
  const ids=f.proof.map(p=>p.id), n=ids.length, idx=new Map(ids.map((x,i)=>[x,i]));
  const par=f.proof.map(p=>p.parents.filter(q=>idx.has(q)).map(q=>idx.get(q)));
  const cons=new Array(n).fill(-1); par.forEach((ps,i)=>ps.forEach(q=>{assert.equal(cons[q],-1);cons[q]=i;}));
  // state: BigInt mask of computed paid nodes. live(i) iff computed and consumer not computed.
  const B=i=>1n<<BigInt(i);
  let layer=new Map([[0n,{area:0,peak:0,areaCap2:0,peakOK:true}]]);
  // For each state keep (minArea over all orders), (minArea over orders with peak<=2), and min peak.
  layer=new Map([[0n,{a:0,a2:0,pk:0}]]);
  let states=1;
  for(let step=0;step<n;step++){
    const next=new Map();
    for(const [m,v] of layer){
      for(let i=0;i<n;i++){
        if(m&B(i))continue;
        if(!par[i].every(q=>m&B(q)))continue;
        const m2=m|B(i);
        let live=0; for(let j=0;j<n;j++) if((m2&B(j))&&!(cons[j]>=0&&(m2&B(cons[j])))) live++;
        // transient: inputs read then output overwrites a dying paid parent; if no paid parent, +1 slot
        let liveBefore=0; for(let j=0;j<n;j++) if((m&B(j))&&!(cons[j]>=0&&(m&B(cons[j])))) liveBefore++;
        const tr=liveBefore+(par[i].length===0?1:0);
        const a=v.a+live, pk=Math.max(v.pk,tr);
        const a2=(v.a2!==Infinity&&tr<=2)?v.a2+live:Infinity;
        const o=next.get(m2);
        if(!o) next.set(m2,{a,a2,pk});
        else {o.a=Math.min(o.a,a);o.a2=Math.min(o.a2,a2);o.pk=Math.min(o.pk,pk);}
      }
    }
    layer=next; states+=next.size;
  }
  assert.equal(layer.size,1);
  const [r]=layer.values();
  return {graph:f.graph.name,V:f.graph.n,paid:n,downset_states:states,min_area_all_orders:r.a,min_area_peak_le_2:r.a2,min_peak:r.pk,claimed:7*f.graph.n-4};
}
const out=[];
packet.fixtures.forEach((f,k)=>{ if(only!==null&&k!==only)return; if(f.graph.n>VMAX){out.push({graph:f.graph.name,V:f.graph.n,skipped:'V>'+VMAX});return;}
  const t=Date.now(); const r=dp(f); r.ms=Date.now()-t; out.push(r);});
console.log(JSON.stringify(out));

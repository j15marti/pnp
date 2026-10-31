"use strict";
function rebuild(q,b){
  let C=[],t=1,p=2,at=3,dt=4,ap=5,dp=6,f=[7,8,9],z=Array.from({length:q},(_,j)=>10+j),nv=9+q;
  const G=(L,a,d)=>{for(const x of [-1,1])for(const y of [-1,1])C.push([L,x*a,y*d]);};
  G(t,at,dt);G(-p,ap,dp);
  for(let j=0;j<q;j++)C.push([b[j]?t:-t,-z[j],p]);
  if(q===3)C.push(z.slice());else{
    let y=Array.from({length:q-3},(_,j)=>nv+j+1);
    nv+=q-3;C.push([z[0],z[1],y[0]]);
    for(let i=0;i<q-4;i++)C.push([-y[i],z[i+2],y[i+1]]);
    C.push([-y[q-4],z[q-2],z[q-1]]);
  }
  for(let j=0;j<Math.ceil(q**(5/3));j++)C.push(f.slice());
  return {C,nv};
}
function count(C,a){return C.map(c=>c.filter(l=>a[Math.abs(l)]===(l>0?1:0)).length);}
function hist(t){return [0,1,2,3].map(k=>t.filter(x=>x===k).length);}
function extreme(C){
  let z=[0,0,0,0],none=0;
  for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){
    let pos=false,neg=false;
    for(const u of C[i])for(const v of C[j])if(u===v)pos=true;else if(u===-v)neg=true;
    if(!neg){z[0]++;z[3]++}
    if(!pos){z[1]++;z[2]++}
    if(pos&&neg)none++;
  }
  return {z,none};
}
function verify(raw){
  let n=0,pairs=0,assignments=0,bytes=0;
  if(raw.schema!=="ARC-BOUNDED-GUEST-INPUT273")throw Error("schema");
  for(const r of raw.cases){
    n++;const b=Array.from({length:r.q},(_,j)=>r.variant==="allzero"?0:r.variant==="lastone"?(j===r.q-1?1:0):j%2);
    const {C,nv}=rebuild(r.q,b);
    if(C.length!==r.sourceDiagnostics.clauses)throw Error("clauses");
    let a0=Array(nv+1).fill(0),a1=Array(nv+1).fill(1),T0=count(C,a0),T1=count(C,a1);
    if(JSON.stringify(hist(T0))!==JSON.stringify(r.sourceDiagnostics.endpoint0)||JSON.stringify(hist(T1))!==JSON.stringify(r.sourceDiagnostics.endpoint1))throw Error("endpoints");
    T0.forEach((x,i)=>{if(x+T1[i]!==3)throw Error("complement");});
    let pair=extreme(C);pairs+=C.length*(C.length-1)/2*4;
    if(JSON.stringify(pair.z)!==JSON.stringify(r.sourceDiagnostics.extremeModes)||pair.none!==r.sourceDiagnostics.noExtremePairs)throw Error("pair");
    let flip=a1.slice();
    for(let i=1;i<=Math.min(4,nv);i++){flip[i]^=1;if(JSON.stringify(hist(count(C,flip)))!==JSON.stringify(r.sourceDiagnostics.flipTrail[i-1].hist))throw Error("flip");}
    const summarySat=b.includes(1);
    if(r.sourceSAT!==summarySat||r.children.length!==r.q)throw Error("source label");
    if(r.q<=4){
      let sat=false;
      for(let mask=0;mask<2**nv;mask++){
        assignments++;let a=Array.from({length:nv+1},(_,j)=>j===0?0:(mask>>(j-1))&1);
        if(count(C,a).every(x=>x>0))sat=true;
      }
      if(sat!==summarySat)throw Error("enumerated SAT");
    }
    for(let j=0;j<r.q;j++){
      let c=r.children[j];if(c.j!==j||c.sourcePin!==b[j]||c.guestSAT!==!!b[j])throw Error("child bit");
      if(c.trace.guestIndexedJumps<1||c.trace.hostInputBufferReads<c.childChars||c.trace.hostIndexCellClears<=0)throw Error("trace");
      if(c.trace.peakBufferCells!==c.childChars)throw Error("buffer");
      if(c.trace.hostIndexCellClears!==c.trace.guestIndexedJumps*Math.ceil(Math.log2(2*c.childChars+4)))throw Error("erasure tariff");
      bytes+=c.trace.hostInputBufferReads;
    }
    if(r.chargedController.childCharactersOutput!==r.children.reduce((s,c)=>s+c.childChars,0))throw Error("output");
    if(r.chargedController.peakLiveChildBuffer!==Math.max(...r.children.map(c=>c.childChars)))throw Error("peak");
  }
  if(n!==12||raw.checks.childLabels!==93||bytes!==raw.checks.byteReads)throw Error("aggregate");
  return {pass:true,case_count:n,child_count:raw.checks.childLabels,complement_checks:raw.cases.reduce((s,r)=>s+r.sourceDiagnostics.clauses,0),
    original_pair_modes_checked:pairs,complete_assignments_evaluated:assignments,guest_input_reads_checked:bytes};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");const raw=JSON.parse(fs.readFileSync(process.argv[2]||"results/raw/arc/2026-10-31_0606_LSPV4_ARC_BOUNDED_GUEST273_raw.json","utf8"));
 process.stdout.write(JSON.stringify(verify(raw),null,2)+"\n");
}

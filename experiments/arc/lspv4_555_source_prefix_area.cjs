'use strict';
// LSPV-4/555 independent source-order resource audit for original /386 grammar.
// Usage: node experiments/arc/lspv4_555_source_prefix_area.cjs [--os]
// Requires unmodified published W29 seed and original /386 checker in the repo.
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_1734_LSPV4_554_W29_SOURCE_QUOTIENT_ACCEPTED.json');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
function assert(b,m){if(!b)throw Error(m)}
function fresh(t){
 assert(Number.isSafeInteger(t)&&t>=1&&6*t+3<Number.MAX_SAFE_INTEGER,'unsafe t');
 const g=6*t+1;
 const edges=[];for(let j=0;j<t;j++)for(const [a,b] of [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])edges.push([4*j+a,4*j+b]);
 const shift=(x,j)=>x===0?0:Math.sign(x)*(Math.abs(x)===19?g:Math.abs(x)+(j>0?6*(j-1):0));
 const change=(r,j=0)=>{let q=clone(r);q.c=q.c.map(x=>shift(x,j));if(q.source>=4)q.source+=4*(j-1);if(q.pivot)q.pivot=shift(q.pivot,j);return q};
 const records=[...seed.records.slice(0,17).map(x=>change(x)),...seed.records.slice(17,44).map(x=>change(x))];
 for(let j=1;j<t;j++)records.push(...seed.records.slice(44,60).map(x=>change(x,j)));
 records.push(change(seed.records.at(-1)));
 const d={spec:{h:4*t,edges,charge:Array.from({length:4*t},(_,i)=>+(i===0)),guard:g},gate_defs:[[1,g+2,1,-1]],records,
 summary:{source:16*t+1,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:16*t+29}};
 if(t===3)assert(JSON.stringify(d)===JSON.stringify(seed),'failed exact W29 seed recreation');
 return d;
}
function sourceFirst(d){
 const order=d.records.map((r,i)=>r.kind==='SOURCE'?i:-1).filter(i=>i>=0)
 .concat(d.records.map((r,i)=>r.kind!=='SOURCE'?i:-1).filter(i=>i>=0));
 const renumber=new Map(order.map((original,newIndex)=>[original,newIndex]));
 const q=clone(d);q.records=order.map(i=>({...d.records[i],parents:d.records[i].parents.map(j=>renumber.get(j))}));
 return q;
}
function key(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function audit(d){
 assert(d.summary.paid_total===29&&d.gate_defs.length===1,'paid owner');
 const {h,edges,charge,guard}=d.spec;assert(h===4*(edges.length/6)&&charge.length===h,'source topology');
 let occ=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{occ[a].push(i+1);occ[b].push(i+1)});
 const expected=new Map();
 for(let v=0;v<h;v++){
  assert(occ[v].length===3,'not cubic');let clauses=new Set();
  for(let mask=0;mask<8;mask++){let bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
   if((bits[0]+bits[1]+bits[2])%2===charge[v])continue;
   clauses.add(JSON.stringify(key([...occ[v].map((x,j)=>bits[j]?-x:x),-guard])));
  }expected.set(v,clauses);
 }
 const seen=new Set(),known=[],last=new Map(),depth=[];
 d.records.forEach((r,i)=>r.parents.forEach(p=>last.set(p,i)));
 let live=new Set(),area=0,peak=0,res=0,refdigits=0,apps=0,digitcount=0;
 for(let i=0;i<d.records.length;i++){
  const r=d.records[i];assert(r.parents.every(p=>Number.isSafeInteger(p)&&p>=0&&p<i),'non-chronological reference');
  assert(JSON.stringify(r.c)===JSON.stringify(key(r.c)),'noncanonical clause');
  for(const p of r.parents){apps++;refdigits+=String(p).length}
  if(r.kind==='SOURCE'){
    assert(r.parents.length===0,'SOURCE with parent');
    if(r.source===-1)assert(JSON.stringify(r.c)===JSON.stringify([guard]),'guard mismatch');
    else assert(expected.has(r.source)&&expected.get(r.source).has(JSON.stringify(r.c)),'forged SOURCE');
    const sig=r.source+':'+JSON.stringify(r.c);assert(!seen.has(sig),'duplicate SOURCE');seen.add(sig);
    digitcount+=r.c.reduce((s,x)=>s+String(Math.abs(x)).length,0);depth[i]=0;
  }else{
    assert(r.kind==='RES'&&r.parents.length===2,'non-RES rule');res++;
    const [a,b]=r.parents.map(j=>known[j]),p=r.pivot;
    assert(a.includes(p)&&b.includes(-p),'wrong signed pivot');
    assert(JSON.stringify(key([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]))===JSON.stringify(r.c),'wrong resolvent');
    depth[i]=1+Math.max(...r.parents.map(j=>depth[j]));
    if(last.has(i))live.add(i);
  }
  known.push(r.c);peak=Math.max(peak,live.size);
  for(const p of r.parents)if(d.records[p].kind==='RES'&&last.get(p)===i)live.delete(p);
  area+=live.size;
 }
 assert(res===28&&apps===56&&seen.size===4*h+1,'count/arity/source binding');
 for(let [v,cls] of expected)for(let c of cls)assert(seen.has(v+':'+c),'missing mandatory SOURCE');
 assert(seen.has('-1:'+JSON.stringify([guard])),'missing guard');
 assert(known.at(-1).length===0,'missing empty goal');
 return {work:res+d.gate_defs.length,sources:seen.size,records:d.records.length,referenceApplications:apps,referenceDigits:refdigits,sourceLiteralDigits:digitcount,peakFreshResultSlots:peak,retainedResultSlotSteps:area,dependencySpan:Math.max(...depth),certificateBytes:Buffer.byteLength(JSON.stringify(d)+'\n')};
}
function verifyOS(packet,dir,label){
 const f=path.join(dir,label+'.json');fs.writeFileSync(f,JSON.stringify(packet)+'\n');
 try{const stdout=cp.execFileSync(process.execPath,[checkerPath,f],{encoding:'utf8',timeout:30000,stdio:['ignore','pipe','pipe']});
 return {accepted:true,checker:JSON.parse(stdout.trim()),packetSHA256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')};}
 catch(e){return {accepted:false,error:String(e.stderr||e.message).slice(0,350)}}
}
function main(){
 const runOS=process.argv.includes('--os'),temp=runOS?fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-555-')):null,rows=[];
 try{
 for(const t of [1,2,3,4,5,8,12,16,32,64]){
  const late=fresh(t),front=sourceFirst(late),l=audit(late),f=audit(front);
  assert(l.work===29&&f.work===29&&l.peakFreshResultSlots===f.peakFreshResultSlots,'work/peak changed');
  assert(f.retainedResultSlotSteps===144&&l.retainedResultSlotSteps===144+16*(t-1),'area identity');
  assert(l.referenceDigits===92,'late refs changed');
  const anticipated=38+Array.from({length:27},(_,i)=>String(16*t+1+i).length).reduce((a,b)=>a+b,0);
  assert(f.referenceDigits===anticipated,'prefix reference digits');
  let result={t,late:l,sourceFirst:f,deltaArea:l.retainedResultSlotSteps-f.retainedResultSlotSteps,deltaReferenceDigits:f.referenceDigits-l.referenceDigits};
  if(runOS&&t<=16){result.nativeLate=verifyOS(late,temp,'late'+t);result.nativeSourceFirst=verifyOS(front,temp,'front'+t);
   assert(result.nativeLate.accepted=== (t!==2)&&result.nativeSourceFirst.accepted===(t!==2),'original OS verdict changed');
   if(t===8){for(const [name,edit] of [
      ['forged_source',d=>{let i=d.records.findIndex(r=>r.kind==='SOURCE'&&r.source===4);d.records[i].c[0]*=-1}],
      ['underpaid',d=>{d.summary.paid_total--}],
      ['bad_parent',d=>{d.records.at(-1).parents[1]=999999}],
      ['no_owner',d=>{d.gate_defs=[];d.summary.paid_gates=0;d.summary.paid_total=28}]
    ]){let bad=clone(front);edit(bad);let check=verifyOS(bad,temp,'bad_'+name);assert(!check.accepted,'hostile accepted '+name);result[name]='REJECT';}}}
  rows.push(result);
 }
 return {status:'PROVED/RESTRICTED fixed-deduction-order and COMPUTATIONAL',originalChecker:'experiments/arc/lspv2_386_independent_verify.js',originalCheckerGitBlob:'338305c0ce101704205e57543756b8127074a986',baselineGitBlob:'035d681e2d18e8b12191b984d59bcf870d3915d0',runtime:runOS?'native Node OS subprocess':'independent mathematical structural audit only',rows,fullHistoricalRmix341Authenticated:false};
 }finally{if(temp)fs.rmSync(temp,{recursive:true,force:true})}
}
console.log(JSON.stringify(main(),null,2));

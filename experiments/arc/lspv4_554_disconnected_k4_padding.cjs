'use strict';
// LSPV-4/554. Requires Node >=18 and repository checkout.
// Run: node experiments/arc/lspv4_554_disconnected_k4_padding.cjs
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const base=JSON.parse(fs.readFileSync(path.join(root,'results/raw/arc/2026-11-11_1734_LSPV4_554_W29_SOURCE_QUOTIENT_ACCEPTED.json'),'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const key=xs=>[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function packet(t){
 assert(Number.isSafeInteger(t)&&t>=1&&6*t+2<=Number.MAX_SAFE_INTEGER);
 const h=4*t,edges=[];
 for(let j=0;j<t;j++){const z=4*j;edges.push([z,z+1],[z,z+2],[z,z+3],[z+1,z+2],[z+1,z+3],[z+2,z+3])}
 const charge=Array(h).fill(0);charge[0]=1;
 const guard=6*t+1;
 const occ=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{occ[u].push(i+1);occ[v].push(i+1)});
 const translate=x=>x===19?guard:x===-19?-guard:x;
 const originalSources=base.records.slice(0,17).map(r=>{const z=clone(r);z.c=z.c.map(translate);return z});
 const extra=[];
 for(let v=4;v<h;v++)for(let mask=0;mask<8;mask++){
  const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
  if(bits.reduce((a,b)=>a+b,0)%2===0)continue;
  extra.push({kind:'SOURCE',source:v,parents:[],c:key([...occ[v].map((x,i)=>bits[i]?-x:x),-guard])});
 }
 const source=[...originalSources,...extra],srcN=source.length;
 assert.strictEqual(srcN,16*t+1);
 const res=base.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='RES');
 assert.strictEqual(res.length,28);
 const dest=new Map(res.map(({i},j)=>[i,srcN+j]));
 const proof=res.map(({r})=>{
  const z=clone(r);z.c=z.c.map(translate);z.pivot=translate(z.pivot);
  z.parents=z.parents.map(p=>p<17?p:dest.get(p));
  assert(z.parents.every(Number.isInteger),'dangling proof parent');
  return z;
 });
 return {spec:{h,edges,charge,guard},gate_defs:[[1,guard+1,1,-1]],records:[...source,...proof],
 summary:{source:srcN,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:srcN+28}};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-554-pad-'));
const results=[];
try{
 for(const t of [1,2,3,4,5,6,8,12,16]){
  const d=packet(t),file=path.join(tmp,'t'+t+'.json');fs.writeFileSync(file,JSON.stringify(d)+'\n');
  const x=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:25000});
  const accept=x.status===0;assert.strictEqual(accept,t!==2,'t='+t+' '+x.stderr);
  results.push({t,h:4*t,accept,bytes:fs.statSync(file).size,stdout:x.stdout.trim(),stderr:accept?'':x.stderr.trim().slice(0,400)});
 }
 const forged=packet(8);forged.records[0].c=[-1,2,3,-forged.spec.guard];
 const p=path.join(tmp,'forged.json');fs.writeFileSync(p,JSON.stringify(forged)+'\n');
 const x=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:25000});assert.notStrictEqual(x.status,0,'forged original SOURCE accepted');
 console.log(JSON.stringify({status:'PASS',checker:'experiments/arc/lspv2_386_independent_verify.js',results,forgedSourceRejected:true,limitations:'finite representable ID range; no full mixed checker'},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true})}

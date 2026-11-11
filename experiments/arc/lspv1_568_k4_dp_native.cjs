'use strict';
// LSPV-1/568: native archived /386 guarded odd-K4 Resolution certificate.
// Recomputes all source clauses and all paid RES steps; no certificate is hardcoded.
// Usage: node experiments/arc/lspv1_568_k4_dp_native.cjs
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
 crypto=require('node:crypto'),vm=require('node:vm'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const canonical=(c)=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function sourceSpec(){
 const h=4,edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],charge=[1,0,0,0],guard=7;
 return {h,edges,charge,guard};
}
function construct(){
 const spec=sourceSpec(),{h,edges,charge,guard}=spec,all=[];
 for(let v=0;v<h;v++){
  const inc=[];edges.forEach(([a,b],j)=>{if(a===v||b===v)inc.push(j+1)});
  assert.equal(inc.length,3);
  for(let mask=0;mask<8;mask++){
   const bit=inc.map((_,i)=>(mask>>i)&1);
   if(bit.reduce((a,b)=>a+b,0)%2!==charge[v]){
    all.push({kind:'SOURCE',c:canonical([...inc.map((x,i)=>bit[i]?-x:x),-guard]),parents:[],source:v});
   }
  }
 }
 all.push({kind:'SOURCE',c:[guard],parents:[],source:-1});
 assert.equal(all.length,17);
 const bank=new Map(all.map((r,i)=>[JSON.stringify(r.c),i]));
 let active=all.map((_,i)=>i);
 const order=[1,2,4,3,5,6,7];
 for(const pivot of order){
  const pos=active.filter(i=>all[i].c.includes(pivot));
  const neg=active.filter(i=>all[i].c.includes(-pivot));
  const rest=active.filter(i=>!all[i].c.includes(pivot)&&!all[i].c.includes(-pivot));
  if(pos.length===0||neg.length===0){active=rest;continue}
  const children=[];
  for(const a of pos)for(const b of neg){
   const union=[...new Set([...all[a].c.filter(x=>x!==pivot),...all[b].c.filter(x=>x!==-pivot)])];
   if(union.some(x=>union.includes(-x)))continue; // tautological resolvent
   const c=canonical(union),key=JSON.stringify(c);
   let i=bank.get(key);
   if(i===undefined){i=all.length;all.push({kind:'RES',c,parents:[a,b],pivot});bank.set(key,i)}
   children.push(i);
  }
  active=[...new Set([...rest,...children])].sort((i,j)=>all[i].c.length-all[j].c.length);
  const keep=[];
  for(const i of active){
   if(!keep.some(j=>all[j].c.every(x=>all[i].c.includes(x))))keep.push(i);
  }
  active=keep;
  if(active.some(i=>all[i].c.length===0))break;
 }
 const sink=all.findIndex((r,i)=>i>=17&&r.c.length===0);
 assert(sink>=17,'expected empty clause');
 const ancestry=new Set(),work=[sink];
 while(work.length){
  const i=work.pop();if(ancestry.has(i))continue;
  ancestry.add(i);work.push(...all[i].parents);
 }
 for(let i=0;i<17;i++)assert(ancestry.has(i),'original SOURCE missing from sink ancestry');
 const retained=all.map((_,i)=>i).filter(i=>i<17||ancestry.has(i));
 const renumber=new Map(retained.map((i,j)=>[i,j]));
 const records=retained.map(i=>({...all[i],parents:all[i].parents.map(x=>renumber.get(x))}));
 assert.equal(records.at(-1).c.length,0);
 const nres=records.filter(r=>r.kind==='RES').length;
 assert.equal(nres,28);
 assert.equal(records.length,45);
 function packet(withOwner){
  const ng=Number(withOwner);
  return {spec,gate_defs:withOwner?[[0,8,1,4]]:[],records,
   summary:{source:17,def_views:0,resolution:nres,paid_gates:ng,
    paid_total:nres+ng,live_records:records.length}};
 }
 return {core:packet(false),cli:packet(true),order,unpruned:all.length,
   sourceAncestors:17,paidResolution:nres};
}
function independentCheck(packet){
 const {spec,records}=packet;
 const used=new Set();
 for(let i=0;i<records.length;i++){
  const r=records[i];assert.deepEqual(r.c,canonical(r.c));
  assert(r.c.every(x=>x!==0&&!r.c.includes(-x)));
  if(r.kind==='SOURCE'){
   assert.equal(r.parents.length,0);
   if(r.source===-1)assert.deepEqual(r.c,[spec.guard]);
   else{
    const inc=spec.edges.flatMap(([a,b],i)=>a===r.source||b===r.source?[i+1]:[]);
    const withGuard=r.c.filter(x=>x!==-spec.guard);
    assert.equal(withGuard.length,3);
    assert.deepEqual(withGuard.map(Math.abs).sort((a,b)=>a-b),inc);
    const signParity=withGuard.reduce((p,x)=>p^(x<0?1:0),0);
    assert.notEqual(signParity,spec.charge[r.source]);
   }
  } else {
   assert.equal(r.kind,'RES');
   assert.equal(r.parents.length,2);
   const [a,b]=r.parents;
   assert(a<i&&b<i&&a>=0&&b>=0);
   const A=records[a].c,B=records[b].c,p=r.pivot;
   assert(A.includes(p)&&B.includes(-p));
   assert.deepEqual(r.c,canonical([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]));
  }
 }
 let assignments=0;
 for(let m=0;m<(1<<spec.edges.length);m++){
  const sat=records.filter(r=>r.kind==='SOURCE').every(r=>r.c.some(l=>{
   const val=Math.abs(l)===spec.guard?1:(m>>(Math.abs(l)-1))&1;
   return l>0?val===1:val===0;
  }));
  if(sat)assignments++;
 }
 assert.equal(assignments,0,'source incorrectly satisfiable');
 const visited=new Set(),todo=[records.length-1];while(todo.length){
  const i=todo.pop();if(visited.has(i))continue;visited.add(i);todo.push(...records[i].parents);
 }
 assert.equal(records.filter(r=>r.kind==='SOURCE'&&visited.has(records.indexOf(r))).length,17);
 return {sourceAssignments:1<<spec.edges.length,models:assignments,ancestralSources:17};
}
function nativeChecker(){
 const buf=fs.readFileSync(checkerPath);
 const blob=crypto.createHash('sha1').update('blob '+buf.length+'\0').update(buf).digest('hex');
 assert.equal(blob,'338305c0ce101704205e57543756b8127074a986',
  'original checker blob mismatch');
 const ctx={require,process:{argv:[]},console};
 vm.runInNewContext(buf.toString('utf8')+'\nthis.authenticCheckProof=checkProof;',ctx,
  {filename:checkerPath,timeout:10000});
 return {check:ctx.authenticCheckProof,blob};
}
function main(){
 const p=construct(),ind=independentCheck(p.cli),{check,blob}=nativeChecker();
 const core=check(p.core,{control:true}),withOwner=check(p.cli,{control:true});
 assert.equal(core.paid,28);assert.equal(withOwner.paid,29);
 let rejected=0;
 function negative(change){const d=structuredClone(p.cli);change(d);try{check(d,{control:false})}
  catch(e){rejected++;return}throw Error('corrupted packet accepted')}
 negative(d=>d.records.at(-1).pivot=999999);
 negative(d=>d.records.at(-1).parents[0]=999);
 negative(d=>d.records[0].c[0]*=-1);
 negative(d=>d.summary.paid_total--);
 negative(d=>d.records.splice(0,1));
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp568-'));
 try{
  const corePath=path.join(temp,'core28.json'),cliPath=path.join(temp,'cli29.json');
  fs.writeFileSync(corePath,JSON.stringify(p.core));
  fs.writeFileSync(cliPath,JSON.stringify(p.cli));
  const good=cp.spawnSync(process.execPath,[checkerPath,cliPath],{encoding:'utf8'});
  assert.equal(good.status,0,good.stderr);
  const checked=JSON.parse(good.stdout.trim());
  assert.equal(checked.paid,29);assert.equal(checked.negativeTests,11);
  const reject=cp.spawnSync(process.execPath,[checkerPath,corePath],{encoding:'utf8'});
  assert.notEqual(reject.status,0,'expected synthetic zero-owner CLI failure');
  assert.match(reject.stderr,/accepted a corrupted proof/);
  console.log(JSON.stringify({id:'LSPV1-568',checkerBlob:blob,permutation:p.order,
   corePaid:28,cliPaid:29,records:45,sourceRecords:17,liveRES:28,ownerDeclarations:1,
   ownerFacets:0,independent:ind,corruptionsRejected:rejected,fullCLI:checked,
   zeroOwnerCLIReject:true,corePacketSha256:crypto.createHash('sha256').update(fs.readFileSync(corePath)).digest('hex'),
   cliPacketSha256:crypto.createHash('sha256').update(fs.readFileSync(cliPath)).digest('hex')},null,2));
  if(process.argv.includes('--emit')){
   for(const [name,obj] of [['2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json',p.core],
                             ['2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json',p.cli]]){
    fs.writeFileSync(path.join(root,'results/raw/arc',name),JSON.stringify(obj,null,2)+'\n');
   }
  }
 }finally{fs.rmSync(temp,{recursive:true,force:true})}
}
if(require.main===module)main();
module.exports={construct,independentCheck};

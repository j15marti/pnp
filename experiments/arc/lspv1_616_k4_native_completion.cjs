'use strict';
// LSPV-1/616: inspect the exact original /341 K4 SOURCE-to-terminal fiber.
// Run from the repository root: node experiments/arc/lspv1_616_k4_native_completion.cjs
const fs=require('fs'), path=require('path'), crypto=require('crypto'), vm=require('vm'), assert=require('assert');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const fixturePath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checker=fs.readFileSync(checkerPath,'utf8');
const source=fs.readFileSync(fixturePath,'utf8');
const blobHash=s=>crypto.createHash('sha1').update('blob '+Buffer.byteLength(s)+'\0'+s).digest('hex');
assert.equal(blobHash(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0','checker pin');
assert.equal(blobHash(source),'fe27fe1011d0021e721ccaeb747ed58da65d7464','fixture pin');
const packet=JSON.parse(source);
const original=packet.fixtures[0];
assert.equal(original.graph.name,'K4');
assert.deepEqual(original.charges,[1,0,0,0]);
const edgeIds=original.graph.edges.flatMap(([u,v],i)=>u===0||v===0?[i]:[]);
const sourceIndices=original.clauses.flatMap((c,i)=>c.vertex===0?[i]:[]);
assert.equal(edgeIds.length,3);assert.equal(sourceIndices.length,4);
const choose4=[];
for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)for(let c=b+1;c<8;c++)for(let d=c+1;d<8;d++)choose4.push([a,b,c,d]);
const popParity=n=>(n.toString(2).split('1').length-1)%2;
function freshPacket(S) {
 const f=JSON.parse(JSON.stringify(original));
 f.charges[0]=true;
 for(let t=0;t<4;t++) f.clauses[sourceIndices[t]].literals=edgeIds.map((e,b)=>(S[t]&(1<<b))?-(e+1):e+1);
 return {fixtures:[f],summary:[packet.summary[0]]};
}
function nativeRun(p) {
 const logs=[];
 const context={
  require(name){assert.equal(name,'fs');return {readFileSync:()=>JSON.stringify(p)};},
  process:{argv:['node','original341','fixture.json']},
  console:{log:x=>logs.push(String(x))}
 };
 try {
  vm.runInNewContext(checker,context,{timeout:3000});
  const res=JSON.parse(logs.at(-1));
  return {accept:true,assertion_groups:res.checks};
 } catch(e) {return {accept:false,reason:String(e).replace(/^Error: /,'')};}
}
function models(f){
 const E=f.graph.edges.length;let count=0;
 for(let v=0;v<(1<<E);v++){
  if(f.clauses.every(c=>c.literals.some(l=>{
   const b=(v>>(Math.abs(l)-1))&1;return l>0?b===1:b===0;
  })))count++;
 }
 return count;
}
function affine(S){
 const allowed=a=>!S.includes(a);const matches=[];
 for(let mask=1;mask<8;mask++)for(let rhs=0;rhs<2;rhs++)
  if(Array.from({length:8},(_,a)=>Number(popParity(a&mask)===rhs)===Number(allowed(a))).every(Boolean))matches.push([mask,rhs]);
 return matches;
}
const cases=[];const reasons={};const hist={};const affineModels={};
for(const S of choose4){
 const p=freshPacket(S),n=models(p.fixtures[0]),rows=affine(S),r=nativeRun(p);
 const expected=S.join(',')==='0,3,5,6';
 assert.equal(r.accept,expected,'full original checker acceptance mismatch for '+S);
 assert.equal(n===0,expected,'K4 UNSAT spectrum mismatch for '+S);
 assert(rows.length<=1);
 const key=String(n);hist[key]=(hist[key]||0)+1;
 if(rows.length)affineModels[key]=(affineModels[key]||0)+1;
 if(!r.accept)reasons[r.reason]=(reasons[r.reason]||0)+1;
 cases.push({forbidden:S,models:n,affine_row:rows[0]||null,native:r});
}
assert.equal(cases.length,70);
assert.equal(cases.filter(x=>x.native.accept).length,1);
assert.equal(cases.filter(x=>x.affine_row).length,14);
assert.deepEqual(hist,{'0':1,'2':16,'4':36,'6':16,'8':1});
assert.deepEqual(affineModels,{'0':1,'4':12,'8':1});
const base=freshPacket([0,3,5,6]);
const badSource=JSON.parse(JSON.stringify(base));badSource.fixtures[0].clauses[0].literals[0]=999;
const badParent=JSON.parse(JSON.stringify(base));badParent.fixtures[0].proof[0].parents[0]='not-source';
const badParity=JSON.parse(JSON.stringify(base));badParity.fixtures[0].charges[0]=false;
const hostile={bad_source:nativeRun(badSource),bad_parent:nativeRun(badParent),bad_global_charge:nativeRun(badParity)};
assert(Object.values(hostile).every(x=>!x.accept));
const out={result:'LSPV-1/616',date:'2026-11-13 PST',checker_blob:blobHash(checker),fixture_blob:blobHash(source),
 classification:'restricted original-checker K4 exact completion, not full historical R_mix341',
 counts:{source_prefix_family:70,full_original_checker_accept:1,full_original_checker_reject:69,
 affine_local_rows:14,non_affine_local:56,models_histogram:hist,affine_models_histogram:affineModels,native_rejection_reasons:reasons},
 hostile, cases};
console.log(JSON.stringify(out,null,2));

'use strict';
// LSPV-2/548, recovered /341 fixture checker differential. NOT full R_mix341.
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..'),base=path.join(root,'experiments/arc');
const prod=path.join(base,'lspv2_341_mixed_tseitin_min_dag.js'),check=path.join(base,'lspv2_341_independent_verify.js');
const pins={producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(blob(fs.readFileSync(prod)),pins.producer);assert.equal(blob(fs.readFileSync(check)),pins.checker);
const checker=new Function('require','process','console',fs.readFileSync(check,'utf8'));
const copy=x=>JSON.parse(JSON.stringify(x));
function validate(p){const output=[];try{
 checker(mod=>{assert.equal(mod,'fs');return {readFileSync:()=>JSON.stringify(p)};},
 {argv:['node','verify','payload.json']},{log:x=>output.push(x)});
 return {ok:true,checks:JSON.parse(output.at(-1)).checks};
 }catch(e){return {ok:false,error:String(e.message)};}}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2_548_'));
function native(p){const fn=path.join(tmp,'packet.json');fs.writeFileSync(fn,JSON.stringify(p));
 const r=cp.spawnSync(process.execPath,[check,fn],{encoding:'utf8',timeout:6000,maxBuffer:16000000});
 if(r.error)throw r.error;
 return r.status===0?{ok:true,checks:JSON.parse(r.stdout).checks}:{ok:false,error:r.stderr.trim().slice(0,220)};
}
function paths(v,p=[]){let a=[];if(Array.isArray(v))v.forEach((x,i)=>a.push(...paths(x,p.concat(i))));
 else if(v&&typeof v==='object')for(const k of Object.keys(v)){a.push(p.concat(k));a.push(...paths(v[k],p.concat(k)));}
 return a;}
function greed(p){const removed=[];for(const q of paths(p).reverse()){
 let at=p;for(const k of q.slice(0,-1)){if(at==null)break;at=at[k];}
 const k=q.at(-1);if(at==null||Array.isArray(at)||!(k in at))continue;
 const x=at[k];delete at[k];if(validate(p).ok)removed.push(q.join('.'));else at[k]=x;
 }return removed;}
function renumber(p){const m=new Map();for(let i=0;i<16;i++)m.set('s'+i,i);
 for(let i=0;i<15;i++)m.set('d'+i,16+i);
 const f=p.fixtures[0],v=x=>m.has(x)?m.get(x):x;
 f.clauses.forEach(c=>c.id=v(c.id));f.deleted.forEach(d=>d.sourceId=v(d.sourceId));
 f.proof.forEach(n=>{if('id' in n)n.id=v(n.id);n.parents=n.parents.map(v);});
 return p;}
function run(){try{
 const full=JSON.parse(cp.execFileSync(process.execPath,[prod],{encoding:'utf8',maxBuffer:16000000}));
 assert(validate(full).ok&&native(full).checks===30714);
 const f=full.fixtures[0],original={fixtures:[copy(f)],summary:[null]};
 const before=JSON.stringify(original).length,pruned=copy(original),removed=greed(pruned);
 const numbered=copy(pruned);numbered.fixtures[0].proof.at(-1).id='d14';renumber(numbered);
 const without=renumber(copy(pruned));
 const cases=[['original-full',full,true],['original-K4',original,true],['pruned-K4',pruned,true],
 ['integer-IDs-with-sink',numbered,true],['integer-IDs-no-sink',without,true]];
 const bad=(name,fn)=>{let p=copy(numbered);fn(p.fixtures[0]);cases.push([name,p,false]);};
 bad('signed-literal-corrupt',f=>f.clauses[0].literals[0]*=-1);
 bad('source-ID-duplicate',f=>f.clauses[1].id=f.clauses[0].id);
 bad('dangling-parent',f=>f.proof[0].parents[0]=999);
 bad('AND3-truth-table-corrupt',f=>f.proof[0].table^=1);
 bad('paid-ID-duplicate',f=>f.proof[1].id=f.proof[0].id);
 bad('XOR-sink-corrupt',f=>f.proof.at(-1).row.rhs=0);
 bad('referenced-paid-ID-missing',f=>delete f.proof[0].id);
 const results=cases.map(([name,p,expect])=>{
 const c=validate(p),n=native(p);assert.equal(c.ok,expect,name);assert.equal(n.ok,expect,name);
 if(expect)assert.equal(c.checks,n.checks);
 const b=Buffer.from(JSON.stringify(p));return {name,accept:n.ok,checks:n.checks||null,bytes:b.length,sha256:sha(b),hex:b.toString('hex')};
 });
 assert(results.slice(1,5).every(x=>x.checks===1401));
 const source='p cnf 6 16\n'+f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
 return {status:'COMPUTATIONAL, checker-relative',pins,source:{dimacs:source,sha256:sha(Buffer.from(source)),bytes:Buffer.byteLength(source)},
 input_bytes_before_pruning:before,removed,paid_nodes:15,results,
 open:'P2-D1, P2-C3, P2-B1, B2/B3, P vs NP'};
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

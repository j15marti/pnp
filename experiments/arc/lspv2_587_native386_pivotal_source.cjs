'use strict';
// LSPV-2/587 reference constructor/replayer. Does NOT replace the archived native checker.
// Usage: node experiments/arc/lspv2_587_native386_pivotal_source.cjs CHECKER SEED OUT
const fs=require('node:fs'),cp=require('node:child_process'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const [checker,seedFile,outFile]=process.argv.slice(2);
if(!checker||!seedFile||!outFile)throw Error('usage: node SCRIPT CHECKER SEED OUTPUT');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(sha(fs.readFileSync(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const seedBytes=fs.readFileSync(seedFile);assert.equal(sha(seedBytes),'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0');
const seed=JSON.parse(seedBytes),key=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function build(k){
 const h=4*k,E=6*k,g=E+1,edges=[];
 for(let c=0;c<k;c++)for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([4*c+a,4*c+b]);
 const inc=Array.from({length:h},()=>[]);edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
 const records=[];for(let v=0;v<h;v++)for(let m=0;m<8;m++){
  let bits=[m&1,(m>>1)&1,(m>>2)&1];if((bits[0]^bits[1]^bits[2])===(v===0?1:0))continue;
  records.push({kind:'SOURCE',c:key([...inc[v].map((n,j)=>bits[j]?-n:n),-g]),parents:[],source:v});
 }
 records.push({kind:'SOURCE',c:[g],parents:[],source:-1});
 for(let i=0;i<16;i++)assert.deepEqual(records[i].c,seed.records[i].c.map(x=>x===-7?-g:x));
 const map=i=>i<16?i:i===16?4*h:i+4*h-16;
 for(const r of seed.records.slice(17))records.push({kind:'RES',c:r.c.map(x=>x===-7?-g:x),parents:r.parents.map(map),pivot:r.pivot===7?g:r.pivot});
 return {spec:{h,edges,charge:Array.from({length:h},(_,i)=>i===0?1:0),guard:g},gate_defs:[[0,E+2,1,4]],records,summary:{source:4*h+1,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:records.length}};
}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-587-')),file=path.join(dir,'packet.json');
function native(buf){fs.writeFileSync(file,buf);let r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000});return {ok:r.status===0&&!r.error,out:r.stdout,err:String(r.stderr).slice(-120)};}
const rows=[];
try{
 for(const k of [3,4,8]){
  const x=build(k),buf=Buffer.from(JSON.stringify(x)+'\n'),m=4*x.spec.h+1,good=native(buf);
  assert(good.ok,'original CLI rejected '+k+': '+good.err);
  const parsed=JSON.parse(good.out);assert.equal(parsed.paid,29);assert.equal(parsed.sources,m);
  const positions=[...buf.toString('utf8').matchAll(/"source":(-?\d+)/g)].map(a=>a.index+a[0].length-1);
  assert.equal(positions.length,m+1);
  const neighborSHA=[];
  for(let i=0;i<m;i++){
   let p=positions[i],b=Buffer.from(buf);b[p]^=1;
   assert(b[p]>=48&&b[p]<=57);assert.notEqual(JSON.parse(b).records[i].source,x.records[i].source);
   const bad=native(b);assert(!bad.ok,'original CLI accepted SOURCE '+i+' byte mutation');
   neighborSHA.push(sha(b));
  }
  rows.push({k,vertices:4*k,source_records:m,certificate_bytes:buf.length,sha256:sha(buf),paid:29,pivotal_source_bits:m,mutation_digest:sha(Buffer.from(neighborSHA.join('\n')+'\n')),native_assertions:parsed.assertions});
 }
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const result={model:'unchanged archived /386 complete CLI; not full R_mix341',native_checker_sha256:sha(fs.readFileSync(checker)),seed_sha256:sha(seedBytes),native_accepts:rows.length,native_rejects:rows.reduce((a,x)=>a+x.pivotal_source_bits,0),theorem:'each SOURCE id contains a distinct bit whose flip rejects while logical work remains 29',rows,limitation:'restricted native certificate membership bit probes, not SAT decision time or historical mixed-calculus lower bound'};
fs.writeFileSync(outFile,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));

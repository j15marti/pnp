#!/usr/bin/env node
'use strict';
// LSPV-2/554. An executable differential harness for an archived ORIGINAL /386
// checker, NOT a reconstructed or complete historical R_mix341 checker.
// Usage: node experiments/arc/lspv2_554_gate_owner_dag_transport.cjs [--emit DIR]
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto');
const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0213_LSPV2_553_ACCEPTED_PREFIX_K1.json');
const expectedChecker='338305c0ce101704205e57543756b8127074a986';
const expectedSeed='5426883cf45e4fbccc5cc8661e91c08e4e0cb625';
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
function gitblob(data){
  return crypto.createHash('sha1').update(Buffer.concat([
    Buffer.from('blob '+data.length+'\0'),data])).digest('hex');
}
function insist(cond,msg){if(!cond)throw Error(msg)}
const checkerBytes=fs.readFileSync(checkerPath),seedBytes=fs.readFileSync(seedPath);
insist(gitblob(checkerBytes)===expectedChecker,'archived original /386 checker SHA drift');
insist(gitblob(seedBytes)===expectedSeed,'archived accepted seed SHA drift');
const seed=JSON.parse(seedBytes.toString('utf8'));
function augmented(){
  const x=JSON.parse(JSON.stringify(seed));
  insist(x.records[0].kind==='DEF' && x.records[1].kind==='SOURCE','unexpected seed');
  insist(x.gate_defs.length===1 && x.summary.paid_total===29,'seed weights drift');
  x.gate_defs=[[0,8,1,4],[1,9,2,5],[2,10,8,3]];
  x.records.splice(1,0,
    {kind:'DEF',gate:1,c:[2,-9],parents:[]},
    {kind:'DEF',gate:2,c:[3,-10],parents:[]});
  // Original index 0 stays 0; every other old record moves +2.
  for(let i=3;i<x.records.length;i++){
    x.records[i].parents=x.records[i].parents.map(j=>j===0?0:j+2);
  }
  Object.assign(x.summary,{def_views:3,paid_gates:3,
    paid_total:31,live_records:x.records.length});
  return x;
}
const base=augmented();
const orders=[[0,1,2],[0,2,1],[1,0,2],
              [1,2,0],[2,0,1],[2,1,0]];
const cases=orders.map(order=>{
  const q=JSON.parse(JSON.stringify(base));
  q.gate_defs=order.map(i=>base.gate_defs[i]);
  return {name:'owner_order_'+order.join(''),expect:order.indexOf(0)<order.indexOf(2),
    packet:q,order};
});
const mutate=(name,fn)=>{
  const q=JSON.parse(JSON.stringify(base));fn(q);
  cases.push({name,expect:false,packet:q});
};
mutate('wrong_signed_def_facet',q=>q.records[1].c=[1,-9]);
mutate('missing_parent_gate_owner',q=>q.gate_defs.splice(0,1));
mutate('incorrect_paid_count',q=>q.summary.paid_total--);
mutate('bad_res_parent',q=>q.records.at(-1).parents[0]=999);
mutate('forged_source_clause',q=>q.records[3].c=[-7]);
mutate('unrecognized_local_convert',q=>q.records[1].kind='LOCAL-CONVERT');
const outdir=process.argv[2]==='--emit'?process.argv[3]:null;
if(outdir)fs.mkdirSync(outdir,{recursive:true});
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-554-'));
const results=[];
try{
  for(const item of cases){
    const bytes=Buffer.from(JSON.stringify(item.packet)+'\n','utf8');
    const filename=path.join(tmp,item.name+'.json');
    fs.writeFileSync(filename,bytes);
    if(outdir)fs.writeFileSync(path.join(outdir,item.name+'.json'),bytes);
    const run=spawnSync(process.execPath,[checkerPath,filename],
      {encoding:'utf8',timeout:30000,maxBuffer:1024*1024});
    const accepted=run.status===0 && !run.error;
    insist(accepted===item.expect,'unexpected original-checker result: '+item.name+
      ' status='+run.status+' stderr='+(run.stderr||'').slice(0,300));
    let result={name:item.name,accepted,expected:item.expect,
      bytes:bytes.length,sha256:sha256(bytes),order:item.order||null,
      mode:'actual operating-system Node.js subprocess'};
    if(accepted){
      let line=run.stdout.trim().split('\n').at(-1);
      let observed=JSON.parse(line);
      insist(observed.paid===31 && observed.res===28 &&
             observed.def===3 && observed.sources===17 &&
             observed.records===48 && observed.negativeTests===11,
             'positive checker counters drift');
      result.native={paid:observed.paid,res:observed.res,def:observed.def,
        sources:observed.sources,records:observed.records,
        negativeTests:observed.negativeTests,assertions:observed.assertions};
    }else{
      result.error=(run.stderr||String(run.error||'')).split('\n').slice(0,2).join('\n');
    }
    results.push(result);
  }
}finally{
  for(const name of fs.readdirSync(tmp))fs.unlinkSync(path.join(tmp,name));
  fs.rmdirSync(tmp);
}
const summary={run:'LSPV2_554',original_checker_blob:expectedChecker,
  original_seed_blob:expectedSeed,accepted:results.filter(x=>x.accepted).length,
  rejected:results.filter(x=>!x.accepted).length,logical_cost:31,
  original_source_clauses:17,paid_resolutions:28,paid_owners:3,
  zero_paid_facets:3,validated_via:'original OS Node CLI including 11 native negative controls',
  status:'PROVED/RESTRICTED+COMPUTATIONAL; P vs NP OPEN',results};
if(outdir)fs.writeFileSync(path.join(outdir,'results.json'),JSON.stringify(summary,null,2)+'\n');
process.stdout.write(JSON.stringify(summary,null,2)+'\n');

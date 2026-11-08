'use strict';
/*
 LSPV-3/499: Composition adapter for the recovered historical SOURCE/AND3/XOR
 checker and LSPV-3/490 external-source binder, plus a provenance-bit firewall.
 It does NOT implement RES, DEF, LOCAL-CONVERT, branch discharge, or full R_mix341.
*/
function insist(ok,msg){if(!ok)throw Error('LSPV3-499 '+msg);}
function firewall(packet){
  insist(packet&&Array.isArray(packet.fixtures),'packet fixtures');
  let rows=0;
  for(const f of packet.fixtures){
    insist(f&&f.graph&&Array.isArray(f.graph.edges)&&Array.isArray(f.proof),'fixture');
    const E=f.graph.edges.length, upper=1n<<BigInt(E);
    for(const node of f.proof){
      if(!node.row)continue;
      rows++;
      const s=node.row.mask;
      insist(typeof s==='string' && (/^0x[0-9a-fA-F]+$/.test(s)||/^(0|[1-9][0-9]*)$/.test(s)),'noncanonical affine mask');
      const z=BigInt(s);
      insist(z>=0n && z<upper,'phantom original-variable bit');
    }
  }
  return {fixtures:packet.fixtures.length,checkedAffineRows:rows};
}
function validate(packet,source,fixtureIndex,nativeVerify,sourceAdapter){
  insist(typeof nativeVerify==='function'&&sourceAdapter&&typeof sourceAdapter.bind==='function','trusted interfaces');
  const native=nativeVerify(packet);
  insist(native&&Array.isArray(native.cases),'native checker failed');
  const masks=firewall(packet);
  insist(Number.isInteger(fixtureIndex)&&fixtureIndex>=0&&fixtureIndex<packet.fixtures.length,'fixture index');
  const f=packet.fixtures[fixtureIndex];
  const matched=sourceAdapter.bind(f,source);
  const check=native.cases.find(x=>x.name===f.graph.name);
  insist(check&&check.proofNodes===f.proof.length,'native proof summary not matched');
  return {fixture:f.graph.name,externalClauseCount:matched.clauses,originalVariables:matched.nv,proofNodes:check.proofNodes,
          bridgeless:check.bridgeless,certifiedMinimum:check.certifiedMinimum,firewall:masks};
}
if(typeof module!=='undefined')module.exports={firewall,validate};
if(typeof require==='function'&&typeof module!=='undefined'&&require.main===module){
 const fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
 const checkerPath=path.join(__dirname,'lspv2_341_independent_verify.js');
 const binderPath=path.join(__dirname,'lspv3_490_external_source_bind.cjs');
 function gitBlob(s){return crypto.createHash('sha1').update('blob '+Buffer.byteLength(s)+'\0'+s).digest('hex');}
 insist(gitBlob(fs.readFileSync(checkerPath,'utf8'))==='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0','historical checker blob changed');
 insist(gitBlob(fs.readFileSync(binderPath,'utf8'))==='b113119b7b87dac7510603804d91918e80f301b0','source binder blob changed');
 const bind=require(binderPath);
 function runNative(file){
   const p=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',maxBuffer:64*1024*1024});
   insist(p.status===0,'historical checker rejected: '+String(p.stderr).slice(0,1200));
   return JSON.parse(p.stdout);
 }
 const pktPath=process.argv[2], packet=JSON.parse(fs.readFileSync(pktPath,'utf8'));
 const native=runNative(pktPath), adapterTest=bind.selftest(packet);
 const positive=packet.fixtures.map((f,i)=>validate(packet,bind.serialize(f),i,()=>native,bind));
 let phantomAccepted=false,phantomRejected=false;
 const altered=JSON.parse(JSON.stringify(packet)),f=altered.fixtures[0];
 const x=f.proof.find(q=>q.rule==='XOR' && q.parents.every(id=>f.proof.some(v=>v.id===id && v.row)));
 insist(x,'no two-row XOR gate');
 const high=1n<<BigInt(f.graph.edges.length);
 for(const id of x.parents){const p=f.proof.find(v=>v.id===id);p.row.mask=(BigInt(p.row.mask)^high).toString();}
 const tmp=path.join(os.tmpdir(),'lspv3_499_phantom_'+process.pid+'.json');
 try{
   fs.writeFileSync(tmp,JSON.stringify(altered));
   phantomAccepted=Boolean(runNative(tmp));
   try{firewall(altered);}catch(e){phantomRejected=/phantom original-variable bit/.test(e.message);}
 }finally{try{fs.unlinkSync(tmp);}catch(e){}}
 insist(phantomAccepted&&phantomRejected,'phantom control failed');
 const out={status:'PASS',sourceBinderChecks:adapterTest.checks,sourceBinderRejects:adapterTest.rejections,
    SATMutantsRejected:adapterTest.essentialMutants,historicalChecks:native.checks,fixtureCount:positive.length,
    packetBytes:fs.statSync(pktPath).size,composed:positive,phantomMaskNativeAccepted:phantomAccepted,
    phantomMaskWrapperRejected:phantomRejected,scope:'historical SOURCE/AND3/XOR only'};
 console.log(JSON.stringify(out,null,2));
}

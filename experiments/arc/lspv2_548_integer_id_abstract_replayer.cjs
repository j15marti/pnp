'use strict';
/*
 LSPV-2/548 independent typed source-bound abstract transition replayer.
 Not the original historical verifier; not a complete R_mix341 implementation.
 Run with Node 18+: node experiments/arc/lspv2_548_integer_id_abstract_replayer.cjs
 Independently replay the exact UTF-8 hex corpus in results/raw/arc.
*/
const REFERENCE548=(function(){
const equals=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const assert=(p,msg)=>{if(!p)throw Error(msg);};
function reference(packet, independentClauses){
 const f=packet.fixtures?.[0];
 assert(f&&f.graph,'missing fixture');
 const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 assert(f.graph.n===4&&equals(f.graph.edges,E),'not source graph K4');
 assert(equals(f.charges,[1,0,0,0]),'not odd-charge K4');
 assert(Array.isArray(f.clauses)&&f.clauses.length===16,'source cardinality');
 assert(equals(f.clauses.map(c=>c.literals),independentClauses),'external signed-source mismatch');
 const inc=Array.from({length:4},(_,v)=>E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0));
 const sat=(c,b)=>c.some(l=>b[Math.abs(l)-1]===(l>0?1:0));
 const value=(tab,support,b)=>{let i=0;for(let j=0;j<support.length;j++)i|=b[support[j]]<<j;return (tab>>i)&1;};
 const table=(support,test)=>{let t=0;for(let m=0;m<1<<support.length;m++){
  const b=Array(6).fill(0);support.forEach((v,j)=>b[v]=(m>>j)&1);
  if(test(b))t|=1<<m;
 }return t;};
 const known=new Map(),parents=new Map(),sources=new Set(),paid=new Set();
 for(const c of f.clauses){
  assert(Number.isSafeInteger(c.vertex)&&c.vertex>=0&&c.vertex<4,'source vertex range');
  const support=inc[c.vertex];
  const real=[...new Set(c.literals.map(l=>Math.abs(l)-1))].sort((a,b)=>a-b);
  assert(equals(real,[...support].sort((a,b)=>a-b)),'source literal support');
  assert((typeof c.id==='string'||Number.isSafeInteger(c.id))&&!known.has(c.id),'unique primitive SOURCE ID');
  known.set(c.id,{kind:'factor',support,table:table(support,b=>sat(c.literals,b)),depth:0});
  parents.set(c.id,[]);sources.add(c.id);
 }
 assert(Array.isArray(f.proof)&&f.proof.length>0,'proof missing');
 const ruleCounts={AND3:0,XOR:0};let span=0;
 for(let i=0;i<f.proof.length;i++){
  const n=f.proof[i];
  assert(n&&typeof n==='object','bad paid record');
  const missing=!Object.prototype.hasOwnProperty.call(n,'id');
  assert((missing&&i===f.proof.length-1)||typeof n.id==='string'||Number.isSafeInteger(n.id),'bad paid key');
  const id=n.id;
  assert(!known.has(id)&&!paid.has(id),'duplicate paid identity');
  assert(Array.isArray(n.parents)&&n.parents.length===2&&n.parents[0]!==n.parents[1],'binary distinct antecedents');
  const a=known.get(n.parents[0]),b=known.get(n.parents[1]);
  assert(a!==undefined&&b!==undefined,'dangling parent');
  let v;
  if(n.rule==='AND3'){
   assert(n.kind==='factor'&&a.kind==='factor'&&b.kind==='factor','bad AND3 parent kinds');
   const support=[...new Set(a.support.concat(b.support))];
   assert(support.length<=3&&equals(n.support,support),'AND3 support differs');
   const trueTable=table(support,bits=>value(a.table,a.support,bits)&&value(b.table,b.support,bits));
   assert(n.table===trueTable,'incorrect AND3 Boolean table');
   v={kind:'factor',support,table:trueTable};
   if(n.row!==undefined){
    assert(n.row&&Number.isSafeInteger(n.row.rhs)&&(n.row.rhs===0||n.row.rhs===1),'bad affine RHS');
    const mask=BigInt(n.row.mask),rhs=n.row.rhs;
    assert(mask>=0n&&mask<64n,'affine row outside 6-variable source');
    for(let e=0;e<6;e++)assert(((mask>>BigInt(e))&1n)!==1n||support.includes(e),'affine var outside AND3 support');
    const affineTable=table(support,bits=>{
     let x=0;for(let e=0;e<6;e++)if((mask>>BigInt(e))&1n)x^=bits[e];
     return x===rhs;
    });
    assert(affineTable===trueTable,'affine alias not equivalent');
    v.row={mask,rhs};
   }
  }else if(n.rule==='XOR'){
   assert(n.kind==='affine'&&n.row&&a.row&&b.row,'XOR missing affine premise');
   const mask=a.row.mask^b.row.mask,rhs=a.row.rhs^b.row.rhs;
   assert(BigInt(n.row.mask)===mask&&n.row.rhs===rhs,'incorrect GF(2) sum');
   v={kind:'affine',row:{mask,rhs}};
  }else return {status:'MAY_UNAUTHENTICATED',unknown_rule:n.rule,index:i,minimum_projected_cost:0};
  v.depth=1+Math.max(a.depth,b.depth);
  span=Math.max(span,v.depth);known.set(id,v);parents.set(id,n.parents);
  paid.add(id);ruleCounts[n.rule]++;
 }
 const sink=f.proof.at(-1),last=known.get(sink.id);
 assert(last?.kind==='affine'&&last.row.mask===0n&&last.row.rhs===1,'terminal not false affine row');
 const anc=new Set(),visit=id=>{if(anc.has(id))return;anc.add(id);for(const p of parents.get(id)||[])visit(p);};
 visit(sink.id);
 assert([...sources].every(id=>anc.has(id)),'genuine signed sources not all connected to sink');
 return {status:'ACCEPT_TYPED_REFERENCE_ONLY',original_source_clauses:sources.size,paid_nodes:paid.size,
  counts:ruleCounts,span,all_original_sources_reachable:true,
  missing_terminal_id:!Object.prototype.hasOwnProperty.call(sink,'id'),
  cost_projection:paid.size};
}
function corpus(data){
 const src=data.source.dimacs.split(/\r?\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('p '));
 const clauses=src.map(s=>s.split(/\s+/).map(Number).slice(0,-1));
 const result=[];
 for(const item of data.tests){
  const hex=item.raw_hex;
  const input=typeof Buffer==='undefined'?
    String.fromCharCode(...hex.match(/../g).map(k=>parseInt(k,16))):Buffer.from(hex,'hex').toString('utf8');
  let outcome;
  try{outcome=reference(JSON.parse(input),clauses)}
  catch(e){outcome={status:'REJECT_TYPED_REFERENCE_ONLY',reason:String(e.message)};}
  const actual=outcome.status==='ACCEPT_TYPED_REFERENCE_ONLY'?'ACCEPT':
      outcome.status==='MAY_UNAUTHENTICATED'?'MAY':'REJECT';
  assert(actual===item.observed,'differential mismatch: '+item.name);
  result.push({name:item.name,original_result:item.observed,reference_result:actual,
   logical_work:outcome.paid_nodes??null,span:outcome.span??null,
   missing_terminal_id:outcome.missing_terminal_id??null,
   diagnostic:outcome.reason??null});
 }
 assert(result.length===12,'expected exact /548 corpus');
 assert(result.filter(v=>v.reference_result==='ACCEPT').length===5,'expected positives');
 assert(result.filter(v=>v.reference_result==='REJECT').length===7,'expected hostile rejects');
 return {status:'COMPUTATIONAL; distinct strictly typed reference replayer, not native R_mix341',
         cases:result.length,agreement:result.length,results:result,
         open:'P2-D1 P2-C3 P2-B1 B2/B3; P vs NP'};
}
return {reference,corpus};
})();
if(typeof module!=='undefined'){
 module.exports=REFERENCE548;
 if(require.main===module){
  const fs=require('fs'),path=require('path');
  const datasetPath=path.resolve(__dirname,'../../results/raw/arc/2026-11-10_2112_LSPV2_548_NATIVE_INTEGER_ID_BYTE_CORPUS.json');
  const result=REFERENCE548.corpus(JSON.parse(fs.readFileSync(datasetPath,'utf8')));
  process.stdout.write(JSON.stringify(result,null,2)+'\n');
 }
}

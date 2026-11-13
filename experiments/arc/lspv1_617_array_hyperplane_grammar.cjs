'use strict';
// LSPV-1/617: independent audit of the archived /341 accepted Array-support subset.
// Run: node experiments/arc/lspv1_617_array_hyperplane_grammar.cjs results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json
// This auditor is NOT an authoritative R_mix341 or original /341 checker.
function ck(ok,why){if(!ok)throw Error('LSPV1/617: '+why);}
function parity(mask,x){let v=0;for(let j=0;j<3;j++)if((mask>>j)&1)v^=(x>>j)&1;return v;}
function affine(forbidden){
 const S=new Set(forbidden),out=[];
 for(let m=1;m<8;m++)for(let rhs=0;rhs<=1;rhs++)
  if(Array.from({length:8},(_,x)=>Number(!S.has(x))===Number(parity(m,x)===rhs)).every(Boolean))out.push({m,rhs});
 return out;
}
function audits(data){
 ck(Array.isArray(data.fixtures),'missing fixtures');
 let checks=0;function check(ok,why){checks++;ck(ok,why);}
 function fixture(f){
  const V=f.graph.n,E=f.graph.edges.length,N=f.clauses.length;
  check(N===4*V,'source count');
  const inc=Array.from({length:V},()=>[]);
  f.graph.edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
  check(inc.every(a=>a.length===3),'cubic');
  for(let u=0;u<V;u++)for(let v=u+1;v<V;v++)
   check(new Set([...inc[u],...inc[v]]).size>3,'different vertices share triple');
  const nodes=new Map(),forbidden=Array.from({length:V},()=>[]);
  for(const c of f.clauses){
   check(!nodes.has(c.id),'duplicate SOURCE id');
   const x=inc[c.vertex].reduce((sum,e,i)=>{
    const lit=c.literals.find(y=>Math.abs(y)===e+1);
    check(lit!==undefined,'missing signed incidence literal');
    return sum+(Number(lit<0)<<i);
   },0);
   forbidden[c.vertex].push(x);
   nodes.set(c.id,{sources:new Set([c.id]),vertices:new Set([c.vertex]),row:null,kind:'factor'});
  }
  check(forbidden.every(a=>a.length===4&&new Set(a).size===4),'SOURCE patterns');
  const hist={AND3:0,XOR:0},rowCount=Array(V).fill(0);
  for(const p of f.proof){
   check(!nodes.has(p.id),'duplicate paid id');
   const a=nodes.get(p.parents[0]),b=nodes.get(p.parents[1]);
   check(!!a&&!!b&&p.parents[0]!==p.parents[1],'missing/repeated parent');
   for(const id of a.sources)check(!b.sources.has(id),'source ancestor reused');
   const ss=new Set([...a.sources,...b.sources]);
   const vs=new Set([...a.vertices,...b.vertices]);
   if(p.rule==='AND3'){
    hist.AND3++;
    check(a.kind==='factor'&&b.kind==='factor'&&vs.size===1,'cross-vertex AND3');
    check(Array.isArray(p.support),'non-Array AND3 support');
    const v=[...vs][0];
    check(p.support.length===3&&new Set(p.support).size===3&&
     inc[v].every(e=>p.support.includes(e)),'incorrect Array support');
    if(p.row){
     check(ss.size===4,'premature affine row');
     const c=affine(forbidden[v]);
     check(c.length===1,'local nonaffine SOURCE');
     // Use BigInt: JavaScript << on Number silently wraps shift distances mod 32.
     const mask=inc[v].reduce((acc,e,j)=>acc|(((c[0].m>>j)&1)?(1n<<BigInt(e)):0n),0n);
     check((BigInt(p.row.mask)&((1n<<BigInt(E))-1n))===mask&&p.row.rhs===c[0].rhs,
       'incorrect local row');
     rowCount[v]++;
    }
   }else if(p.rule==='XOR'){
    hist.XOR++;
    check(!!a.row&&!!b.row&&p.kind==='affine','bad XOR premises');
    check(BigInt(p.row.mask)===(BigInt(a.row.mask)^BigInt(b.row.mask))&&
     p.row.rhs===(a.row.rhs^b.row.rhs),'bad XOR row');
   }else ck(false,'unsupported opcode '+p.rule);
   nodes.set(p.id,{sources:ss,vertices:vs,row:p.row||null,kind:p.rule==='AND3'?'factor':'affine'});
  }
  const last=f.proof.at(-1),goal=nodes.get(last.id);
  check(goal.sources.size===N,'missing source ancestry');
  check(BigInt(last.row.mask)===0n&&last.row.rhs===1,'wrong sink');
  check(hist.AND3===3*V&&hist.XOR===V-1,'wrong rule histogram');
  check(rowCount.every(x=>x===1),'not one carrier per vertex');
  return {name:f.graph.name,vertices:V,edges:E,sources:N,paid:f.proof.length,
   AND3:hist.AND3,XOR:hist.XOR,row_carriers:rowCount.reduce((a,b)=>a+b,0),
   terminal_live_sources:goal.sources.size};
 }
 const positives=data.fixtures.map(fixture);
 const f=data.fixtures[0],serialized=JSON.stringify(f),rejected=[];
 for(const [name,mutator] of [
  ['duplicate-parent',f=>{f.proof[0].parents[1]=f.proof[0].parents[0]}],
  ['premature-affine-row',f=>{f.proof[0].row={mask:'0x0',rhs:0}}],
  ['cross-vertex-AND3',f=>{f.proof[0].parents[1]=f.clauses.find(c=>c.vertex!==f.clauses[0].vertex).id}],
  ['wrong-sink',f=>{f.proof.at(-1).row.rhs^=1}],
  ['non-Array-support',f=>{f.proof[0].support='012'}]
 ]){
  const copy=JSON.parse(serialized);mutator(copy);
  let bad=false;try{fixture(copy)}catch(e){bad=true}
  check(bad,'hostile not caught '+name);rejected.push(name);
 }
 const inc=Array.from({length:f.graph.n},()=>[]);
 f.graph.edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
 const rows=new Map();
 for(const p of f.proof)if(p.rule==='AND3'&&p.row){
  const v=inc.findIndex(t=>t.length===p.support.length&&t.every(e=>p.support.includes(e)));
  check(v>=0&&!rows.has(v),'K4 row owner');rows.set(v,p.row);
 }
 check(f.graph.n===4&&rows.size===4,'not K4');
 let restMask=0n,restRhs=0;
 for(let v=1;v<4;v++){restMask^=BigInt(rows.get(v).mask);restRhs^=rows.get(v).rhs}
 const cases=[],hits=[];
 function choose(start,prior){
  if(prior.length===4){
   const c=affine(prior);cases.push({patterns:prior.slice(),local_affine:c.length===1});
   if(c.length===1){
    let mask=0n;for(let j=0;j<3;j++)if((c[0].m>>j)&1)mask^=1n<<BigInt(inc[0][j]);
    if((restMask^mask)===0n&&(restRhs^c[0].rhs)===1)hits.push(prior.slice());
   }
   return;
  }
  for(let i=start;i<8;i++)choose(i+1,[...prior,i]);
 }
 choose(0,[]);
 check(cases.length===70,'K4 4-subsets');
 check(cases.filter(c=>c.local_affine).length===14,'K4 affine count');
 check(hits.length===1&&hits[0].join(',')==='0,3,5,6','K4 one global XOR');
 for(let k=1;k<=3;k++)check(![0,4,8].includes(8-k),'premature affine cardinality');
 return {status:'PASS',scope:'Original-/341 Array-support proof-body structural audit; original checker not executed here.',
  checker_git_blob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  input_git_blob:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
  seven_original_accepted_fixture_structure:positives,
  K4_four_subsets:cases.length,K4_affine_source_subsets:cases.filter(c=>c.local_affine).length,
  K4_terminal_XOR_source_sets:hits,
  hostile_structural_mutations_rejected:rejected,
  structural_assertions:checks,random_seed:null};
}
if(typeof module!=='undefined')module.exports={audits};
if(typeof require!=='undefined'&&require.main===module){
 const fs=require('fs');
 const out=audits(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));
 process.stdout.write(JSON.stringify(out,null,2)+'\n');
}

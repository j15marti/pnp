'use strict';
// LSPV-4/426 independent (not imported from Python) exact Tseitin/port-structure referee.
// Run: node lspv4_426_independent.js results/raw/arc/2026-11-05_1731_LSPV4_426_COMPOSED_PORT_summary.json
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
if(process.argv.length<3)throw Error('Supply raw JSON filename');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const binary=(v,k)=>Number(v).toString(2).padStart(k,'0');
const graphs={K4:{n:4,edges:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]},cube:{n:8,edges:[]}};
for(let u=0;u<8;u++)for(let i=0;i<3;i++){let v=u^(1<<i);if(u<v)graphs.cube.edges.push([u,v])}
graphs.cube.edges.sort((a,b)=>(a[0]-b[0])||(a[1]-b[1]));
let checks=0;
for(const r of data.rows){
 let {n,edges}=graphs[r.graph],E=edges.length,B=r.blocks,w=Math.floor(Math.log2(B*E))+1;
 assert.equal(edges.length,3*n/2);checks++;
 let clauses=[];
 for(let block=0;block<B;block++)for(let vert=0;vert<n;vert++){
  let incident=[];for(let e=0;e<E;e++)if(edges[e].includes(vert))incident.push(block*E+e+1);
  assert.equal(incident.length,3);checks++;
  let bit=(r.kind==='UNSAT'&&block===Math.floor(B/2)&&vert===0)?1:0;
  for(let mask=0;mask<8;mask++){
   let par=((mask&1)+((mask>>1)&1)+((mask>>2)&1))&1;
   if(par===bit)continue;
   clauses.push(incident.map((id,j)=>((mask>>j)&1)?-id:id));
  }
 }
 assert.equal(clauses.length,4*n*B);checks++;
 let encoded=binary(B,32)+binary(n,16)+binary(w,8)+binary(clauses.length,32);
 for(let c of clauses)for(let lit of c)encoded+=(lit<0?'1':'0')+binary(Math.abs(lit),w);
 assert.equal(encoded.length,r.root_bits);checks++;
 assert.equal(crypto.createHash('sha256').update(encoded).digest('hex'),r.source_sha256);checks++;
 assert.equal(r.root_label,r.kind==='SAT');checks++;
 let size=B,count=1;
 for(let level of r.levels){
   let q=Math.floor(Math.sqrt(size));if(q*q!==size)q=size;
   size/=q;count*=q;
   assert.equal(level.groups,count);checks++;
   assert.equal(level.blocks_per_group,size);checks++;
   let ww=Math.floor(Math.log2(size*E))+1;
   assert.equal(level.max_child_bits,88+3*(4*n*size)*(ww+1));checks++;
 }
 assert.equal(size,1);assert.equal(count,B);checks+=2;
 assert.ok(r.ledger.root_reads>0);checks++;
 assert.ok(r.ledger.index_digits_written>=r.ledger.root_reads);checks++;
 assert.equal(r.ledger.index_digits_written,r.ledger.index_digit_erasures);checks++;
 for(let blockChoice of [0,Math.floor(B/2)]){
  let charge=(r.kind==='UNSAT' && blockChoice===Math.floor(B/2))?1:0;
  let cv=clauses.slice(blockChoice*4*n,blockChoice*4*n+4*n),lo=blockChoice*E;
  let sat=false;
  for(let mask=0;mask<(1<<E);mask++){
   if(cv.every(row=>row.some(lit=>{
    let bit=(mask>>(Math.abs(lit)-lo-1))&1;
    return lit>0?bit===1:bit===0;
   }))){sat=true;break}
  }
  assert.equal(sat,charge===0);checks++;
 }
}
assert.equal(data.rows.length,8);checks++;
assert.equal(data.tests,6109);checks++;
console.log(JSON.stringify({independent_checks:checks,rows:data.rows.length,all_root_sha_and_recursion_lengths_valid:true}));
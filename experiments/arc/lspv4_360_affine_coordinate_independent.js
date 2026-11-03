"use strict";
// LSPV4 360. Separately authored independent referee of authenticated
// local ROW macros (three paid AND3 inferences each) and XOR DAG replay.
// Usage: node experiments/arc/lspv4_360_affine_coordinate_independent.js results/raw/arc/2026-11-03_0536_LSPV4_AFFINE_COORDINATE_REPLAY360_summary.json
const fs=require('fs'),assert=require('assert');
const path=process.argv[2]||'results/raw/arc/2026-11-03_0536_LSPV4_AFFINE_COORDINATE_REPLAY360_summary.json';
const raw=JSON.parse(fs.readFileSync(path,'utf8'));
function graph(k){
 if(k===0){const e=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)e.push([u,v]);return [e,4];}
 const e=new Set();for(let i=0;i<k;i++)for(const [a,b] of [[i,(i+1)%k],[i+k,(i+1)%k+k],[i,i+k]])e.add([Math.min(a,b),Math.max(a,b)].join(':'));
 return [Array.from(e).map(s=>s.split(':').map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),2*k];
}
function source(E,h,odd){
 const F=[],rows=[];
 for(let v=0;v<h;v++){
  const edges=[];E.forEach(([a,b],i)=>{if(a===v||b===v)edges.push(i+1)});
  assert.equal(edges.length,3);
  const ids=[];
  for(let z=0;z<8;z++){
    const p=(z&1)^((z>>1)&1)^((z>>2)&1),charge=odd&&v===0?1:0;
    if(p!==charge){ids.push(F.length);F.push(edges.map((j,t)=>(z>>t&1)?-j:j));}
  }
  rows.push({edges,ids,rhs:Number(odd&&v===0)});
 }
 return {F,rows};
}
function sat(F,n){let count=0;for(let a=0;a<(1<<n);a++)if(F.every(C=>C.some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0))))count++;return count;}
function checkRows(F,rows){
 for(const r of rows){
  assert.equal(r.ids.length,4);
  if(![0,1].includes(r.rhs)||new Set(r.ids).size!==4||new Set(r.edges).size!==3)throw Error('bad row');
  for(const id of r.ids){if(!Number.isInteger(id)||id<0||id>=F.length||F[id].length!==3||F[id].some(l=>!r.edges.includes(Math.abs(l))))throw Error('source support mismatch');}
  for(let z=0;z<8;z++){
   const valid=r.ids.every(i=>F[i].some(l=>(((z>>r.edges.indexOf(Math.abs(l)))&1)===Number(l>0))));
   assert.equal(valid,(((z&1)^((z>>1)&1)^((z>>2)&1))===r.rhs));
  }
 }
}
function checkXors(rows){
 let mask=0n,charge=0;
 for(const r of rows){for(const e of r.edges)mask^=1n<<BigInt(e-1);charge^=r.rhs;}
 return mask===0n&&charge===1;
}
function certificate(rows){
 const nodes=rows.map(r=>({op:'row',sources:r.ids.slice(),triple:r.edges.slice(),rhs:r.rhs}));
 let acc=0;for(let i=1;i<rows.length;i++){nodes.push({op:'xor',parents:[acc,i]});acc=nodes.length-1;}
 return nodes;
}
function verifyCoordinates(F,nodes){
 for(let j=0;j<nodes.length;j++){
   const r=nodes[j];
   if(r.op==='row'){
     if(r.sources.length!==4||new Set(r.sources).size!==4||r.triple.length!==3||new Set(r.triple).size!==3||r.sources.some(i=>!Number.isInteger(i)||i<0||i>=F.length))throw Error('bad source ids');
     checkRows(F,[{edges:r.triple,ids:r.sources,rhs:r.rhs}]);
   }else if(r.op==='xor'){
     if(r.parents.length!==2||r.parents.some(i=>!Number.isInteger(i)||i<0||i>=j))throw Error('bad parent');
   }else throw Error('unsupported rule');
 }
 const coords=new Set(F.flat().map(x=>Math.abs(x)));
 for(const c of [...coords,null]){
   const bits=Array(nodes.length).fill(0);
   nodes.forEach((r,i)=>{
      if(r.op==='row')bits[i]=c===null?r.rhs:Number(r.triple.includes(c));
      else bits[i]=bits[r.parents[0]]^bits[r.parents[1]];
   });
   if(bits[bits.length-1]!==Number(c===null))throw Error('not a contradiction');
 }
 return {charged:3*nodes.filter(x=>x.op==='row').length+nodes.filter(x=>x.op==='xor').length,scratch:nodes.length};
}
function malformed(s){
 const lines=s.split('\n').filter((x,i,a)=>!(i===a.length-1&&x===''));
 if(!lines.length)throw Error('missing');const m=lines[0].match(/^p cnf ([0-9]+) ([0-9]+)$/);if(!m)throw Error('header');
 if(lines.length!==Number(m[2])+1)throw Error('count');
 for(const x of lines.slice(1)){const t=x.trim().split(/\s+/);if(t[t.length-1]!=='0'||t.slice(0,-1).some(v=>!/^(-?[1-9][0-9]*)$/.test(v)||Math.abs(Number(v))>Number(m[1])))throw Error('clause');}
}
const bad=['','p cnf a 1\n1 0\n','p cnf 2 2\n1 0\n','p cnf 1 1\n2 0\n','p cnf 1 1\n1 0 0\n','p cnf 1 1\n1\n','p cnf 1 1\n-0 0\n','p cnf 1 1\n+1 0\n','p cnf 1 1\n1 0\nextra','p CNF 1 1\n1 0\n'];
let assertions=0,deletions=0,flips=0,invalid=0;
for(const t of bad){assert.throws(()=>malformed(t));invalid++;}
for(const row of raw.rows){
 const k=row.name==='K4'?0:Number(row.name.replace('prism',''));
 const [E,h]=graph(k),odd=source(E,h,true),even=source(E,h,false);
 checkRows(odd.F,odd.rows);checkRows(even.F,even.rows);assert(checkXors(odd.rows));assert(!checkXors(even.rows));
 const proof=certificate(odd.rows),rec=verifyCoordinates(odd.F,proof);
 assert.equal(rec.charged,row.q_charged);assert.equal(rec.scratch,row.coord_scratch_bits);
 assert.throws(()=>verifyCoordinates(even.F,proof));
 const forged=proof.map(r=>({...r}));forged[0]={...forged[0],rhs:1-forged[0].rhs};assert.throws(()=>verifyCoordinates(odd.F,forged));
 assertions+=4;assert.equal(odd.F.length,row.m);
 assert.equal(row.streamed_authentication_literal_reads,3*odd.F.length);
 assert.equal(row.authentication_source_lit_reads,3*odd.F.length*(odd.F.length+1)/2);
 assertions+=2;
 assert.equal(row.q_charged,4*h-1);assert.equal(row.coord_scratch_bits,2*h-1);
 assert.equal(row.dense_table_slots,(2*h-1)*(E.length+1));assertions+=8+8*h*2;
 if(E.length<=12){
   assert.equal(sat(odd.F,E.length),0);assert.equal(sat(even.F,E.length),2**(E.length-h+1));assertions+=2;
   for(let i=0;i<odd.F.length;i++){
     assert(sat(odd.F.filter((_,j)=>j!==i),E.length)>0);deletions++;
     for(let j=0;j<3;j++){const F=odd.F.map(x=>x.slice());F[i][j]*=-1;assert(sat(F,E.length)>0);flips++;}
   }
 }
}
assert.equal(deletions,raw.deletion_SAT_controls);assert.equal(flips,raw.signflip_SAT_controls);assert.equal(invalid,raw.malformed_rejected);
console.log(JSON.stringify({status:'PASS',independent_checks:assertions+deletions+flips+invalid,source_deletion_SAT:deletions,signflip_SAT:flips,malformed_rejections:invalid,fixtures:raw.rows.map(x=>x.name),host_rss_bytes:process.memoryUsage().rss},null,2));

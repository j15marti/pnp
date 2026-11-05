// Compact source-authenticated strict-3CNF checkpoint test. Node >=18.
function build(finalOne){
 const core=[[[-1],[1,2],[-1,-2]],[[finalOne?3:-3],[-2,3],[2,-3]]];
 let fresh=4;
 const children=core.map(part=>part.flatMap(clause=>{
   const k=3-clause.length, ids=Array.from({length:k},()=>fresh++);
   return Array.from({length:1<<k},(_,mask)=>[...clause,...ids.map((v,i)=>mask&(1<<i)?-v:v)]);
 }));
 const n=fresh-1;
 const sat=(clauses,mask)=>clauses.every(c=>c.some(l=>!!(mask&(1<<(Math.abs(l)-1)))===(l>0)));
 const solutions=children.map(c=>Array.from({length:1<<n},(_,i)=>i).filter(m=>sat(c,m)));
 const combined=Array.from({length:1<<n},(_,i)=>i).filter(m=>sat(children.flat(),m));
 const proj=solutions.map(s=>[0,1].filter(u=>s.some(m=>Number(!!(m&2))===u)));
 const source='p cnf '+n+' '+children.flat().length+'\n'+children.flat().map(c=>c.join(' ')+' 0\n').join('');
 return {n,clauses:children.flat().length,source,projections:proj,
  child_sat:solutions.map(s=>s.length>0),parent_sat:combined.length>0,
  child_counts:solutions.map(s=>s.length),parent_count:combined.length};
}
const bad=build(false),good=build(true);
if(bad.n!==11||bad.clauses!==16||bad.parent_sat||!good.parent_sat||
 JSON.stringify(bad.projections)!=='[[1],[0]]'||JSON.stringify(good.projections)!=='[[1],[1]]'||
 JSON.stringify(bad.child_sat)!=='[true,true]')throw Error('semantic checkpoint failure');
const capacity=[256,1024,4096,65536].map(N=>({N,Q:Math.floor(N**.6),L:Math.floor(Math.sqrt(N)),
 bits:Math.floor(N**.6)*Math.floor(Math.sqrt(N)),padded_steps:N*N}));
for(const x of capacity)if(x.padded_steps<=x.bits)throw Error('capacity');
console.log(JSON.stringify({schema:'lspv2_428_replay',bad,good,capacity},null,2));

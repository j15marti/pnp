// LSPV-2/521 independent ES2022 scoped resolution/abstract CEGAR validator.
// A separate R_branch_res521 test model. NOT an R_mix341 checker.
import crypto from 'node:crypto';
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;const ok=(v,msg)=>{checks++;if(!v)throw Error(msg)};
function formula(q){
 let out=[];
 for(let v=0;v<4;v++){
  const inc=E.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
  for(let a=0;a<8;a++){
   const bs=[(a>>2)&1,(a>>1)&1,a&1];
   if((bs[0]^bs[1]^bs[2])!==q[v])out.push(inc.map((x,j)=>bs[j]?-x:x));
  }
 }
 return out;
}
function encode(cs){return 'T3|6|'+cs.length+'|'+cs.map(c=>c.join(',')).join('|')+'\n'}
function parse(s){
 if(!s.endsWith('\n'))throw Error('malformed');
 let p=s.slice(0,-1).split('|');
 if(p[0]!=='T3'||p[1]!=='6'||p[2]!=='16'||p.length!==19)throw Error('malformed');
 let cs=p.slice(3).map(c=>c.split(',').map(Number));
 if(cs.some(c=>c.length!==3||new Set(c.map(Math.abs)).size!==3||c.some(x=>!Number.isInteger(x)||Math.abs(x)<1||Math.abs(x)>6))||encode(cs)!==s)throw Error('malformed');
 return cs;
}
function models(cs){let out=[];
 for(let a=0;a<64;a++){
  let bits=E.map((_,i)=>(a>>i)&1);
  if(cs.every(c=>c.some(x=>bits[Math.abs(x)-1]===(x>0?1:0))))out.push(bits);
 }return out;
}
function scopedResolution(a,b,p){
 if(!a.c.includes(p)||!b.c.includes(-p))throw Error('bad-pivot');
 let g=[...a.ctx,...b.ctx];if(g.some(x=>g.includes(-x)))throw Error('bad-context');
 let c=[...new Set([...a.c.filter(x=>x!==p),...b.c.filter(x=>x!==-p)])];
 if(c.some(x=>c.includes(-x)))throw Error('tautological');
 return {c,ctx:[...new Set(g)]};
}
// Proposed E_XOR521: accept only four authentic facets encoding one 3-bit parity.
function fourFacetXor(cs){
 let ids=[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b);
 if(cs.length!==4||ids.length!==3||cs.some(c=>c.length!==3||c.some(x=>!ids.includes(Math.abs(x)))))throw Error('invalid facets');
 let found=[];
 for(let k=0;k<8;k++){
  let b=Array(6).fill(0);ids.forEach((id,j)=>b[id-1]=(k>>(2-j))&1);
  if(cs.every(c=>c.some(x=>b[Math.abs(x)-1]===(x>0?1:0))))found.push(ids.reduce((p,id)=>p^b[id-1],0));
 }
 if(found.length!==4||new Set(found).size!==1)throw Error('invalid facets');
 return {ids,parity:found[0]};
}
function algebra(cs){
 let r=[0,4,8,12].map(k=>fourFacetXor(cs.slice(k,k+4)));
 let acc=r[0];for(let i=1;i<4;i++){
  let b=r[i];
  acc={ids:acc.ids.filter(x=>!b.ids.includes(x)).concat(b.ids.filter(x=>!acc.ids.includes(x))),parity:acc.parity^b.parity};
 }
 ok(acc.ids.length===0,'parity cancellation');return acc.parity===1;
}
let tally={cases:0,sat:0,unsat:0,ghost_paths:0,replay_rejected:0,bad_pivots:0,malformed:0};
let fingerprints=[];
for(let n=0;n<16;n++){
 let q=[3,2,1,0].map(i=>(n>>i)&1),cs=formula(q),source=encode(cs);
 ok(JSON.stringify(parse(source))===JSON.stringify(cs),'source roundtrip');
 let m=models(cs),isSat=q.reduce((a,b)=>a+b,0)%2===0;
 ok(m.length===(isSat?8:0),'truth table');
 ok(algebra(cs)!==isSat,'GF2 control');
 tally.cases++;tally[isSat?'sat':'unsat']++;
 fingerprints.push({charge:q.join(''),sha256:crypto.createHash('sha256').update(source).digest('hex'),models:m.length});
 if(isSat)for(let x=1;x<=6;x++){
  ok(m.some(a=>a[x-1]===0)&&m.some(a=>a[x-1]===1),'both branch models');
  let a={c:[x],ctx:[x]},b={c:[-x],ctx:[-x]};
  tally.ghost_paths++; // ASSUME (+) 1, ASSUME (-) 1, ghost join 0, RES 1.
  try{scopedResolution(a,b,x);throw Error('unexpected');}
  catch(e){ok(e.message==='bad-context','scope replay');tally.replay_rejected++}
  try{scopedResolution(b,a,x);throw Error('unexpected');}
  catch(e){ok(e.message==='bad-pivot','orientation');tally.bad_pivots++}
 }
}
let base=encode(formula([0,0,0,0]));
for(let bad of [base.slice(0,-1),'X'+base.slice(1),base.replace('T3|6|16|','T3|6|15|'),base.replace('T3|6|16|','T3|06|16|'),base.replace('T3|6|16|','T3|6|016|'),base.replace(',','0,')]){
 try{parse(bad);throw Error('unexpected');}catch(e){ok(e.message==='malformed','bad source');tally.malformed++;}
}
ok(tally.cases===16&&tally.sat===8&&tally.unsat===8,'case count');
ok(tally.ghost_paths===48&&tally.replay_rejected===48&&tally.bad_pivots===48,'scope counts');
ok(tally.malformed===6,'malformed count');
console.log(JSON.stringify({status:'PASS',model:'R_branch_res521 (not historical R_mix341)',checks,tally,fingerprints},null,2));

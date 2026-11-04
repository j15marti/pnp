#!/usr/bin/env node
'use strict';
// Standalone public finite K4 source-typing audit, no dependencies.
let checks=0;
const ok=(b,m)=>{checks++;if(!b)throw Error('check '+checks+': '+m);};
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const vertex=v=>edges.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
const phi=charge=>{
 const all=[];
 for(let v=0;v<4;v++)for(let i=0;i<8;i++){
  const bits=[(i>>2)&1,(i>>1)&1,i&1];
  if((bits[0]^bits[1]^bits[2])===charge[v])continue;
  all.push(vertex(v).map((x,k)=>bits[k]?-x:x));
 }return all;
};
const val=(cl,a)=>cl.some(x=>x>0?!!a[x]:!a[-x]);
const sat=(f,a)=>f.every(c=>val(c,a));
const vars=Array.from({length:64},(_,q)=>Object.fromEntries(Array.from({length:6},(_,i)=>[i+1,!!(q&(1<<i))])));
const odd=phi([1,0,0,0]),even=phi([0,0,0,0]);
const gdef=(o,a,b)=>[[-o,a],[-o,b],[o,-a,-b]];
const D=[...gdef(7,1,2),...gdef(8,7,3),...gdef(9,8,4)];
const ext=x=>({...x,7:x[1]&&x[2],8:x[1]&&x[2]&&x[3],9:x[1]&&x[2]&&x[3]&&x[4]});
ok(odd.length===16&&even.length===16,'16 clauses per charge');
let o=0,e=0;
for(const x of vars){
 const y=ext(x);
 ok(sat(D,y),'conservative completion');
 ok(sat(odd,x)===sat([...odd,...D],y),'odd projection');
 ok(sat(even,x)===sat([...even,...D],y),'even projection');
 o+=sat(odd,x);e+=sat(even,x);
}
ok(o===0&&e===8,'odd/even models 0/8');
let nd=0,nf=0;
for(let j=0;j<odd.length;j++){
 const rest=odd.filter((_,k)=>j!==k);
 ok(vars.some(x=>sat(rest,x)),'clause deletion SAT');nd++;
 for(let k=0;k<3;k++){
  const m=odd.map(c=>c.slice());m[j][k]*=-1;
  ok(vars.some(x=>sat(m,x)),'sign flip SAT');nf++;
 }
}
const base={};for(let i=1;i<=6;i++)base[i]=new Set([i]);
for(const [o,a,b] of [[7,1,2],[8,7,3],[9,8,4]]){
 ok(!base[o]&&!!base[a]&&!!base[b],'fresh gate');
 base[o]=new Set([...base[a],...base[b]]);
}
const p=[[-9,8],[-9,4]];
const lexical=[...new Set(p.flat().map(Math.abs))].sort((a,b)=>a-b);
const support=[...new Set(lexical.flatMap(i=>[...base[i]]))].sort((a,b)=>a-b);
ok(JSON.stringify(lexical)==='[4,8,9]','untagged support 3');
ok(JSON.stringify(support)==='[1,2,3,4]','base support 4');
let mask=0;
for(let i=0;i<8;i++){
 const q={9:!!(i&4),8:!!(i&2),4:!!(i&1)};
 if(sat(p,q))mask|=1<<i;
}
ok(mask===143,'8-row mask');
const checkDefs=seq=>{
 const old=new Set([1,2,3,4,5,6]);
 for(const [o,a,b] of seq){if(old.has(o)||!old.has(a)||!old.has(b))return false;old.add(o);}
 return true;
};
ok(!checkDefs([[7,1,2],[7,7,3]]),'duplicate output rejected');
ok(!checkDefs([[7,8,2],[8,7,3]]),'forward reference rejected');
ok((mask^1)!==mask,'corrupt mask rejected');
console.log(JSON.stringify({result:'PASS',assertions:checks,odd_models:o,even_models:e,source_deletions:nd,sign_flips:nf,gate_definitions:3,gate_cnf_clauses:9,untagged_support:lexical.length,base_support:support.length,truth_mask:mask}));

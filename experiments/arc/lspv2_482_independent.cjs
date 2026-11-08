'use strict';
const assert=require('node:assert/strict');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;
function source(mask){
 const clauses=[];
 for(let v=0;v<4;v++){
  const ids=[];edges.forEach(([u,w],i)=>{if(u===v||w===v)ids.push(i+1)});
  for(let bits=0;bits<8;bits++){
   const parity=((bits&1)+((bits>>1)&1)+((bits>>2)&1))&1;
   if(parity===((mask>>v)&1))continue;
   clauses.push(ids.map((z,j)=>((bits>>j)&1)?-z:z));
  }
 }
 return 'p cnf 6 16\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');
}
function classify(text){
 const lines=text.trim().split('\n');
 if(lines.length!==17||lines[0].trim()!=='p cnf 6 16')return 'MALFORMED';
 const cs=[];
 for(const row of lines.slice(1)){
  const tokens=row.trim().split(/\s+/);
  if(tokens.length!==4||tokens[3]!=='0'||!tokens.slice(0,3).every(s=>/^-?\d+$/.test(s)))return 'MALFORMED';
  const c=tokens.slice(0,3).map(Number);
  if(!c.every(z=>Math.abs(z)>=1&&Math.abs(z)<=6)||new Set(c.map(z=>Math.abs(z))).size!==3)return 'MALFORMED';
  cs.push(c);
 }
 for(let a=0;a<64;a++)if(cs.every(c=>c.some(z=>((a>>(Math.abs(z)-1))&1)===(z>0?1:0))))return 'SAT';
 return 'UNSAT';
}
function strip(a){while(Array.isArray(a)&&a[0]==='PAD'&&Number.isInteger(a[1])&&a[1]>=0&&Number.isInteger(a[2])&&a[2]>=0)a=a[3];return a;}
function criterion(t4,s4,k,h){
 const T4=Math.max(t4,4*k,4*h),S4=Math.max(s4,4*h);
 const direct=(10*t4<=Math.max(44,24+5*T4))&&(2*s4<=Math.max(4,S4));
 const iff=(5*T4>=10*t4-24)&&(S4>=2*s4);
 return {direct,iff};
}
let sat=0,unsat=0;
for(let m=0;m<16;m++){
 const ans=classify(source(m));
 const parity=[0,1,2,3].reduce((s,j)=>s+((m>>j)&1),0)&1;
 assert.equal(ans,parity?'UNSAT':'SAT');checks++;
 assert.equal(strip(['PAD',9,8,['PAD',4,3,'CORE']]),'CORE');checks++;
 sat+=ans==='SAT';unsat+=ans==='UNSAT';
}
assert.equal(sat,8);assert.equal(unsat,8);checks+=2;
let x=source(0);
const bad=[x.replace('p cnf 6 16','p cnf 6 17'),x.replace(/ 0\n/,' 3\n'),x.replace('1 2 3','1 1 3'),'','not a CNF'];
for(let b of bad){assert.equal(classify(b),'MALFORMED');checks++;}
for(let t4=5;t4<=20;t4++)for(let s4=5;s4<=20;s4++)for(let k=0;k<10;k++)for(let h=0;h<10;h++){
 const z=criterion(t4,s4,k,h);assert.equal(z.direct,z.iff);checks++;
}
const examples=[[5,4,true],[4,3,false],[5,3,false],[4,4,false]];
for(let [k,h,v] of examples){assert.equal(criterion(12,8,k,h).direct,v);checks++;}
assert.equal(checks,25643);
console.log(JSON.stringify({status:'INDEPENDENT COMPUTATIONAL',checks,sat,unsat,malformed:bad.length,native_flmv:false,unrestricted_sat:false},null,2));

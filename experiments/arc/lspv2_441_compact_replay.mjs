#!/usr/bin/env node
// LSPV-2/441 executable finite control. This is NOT native logspace/FLMV code.
const assert = (ok, msg) => { if(!ok) throw Error(msg); checks++ };
let checks=0;
const data=[
 [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 [8,Array.from({length:8},(_,u)=>[0,1,2].map(k=>[u,u^(1<<k)]).filter(([a,b])=>a<b)).flat()],
 [10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+(i+2)%5]),...Array.from({length:5},(_,i)=>[i,5+i])]],
];
const xor=a=>a.reduce((x,y)=>x^y,0);
const edgeSort=(a,b)=>a[0]-b[0]||a[1]-b[1];
const nbrs=(H,E)=>Array.from({length:H},(_,u)=>E.flatMap(([a,b])=>a===u?[b]:b===u?[a]:[]).sort((a,b)=>a-b));
function source(H,E,c){
 const A=nbrs(H,E),wid=(3*H).toString(2).length;
 const id=(u,v)=>{const a=Math.min(u,v),b=Math.max(u,v);return 3*a+A[a].indexOf(b)+1};
 let s='11100011'+'1'.repeat(H)+'0'+'1'.repeat(3*H)+'0';
 for(let v=0;v<H;v++){
   const ids=A[v].map(u=>id(u,v)).sort((a,b)=>a-b);
   for(let m=0;m<8;m++){
     const b=[(m>>2)&1,(m>>1)&1,m&1];
     if(xor(b)!==c[v])s+=b.map((x,i)=>x+ids[i].toString(2).padStart(wid,'0')).join('');
   }
 }
 return s+'10';
}
function recognize(s){
 if(!/^[01]+$/.test(s)||!s.startsWith('11100011'))return 'MALFORMED';
 let i=8,H=0;while(s[i]==='1'){H++;i++}
 if(s[i++]!=='0'||H<4||H%2||s.slice(i,i+3*H)!=='1'.repeat(3*H)||s[i+3*H]!=='0')return 'MALFORMED';
 i+=3*H+1;const w=(3*H).toString(2).length;
 if(s.length!==i+12*H*(w+1)+2||!s.endsWith('10'))return 'MALFORMED';
 const ids=[],charge=[];
 for(let v=0;v<H;v++){
   const q=[];
   for(let row=0;row<4;row++){
     const z=[];
     for(let k=0;k<3;k++){
       const b=+s[i++],j=parseInt(s.slice(i,i+w),2);i+=w;
       if(!(j>=1&&j<=3*H))return 'MALFORMED';z.push([b,j]);
     }
     if(new Set(z.map(x=>x[1])).size!==3)return 'MALFORMED';
     q.push(z);
   }
   const z=q[0].map(x=>x[1]);
   if(z.some((x,k)=>k&&z[k-1]>=x)||q.some(row=>row.some((x,k)=>x[1]!==z[k])))return 'OUTSIDE';
   const ch=1^xor(q[0].map(x=>x[0]));let p=0;
   for(let m=0;m<8;m++){const b=[(m>>2)&1,(m>>1)&1,m&1];
     if(xor(b)!==ch){if(q[p++].some((x,k)=>x[0]!==b[k]))return 'OUTSIDE'}
   }
   ids.push(z);charge.push(ch);
 }
 const A=[];
 for(let u=0;u<H;u++){
   const a=[];for(const j of ids[u]){
     const hits=ids.flatMap((row,v)=>row.includes(j)?[v]:[]);
     if(hits.length!==2||!hits.includes(u))return 'OUTSIDE';
     a.push(hits[0]===u?hits[1]:hits[0]);
   }
   if(new Set(a).size!==3||a.includes(u))return 'OUTSIDE';
   A.push(a.sort((x,y)=>x-y));
 }
 for(let u=0;u<H;u++){
   const mapped=A[u].map(v=>{const a=Math.min(u,v),b=Math.max(u,v);return 3*a+A[a].indexOf(b)+1}).sort((x,y)=>x-y);
   if(JSON.stringify(mapped)!==JSON.stringify(ids[u])||A[u].some(v=>!A[v].includes(u)))return 'OUTSIDE';
 }
 const E=[];for(let v=0;v<H;v++)for(const u of A[v])if(v<u)E.push([v,u]);E.sort(edgeSort);
 const seen=new Set(),comp=[];
 for(let v=0;v<H;v++)if(!seen.has(v)){
   const todo=[v],members=[];seen.add(v);
   for(const u of todo){members.push(u);for(const z of A[u])if(!seen.has(z)){seen.add(z);todo.push(z)}}
   comp.push(xor(members.map(z=>charge[z])));
 }
 return comp.some(Boolean)?'UNSAT':'SAT';
}
for(const [H,E] of data){for(const parity of [0,1]){
 const c=Array(H).fill(0);c[0]=parity;const s=source(H,E,c);
 assert(recognize(s)===(parity?'UNSAT':'SAT'),'connected parity');
 assert(recognize('0'+s.slice(1))==='MALFORMED','bad magic');
 const start=8+(H+1)+(3*H+1);
 assert(recognize(s.slice(0,start)+(s[start]==='0'?'1':'0')+s.slice(start+1))==='OUTSIDE','sign forged');
}}
const K4=data[0][1],E=[...K4,...K4.map(([a,b])=>[a+4,b+4])];
for(const [a,b,answer] of [[0,0,'SAT'],[1,0,'UNSAT'],[1,1,'UNSAT']]){
 const c=Array(8).fill(0);c[0]=a;c[4]=b;
 assert(recognize(source(8,E,c))===answer,'disconnected parity');
}
console.log(JSON.stringify({run:'LSPV-2/441 compact source-only signed Tseitin controls',checks,source_cases:9,classification:'FINITE HOST SEMANTICS ONLY'}));

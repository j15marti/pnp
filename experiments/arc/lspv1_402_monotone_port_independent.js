#!/usr/bin/env node
/* Independent signed-CNF-to-monotone-port verification. Node.js built-ins only. */
const fs=require('fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;function ok(cond,label){if(!cond)throw Error(label);checks++}
function valid(F,n){return Number.isInteger(n)&&n>0&&Array.isArray(F)&&F.every(c=>Array.isArray(c)&&c.length>=1&&c.length<=3&&c.every(v=>Number.isInteger(v)&&v!==0&&Math.abs(v)<=n)&&new Set(c.map(Math.abs)).size===c.length)}
function satCount(F,n){let c=0;for(let b=0;b<(1<<n);b++){let good=F.every(C=>C.some(l=>{let v=!!(b&(1<<(Math.abs(l)-1)));return l>0?v:!v}));if(good)c++}return c}
function port(F,n,flags,t){let g=true,h=false;for(let i=0;i<n;i++){let a=!!(flags&(1<<i)),b=!!(flags&(1<<(n+i)));g=g&&(a||b);h=h||(a&&b)}for(const clause of F){let allwrong=clause.every(l=>{let j=Math.abs(l)-1;return !!(flags&(1<<(l>0?n+j:j)))});h=h||allwrong}return h||(t&&g)}
let cls=[];for(let u=-1;u<=1;u++)for(let v=-1;v<=1;v++){let C=[];if(u)C.push(u*1);if(v)C.push(v*2);if(C.length)cls.push(C)}
ok(JSON.stringify(cls)===JSON.stringify(raw.clauses),'original clause order');
let sat=0,unsat=0;
for(let mask=0;mask<256;mask++){
 const F=cls.filter((_,i)=>mask&(1<<i));const count=satCount(F,2);
 const row=raw.rows[mask];ok(row.mask===mask,'row mask');ok(count===row.models,'model count');
 let ess=false,w=null;
 for(let flags=0;flags<16;flags++){
  let a=port(F,2,flags,0),b=port(F,2,flags,1);ok(!a||b,'port monotonicity');
  if(!a&&b&&!ess){ess=true;w=Array.from({length:4},(_,i)=>(flags>>i)&1).join('')}
 }
 ok(ess===row.essential,'essentiality');
 ok((w===null)===(row.witness===null),'witness presence'); if(row.witness!==null){let vv=[...row.witness].map(Number);let ff=vv.reduce((s,b,i)=>s|(b<<i),0);ok(!port(F,2,ff,0)&&port(F,2,ff,1),'published witness independently checks')}
 if(ess){let flags=[...w].map(Number);ok(flags[0]+flags[2]===1 && flags[1]+flags[3]===1,'coherent signs')}
 sat+=count>0?1:0;unsat+=count===0?1:0;
}
ok(sat===95&&unsat===161&&raw.sat_count===sat&&raw.unsat_count===unsat,'label totals');
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
function parityF(charges){const F=[];for(let v=0;v<4;v++){const inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let b=0;b<8;b++){let p=0,C=[];for(let j=0;j<3;j++){let bit=(b>>j)&1;p+=bit;C.push(bit?-inc[j]:inc[j])}if(p%2!==charges[v])F.push(C)}}return F}
for(const [i,charges] of [[0,[0,0,0,0]],[1,[1,0,0,0]]]){
 const F=parityF(charges);let count=satCount(F,6), essential=false;
 for(let v=0;v<4096;v++){if(port(F,6,v,1) && !port(F,6,v,0)){essential=true;break}}
 ok(raw.parity[i].models===count && raw.parity[i].essential===essential,'K4 port controls');
}
const corrupt=JSON.parse(JSON.stringify(raw));corrupt.rows[5].essential=!corrupt.rows[5].essential;
ok(corrupt.rows[5].essential!==raw.rows[5].essential,'detect modified essential flag');
const corrupt2=JSON.parse(JSON.stringify(raw));corrupt2.rows[17].models++;
ok(corrupt2.rows[17].models!==satCount(cls.filter((_,i)=>17&(1<<i)),2),'detect forged model count');
const malformed=[[[[]],2],[[[0]],2],[[[3]],2],[[[1,-1]],2],[[[1,2,1]],2],[[[1]],0]];
for(let [F,n] of malformed)ok(!valid(F,n),'invalid source');
console.log(JSON.stringify({independent_assertions:checks,configs:256,labels:[sat,unsat],k4:[raw.parity[0].models,raw.parity[1].models],tamper_checks:2}));

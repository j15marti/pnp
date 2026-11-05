#!/usr/bin/env node
// LSPV-4/420 independent compact exact replay of published graph matrices.
// The large Python producer and second independent referee are in the ZIP.
// No input from GitHub's report is trusted as a theorem.
const fixtures=[
 {name:'K4/even/all',cols:[3,5,9,6,10,12],u:0,width:5,sat:8},
 {name:'K4/odd/all',cols:[3,5,9,6,10,12],u:1,width:1,sat:0},
 {name:'cube/even/all',cols:[3,9,17,6,130,12,68,40,48,144,96,192],u:3,width:9,sat:32},
 {name:'cube/odd/all',cols:[3,9,17,6,130,12,68,40,48,144,96,192],u:1,width:1,sat:0}
];
let checks=0;
function ok(condition,label){checks++;if(!condition)throw new Error(label);}
function span(columns){let a=new Set([0]);for(const v of columns){for(const x of [...a])a.add(x^v);}return a;}
function accepts(cols,u,a){let b=u;for(let i=0;i<cols.length;i++)if(Math.floor(a/2**i)%2)b^=cols[i];return b===0;}
function cut(cols,u,j){
 const n=cols.length;
 let futures=new Set();
 for(let p=0;p<2**j;p++){
  let f='';
  for(let q=0;q<2**(n-j);q++)f+=accepts(cols,u,p+q*2**j)?'1':'0';
  futures.add(f);
 }
 return {total:futures.size,live:[...futures].filter(x=>x.includes('1')).length};
}
for(const obj of fixtures){
 const k=obj.cols.length, rank=Math.log2(span(obj.cols).size);
 const consistent=span(obj.cols).has(obj.u);
 ok(Number.isInteger(rank),obj.name);
 let models=0,width=0;
 for(let a=0;a<2**k;a++)models+=Number(accepts(obj.cols,obj.u,a));
 ok(models===obj.sat,obj.name+' model count');
 for(let j=0;j<=k;j++){
  let rp=Math.log2(span(obj.cols.slice(0,j)).size);
  let rq=Math.log2(span(obj.cols.slice(j)).size);
  const d=rp+rq-rank;
  const expLive=consistent?2**d:0;
  const expTotal=consistent?expLive+Number(d<rp):1;
  const observed=cut(obj.cols,obj.u,j);
  ok(observed.live===expLive,obj.name+' live cut '+j);
  ok(observed.total===expTotal,obj.name+' total cut '+j);
  width=Math.max(width,observed.total);
 }
 ok(width===obj.width,obj.name+' max width');
}
console.log(JSON.stringify({status:'PASS',checks,fixtures:fixtures.length}));

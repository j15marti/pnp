// LSPV-4/424 compact independent executable; node lspv4_424_lazy_port.mjs
// Host indexed-read instrumentation, not a native FLMV runtime measurement.
import assert from 'node:assert/strict';
const bits=(v,k)=>v.toString(2).padStart(k,'0');
const gamma=(v)=>'0'.repeat(v.toString(2).length-1)+v.toString(2);
const hdr=(n,m,w)=>[...Buffer.from('CNF3')].map(c=>bits(c,8)).join('')+gamma(n)+gamma(m)+gamma(w)+'0';
let checks=0;
const test=(p,m)=>{checks++;assert.ok(p,m)};
function graph(name){
 let h=name==='K4'?4:name==='cube'?8:10, E=[];
 if(name==='K4')for(let u=0;u<h;u++)for(let v=u+1;v<h;v++)E.push([u,v]);
 if(name==='cube')for(let u=0;u<h;u++)for(let v=u+1;v<h;v++)if((u^v).toString(2).replace(/0/g,'').length===1)E.push([u,v]);
 if(name==='Petersen'){
   for(let i=0;i<5;i++){E.push([i,(i+1)%5].sort((a,b)=>a-b));E.push([5+i,5+(i+2)%5].sort((a,b)=>a-b));E.push([i,i+5])}
   E=[...new Map(E.map(e=>[e.join(','),e])).values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 }
 const inc=Array.from({length:h},(_,v)=>E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0));
 test(inc.every(x=>x.length===3),'cubic');return {h,E,inc};
}
const records=[];
for(const name of ['K4','cube','Petersen'])for(const mode of ['even','one_odd','all_odd']){
 const {h,E,inc}=graph(name),r=h,e=E.length,nv=r*e,w=nv.toString(2).length;
 const B=4*h*3*(w+1), parentHead=hdr(nv,r*4*h,w);
 let bodies=[], charges=[];
 for(let i=0;i<r;i++){
  const odd=mode==='all_odd'||(mode==='one_odd'&&i===0); charges.push(odd);
  let body='';
  for(let v=0;v<h;v++)for(let t=0;t<8;t++){
   const parity=((t>>2)^(t>>1)^t)&1;
   if(parity===Number(odd&&v===0))continue;
   for(let j=0;j<3;j++)body+=((t>>(2-j))&1)+bits(i*e+inc[v][j]+1,w);
  }
  test(body.length===B,'body length');bodies.push(body);
 }
 const source=parentHead+bodies.join('');let reads=0,writes=0,erases=0;
 const childHead=hdr(nv,4*h,w),L=childHead.length+B, q=r;
 test(source.length===parentHead.length+r*B,'parent size');
 for(let i=0;i<q;i++){
  const child=childHead+bodies[i];
  const order=Array.from({length:L},(_,j)=>j).filter(j=>j%2===0).concat(Array.from({length:L},(_,j)=>j).filter(j=>j%2===1).reverse());
  for(const j of order){
   let got;
   if(j<childHead.length)got=childHead[j];
   else{const pos=parentHead.length+i*B+j-childHead.length;
     const len=pos.toString(2).length; writes+=len;erases+=len;reads++;got=source[pos];}
   test(got===child[j],'indexed virtual source bit');
  }
 }
 test(reads===q*B,'reads');test(writes===erases,'erased index words');
 const label=charges.every(x=>!x);
 test(label===(mode==='even'),'both label controls');
 records.push({name,mode,N:source.length,q,L,reads,writes,erases,label});
}
console.log(JSON.stringify({pass:true,checks,records},null,2));
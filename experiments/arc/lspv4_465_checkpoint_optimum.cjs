#!/usr/bin/env node
"use strict";
/* LSPV-4/465 static checkpoint anchor optimum. Abstract indexed-header probes,
   not an instruction-level FLMV simulator. Finite signed proper-3CNF controls. */
let checks=0;
function ok(c,m){if(!c)throw Error("FAIL "+m);checks++}
const bits=(n,k)=>n.toString(2).padStart(k,"0"),val=s=>parseInt(s,2);
function make(h){
 let src="",offsets=[],payloads=[];
 for(let v=0;v<h;v++){
  const off=src.length;let payload="";
  for(let c=0;c<1+v%3;c++)for(let j=0;j<3;j++)
   payload+=((v+c+j)%2?"1":"0")+bits(1+9*v+3*c+j,16);
  offsets.push(off);payloads.push(payload);src+=bits(payload.length,16)+payload;
 }
 return {src,offsets,payloads,h};
}
function header(src,p){
 if(p<0||p+16>src.length)throw Error("header truncated");
 let n=val(src.slice(p,p+16));
 if(n<1||n%51||p+16+n>src.length)throw Error("header malformed");
 return n;
}
function parse(f){
 let p=0,out=[];
 for(let i=0;i<f.h;i++){
  const n=header(f.src,p);out.push(p);
  for(let z=0;z<n;z+=51){
   let ids=[];
   for(let j=0;j<3;j++){
    const lit=f.src.slice(p+16+z+j*17,p+16+z+(j+1)*17);
    if(!/^[01]{17}$/.test(lit))throw Error("literal malformed");
    const id=val(lit.slice(1));
    if(!id||ids.includes(id))throw Error("not proper 3CNF");
    ids.push(id);
   }
  }
  p+=16+n;
 }
 if(p!==f.src.length)throw Error("trailing data");
 return out;
}
function layout(h,m){
 if(!Number.isInteger(m)||m<1||m>h)throw Error("bad m");
 let a=Math.floor(h/m),r=h%m,starts=[],x=0;
 for(let j=0;j<m;j++){starts.push(x);x+=a+(j<r?1:0)}
 return {a,r,starts};
}
function block(v,p){
 const z=p.r*(p.a+1);
 return v<z?Math.floor(v/(p.a+1)):p.r+Math.floor((v-z)/p.a);
}
function locate(f,v,p){
 const j=block(v,p),start=p.starts[j];let addr=p.addresses[j],reads=0;
 for(let k=start;k<v;k++){addr+=16+header(f.src,addr);reads++}
 return {addr,reads};
}
function opt(h,m){
 const a=Math.floor(h/m),r=h%m;
 return (m-r)*a*(a-1)/2+r*(a+1)*a/2;
}
function brute(h,m){
 let best=Infinity;
 function rec(left,g,c){
  if(g===1){best=Math.min(best,c+left*(left-1)/2);return}
  for(let x=1;x<=left-g+1;x++)rec(left-x,g-1,c+x*(x-1)/2);
 }rec(h,m,0);return best;
}
function post(v,h,out){
 if(v>=h)return;
 post(2*v+1,h,out);post(2*v+2,h,out);out.push(v);
}
function k4(charge){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],clauses=[];
 for(let v=0;v<4;v++){
  let e=edges.map((x,i)=>x.includes(v)?i:-1).filter(x=>x>=0);
  for(let q=0;q<8;q++){
   let b=e.map((_,j)=>(q>>j)&1);
   if(b.reduce((x,y)=>x^y,0)===charge[v])continue;
   clauses.push(e.map((idx,j)=>b[j]?-(idx+1):idx+1));
  }
 }return clauses;
}
function count(cs){
 let ans=0;
 for(let a=0;a<64;a++)
  if(cs.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))ans++;
 return ans;
}
function run(){
 let results=[],lookups=0,reads=0,virtualBits=0,partitions=0;
 for(let h of [3,7,15,31,63,127,255,511]){
  let f=make(h),oracle=parse(f),order=[];post(0,h,order);
  ok(order.length===h,"postorder count");
  const budgets=[...new Set([1,2,4,8,16,32,64,h])].filter(m=>m<=h);
  for(let m of budgets){
   let p=layout(h,m);p.addresses=p.starts.map(v=>oracle[v]);
   let q=0;
   for(let v of order){
    const x=locate(f,v,p);q+=x.reads;reads+=x.reads;lookups++;
    ok(x.addr===oracle[v],"source base");
    let n=header(f.src,x.addr);
    ok(f.src.slice(x.addr+16,x.addr+16+n)===f.payloads[v],"original payload");
    for(let call=0;call<3;call++)for(let b of [0,1,16,32,n-1]){
     ok(f.src[x.addr+16+b]===f.payloads[v][b],"cached guest bit");
     virtualBits++;
    }
   }
   ok(q===opt(h,m),"exact optimal probes");
   let S=m*Math.ceil(Math.log2(f.src.length+1));
   results.push({h,m,sourceBits:f.src.length,lookupHeaderProbes:q,anchorBits:S});
  }
 }
 for(let h=2;h<=10;h++)for(let m=1;m<=h;m++){
  ok(brute(h,m)===opt(h,m),"global composition optimum");partitions++;
 }
 const even=k4([0,0,0,0]),odd=k4([1,0,0,0]);
 ok(even.length===16&&odd.length===16,"proper parity source count");
 ok(count(even)===8&&count(odd)===0,"both labels");
 ok([...even,...odd].every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper 3CNF");
 let f=make(15),err=0;
 try{parse({...f,src:"1111111111111111"+f.src.slice(16)})}catch(e){err++}
 try{parse({...f,src:f.src.slice(0,33)+f.src.slice(16,33)+f.src.slice(50)})}catch(e){err++}
 try{layout(15,0)}catch(e){err++}
 ok(err===3,"malformed controls");
 return {label:"LSPV4_465",status:"PASS",checks,partitions,sourceInstances:8,
  budgetConfigurations:results.length,lookups,lookupHeaderProbes:reads,
  cachedVirtualBitReads:virtualBits,corruptControls:err,
  parityControls:{evenK4Models:8,oddK4Models:0},
  samples:results.filter(r=>[127,511].includes(r.h)&&[1,8,32,r.h].includes(r.m))};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));

#!/usr/bin/env node
// LSPV-4/430 compact standalone decisive-control replay.
// Tests source-bound witness pivots, distinct from general SAT hardness.
import assert from 'node:assert/strict';
const magic='11011010',un=n=>'1'.repeat(n)+'0',width=n=>Math.max(1,n.toString(2).length);
let assertions=0;
function ok(x,m){assert.ok(x,m);assertions++}
function encode(nx,ny,h,core,tail){
 const lit=([ns,i,sgn])=>String(ns)+String(sgn)+i.toString(2).padStart(width(ns?ny:nx),'0');
 return magic+un(nx)+un(ny)+h.join('')+core.map(c=>'10'+c.map(lit).join('')).join('')+tail.map(c=>'11'+c.map(lit).join('')).join('')+'00';
}
function verify(b){
 if(!/^[01]+$/.test(b)||!b.startsWith(magic))throw Error('magic');
 let p=magic.length;
 function unary(){let k=0;while(b[p]==='1'){p++;k++}if(!k||b[p++]!=='0')throw Error('unary');return k}
 const nx=unary(),ny=unary(),W=[width(nx),width(ny)];
 if(p+ny>b.length)throw Error('h');
 const h=b.slice(p,p+ny).split('').map(Number);p+=ny;
 let core=0,tails=0,cut=null,tailSeen=false;
 while(true){
  if(p+2>b.length)throw Error('tag');const tag=b.slice(p,p+2);p+=2;
  if(tag==='00'){if(p!==b.length||!core)throw Error('trailing/empty');return {core,tails,cut:cut??p-2}}
  if(tag!=='10'&&tag!=='11'||tag==='10'&&tailSeen)throw Error('order');
  if(tag==='11'&&!tailSeen){cut=p-2;tailSeen=true}
  const seen=new Set();let witnessed=false;
  for(let j=0;j<3;j++){
   if(p+2>b.length)throw Error('literal');const ns=Number(b[p++]),s=Number(b[p++]);
   if(p+W[ns]>b.length)throw Error('index');
   const i=parseInt(b.slice(p,p+W[ns]),2);p+=W[ns];
   if(i<1||i>(ns?ny:nx)||seen.has(ns+':'+i))throw Error('duplicate/range');
   seen.add(ns+':'+i);
   if(tag==='10'&&ns)throw Error('private core');
   if(ns&&(h[i-1]^s)===1)witnessed=true;
  }
  if(tag==='11'){if(!witnessed)throw Error('uncovered');tails++}else core++;
 }
}
// A proper, fixed satisfying core; certification costs do not depend on whether core is hard.
const core=[[[0,1,0],[0,2,0],[0,3,0]]], nx=3,ny=4,h=[1,1,1,1];
let pivotal=0;
for(const [q,k] of [[4,8],[8,32],[16,64]]){
 for(let t=0;t<q;t++){
  const tail=Array.from({length:k},(_,j)=>[[1,j%4+1,0],[0,1,(t+j)%2],[0,2,Math.floor((t+j)/2)%2]]);
  const bits=encode(nx,ny,h,core,tail);ok(verify(bits).tails===k,'valid source');
  const prefix=bits.indexOf('11',magic.length+nx+1+ny+1+ny); // first tail tag after core
  const stride=2+(2+width(ny))+2*(2+width(nx));
  for(let j=0;j<k;j++){
   const pos=prefix+j*stride+3;ok(bits[pos]==='0','witness sign');
   const changed=bits.slice(0,pos)+'1'+bits.slice(pos+1);
   let rejected=false;try{verify(changed)}catch{rejected=true}
   ok(rejected,'pivotal mutation must reject');pivotal++;
  }
 }
}
console.log(JSON.stringify({assertions,pivotal,scope:'independent certificate validation only',PvsNP:'OPEN'}));

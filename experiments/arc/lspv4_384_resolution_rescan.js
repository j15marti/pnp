'use strict';
const assert=require('assert');
const norm=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
function verify(F,P){
 if(!Number.isSafeInteger(F.n)||F.n<0||!Array.isArray(F.c)||!Array.isArray(P)||!P.length)throw Error('grammar');
 const ok=c=>Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=F.n)&&new Set(c).size===c.length&&!c.some(x=>c.includes(-x))&&JSON.stringify(c)===JSON.stringify(norm(c));
 if(!F.c.every(ok))throw Error('source');
 const D=[];let q=0;
 for(const r of P){
  if(r.kind==='s'){
   if(!Number.isInteger(r.index)||r.index<0||r.index>=F.c.length||JSON.stringify(r.c)!==JSON.stringify(F.c[r.index]))throw Error('source reference');
  }else if(r.kind==='r'){
   if(![r.a,r.b].every(z=>Number.isInteger(z)&&z>=0&&z<D.length))throw Error('future reference');
   const A=D[r.a],B=D[r.b];
   if(!Number.isInteger(r.v)||r.v<=0||!A.includes(r.v)||!B.includes(-r.v))throw Error('pivot');
   const C=norm([...new Set([...A.filter(z=>z!==r.v),...B.filter(z=>z!==-r.v)])]);
   if(C.some(z=>C.includes(-z))||JSON.stringify(r.c)!==JSON.stringify(C))throw Error('inference');
   q++;
  }else throw Error('node');
  if(!ok(r.c))throw Error('conclusion grammar');
  D.push(r.c);
 }
 if(D.at(-1).length)throw Error('nonempty conclusion');
 return q;
}
function horn(k){
 const c=[[1]];for(let j=1;j<=k;j++)c.push([-j,j+1]);c.push([-(k+1)]);
 const F={n:k+1,c:c.map(norm)},P=c.map((x,i)=>({kind:'s',index:i,c:x}));let prev=0;
 for(let j=1;j<=k+1;j++){P.push({kind:'r',a:prev,b:j,v:j,c:j<=k?[j+1]:[]});prev=P.length-1;}
 return [F,P];
}
let checks=0;
for(let k=0;k<=256;k++){const [f,p]=horn(k);assert.equal(verify(f,p),k+1);checks++;
 const x=JSON.parse(JSON.stringify(p));x.at(-1).v=k+3;assert.throws(()=>verify(f,x));checks++;
 const y=JSON.parse(JSON.stringify(p));y.at(-1).a=y.length+1;assert.throws(()=>verify(f,y));checks++;}
for(const bad of [[1,1],[1,-1],[0],[-1,1]]){assert.throws(()=>verify({n:1,c:[bad]},[{kind:'s',index:0,c:bad}]));checks++;}
assert.equal(verify({n:0,c:[[]]},[{kind:'s',index:0,c:[]}]),0);checks++;
console.log(JSON.stringify({assertions:checks,horn_chains:257,malformed:4,errors:0}));

#!/usr/bin/env node
'use strict';
// Independent LSPV1-478 polynomial-ring identity and alias audit, without Python/shared code.
const crypto=require('crypto');
const primes=[2,3,5,7];let checks=0,negativeRejections=0;
function poly(p,terms){let z=new Map();for(let [mon,c] of terms){let key=mon.slice().sort((a,b)=>a-b).join('.');let v=((z.get(key)||0)+c)%p;if(v<0)v+=p;v?z.set(key,v):z.delete(key)}return z}
const cn=(p,a)=>poly(p,[[[],a]]), vr=(p,i)=>poly(p,[[[i],1]]);
function plus(p,a,b,ca=1,cb=1){return poly(p,[...Array.from(a.entries()).map(([k,v])=>[k?k.split('.').map(Number):[],ca*v]),...Array.from(b.entries()).map(([k,v])=>[k?k.split('.').map(Number):[],cb*v])]);}
function times(p,a,b){let terms=[];for(let [aK,aV] of a)for(let [bK,bV] of b)terms.push([[...(aK?aK.split('.').map(Number):[]),...(bK?bK.split('.').map(Number):[])],aV*bV]);return poly(p,terms)}
function lit(p,x){return x>0?vr(p,x):plus(p,cn(p,1),vr(p,-x),1,-1)}
function falsity(p,clause){return clause.reduce((acc,x)=>times(p,acc,plus(p,cn(p,1),lit(p,x),1,-1)),cn(p,1))}
function alias(p,a,m){return poly(p,Array.from(a).map(([key,v])=>[(key?key.split('.').map(Number):[]).map(z=>m[z]||z),v]));}
function equal(a,b){return a.size===b.size&&[...a].every(([k,v])=>b.get(k)===v)}
for(let p of primes){for(let mask=0;mask<8;mask++){
 let C=[1,2,3].map((x,i)=>mask&(1<<i)?-x:x);
 let a=4, alpha=C[2]>0?a:-a, P=[C[0],C[1],alpha],Q=[C[0],C[2],-alpha], sigma={[a]:3};
 let pc=falsity(p,C), pp=falsity(p,P),pq=falsity(p,Q);
 if(!equal(alias(p,pp,sigma),pc))throw Error('source alias');checks++;
 let bool=plus(p,times(p,vr(p,3),vr(p,3)),vr(p,3),1,-1);
 let rhs=times(p,plus(p,cn(p,1),lit(p,C[0]),1,-1),bool);
 if(!equal(alias(p,pq,sigma),plus(p,cn(p,0),rhs,0,-1)))throw Error('Q axiom');checks++;
 let recon=plus(p,times(p,pp,plus(p,cn(p,1),lit(p,C[2]),1,-1)),times(p,pq,plus(p,cn(p,1),lit(p,C[1]),1,-1)));
 if(!equal(recon,pc))throw Error('reconstruct');checks++;
 let malformedP=[C[0],C[1],-alpha];
 if(!equal(alias(p,falsity(p,malformedP),sigma),pc))negativeRejections++;checks++;
 for(let x0=0;x0<2;x0++)for(let x1=0;x1<2;x1++)for(let x2=0;x2<2;x2++){
  let asg={1:x0,2:x1,3:x2};
  let val=t=>t>0?asg[t]:1-asg[-t];
  let source=C.some(t=>val(t)===1), split=false;
  for(let z=0;z<2;z++){asg[4]=z;if(P.some(t=>val(t)===1)&&Q.some(t=>val(t)===1))split=true}
  if(source!==split)throw Error('equisatisfiable');checks++;
 }
 }}
if(negativeRejections!==32)throw Error('expected 32 negative rejections');
let blowup=[];
for(let k=1;k<=12;k++){let p=3,f=cn(p,1);for(let i=1;i<=k;i++)f=times(p,f,plus(p,cn(p,1),vr(p,i),1,-1));if(f.size!==2**k)throw Error('blowup');blowup.push(f.size);checks++;}
console.log(JSON.stringify({id:'LSPV1-478',checker:'independent JS polynomial-ring identities and Boolean witnesses',checks,negative_rejections:negativeRejections,blowup,script_sha256:crypto.createHash('sha256').update(require('fs').readFileSync(__filename)).digest('hex')},null,2));

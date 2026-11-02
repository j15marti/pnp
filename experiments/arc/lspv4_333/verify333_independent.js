#!/usr/bin/env node
/* Independent no-producer-import exact source and transfer referee for LSPV4 333. */
'use strict';
const A=require('node:assert/strict');
let tests=0;function check(x,m){tests++;A.ok(x,m);}
const B=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
const Z=[...B,...B.map(c=>c.map(v=>-v))];
const val=(a,i)=>(a>>>(i-1))&1;
const sat=(f,a)=>f.every(c=>c.some(v=>val(a,Math.abs(v))===(v>0?1:0)));
function chain(t){
 let f=[];for(let i=0;i<t;i++)for(const c of Z)f.push(c.map(v=>Math.sign(v)*(Math.abs(v)+6*i)));
 for(let i=0;i<t-1;i++){const a=8*i+1,b=8*(i+1),v=f[a][1];f[a][1]=f[b][0];f[b][0]=v;}
 return f;
}
function canonical(f,n){
 if(n<1||n%3||3*f.length!==4*n)return false;
 const seen=new Set(),counts=new Map();
 for(const c of f){
  if(c.length!==3||new Set(c.map(Math.abs)).size!==3)return false;
  if(c.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>n))return false;
  if(!(c.every(v=>v>0)||c.every(v=>v<0)))return false;
  let key=c.slice().sort((a,b)=>a-b).join('/');
  if(seen.has(key))return false;seen.add(key);
  for(const v of c)counts.set(v,(counts.get(v)||0)+1);
 }
 for(let i=1;i<=n;i++)if(counts.get(i)!==2||counts.get(-i)!==2)return false;
 return true;
}
function connected(f,n){
 let adj=Array.from({length:n},()=>new Set());
 for(const c of f)for(const a of c)for(const b of c)adj[Math.abs(a)-1].add(Math.abs(b)-1);
 let seen=new Set([0]),q=[0];
 for(let j=0;j<q.length;j++)for(const k of adj[q[j]])if(!seen.has(k)){seen.add(k);q.push(k);}
 return seen.size===n;
}
const H=a=>Z.slice(2).every(c=>c.some(v=>val(a,Math.abs(v))===(v>0?1:0)));
const sig=a=>4*val(a,1)+2*val(a,4)+val(a,5);
const Cin=a=>val(a,1)||val(a,2)||val(a,3);
const valid=[];for(let a=0;a<64;a++)if(H(a))valid.push(a);
check(valid.length===27,'H count');
const v=Array(8).fill(0n),u=Array.from({length:8},(_,r)=>BigInt(!!((r&4)||(r&2)||(r&1))));
const M=Array.from({length:8},()=>Array(8).fill(0n));
for(const a of valid)if(Cin(a))v[sig(a)]++;
for(let r=0;r<8;r++)for(const b of valid){
 let a1=(r>>2)&1,a4=(r>>1)&1,a5=r&1;
 if((a1||val(b,1)||a5)&&(a4||val(b,2)||val(b,3)))M[r][sig(b)]++;
}
check(v.map(String).join(',')==='4,3,3,3,3,3,3,0','initial vector');
function mul(w){return Array.from({length:8},(_,j)=>w.reduce((sum,x,i)=>sum+x*M[i][j],0n));}
const w1=mul(v),w2=mul(w1),w3=mul(w2);
for(let j=0;j<8;j++)check(w3[j]-15n*w2[j]-50n*w1[j]+36n*v[j]===0n,'annihilator');
let w=v,seq=[];
for(let t=1;t<=12;t++){seq.push(w.reduce((sum,x,i)=>sum+x*u[i],0n));w=mul(w);}
check(seq.slice(0,5).map(String).join(',')==='18,318,5630,99702,1765582','recurrence seeds');
for(let t=0;t<9;t++)check(seq[t+3]===15n*seq[t+2]+50n*seq[t+1]-36n*seq[t],'recurrence');
let brute={},rows=0;
for(let t=1;t<=3;t++){
 const f=chain(t),n=6*t;
 check(canonical(f,n)&&connected(f,n),'canonical connected');
 let ct=0;for(let a=0;a<(1<<n);a++){if(sat(f,a))ct++;rows++;}
 brute[t]=ct;check(BigInt(ct)===seq[t-1],'exact source count');
}
const orig=[...Z,...Z.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+6)))],F=chain(2);
let o=0,z=0,both=0,less=0,more=0,yes=0,no=0;
for(let a=0;a<4096;a++){
 let q=sat(orig,a),r=sat(F,a);
 if(q)o++;if(r)z++;if(q&&r)both++;if(q&&!r)less++;if(!q&&r)more++;
 if(r&&val(a,2)===1&&val(a,4)===1){if(val(a,1)===0)yes++;else no++;}
}
check(o===324&&z===318&&both===270&&less===54&&more===48,'semantic nonpreservation');
check(yes===53&&no===0,'same original opposite labels');
// Exact original-clause extremal S/U constraints, compared with brute assignments.
let modes=0;
for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++)
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  const demand=new Map();let possible=true;
  for(const [c,s] of [[F[i],x],[F[j],y]])for(const lit of c){
   let q=(lit>0?1:0)^s,k=Math.abs(lit);
   if(demand.has(k)&&demand.get(k)!==q)possible=false;
   demand.set(k,q);
  }
  let observed=false;
  for(let a=0;a<4096;a++){
   const match=(c,s)=>c.every(lit=>val(a,Math.abs(lit))===((lit>0?1:0)^s));
   if(match(F[i],x)&&match(F[j],y)){observed=true;break;}
  }
  check(possible===observed,'S/U pair source');
  modes++;
 }
for(const cl of F)for(let a=0;a<4096;a++){
 const v=cl.filter(l=>val(a,Math.abs(l))===(l>0?1:0)).length;
 const q=cl.filter(l=>val(a^4095,Math.abs(l))===(l>0?1:0)).length;
 check(v+q===3,'complement source invariant');
}
const malformed=[F.concat([F[0]]),[[1,-2,3],...F.slice(1)],[[1,1,3],...F.slice(1)],
 F.slice(0,-1),[[1,2,13],...F.slice(1)],[[0,2,3],...F.slice(1)]];
for(const a of malformed)check(!canonical(a,12),'malformed');
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const G=W.map((cl,i)=>cl.map(l=>(i===6||i===11)&&Math.abs(l)===4?-l:l));
const mixed=G.filter(c=>!(c.every(l=>l>0)||c.every(l=>l<0))).length;
check(mixed===16&&!canonical(G,15),'signed231 not monotone');
console.log(JSON.stringify({run:'CONNECTED_MONOTONE_TRANSFER333',role:'independent no-import Node referee',
 assertion_groups:tests,source_rows:rows,source_extreme_modes:modes,
 models:brute,seq:seq.map(String),source_semantics:{old:324,new:318,shared:270,lost:54,gained:48},
 sibling_pins:{SAT:53,UNSAT:0},prior_signed_connector_mixed_per_20:mixed,P_vs_NP:'OPEN'},null,2));

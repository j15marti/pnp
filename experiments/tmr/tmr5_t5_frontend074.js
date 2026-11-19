// TMR-5/074 independent elementary proof-table replay. Node 22, no packages.
// Exact large-source bit-compiler and end-to-end witness replay in companion Python.
'use strict';
let checks=0;const check=(v,s)=>{checks++;if(!v)throw Error('check '+checks+': '+s)};
const neq=(...v)=>new Set(v).size>1;
const c5=(a,b)=>[1,4].includes((b-a+5)%5);
const t5=(a,b)=>[1,3].includes((b-a+5)%5);
const countWalk=(a,b,steps)=>{let frontier=Array(5).fill(0);frontier[a]=1;
  for(let k=0;k<steps;k++){let next=Array(5).fill(0);for(let i=0;i<5;i++)for(let j=0;j<5;j++)if(c5(i,j))next[j]+=frontier[i];frontier=next;}return frontier[b]};
const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
let splitCount=0,naeCount=0,walkCount=0,gadgetCount=0;
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)for(let d=0;d<2;d++){
 let options=[0,1].filter(s=>neq(a,b,s)&&neq(1-s,c,d));
 check(!!options.length===neq(a,b,c,d),'NAE4 split exact');splitCount++;
}
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
 let allowed=perms.filter(v=>v[0]!==(a?0:1)&&v[1]!==(b?0:1)&&v[2]!==(c?0:1));
 check(!!allowed.length===neq(a,b,c),'NAE3 triangle exact');naeCount++;
}
for(let a=0;a<5;a++)for(let b=0;b<5;b++){
 const d=(b-a+5)%5;
 check(countWalk(a,b,2)===[2,0,1,1,0][d],'anchored length2 path');
 check(countWalk(a,b,3)===[0,3,1,1,3][d],'inequality length3 path');walkCount+=2;
 let ext=[];
 for(let z=0;z<5;z++)for(let w=0;w<5;w++)if(t5(a,z)&&t5(a,w)&&t5(w,z)&&t5(w,b))ext.push([z,w]);
 check(ext.length===(d===1||d===4?1:0),'parsimonious T5 gadget');
 if(ext.length)check(ext[0][0]===(a+1)%5&&ext[0][1]===(a+3)%5,'forced auxiliary labels');
 gadgetCount++;
}
// Explicit input-independent bounds after duplicate elimination and active-variable pruning:
// k<=3m; m <= (2k)^3 <=8 n^3; N_D <=333m; A_D <=480m.
// w(N_D)<=12+3w(n), L_D<= (12335+2880w(n))*m < 3000*L.
for(let n=1;n<=32;n++)for(let m=1;m<=Math.min(300,8*n*n*n);m++){
 const w=Math.max(1,Math.ceil(Math.log2(Math.max(n,2))));
 const k=Math.min(n,3*m);const N=57+36*k+168*m,A=80+52*k+244*m;
 const wd=Math.max(1,Math.ceil(Math.log2(Math.max(N,2))));
 const out=N+A+2+2*A*wd;
 const input=n+m+2+3*m*(1+w);
 check(out<3000*input,'uniform source-bit bound');
}
console.log(JSON.stringify({revision:'tmr5-074-proof-tables-v1',runtime:process.version,splitCount,naeCount,walkCount,gadgetCount,checks,failures:0,scope:'table replay and finite arithmetic bound; full encoded-source witness compiler is companion Python'},null,2));

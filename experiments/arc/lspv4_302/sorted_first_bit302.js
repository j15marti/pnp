// LSPV4 sorted-accessor302. Restricted unsorted-row to sorted-row output bit control.
"use strict";
const assert=require("assert");
const P=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
const Q=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
const F=P.concat(Q.map(c=>c.map(x=>-x)));
function source(t){return Array.from({length:t},(_,k)=>F.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+9*k)))).flat();}
function rename(F){return F.map(c=>c.map(x=>Math.sign(x)*({1:10,10:1}[Math.abs(x)]||Math.abs(x))));}
function first(F){return F.filter(c=>c[0]>0).map(c=>c.slice().sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]||a[2]-b[2])[0];}
function valid(F,n){let d=Array.from({length:n+1},()=>[0,0]),seen=new Set();
 for(const c of F){assert(c.length==3&&new Set(c.map(Math.abs)).size==3);
 assert(c.every(x=>Math.sign(x)==Math.sign(c[0])));let key=c.slice().sort((a,b)=>a-b).join(",");
 assert(!seen.has(key));seen.add(key);for(const x of c)d[Math.abs(x)][+(x>0)]++;}
 for(let i=1;i<=n;i++)assert(d[i][0]==2&&d[i][1]==2);
}
function count(F,p){let n=9,free=[];for(let i=1;i<=n;i++)if(!(i in p))free.push(i);let k=0;
 for(let bits=0;bits<2**free.length;bits++){let a={...p};free.forEach((v,j)=>a[v]=(bits>>j)&1);
 if(F.every(c=>c.some(x=>a[Math.abs(x)]==+(x>0))))k++;}return k;}
function hit(m,q){let s=1;for(let i=0;i<q;i++)s*=(m-8-i)/(m-i);return 1-s;}
function pop(x){let b=0;while(x){b+=x%2;x=Math.floor(x/2);}return b;}
function run(){valid(F,9);assert(count(F,{})==70);assert(count(F,{1:0,2:0,8:1,9:1})==2);
 assert(count(F,{3:0,6:1,7:1,9:1})==0);
 let rows=[];
 for(const t of [2,4,8,16,32,64]){let a=source(t),b=rename(a),m=12*t,n=9*t;
 valid(a,n);valid(b,n);assert(a.filter((c,j)=>c.join()!=b[j].join()).length==8);
 assert(first(a).join()==="1,3,5");assert(first(b).join()==="1,12,14");
 let B=Math.ceil(Math.log2(n+1)),H=Math.ceil(Math.log2(m+1)),R=1+3*B,N=2*H+m*R,w=Math.ceil(Math.log2(N+2));
 let q=Math.max(1,Math.floor(m/16)),p=hit(m,q),ones=0;
 for(let j=0;j<m;j++)ones+=pop(2*H+j*R);
 rows.push({t,m,N,q,hit_probability:p,max_average_success:(1+p)/2,
 source_bit_reads:m*R,index_writes:m*w,index_moves:2*m*(w-1),indexed_jumps:m,
 physical_index_xor:2*ones,index_endpoint_xor:0,
 indexed_steps_excluding_arith:m*(3*w-1+R)});
 }
 return {status:"RESTRICTED-PROVED; P versus NP OPEN",F9_global_sat_models:70,
 sat_cube:2,unsat_cube:0,changed_records:8,rows};
}
const result=run();
console.log(JSON.stringify(result,null,2));

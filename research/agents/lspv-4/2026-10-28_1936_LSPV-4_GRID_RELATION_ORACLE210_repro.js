#!/usr/bin/env node
"use strict";
function run(){
 let checks=0,witnesses=0,sourceProbes=0;
 const ck=(v,m)=>{if(!v)throw Error(m||"assert");checks++;};
 const grid=[];
 for(let L=2;L<=11;L++){
  const n=3*L*L,cs=[],occ=new Map(),cut=3*L;
  const id=(t,r,c)=>3*(r*L+c)+t+1;
  const add=c=>{ck(new Set(c.map(Math.abs)).size===3);cs.push(c);for(const v of c)occ.set(v,(occ.get(v)||0)+1);};
  for(let r=0;r<L;r++)for(let c=0;c<L;c++){
    const a=id(0,r,c),b=id(1,r,c),bn=id(1,(r+1)%L,c),d=id(2,r,c),dn=id(2,r,(c+1)%L);
    add([a,b,d]);add([a,bn,d]);add([-a,-b,-dn]);add([-a,-bn,-dn]);
  }
  ck(cs.length===4*L*L);
  for(let v=1;v<=n;v++)ck(occ.get(v)===2&&occ.get(-v)===2);
  const live=new Set();
  for(const c of cs)if(Math.max(...c.map(x=>Math.abs(x)-1))>=cut)
    for(const lit of c)if(Math.abs(lit)-1<cut)live.add(Math.abs(lit)-1);
  const A=Array.from({length:L},(_,c)=>id(0,0,c)-1);
  for(const a of A)ck(live.has(a));
  const signatures=new Set();
  for(let mask=0;mask<(1<<L);mask++){
    const value=Array(n).fill(0);
    for(let r=0;r<L;r++)for(let c=0;c<L;c++)value[id(1,r,c)-1]=1;
    for(let c=0;c<L;c++)value[A[c]]=(mask>>c)&1;
    for(const clause of cs)ck(clause.some(lit=>value[Math.abs(lit)-1]===(lit>0?1:0)));
    signatures.add(A.map(i=>value[i]).join(""));witnesses++;
  }
  ck(signatures.size===(1<<L));
  grid.push({L,n,clauses:cs.length,frontier_size:live.size,
    independent_live_A:L,distinct_feasible_tuples:signatures.size,raw_A_field_bits:L*(1<<L)});
 }
 const oracle=[];
 function sizes(N,mode){const s=[N];while(s[s.length-1]>2){const p=s[s.length-1],q=mode==="half"?Math.floor(p/2):Math.ceil(Math.sqrt(p));ck(q>=2&&q<p);s.push(q);}return s;}
 function mat(root,s){let x=root.slice(),reads=0;for(let d=1;d<s.length;d++){const y=[];for(let j=0;j<s[d];j++){let parity=0;for(const b of x){parity^=b;reads++;}y.push(parity^(j&1));}x=y;}return [x,reads];}
 function val(root,s,d,j,c){if(!d){c.calls++;return root[j];}let parity=0;for(let p=0;p<s[d-1];p++)parity^=val(root,s,d-1,p,c);return parity^(j&1);}
 let seed=2026102819;
 const bit=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)&1;};
 for(const [mode,values] of [["half",[8,16,32,64]],["power",[16,32,64,128,256]]])
  for(const N of values){
   const s=sizes(N,mode),root=Array.from({length:N},bit),[child,reads]=mat(root,s);
   const product=s.slice(0,-1).reduce((a,b)=>a*b,1);
   ck(reads===s.slice(1).reduce((a,v,i)=>a+s[i]*v,0));
   for(let j=0;j<child.length;j++){const c={calls:0};ck(child[j]===val(root,s,s.length-1,j,c));ck(c.calls===product);sourceProbes+=c.calls;}
   if(mode==="power")ck(product<=N*N);
   oracle.push({mode,N,sizes:s,single_query_leaf_probes:product,materialize_all_parent_probes:reads});
  }
 const ranks=[];
 for(const bits of [4,8,12]){let z=(1<<bits)-1,k=0;while(z){const a=z;z--;ck(z<a);k++;}ck(k===(1<<bits)-1);ranks.push({bits,rank:(1<<bits)-1,decreases:k});}
 return {status:"PASS",assertions:checks,witnesses,sourceProbes,grid,oracle,ranks,limits:["Row-major explicit frontier only","Uncached specified oracle only","Neither P=NP nor P!=NP follows"]};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));

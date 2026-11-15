'use strict';
// Independent TMR-5 exact nonaffine rank + authenticated gate-copy Resolution audit.
const runAudit = function runAudit(){
"use strict";
let checks=0,steps=0,negatives=0;
const ok=(v,m)=>{checks++;if(!v)throw Error("FAIL "+m);},bit=(v,i)=>(v>>>i)&1;
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
function build(k){
 const edges=[];for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)edges.push([i,j]);
 const n=3*k+edges.length,blocks=[];
 for(let i=0;i<k;i++)blocks.push([i+1,k+i+1,2*k+i+1]);
 for(let h=0;h<edges.length;h++)blocks.push([edges[h][0]+1,edges[h][1]+1,3*k+h+1]);
 const gates=[],N=a=>{gates.push({op:"not",a});return n+gates.length;},A=(a,b)=>{gates.push({op:"and",a,b});return n+gates.length;};
 const pos=(a,b,c)=>N(A(A(N(a),N(b)),N(c))),negative=(a,b,c)=>N(A(A(a,b),c));
 const outs=blocks.map(b=>A(pos(...b),negative(...b)));
 let out=outs[0];for(let j=1;j<outs.length;j++)out=A(out,outs[j]);
 ok(gates.length===11*blocks.length-1,"gate count");
 return {k,n,edges,blocks,gates,out};
}
const direct=(q,mask)=>q.blocks.every(b=>{const a=bit(mask,b[0]-1),c=bit(mask,b[1]-1),d=bit(mask,b[2]-1);return !(a===c&&c===d);})?1:0;
function computed(q,mask){
 const a=new Uint8Array(q.n+q.gates.length+1);
 for(let i=1;i<=q.n;i++)a[i]=bit(mask,i-1);
 for(let j=0;j<q.gates.length;j++){const t=q.gates[j];a[q.n+j+1]=t.op==="not"?1-a[t.a]:(a[t.a]&a[t.b]);}
 return a[q.out];
}
function rankExact(M){
 let a=M.map(row=>row.map(BigInt)),n=a.length,r=0;
 const abs=v=>v<0n?-v:v,gcd=(x,y)=>{x=abs(x);y=abs(y);while(y){let t=x%y;x=y;y=t;}return x;};
 for(let c=0;c<n;c++){
  let p=r;while(p<n&&a[p][c]===0n)p++;if(p===n)continue;
  [a[r],a[p]]=[a[p],a[r]];
  for(let i=r+1;i<n;i++)if(a[i][c]!==0n){
   const u=a[r][c],v=a[i][c];
   for(let j=c;j<n;j++)a[i][j]=u*a[i][j]-v*a[r][j];
   let g=0n;for(let j=c;j<n;j++)g=gcd(g,a[i][j]);
   if(g>1n)for(let j=c;j<n;j++)a[i][j]/=g;
  }r++;
 }return r;
}
const profiles=[];
for(let k=2;k<=4;k++){
 const q=build(k),count=1<<q.n;
 for(let m=0;m<count;m++)ok(direct(q,m)===computed(q,m),`circuit exact k${k} m${m}`);
 const r=1<<k,E=q.edges.length,table=[];
 for(let x=0;x<r;x++){
  let t=0;for(let i=0;i<k;i++)t+=bit(x,i);const row=[];
  for(let y=0;y<r;y++){
   let sum=0;for(let z=0;z<(1<<E);z++){let m=x|(y<<k);for(let h=0;h<E;h++)m|=bit(z,h)<<(3*k+h);sum+=direct(q,m);}
   let prod=1;for(let i=0;i<k;i++)if(!bit(x,i)&&!bit(y,i))prod=0;
   ok(sum===prod*(1<<(t*(k-t))),"rank row sum");row.push(sum);
  }table.push(row);
 }ok(rankExact(table)===r,"exact rank");
 const col=x=>{let m=0;for(let i=0;i<k;i++)m|=(1-bit(x,i))<<(k+i);
  for(let h=0;h<E;h++){let [i,j]=q.edges[h];m|=(bit(x,i)===bit(x,j)?1-bit(x,i):0)<<(3*k+h);}return m;};
 for(let x=0;x<r;x++){ok(direct(q,x|col(x))===1,"fooling diagonal");
  for(let y=x+1;y<r;y++)ok(direct(q,x|col(y))===0||direct(q,y|col(x))===0,"fooling cross");}
 let w=0;for(let j=k;j<q.n;j++)w|=1<<j;ok(direct(q,w)===1,"degree-witness");
 ok(direct(q,0)===0&&direct(q,count-1)===0,"nontrivial NAE");
 profiles.push({k,variables:q.n,NAE_blocks:q.blocks.length,clauses:2*q.blocks.length,gates:q.gates.length,rank:r,cover:r,truth_table_states:count});
}
function resolutionReplay(k){
 const q=build(k),n=q.n,g=q.gates.length;
 const gateId=(s,j)=>n+4+j+(s==="B"?g:0),w=(s,i)=>i<=n?i:gateId(s,i-n-1);
 const lines=[],gate={A:[],B:[]};
 const add=(c,source)=>{let id=lines.length;lines.push({c:norm(c),source});return id;};
 function res(i,j,p){
  const a=lines[i].c,b=lines[j].c;ok(a.includes(p)&&b.includes(-p),"invalid pivot");
  const c=norm([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)]);
  ok(!c.some(v=>c.includes(-v)),"tautology");steps++;return add(c,false);
 }
 for(let s of ["A","B"])for(let h=0;h<g;h++){
  const t=q.gates[h],out=gateId(s,h),a=w(s,t.a);
  if(t.op==="not")gate[s].push({pos:add([out,a],true),neg:add([-out,-a],true)});
  else {const b=w(s,t.b);gate[s].push({pos:add([out,-a,-b],true),na:add([-out,a],true),nb:add([-out,b],true)});}
 }
 const oa=gateId("A",g-1),ob=gateId("B",g-1),F={},U=[n+1,n+2,n+3];
 for(let a of [1,-1])for(let b of [1,-1])for(let c of [1,-1])F[`${a},${b},${c}`]=add([oa,a*U[0],b*U[1],c*U[2]],true);
 const bu=add([-ob],true),sources=lines.length,ab={},a0={};
 for(let a of [1,-1])for(let b of [1,-1])ab[`${a},${b}`]=res(F[`${a},${b},1`],F[`${a},${b},-1`],U[2]);
 for(let a of [1,-1])a0[a]=res(ab[`${a},1`],ab[`${a},-1`],U[1]);
 const lifted=res(a0[1],a0[-1],U[0]);ok(eq(lines[lifted].c,[oa]),"lifted refutation");
 const pairs=[];
 for(let h=0;h<g;h++){
  const t=q.gates[h];
  function imp(s,z){
   const sf=gate[s][h],st=gate[z][h];
   function transport(line,u,v,reverse){
    if(u===v)return line;
    const j=u-(n+4+(s==="B"?g:0));ok(j>=0&&j<h,"prior gate");
    const pair=pairs[j],e=reverse?(s==="A"?pair.BtoA:pair.AtoB):(s==="A"?pair.AtoB:pair.BtoA);
    return reverse?res(e,line,u):res(line,e,u);
   }
   if(t.op==="not"){const u=w(s,t.a),v=w(z,t.a);
    return res(transport(sf.neg,u,v,true),st.pos,-v);}
   const a=w(s,t.a),aa=w(z,t.a),b=w(s,t.b),bb=w(z,t.b);
   const first=transport(sf.na,a,aa,false),second=transport(sf.nb,b,bb,false);
   return res(second,res(first,st.pos,aa),bb);
  }
  const AtoB=imp("A","B"),BtoA=imp("B","A");
  ok(eq(lines[AtoB].c,[-gateId("A",h),gateId("B",h)]),"gate AtoB");
  ok(eq(lines[BtoA].c,[-gateId("B",h),gateId("A",h)]),"gate BtoA");
  pairs.push({AtoB,BtoA});
 }
 const bpositive=res(lifted,pairs[g-1].AtoB,oa),empty=res(bpositive,bu,ob);
 ok(lines[empty].c.length===0,"empty goal");
 const cost=lines.length-sources;ok(cost<=7+8*g+2,"upper inference count");
 const authenticSources=2*q.gates.reduce((u,t)=>u+(t.op==="not"?2:3),0)+9;
 ok(sources===authenticSources,"source count");
 try{res(bu,lifted,ob);throw Error("accepted illegal pivot");}catch(e){ok(String(e).includes("invalid pivot"),"negative pivot rejected");negatives++;}
 ok(direct(q,0)===0,"false Q restriction exists");
 negatives++;
 return {k,private_F_clauses:8,private_F_resolution_steps:7,gate_count:g,source_clause_count:sources,actual_resolution_steps:cost,proved_upper:7+8*g+2};
}
const proofs=[resolutionReplay(2),resolutionReplay(3)];
return {test:"TMR5_COMPOSED_NAE_RANK_AND_CIRCUIT_GUARD",timestamp_PST:"2026-11-15 01:43 PST",status:"COMPUTATIONAL; symbolic PROVED/RESTRICTED composition awaiting peer review",checks,derived_steps:steps,negative_controls:negatives,failures:0,profiles,proofs,limitations:["No physical finite-tape machine compiled","4-CNF guarded source, not proper 3-CNF","No transfer to arbitrary SAT decision time"]};
};
console.log(JSON.stringify(runAudit(),null,2));

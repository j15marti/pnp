"use strict";
// LSPV-3 ARC-BOUNDARY-CAPACITY122: deterministic ordinary proper-3CNF audit.
// Run: node 2026-10-25_1028_ARC_BOUNDARY_CAPACITY122_repro.js
const ok=(v,m)=>{if(!v)throw Error(m);};
function make(b,S){
 const k=Math.max(0,b-3),M=1<<b,clauses=[];
 for(let u=0;u<M;u++)if(!S[u]){
  const L=Array.from({length:b},(_,i)=>(u>>(b-1-i)&1)?-(i+1):i+1);
  if(b===3)clauses.push(L);
  else {
   const a=Array.from({length:k},(_,j)=>b+u*k+j+1);
   clauses.push([L[0],L[1],a[0]]);
   for(let j=1;j<k;j++)clauses.push([-a[j-1],L[j+1],a[j]]);
   clauses.push([-a[k-1],L[b-2],L[b-1]]);
  }
 }
 return {b,n:b+k*M,clauses};
}
function pin(F,i,bit){
 const a=F.n+1,z=F.n+2,L=bit?i+1:-(i+1);
 return {b:F.b,n:z,clauses:F.clauses.concat([[L,a,z],[L,a,-z],[L,-a,z],[L,-a,-z]])};
}
function encode(F){
 return "p cnf "+F.n+" "+F.clauses.length+"\n"+F.clauses.map(c=>c.join(" ")+" 0\n").join("");
}
function decode(src){
 const lines=src.trimEnd().split("\n"),h=lines.shift().split(" ");
 ok(h.length===4&&h[0]==="p"&&h[1]==="cnf","header");
 const n=+h[2],m=+h[3];ok(Number.isSafeInteger(n)&&n>0&&lines.length===m,"header counts");
 const clauses=lines.map(x=>{
  const p=x.split(/\s+/).map(Number);ok(p.length===4&&p[3]===0,"clause arity");
  const lits=p.slice(0,3);ok(lits.every(v=>Number.isSafeInteger(v)&&v!==0&&Math.abs(v)<=n),"bad literal");
  ok(new Set(lits.map(Math.abs)).size===3,"not proper 3-CNF");
  return lits;
 });
 return {n,clauses};
}
function sat(F){
 function solve(a){
  for(;;){
   let change=false;
   for(const row of F.clauses){
    let trueClause=false,num=0,last=0;
    for(const L of row){let v=a[Math.abs(L)];if(!v){num++;last=L;}else if((v>0)===(L>0)){trueClause=true;break;}}
    if(trueClause)continue;
    if(!num)return false;
    if(num===1){
     const i=Math.abs(last),v=last>0?1:-1;
     if(a[i]!==0&&a[i]!==v)return false;
     if(a[i]===0){a[i]=v;change=true;}
    }
   }
   if(!change)break;
  }
  let pick=0;
  for(const row of F.clauses){
   if(row.some(L=>a[Math.abs(L)]!==0&&((a[Math.abs(L)]>0)===(L>0))))continue;
   for(const L of row)if(!a[Math.abs(L)]){pick=Math.abs(L);break;}
   if(pick)break;
  }
  if(!pick)return true;
  for(const val of [1,-1]){const next=a.slice();next[pick]=val;if(solve(next))return true;}
  return false;
 }
 return solve(new Int8Array(F.n+1));
}
function choose(n,k){let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-k+i)/BigInt(i);return r;}
function audit(){
 let count=0,root=0,first=0,second=0,satSeen=0,unsatSeen=0;
 const assert=(v,msg)=>{count++;ok(v,msg);};
 let seed=122;const rnd=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0;
 const samples={3:[],4:[]};
 for(let m=0;m<256;m++)samples[3].push(Array.from({length:8},(_,i)=>(m>>i)&1));
 const M=16;
 samples[4].push(
  Array(M).fill(0),Array(M).fill(1),
  Array.from({length:M},(_,i)=>+(i===0)),
  Array.from({length:M},(_,i)=>+(i!==0)),
  Array.from({length:M},(_,i)=>+((i>>3&1)===1)),
  Array.from({length:M},(_,i)=>+((i>>3&1)===(i>>2&1))),
  Array.from({length:M},(_,i)=>+(((i>>3&1)^(i>>2&1))===1)),
  Array.from({length:M},(_,i)=>+(((i>>3&1)&(i>>2&1))===1))
 );
 for(let j=0;j<128;j++){
  const order=Array.from({length:M},(_,i)=>i);
  for(let k=M-1;k>0;k--){const a=rnd()%(k+1);[order[k],order[a]]=[order[a],order[k]];}
  const S=Array(M).fill(0);for(let k=0;k<M/2;k++)S[order[k]]=1;
  samples[4].push(S);
 }
 const sizeRanges={};
 for(const b of [3,4]){
  let min=Infinity,max=0;
  for(let ci=0;ci<samples[b].length;ci++){
   const S=samples[b][ci],F=make(b,S),encoded=encode(F),parsed=decode(encoded);
   min=Math.min(min,encoded.length);max=Math.max(max,encoded.length);
   assert(parsed.n===F.n&&parsed.clauses.length===F.clauses.length,"serialize");
   let label=sat(parsed);assert(label===S.some(Boolean),"root b="+b+" case="+ci);
   root++;if(label)satSeen++;else unsatSeen++;
   for(let word=0;word<1<<b;word++){
    const bit=word>>(b-1)&1,F1=pin(F,0,bit),D1=decode(encode(F1));
    label=sat(D1);
    assert(label===S.some((z,u)=>z&&(u>>(b-1)&1)===bit),"child b="+b+" case="+ci+" word="+word);
    first++;if(label)satSeen++;else unsatSeen++;
    let F2=F1;for(let i=1;i<b;i++)F2=pin(F2,i,word>>(b-1-i)&1);
    label=sat(decode(encode(F2)));
    assert(label===Boolean(S[word]),"grandchild b="+b+" case="+ci+" word="+word);
    second++;if(label)satSeen++;else unsatSeen++;
   }
  }
  sizeRanges[b]={instances:samples[b].length,min_serialized_bytes:min,max_serialized_bytes:max};
 }
 let distinguished=0;
 for(let i=0;i<256;i++)for(let j=i+1;j<256;j++){
  assert(samples[3][i].some((z,k)=>z!==samples[3][j][k]),"no distinguishing continuation");
  distinguished++;
 }
 const S=Array(16).fill(0),T=Array(16).fill(0);S[0]=1;T[1]=1;
 const A=make(4,S),B=make(4,T),A1=pin(A,0,0),B1=pin(B,0,0);
 let A2=A1,B2=B1;for(let i=1;i<4;i++){A2=pin(A2,i,0);B2=pin(B2,i,0);}
 const pair={
  root:[sat(decode(encode(A))),sat(decode(encode(B)))],
  level1:[sat(decode(encode(A1))),sat(decode(encode(B1)))],
  level2:[sat(decode(encode(A2))),sat(decode(encode(B2)))],
  A_bytes:[encode(A).length,encode(A1).length,encode(A2).length],
  B_bytes:[encode(B).length,encode(B1).length,encode(B2).length]
 };
 assert(JSON.stringify(pair.root)==="[true,true]","paired roots");
 assert(JSON.stringify(pair.level1)==="[true,true]","paired first levels");
 assert(JSON.stringify(pair.level2)==="[true,false]","paired second levels");
 const bounds=[3,4,5,6,8].map(b=>{
  const M=2**b,C=choose(M,M/2),digits=C.toString(2).length;
  return {b,M,balanced_supports:C.toString(),log2_count_interval:[digits-1,digits],minimum_worst_case_binary_description_bits:digits-1};
 });
 return {run:"ARC-BOUNDARY-CAPACITY122",seed:122,assertions:count,root,first,second,satSeen,unsatSeen,
  distinctPairs:distinguished,sizeRanges,pair,bounds,errors:0,status:"COMPUTATIONAL checks only; exact restricted theorem proved separately; ARC-EDGE-90 OPEN"};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));

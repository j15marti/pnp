"use strict";
// Independent finite signed-3CNF equality checks; not native FLMV execution.
const gamma=w=>"0".repeat(w.toString(2).length-1)+w.toString(2);
const bit=(v,n)=>v.toString(2).padStart(n,"0");
const E=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
const P=[[0,0,1],[0,1,0],[1,0,0],[1,1,1]];
function encode(w,A,B){
 const L=Math.floor(Math.log2(6*w))+1;let s=gamma(w);
 for(let v=0;v<4;v++)for(let j=0;j<w;j++)for(let r=0;r<4;r++){
  const t=v<2?[1-(v===0?A[j]:B[j]),r>>1,r&1]:P[r];
  for(let h=0;h<3;h++)s+=t[h]+bit(6*j+E[v][h],L);
 }return s;
}
function classify(s){
 const N=s.length;if(!/^[01]+$/.test(s))return "MALFORMED";
 let z=0;while(z<N&&s[z]==="0")z++;
 if(z===N||2*z+1>N)return "MALFORMED";
 const w=parseInt(s.slice(z,2*z+1),2),g=2*z+1;
 if(!Number.isSafeInteger(w)||w<1||w>N)return "MALFORMED";
 const L=Math.floor(Math.log2(6*w))+1;
 if(g+48*w*(L+1)!==N)return "MALFORMED";
 for(let v=0;v<4;v++)for(let j=0;j<w;j++){
  const base=g+(v*4*w+4*j)*3*(L+1),anchor=+s[base];
  for(let r=0;r<4;r++)for(let h=0;h<3;h++){
   const want=(v<2?[anchor,r>>1,r&1]:P[r])[h]+bit(6*j+E[v][h],L);
   const off=base+(3*r+h)*(L+1);
   if(s.slice(off,off+L+1)!==want)return "OUT_OF_FAMILY";
  }
 }
 for(let j=0;j<w;j++){
  if(s[g+4*j*3*(L+1)]!==s[g+(4*w+4*j)*3*(L+1)])return "UNSAT";
 }return "SAT";
}
function models(s,w){
 const L=Math.floor(Math.log2(6*w))+1,g=gamma(w).length,C=[];
 for(let c=0;c<16*w;c++){let row=[];for(let h=0;h<3;h++){
  const p=g+(3*c+h)*(L+1);
  row.push([parseInt(s.slice(p+1,p+1+L),2)-1,+s[p]]);
 }C.push(row);}
 let count=0;for(let a=0;a<2**(6*w);a++){
  if(C.every(row=>row.some(([id,z])=>((a>>id)&1)!==z)))count++;
 }return count;
}
function run(){
 let checks=0,negative=0,original=0;const table=[];
 for(const w of [1,2])for(let a=0;a<2**w;a++)for(let b=0;b<2**w;b++){
  const A=Array.from({length:w},(_,j)=>(a>>j)&1),B=Array.from({length:w},(_,j)=>(b>>j)&1);
  const s=encode(w,A,B),label=classify(s),expected=a===b?"SAT":"UNSAT";
  if(label!==expected)throw Error("label");checks++;
  const m=models(s,w);if(m!==(a===b?8**w:0))throw Error("models");checks++;
  table.push({w,a,b,N:s.length,models:m,label});original++;
 }
 for(const w of [1,2,3,4,8,16,32]){
  const A=Array.from({length:w},(_,j)=>j%2),B=A.slice();
  if(classify(encode(w,A,B))!=="SAT")throw Error("SAT");checks++;
  B[w-1]^=1;let s=encode(w,A,B);
  if(classify(s)!=="UNSAT")throw Error("UNSAT");checks++;
  const L=Math.floor(Math.log2(6*w))+1,p=gamma(w).length+3*(L+1);
  let bad=s.slice(0,p)+(s[p]==="0"?"1":"0")+s.slice(p+1);
  if(classify(bad)!=="OUT_OF_FAMILY")throw Error("sign");checks++;negative++;
  bad=s.slice(0,p+1)+(s[p+1]==="0"?"1":"0")+s.slice(p+2);
  if(classify(bad)!=="OUT_OF_FAMILY")throw Error("ID");checks++;negative++;
  for(bad of [s+"0",s.slice(0,-1),s+"X"]){
   if(classify(bad)!=="MALFORMED")throw Error("encoding");checks++;negative++;
  }
 }
 return {status:"PASS",checks,negative_controls:negative,original_sources:original,table,
  note:"Semantic bit-index simulator only; no native FLMV instruction-level run."};
}
return run();
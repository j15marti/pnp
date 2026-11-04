#!/usr/bin/env node
// LSPV-4/397 independent standalone finite referee. No external dependencies.
let checks=0;
function ck(v,msg){if(!v)throw Error(msg);checks++;}
const B=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function satisfied(F,a){return F.every(C=>C.some(l=>l>0?!!a[Math.abs(l)]:!a[Math.abs(l)]))}
function count(F,n){let k=0;for(let b=0;b<2**n;b++){let a={};for(let i=1;i<=n;i++)a[i]=!!(b&(1<<(i-1)));if(satisfied(F,a))k++}return k}
function guard(H){let F=[],n=3;for(let C of H){if(C.length===1){let z=++n;F.push([-3,C[0],z],[-3,C[0],-z])}else if(C.length===2)F.push([-3,...C]);else throw Error("bad input")}return [F,n]}
const totals={SAT:0,UNSAT:0};
for(let b=0;b<256;b++){
  const H=B.filter((_,j)=>!!(b&(1<<j))), originalSAT=count(H,2)>0;
  totals[originalSAT?"SAT":"UNSAT"]++;
  const [F,n]=guard(H);
  ck(F.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"malformed proper3");
  ck(count(F,n)>0,"guarded parent SAT");
  ck(count([...F,[3]],n)>0===originalSAT,"guarded equivalence");
  ck(count([...F,[-3]],n)>0,"guarded x=0");
}
ck(totals.SAT===95&&totals.UNSAT===161,"histogram");
function resolution(a,b,p){ck(a.includes(p)&&b.includes(-p),"pivot");const u=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];ck(u.every(x=>!u.includes(-x)),"tautology");return u.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
const H=[[1],[-1,2],[-2]],d1=resolution(H[1],H[0],-1),d2=resolution(H[2],d1,-2);
ck(d1.join(",")==="2","first derived unit");ck(d2.length===0,"empty proof");
function parity(ch){const adj=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];let ct=0;for(let a=0;a<64;a++){if(adj.every((es,i)=>es.reduce((s,e)=>s+((a>>e)&1),0)%2===ch[i]))ct++}return ct}
ck(parity([1,0,0,0])===0,"odd Tseitin");ck(parity([0,0,0,0])===8,"even Tseitin");
console.log(JSON.stringify({status:"PASS",cases:256,totals,checks,odd_K4:0,even_K4:8}));

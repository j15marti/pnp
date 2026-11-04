#!/usr/bin/env node
"use strict";
// LSPV-4/373 independent compact finite verifier. No dependencies, no oracle.
// Command: node experiments/arc/lspv4_373_php_source_probe_compact.js
let ncheck=0, changes=0, deletions=0;
function ck(a,m){ncheck++; if(!a)throw Error(m)}
function php(h,p=h+1){
  const a=[];
  for(let i=0;i<p;i++){const c=[];for(let j=0;j<h;j++)c.push(i*h+j+1);a.push(c)}
  for(let j=0;j<h;j++)for(let i=0;i<p;i++)for(let k=i+1;k<p;k++)
    a.push([-(i*h+j+1),-(k*h+j+1)]);
  return a;
}
function encode(cnf,n){
  return "p cnf "+n+" "+cnf.length+"\n"+
    cnf.map(c=>c.map(x=>x>0?"+"+x:""+x).join(" ")+" 0\n").join("");
}
function sat(cnf,mask){
  return cnf.every(c=>c.some(x=>Boolean(mask & (1<<(Math.abs(x)-1)))===(x>0)));
}
function hasModel(cnf,n){
  for(let a=0;a<2**n;a++)if(sat(cnf,a))return true;
  return false;
}
function validCNF(s){
  if(!/^[\x00-\x7f]*$/.test(s))return false;
  const rows=s.split("\n");if(rows[rows.length-1]==="")rows.pop();
  if(!rows.length)return false;
  const m=/^p cnf (\d+) (\d+)$/.exec(rows[0]);if(!m)return false;
  const n=Number(m[1]),q=Number(m[2]);if(q!==rows.length-1)return false;
  return rows.slice(1).every(s=>{
    const w=s.split(" ");if(w.at(-1)!=="0")return false;
    return w.slice(0,-1).every(t=>/^[+-][1-9]\d*$/.test(t)&&
      Number(t.slice(1))<=n);
  });
}
const stats=[];
for(let h=1;h<=3;h++){
 const a=php(h), v=h*(h+1), orig=encode(a,v);
 ck(validCNF(orig));ck(!hasModel(a,v),"PHP UNSAT");
 ck(hasModel(php(h,h),h*h),"matched SAT");
 let signs=0;
 for(let i=0;i<a.length;i++){
   const less=a.filter((_,j)=>j!==i);
   ck(hasModel(less,v),"minimal UNSAT source deletion");deletions++;
   for(let k=0;k<a[i].length;k++){
     const b=a.map(c=>c.slice());b[i][k]=-b[i][k];
     const mutated=encode(b,v);
     ck(mutated.length===orig.length);
     ck([...orig].reduce((t,c,j)=>t+(c!==mutated[j]),0)===1);
     ck(validCNF(mutated));
     ck(hasModel(b,v),"sign flip must SAT");
     changes++;signs++;
   }
 }
 ck(signs===h*(h+1)**2);
 stats.push({h,clauses:a.length,sign_fields:signs,encoded_bytes:orig.length});
}
const malformed=["","p cna 1 1\n+1 0\n","p cnf 2 1\n+3 0\n",
 "p cnf 2 1\n+1\n","p cnf 2 2\n+1 0\n",
 "p cnf 2 1\n+0 0\n","p cnf 1 1\nx 0\n","p cnf 2 1\n+1 0\n+2 0\n"];
for(const s of malformed)ck(!validCNF(s),"malformed rejection");
let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function k4(ch){
 const clauses=[];
 for(let v=0;v<4;v++){
   const inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
   for(let mask=0;mask<8;mask++){
     const parity=[0,1,2].reduce((s,j)=>s+Number(Boolean(mask&(1<<j))),0)%2;
     if(parity!==ch[v])clauses.push(inc.map((id,j)=>(mask&(1<<j))?-id:id));
   }
 }
 return clauses;
}
const counts=[];
for(const charges of [[0,0,0,0],[1,0,0,0]]){
 const f=k4(charges);let n=0;
 for(let i=0;i<64;i++)if(sat(f,i))n++;
 counts.push(n);
}
ck(counts[0]===8&&counts[1]===0,"K4 even/odd");
console.log(JSON.stringify({id:"LSPV4_373_PUBLIC",assertions:ncheck,sign_flips:changes,
 clause_deletions:deletions,malformed:malformed.length,k4_even_odd:counts,stats},null,2));
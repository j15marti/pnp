// Independent LSPV-2/402 checker: bit-mask clauses, no producer imports.
"use strict";
const M=7;
function mk(lits){
 let p=0,n=0;
 for(let x of lits){if(x===0||Math.abs(x)>3)throw Error("bad literal");let bit=1<<(Math.abs(x)-1);if(x>0)p|=bit;else n|=bit}
 if(p&n)throw Error("tautology");
 return {p,n};
}
const id=c=>c.p+8*c.n;
function resolve(A,B,v){
 const bit=1<<(v-1);
 let p,n;
 if((A.p&bit)&&(B.n&bit)){p=(A.p&~bit)|B.p;n=A.n|(B.n&~bit)}
 else if((A.n&bit)&&(B.p&bit)){p=A.p|(B.p&~bit);n=(A.n&~bit)|B.n}
 else throw Error("missing pivot");
 if(p&n)throw Error("tautology");
 return {p,n};
}
function satisfied(c,m){return ((c.p&m)|((c.n&(~m))&M))!==0}
function models(C){const out=[];for(let m=0;m<8;m++)if(C.every(c=>satisfied(c,m)))out.push(m);return out}
function closure(gamma){
 const clauses=[...gamma],ids=new Set(clauses.map(id));let appended=0;
 if(ids.size!==gamma.length)throw Error("duplicate");
 while(true){
  const n=clauses.length;
  for(let j=0;j<n;j++)for(let i=0;i<j;i++)for(let v=1;v<=3;v++){
    let c;try{c=resolve(clauses[i],clauses[j],v)}catch{continue}
    if(!ids.has(id(c))){ids.add(id(c));clauses.push(c);appended++}
  }
  if(clauses.length===n)break;
 }
 if(clauses.length>27)throw Error("finite closure exceeds 3^3");
 return {clauses,appended};
}
function checkGraph(name,n,edges){
 const degree=Array(n).fill(0);
 for(let [a,b] of edges){degree[a]++;degree[b]++}
 if(!degree.every(x=>x===3)||edges.length!==3*n/2)throw Error("not cubic");
 let cuts=0,min=Infinity,balanced=0;
 for(let mask=1;mask<(1<<n)-1;mask++){
  let count=0;for(let i=0;i<n;i++)count+=(mask>>i)&1;
  const bd=edges.filter(([a,b])=>(((mask>>a)&1)!==((mask>>b)&1))).length;
  let paritySupport=Array(edges.length).fill(0);
  for(let v=0;v<n;v++)if((mask>>v)&1)edges.forEach(([a,b],e)=>{if(a===v||b===v)paritySupport[e]^=1});
  if(paritySupport.reduce((s,x)=>s+x,0)!==bd)throw Error("GF2 cut correspondence failed");
  cuts++;
  if(3*count>=n && 3*count<=2*n){min=Math.min(min,bd);balanced++}
 }
 return {name,vertices:n,edges:edges.length,subsets_checked:cuts,balanced_subsets:balanced,minimum_balanced_boundary:min};
}
function run(){
 const c=[[-1,2],[1,-2],[-2,3],[2,-3],[1,3],[-1,-3]].map(mk);
 if(models(c).length!==0)throw Error("UNSAT failed");
 const witnesses=[];for(let i=0;i<6;i++){
   const w=models(c.filter((_,j)=>i!==j));if(w.length!==1)throw Error("source indispensable failure");
   witnesses.push(w[0]);
 }
 const cert=[[0,2,2],[1,3,2],[6,5,3],[7,4,3],[8,9,1]],proof=[...c];
 for(let [i,j,v] of cert)proof.push(resolve(proof[i],proof[j],v));
 if(id(proof.at(-1))!==0)throw Error("resolution proof failed");
 const eq=(a,b)=>[mk([-a,b]),mk([a,-b])];
 const neq=(a,b)=>[mk([a,b]),mk([-a,-b])];
 const r1=closure([...eq(1,2),...eq(2,3)]);
 const tgt=eq(1,3);
 if(!tgt.every(t=>r1.clauses.some(c=>(c.p&~t.p)===0&&(c.n&~t.n)===0)))throw Error("XOR1 not covered");
 const r2=closure([...tgt,...neq(1,3)]);
 if(!r2.clauses.some(x=>id(x)===0))throw Error("XOR2 failed");
 if(r1.appended!==2||r2.appended!==5)throw Error("closure count mismatch");
 const even=models([...eq(1,2),...eq(2,3),...eq(1,3)]);
 if(even.length!==2)throw Error("even parity control");
 let rejected=0;for(const test of [
  ()=>resolve(mk([1]),mk([-2]),1),()=>mk([1,-1]),()=>mk([4]),()=>resolve(mk([1,2]),mk([-1,-2]),1)
 ])try{test()}catch{rejected++}
 if(rejected!==4)throw Error("failed malformed checks");
 const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const K33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
 const cube=[];for(let v=0;v<8;v++)for(let b=0;b<3;b++)if(!(v&(1<<b)))cube.push([v,v^(1<<b)]);
 const petersen=[];for(let i=0;i<5;i++){petersen.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5])}
 const g=[checkGraph("K4",4,K4),checkGraph("K3,3",6,K33),checkGraph("cube",8,cube),checkGraph("Petersen",10,petersen)];
 return {status:"COMPUTATIONAL",method:"independent bit masks and exhaustive assignments",
  exact_proof_nodes:cert.length,essential_clause_witnesses:witnesses,
  partial_XOR_translation_nodes:r1.appended+r2.appended,SAT_control_models:even.length,
  graph_cut_controls:g,corrupt_records_rejected:rejected};
}
console.log(JSON.stringify(run(),null,2));
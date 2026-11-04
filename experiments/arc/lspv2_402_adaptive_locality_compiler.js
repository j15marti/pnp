// LSPV-2/402: strict Resolution closure on an odd affine XOR triangle.
"use strict";
const cmp=(a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1);
const norm=a=>[...new Set(a)].sort(cmp);
const key=a=>a.join(",");
function resolve(a,b,p){
 let A=[...a],B=[...b];
 if(A.includes(p)&&B.includes(-p)){A=A.filter(x=>x!==p);B=B.filter(x=>x!==-p)}
 else if(A.includes(-p)&&B.includes(p)){A=A.filter(x=>x!==-p);B=B.filter(x=>x!==p)}
 else throw Error("invalid pivot");
 const c=norm([...A,...B]);if(c.some(x=>c.includes(-x)))throw Error("tautology");
 return c;
}
function parity(vars,rhs){
 const out=[];for(let mask=0;mask<(1<<vars.length);mask++){
  const bits=vars.map((_,j)=>(mask>>j)&1);
  if(bits.reduce((a,b)=>a+b,0)%2!==rhs)out.push(norm(vars.map((v,j)=>bits[j]?-v:v)))
 }return out;
}
function holds(c,m){return c.some(l=>((m>>(Math.abs(l)-1))&1)===(l>0?1:0))}
function models(cnf){return [...Array(8).keys()].filter(m=>cnf.every(c=>holds(c,m)))}
function closure(gamma,k){
 const clauses=gamma.map(norm),known=new Set(clauses.map(key)),steps=[];
 if(known.size!==clauses.length)throw Error("duplicate initial clauses");
 while(true){
  const limit=clauses.length;
  for(let i=0;i<limit;i++)for(let j=0;j<i;j++)for(let p=1;p<=3;p++){
   if(!((clauses[i].includes(p)&&clauses[j].includes(-p))||(clauses[i].includes(-p)&&clauses[j].includes(p))))continue;
   let c;try{c=resolve(clauses[i],clauses[j],p)}catch{continue}
   if(!known.has(key(c))){known.add(key(c));clauses.push(c);steps.push({parents:[j,i],pivot:p,result:c});
     if(clauses.length>3**k)throw Error("finite universe bound violated")}
  }
  if(clauses.length===limit)break;
 }return {clauses,steps};
}
const covered=(clauses,targets)=>targets.every(T=>clauses.some(C=>C.every(l=>T.includes(l))));
function run(){
 const rows=[[[1,2],0],[[2,3],0],[[1,3],1]],groups=rows.map(([v,b])=>parity(v,b));
 const source=groups.flat();
 if(source.length!==6||models(source).length!==0)throw Error("invalid UNSAT source");
 const essential=[];
 for(let i=0;i<6;i++){
   const m=models(source.filter((_,j)=>j!==i));
   if(m.length!==1)throw Error("source not essential");
   essential.push({source:i,witness_assignment_mask:m[0]});
 }
 const proof=[...source],refs=[[0,2,2],[1,3,2],[6,5,3],[7,4,3],[8,9,1]];
 for(const [i,j,p] of refs)proof.push(resolve(proof[i],proof[j],p));
 if(proof.at(-1).length)throw Error("certificate did not reach empty");
 for(let i=0;i<3;i++){const r=closure(groups[i],2);if(!covered(r.clauses,groups[i]))throw Error("AND3 row")}
 const target=parity([1,3],0);
 const one=closure([...groups[0],...groups[1]],3),two=closure([...target,...groups[2]],3);
 if(!covered(one.clauses,target)||one.steps.length!==2)throw Error("first XOR translation");
 if(!two.clauses.some(c=>c.length===0)||two.steps.length!==5)throw Error("second XOR translation");
 const satSource=[parity([1,2],0),parity([2,3],0),parity([1,3],0)].flat();
 if(models(satSource).length!==2)throw Error("SAT control");
 let malformed=0;
 for(const bad of [
   ()=>resolve([1],[-2],1),
   ()=>resolve([1,2],[-1,-2],1),
   ()=>{if(new Set([1,1]).size!==2)throw Error("duplicate source literal")},
   ()=>{if(source.some(c=>c.some(l=>Math.abs(l)>2)))throw Error("header variable bound mismatch")}
 ]){try{bad()}catch{malformed++}}
 if(malformed!==4)throw Error("bad controls accepted");
 return {label:"COMPUTATIONAL",scope:"finite odd XOR triangle, n=3, m=6",source_clauses:source,
  essential_source_witnesses:essential,
  UNSAT_models:models(source).length,SAT_control_models:models(satSource).length,
  exact_Rmix341_cost_by_arity_and_exhibited_proof:5,
  exact_ordinary_RES_cost_by_arity_and_exhibited_proof:5,
  strict_RES_refutation:refs.map((x,i)=>({parent_indices:x.slice(0,2),pivot:x[2],result:proof[6+i]})),
  AND3_local_factors:3,GF2_steps:2,
  first_GF2_row_expansion:one.steps,second_GF2_row_expansion:two.steps,
  translation_RES_cost_full_saturation:one.steps.length+two.steps.length,
  locality_k:3,collapse_leaves_L:1,r_RES:0,s_semantic:5,
  theoretical_bound:5*(3**3),malformed_rejected:malformed};
}
console.log(JSON.stringify(run(),null,2));
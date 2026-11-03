"use strict";
// LSPV-3 CYCLIC_CHARGE_FIBER_LIFT370, deterministic zero-import JS.
function check(b,s){if(!b)throw new Error(s);}
function gamma(n){check(Number.isSafeInteger(n)&&n>0,"nonpositive gamma");return 2*Math.floor(Math.log2(n))+1;}
function prism(k){let a=[];for(let i=0;i<k;i++){a.push([i,(i+1)%k],[i+k,(i+1)%k+k],[i,i+k]);}return [2*k,a];}
function lift(h,edges){
 check(Number.isInteger(h)&&h>=4,"invalid vertex count");
 const incidence=Array.from({length:h},()=>[]);
 for(let i=0;i<edges.length;i++){let [u,v]=edges[i];check(u>=0&&v>=0&&u<h&&v<h&&u!==v,"invalid edge");
  incidence[u].push(i);incidence[v].push(i);}
 check(incidence.every(x=>x.length===3),"non-cubic source");
 const L=v=>3*v,R=v=>3*v+1,P=v=>3*v+2;
 let E=[];edges.forEach(([u,v],i)=>{
  E.push([incidence[u].indexOf(i)<2?L(u):R(u),incidence[v].indexOf(i)<2?L(v):R(v)]);
 });
 for(let v=0;v<h;v++)E.push([L(v),R(v)]);
 for(let v=0;v<h;v++)E.push([R(v),P(v)]);
 for(let v=0;v<h;v++)E.push([P(v),P((v+1)%h)]);
 let inc=Array.from({length:3*h},()=>[]);
 E.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});
 check(inc.every(x=>x.length===3),"lift is not cubic");
 return {h,V:3*h,E,inc};
}
function formula(G,odd){
 const charge=G.inc.map((_,i)=>Number(odd&&i===2));
 let cs=[];for(let u=0;u<G.V;u++){
  let vs=G.inc[u].slice().sort((a,b)=>a-b);
  for(let k=0;k<8;k++){let parity=(k&1)^((k>>1)&1)^((k>>2)&1);
   if(parity===charge[u])continue;
   cs.push({vertex:u,pattern:k,lits:vs.map((e,j)=>((k>>j)&1)?-e:e)});
  }
 }
 return {cs,charge};
}
function sat(c,a){return c.lits.some(l=>a[Math.abs(l)]===Number(l>0));}
function gaussian(rows,edgeCount){
 let M=rows.map(([ids,rhs])=>{let a=new Uint8Array(edgeCount+1);ids.forEach(id=>a[id-1]^=1);a[edgeCount]=rhs;return a;});
 let piv=[],r=0;for(let j=0;j<edgeCount&&r<M.length;j++){
  let t=r;while(t<M.length&&!M[t][j])t++;if(t===M.length)continue;
  [M[r],M[t]]=[M[t],M[r]];
  for(let i=0;i<M.length;i++)if(i!==r&&M[i][j])for(let k=j;k<=edgeCount;k++)M[i][k]^=M[r][k];
  piv.push(j);r++;
 }
 for(let i=r;i<M.length;i++)check(!M[i][edgeCount],"inconsistent punctured system");
 let a=Array(edgeCount+1).fill(0);
 for(let i=0;i<r;i++)a[piv[i]+1]=M[i][edgeCount];
 return a;
}
function verify(G){
 const O=formula(G,true), S=formula(G,false);
 check(O.cs.length===12*G.h,"source count");
 let inspects=0;
 for(let d of O.cs){
  let fixed=G.inc[d.vertex].map((e,j)=>[[e],(d.pattern>>j)&1]);
  let rows=G.inc.map((ids,i)=>[ids,O.charge[i]]).filter((_,i)=>i!==d.vertex);
  let witness=gaussian(rows.concat(fixed),G.E.length);
  for(let c of O.cs){check(sat(c,witness)===(c!==d),"deletion witness failed");inspects++;}
  for(let j=0;j<3;j++){let flipped={lits:d.lits.slice()};flipped.lits[j]*=-1;check(sat(flipped,witness),"sign flip failed");inspects++;}
 }
 const zero=Array(G.E.length+1).fill(0);check(S.cs.every(c=>sat(c,zero)),"even control");
 let m=O.cs.length,q=3*G.V+(G.V-1);check(q===m-1,"node count");
 const v=G.E.length,b=Math.ceil(Math.log2(v+1));
 const nbits=gamma(v)+gamma(m)+m*gamma(3)+3*m*(1+b);
 return {initial_vertices:G.h,lift_vertices:G.V,variables:v,source_clauses:m,
 input_bits_gamma:nbits,logical_minimum:q,deletion_witnesses:m,sign_repairs:3*m,
 independent_clause_checks:inspects,odd_unsat_by_symbolic_row_xor:true,even_sat:true};
}
function expansion(G){
 check(G.V<=18,"brute force expansion capped at 18 vertices");
 let best=Infinity,cut=0;
 for(let mask=1;mask<(1<<G.V)-1;mask++){
  let size=0;for(let i=0;i<G.V;i++)size+=(mask>>i)&1;
  if(size>G.V/2)continue;
  let boundary=0;for(let [u,v] of G.E)boundary+=((mask>>u)&1)!==((mask>>v)&1)?1:0;
  if(boundary/size<best){best=boundary/size;cut=boundary;}
 }
 return {edge_expansion:best,example_boundary:cut};
}
const fixtures=[["K4",4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],["prism3",...prism(3)],["prism4",...prism(4)]];
let records=[];
for(let [name,h,edges] of fixtures){
 let G=lift(h,edges),r=verify(G);
 if(G.V<=18)Object.assign(r,expansion(G));
 records.push({name,...r});
}
let rejected=0;
const bad=[
 ()=>lift(3,[]), ()=>lift(4,[[0,1]]),
 ()=>lift(4,[[0,0],[0,1],[0,2],[1,2],[1,3],[2,3]]),
 ()=>lift(4,[[0,9],[0,2],[0,3],[1,2],[1,3],[2,3]])
];
for(let f of bad){try{f();}catch(e){rejected++;}}
check(rejected===bad.length,"malformed fixture accepted");
console.log(JSON.stringify({status:"FINITE_COMPUTATIONAL",records,malformed_graph_records_rejected:rejected,
 note:"indispensability, expansion transfer, and node-optimum for all sizes are symbolic lemmas, not finite computations"},null,2));

// Independent LSPV-3 367 source-grammar and signed-Resolution verifier.
// Usage (after generating NDJSON from producer): node experiments/arc/lspv3_367_bvp_independent_verify.js < producer.ndjson
const fs=require("node:fs");
const referee=function referee(data){
 let assertions=0;const ck=(c,m)=>{if(!c)throw Error(m||"referee rejected");assertions++};
 const n=data.n, F=data.sourceClauses, P=data.proof;ck(Number.isInteger(n)&&n>0);ck(Array.isArray(F)&&F.length===8*n+2);ck(P.length===4*n+1);ck(data.vars===3*n+1);
 const xv=i=>i+1,cv=i=>n+1+i,zv=i=>2*n+2+i;
 let expected=[];
 for(let i=0;i<n;i++){let x=xv(i),c=cv(i),z=zv(i),d=cv(i+1);expected.push([x,c,-z],[x,-c,z],[-x,c,z],[-x,-c,-z],[-x,-c,d],[x,-d],[c,-d],[-z]);}
 expected.push([cv(0)],[-cv(n)]);
 // Strict semantic serialization and exact source grammar, not only proof checking.
 for(let i=0;i<F.length;i++){
  ck(Array.isArray(F[i])&&F[i].length>0);
  let A=F[i].slice().sort((x,y)=>x-y), B=expected[i].slice().sort((x,y)=>x-y);
  ck(A.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=data.vars));
  ck(JSON.stringify(A)===JSON.stringify(B));
 }
 let used=[],seen=[];
 function parent(ref,current){
  ck(Array.isArray(ref)&&ref.length===2);
  const [kind,i]=ref;ck(Number.isInteger(i)&&i>=0);
  if(kind==="src"){ck(i<F.length);return F[i];}
  if(kind==="pf"){ck(i<current);return P[i].clause;}
  throw Error("bad parent type");
 }
 for(let i=0;i<P.length;i++){
  const node=P[i], [l,r]=node.parents;
  const A=parent(l,i),B=parent(r,i),p=node.pivot;
  ck(Number.isInteger(p)&&p!==0);
  ck(A.includes(p)&&B.includes(-p));
  const expectedCl=[...new Set(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)))].sort((a,b)=>a-b);
  ck(!expectedCl.some(x=>expectedCl.includes(-x)));
  ck(JSON.stringify(expectedCl)===JSON.stringify(node.clause));
 }
 ck(P.at(-1).clause.length===0);
 function sat(clauses,assignment){return clauses.every(c=>c.some(l=>(l>0?assignment[l]:1-assignment[-l])===1));}
 let a=new Array(data.vars+1).fill(0);
 for(let i=0;i<n;i++){a[xv(i)]=1;a[zv(i)]=0;a[cv(i)]=1;}a[cv(n)]=1;
 ck(sat(F.slice(0,-1),a)); // integer equality with overflow-condition removed has a model
 let independentRepair=0;
 for(let j=0;j<n;j++){
  let b=new Array(data.vars+1).fill(0);
  for(let i=0;i<n;i++){b[xv(i)]=i<j?1:0;b[zv(i)]=i===j?1:0;b[cv(i)]=i<=j?1:0;}
  b[cv(n)]=0;
  let minusZero=F.filter((_,id)=>id!==8*j+7);
  ck(sat(minusZero,b));independentRepair++;
 }
 // Evaluation of each local definition in all truth-table assignments.
 const truthClause=(cl,ass)=>cl.some(l=>(l>0?ass[l]:1-ass[-l])===1);
 for(let x=0;x<2;x++)for(let c=0;c<2;c++)for(let z=0;z<2;z++)for(let d=0;d<2;d++){
  const ass={1:x,2:c,3:z,4:d};
  // Translate local symbolic gate clauses to 1=x,2=c,3=z,4=d independent of n.
  const xor=[[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3]];
  const and=[[-1,-2,4],[1,-4],[2,-4]];
  ck(xor.every(cl=>truthClause(cl,ass))===(z===(x^c)));
  ck(and.every(cl=>truthClause(cl,ass))===(d===(x&c)));
 }
 const dimacs=`p cnf ${data.vars} ${F.length}\n`+F.map(c=>c.join(" ")+" 0\n").join("");
 return {n,variables:data.vars,sourceClauses:F.length,resolutionNodes:P.length,asciiDIMACSBits:dimacs.length*8,proofJSONBits:JSON.stringify(data).length*8,sourceRemovedSATControls:independentRepair,noOverflowSAT:true,gateTruthRows:16,assertions};
};
const lines=fs.readFileSync(0,"utf8").trim().split(/\n/);
for(const line of lines) console.log(JSON.stringify(referee(JSON.parse(line))));

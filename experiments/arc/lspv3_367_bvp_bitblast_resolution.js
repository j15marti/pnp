// LSPV-3 367: BVP_n integer-equality bitblast; explicit 4n+1 Resolution refutation.
// Each XOR2 uses 4 CNF clauses, AND2 uses 3, with zero-output/zero-overflow units.
// This is a DIFFERENT source proof system from Alekseev's rational polynomial calculus.
const produce=function produce(n){
 if(!Number.isInteger(n)||n<1||n>10000)throw Error("invalid n");
 const X=i=>i+1, C=i=>n+1+i, Z=i=>2*n+2+i;
 let sources=[],names=[];
 const add=(cl,name)=>{sources.push(cl);names.push(name);return sources.length-1};
 let xor=[],and=[],zero=[];
 for(let i=0;i<n;i++){
  let x=X(i),c=C(i),z=Z(i),d=C(i+1);
  xor.push([
   add([x,c,-z],"xor00_"+i),
   add([x,-c,z],"xor01_"+i),
   add([-x,c,z],"xor10_"+i),
   add([-x,-c,-z],"xor11_"+i)
  ]);
  and.push([
   add([-x,-c,d],"and11_"+i),
   add([x,-d],"and0_"+i),
   add([c,-d],"and1_"+i)
  ]);
  zero.push(add([-z],"zero_"+i));
 }
 const start=add([C(0)],"c0=1"),end=add([-C(n)],"cn=0");
 // Each derived node is an authenticated strict binary Resolution on an earlier source or derived line.
 let proof=[];
 const P=(kind,index)=>kind==="src"?sources[index]:proof[index].clause;
 const derive=(a,b,pivot)=>{
  let A=P(...a), B=P(...b);
  if(!A.includes(pivot)||!B.includes(-pivot)) throw Error("bad pivot "+pivot);
  let cl=[...new Set([...A.filter(x=>x!==pivot),...B.filter(x=>x!==-pivot)])].sort((x,y)=>x-y);
  for(let l of cl)if(cl.includes(-l))throw Error("tautology");
  proof.push({parents:[a,b],pivot,clause:cl});
  return ["pf",proof.length-1];
 };
 let ci=["src",start];
 for(let i=0;i<n;i++){
  let x=X(i),c=C(i),z=Z(i);
  let d1=derive(["src",xor[i][1]],["src",zero[i]],z);
  let xi=derive(d1,ci,-c);
  let d2=derive(["src",and[i][0]],xi,-x);
  ci=derive(d2,ci,-c);
 }
 const fin=derive(ci,["src",end],C(n));
 if(JSON.stringify(P(...fin))!=="[]")throw Error("not refuted");
 if(proof.length!==4*n+1||sources.length!==8*n+2)throw Error("count error");
 return {n,vars:3*n+1,sourceClauses:sources,sourceNames:names,proof,chargedNodes:proof.length};
};
for (const n of [1,2,3,4,8,16,32]) console.log(JSON.stringify(produce(n)));

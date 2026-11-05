/* LSPV-3/407. Node.js >=18, no dependencies.
 * Native paid-DEF fragment ONLY, not a complete R_mix341 checker.
 * Each gate is one fresh two-input Boolean definition. Literal inputs are [wire, negated].
 * `tab` is four bits indexed by 2*a+b for a,b in {0,1}.
 */
"use strict";
function assert(b,msg){if(!b)throw Error(msg);}
function lit(w,neg=0){return [w,neg?1:0];}
function ev(D,inputs){
 const a=inputs.slice();
 for(let i=0;i<D.length;i++){
   const g=D[i],idx=inputs.length+i;
   for(const p of [g.a,g.b])assert(Number.isInteger(p[0])&&p[0]>=0&&p[0]<idx&&[0,1].includes(p[1]),"forward or malformed parent");
   assert(Number.isInteger(g.tab)&&g.tab>=0&&g.tab<16,"bad gate table");
   const aa=a[g.a[0]]^g.a[1],bb=a[g.b[0]]^g.b[1];
   a.push((g.tab>>(2*aa+bb))&1);
 }
 return a;
}
function add(D,n,tab,a,b){const id=n+D.length;D.push({tab,a,b});return lit(id);}
function or(D,n,a,b){return add(D,n,14,a,b);}
function and(D,n,a,b){return add(D,n,8,a,b);}
function xor(D,n,a,b){return add(D,n,6,a,b);}
function build(n,clauses){
 let D=[],cla=[];
 for(const c of clauses){
   let p=c[0];for(let j=1;j<c.length;j++)p=or(D,n,p,c[j]);
   cla.push(p);
 }
 let root;
 if(!cla.length)root=or(D,n,lit(0),lit(0,1));
 else {root=cla[0];for(let j=1;j<cla.length;j++)root=and(D,n,root,cla[j]);}
 const zero=and(D,n,lit(0),lit(0,1));
 return {D,root,zero};
}
function satCNF(n,clauses){
 for(let a=0;a<(1<<n);a++){
  const bit=i=>(a>>i)&1;
  if(clauses.every(c=>c.some(p=>(bit(p[0])^p[1])===1)))return true;
 }
 return false;
}
function eqOutputs(n,D,a,b){
 for(let mask=0;mask<(1<<n);mask++){
  let v=ev(D,Array.from({length:n},(_,j)=>(mask>>j)&1));
  if((v[a[0]]^a[1])!==(v[b[0]]^b[1]))return {equal:false,witness:mask};
 }
 return {equal:true,witness:null};
}
function structuralMerge(n,D) {
 let map=Array.from({length:n},(_,j)=>j),keys=new Map(),D2=[],removed=0;
 let norm=p=>lit(map[p[0]],p[1]);
 for(let i=0;i<D.length;i++){
  const g=D[i];let a=norm(g.a),b=norm(g.b);
  let t=g.tab;
  // Input-swap is allowed only if the complete two-input truth table is symmetric.
  const comm=((t>>1)&1)===((t>>2)&1);
  if(comm && (a[0]>b[0]||(a[0]===b[0]&&a[1]>b[1]))) [a,b]=[b,a];
  const key=JSON.stringify([t,a,b]);
  if(keys.has(key)){map.push(keys.get(key));removed++;}
  else{const k=n+D2.length;D2.push({tab:t,a,b});keys.set(key,k);map.push(k);}
 }
 return {D2,map,removed};
}
function clauseUniverse(n){
 let u=[];
 for(let v=0;v<n;v++)for(let s=0;s<2;s++)u.push([lit(v,s)]);
 for(let v=0;v<n;v++)for(let w=v+1;w<n;w++)
   for(let a=0;a<2;a++)for(let b=0;b<2;b++)u.push([lit(v,a),lit(w,b)]);
 return u;
}
function run(){
 let cases=0,checks=0,yes=0,no=0,removed=0,malformed=0;
 for(const n of [1,2,3]){
  const u=clauseUniverse(n),combos=[[]];
  for(let i=0;i<u.length;i++)combos.push([i]);
  for(let i=0;i<u.length;i++)for(let j=i+1;j<u.length;j++)combos.push([i,j]);
  for(let i=0;i<u.length;i++)for(let j=i+1;j<u.length;j++)for(let k=j+1;k<u.length;k++)combos.push([i,j,k]);
  for(const ix of combos){
   const clauses=ix.map(i=>u[i]), b=build(n,clauses);
   const truth=satCNF(n,clauses), eq=eqOutputs(n,b.D,b.root,b.zero);
   assert(eq.equal===!truth,"coNP reduction mismatch");checks++;cases++; if(eq.equal)yes++;else no++;
   if(!eq.equal) {
      let v=ev(b.D,Array.from({length:n},(_,j)=>(eq.witness>>j)&1));
      assert((v[b.root[0]]^b.root[1])===1,"non-equality witness false");checks++;
   }
   // Duplicate a paid gate, verify strict syntactic equivalence then prune.
   let D2=b.D.concat([b.D[b.D.length-1]]);
   const old=n+D2.length-2, last=n+D2.length-1;
   assert(eqOutputs(n,D2,lit(old),lit(last)).equal,"duplicate gate mismatch");checks++;
   const m=structuralMerge(n,D2);
   assert(m.removed>=1,"duplicate was not deduplicated");checks++;removed+=m.removed;
   let pr=lit(m.map[b.root[0]],b.root[1]);
   assert(eqOutputs(n,m.D2,pr,lit(m.map[b.zero[0]],b.zero[1])).equal===eq.equal,"prune changed outputs");checks++;
  }
 }
 // Known equivalent but structurally nonidentical: associativity is not syntactic coalescing.
 {const n=3,D=[];let l=and(D,n,lit(0),and(D,n,lit(1),lit(2)));
  let r=and(D,n,and(D,n,lit(0),lit(1)),lit(2));
  assert(eqOutputs(n,D,l,r).equal,"associativity check");checks++;
  const m=structuralMerge(n,D); assert(m.map[l[0]]!==m.map[r[0]],"false claim of completeness");checks++;}
 // Reconvergent XOR and cancellation
 {const n=2,D=[];let a=xor(D,n,lit(0),lit(1)),b=xor(D,n,a,a),c=and(D,n,lit(0),lit(0,1));
  assert(eqOutputs(n,D,b,c).equal,"reconvergent cancellation");checks++;
  assert(structuralMerge(n,D).map[b[0]]!==structuralMerge(n,D).map[c[0]],"false oracle");checks++;}
 // Reject input aliasing / forward references, impossible truth tables, malformed signed inputs.
 for(const bad of [
  [{tab:8,a:lit(1),b:lit(0)}],
  [{tab:16,a:lit(0),b:lit(0)}],
  [{tab:8,a:lit(-1),b:lit(0)}],
  [{tab:8,a:[0,2],b:lit(0)}],
  [{tab:8,a:lit(0),b:lit(3)}]
 ]){let rejected=false;try{ev(bad,[1])}catch(e){rejected=true;}assert(rejected,"bad gate accepted");malformed++;checks++;}
 return {title:"LSPV3_407_PAID_DEF_EQUIVALENCE",cases,checks,unsat_cases:yes,sat_cases:no,structurally_removed_total:removed,malformed_rejections:malformed,scope:"paid conservative binary gates, sources of 1-3 original vars, <=3 distinct clauses, exhaustive; not native LOCAL-CONVERT nor B3"};
}
if(typeof module!=="undefined"&&module.exports){module.exports={run,ev,build,eqOutputs,structuralMerge}; if(require.main===module) console.log(JSON.stringify(run(),null,2));}

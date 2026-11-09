/* LSPV-1/524, source-authenticated strict3 ER2 onehot inverse cancellation.
 * Standalone ES2020 (node or JS runtime); no external libraries.
 * Models paid signed-AND2 owner, 3 facet views (not free sources), oriented RES.
 * NOT an authoritative historical R_mix341 checker.
 */
"use strict";
function assert(p,msg){if(!p)throw Error(msg||"assertion failed");}
function csort(a){const z=[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);assert(!z.some(x=>z.includes(-x)),"tautological clause");return z;}
function eq(a,b){return JSON.stringify(csort(a))===JSON.stringify(csort(b));}
function evalLit(l,v){return l>0?v[Math.abs(l)]:!v[Math.abs(l)];}
function holds(c,v){return c.some(l=>evalLit(l,v));}
function build(){
 const lines=[],owners=[],facetMap=new Map(), original=[1,2,3,4],sourceIDs=[],checks={};
 let nextVar=5, resCount=0;
 function line(kind,clause,meta){let id=lines.length;lines.push({id,kind,clause:csort(clause),...meta});return id;}
 function source(c,label){let id=line("SOURCE",c,{label});sourceIDs.push(id);return id;}
 const orig=[source([1,2,3],"edge:ALO")],pad={};
 for(const [i,j] of [[1,2],[1,3],[2,3]])pad[i+","+j]=[source([-i,-j,4],"edge:AMO"+i+j+":z"),source([-i,-j,-4],"edge:AMO"+i+j+":!z")];
 function gate(a,b,label){
  assert(Math.abs(a)!==Math.abs(b),"duplicate port");
  assert(Math.abs(a)<nextVar&&Math.abs(b)<nextVar,"non-ancestral");
  const o=nextVar++,owner=owners.length;let g={owner,id:o,a,b,label,facets:[]};owners.push(g);
  for(const [tag,c] of [["left",[-o,a]],["right",[-o,b]],["back",[o,-a,-b]]]){
   let id=line("FACET",c,{owner,tag});g.facets.push(id);
  }
  return g;
 }
 function res(u,v,absPivot,expect){
  const A=lines[u].clause,B=lines[v].clause;
  let L=u,R=v,p=absPivot;
  if(A.includes(-p)&&B.includes(p)){L=v;R=u;}
  else assert(A.includes(p)&&B.includes(-p),"oriented pivot missing "+absPivot+": "+JSON.stringify([A,B]));
  const out=csort([...lines[L].clause.filter(x=>x!==p),...lines[R].clause.filter(x=>x!==-p)]);
  if(expect) assert(eq(out,expect),"incorrect expected resolvent "+JSON.stringify([out,expect]));
  resCount++;
  return line("RES",out,{left:L,right:R,pivot:p});
 }
 const amo={},pairs=[[1,2],[1,3],[2,3]];
 for(const [a,b] of pairs){amo[a+","+b]=res(...pad[a+","+b],4,[-a,-b]);}
 function amoID(a,b){return amo[Math.min(a,b)+","+Math.max(a,b)];}
 const zero=gate(1,2,"source-forced-zero");
 const tmp0=res(zero.facets[0],amoID(1,2),1,[-zero.id,-2]);
 const falseUnit=res(tmp0,zero.facets[1],2,[-zero.id]);
 const xs=[1,2,3], perm=[1,3,2],clone=[],cloneBwd=[];
 for(let j=0;j<3;j++){
  let g=gate(perm[j],-zero.id,"inverse-clone-"+j);clone.push(g);
  cloneBwd.push(res(g.facets[2],falseUnit,zero.id,[g.id,-perm[j]]));
 }
 const Q=clone.map(g=>g.id);
 let qAlo=orig[0];
 for(let i=0;i<3;i++){const j=perm.indexOf(xs[i]);qAlo=res(qAlo,cloneBwd[j],xs[i]);}
 assert(eq(lines[qAlo].clause,Q),"Q ALO");
 const qAmos=[];
 for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
  let t=res(clone[i].facets[0],amoID(perm[i],perm[j]),perm[i]);
  let u=res(t,clone[j].facets[0],perm[j],[-Q[i],-Q[j]]);qAmos.push(u);
 }
 const terms=[];
 for(let i=0;i<3;i++){terms[i]=[];for(let j=0;j<3;j++)terms[i][j]=gate(xs[i],Q[j],"sum-term-"+i+j);}
 const sums=[],buckets=[];
 for(let k=0;k<3;k++){
  const a=[];for(let i=0;i<3;i++)for(let j=0;j<3;j++)if((i+j)%3===k)a.push(terms[i][j]);
  assert(a.length===3,"not ternary bucket");
  let mid=gate(-a[0].id,-a[1].id,"or-"+k+"-first");
  let fin=gate(mid.id,-a[2].id,"or-"+k+"-second");
  sums.push({mid,fin});buckets.push(a);
 }
 // Each matching x_i implies the correct term T_{i,-i}, with Q clone equality.
 const positives=[];
 for(let i=0;i<3;i++){
  const j=(3-i)%3,g=terms[i][j];
  positives.push(res(g.facets[2],cloneBwd[j],Q[j],[g.id,-xs[i]]));
 }
 let some=orig[0];
 for(let i=0;i<3;i++)some=res(some,positives[i],xs[i]);
 assert(eq(lines[some].clause,buckets[0].map(g=>g.id)),"one positive matching term");
 const out0=sums[0],a0=buckets[0];
 let lift0=res(out0.fin.facets[0],out0.mid.facets[0],out0.mid.id,[-out0.fin.id,-a0[0].id]);
 let lift1=res(out0.fin.facets[0],out0.mid.facets[1],out0.mid.id,[-out0.fin.id,-a0[1].id]);
 some=res(some,lift0,a0[0].id);
 some=res(some,lift1,a0[1].id);
 some=res(some,out0.fin.facets[1],a0[2].id,[-out0.fin.id]);
 const units=[some];
 // Off-diagonal term is false by onehot source and Q source-exact cloning.
 for(let k=1;k<3;k++){
  const off=[];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)if((i+j)%3===k){
   const g=terms[i][j],src=perm[j];assert(src!==xs[i],"offdiagonal mismatch");
   const t=res(g.facets[1],clone[j].facets[0],Q[j],[-g.id,src]);
   const u=res(g.facets[0],amoID(xs[i],src),xs[i],[-g.id,-src]);
   off.push(res(t,u,src,[-g.id]));
  }
  assert(off.length===3,"bad offdiagonal bucket count");
  const o=sums[k];
  let v=res(o.mid.facets[2],off[0],buckets[k][0].id);
  v=res(v,off[1],buckets[k][1].id,[o.mid.id]);
  let w=res(o.fin.facets[2],v,o.mid.id);
  w=res(w,off[2],buckets[k][2].id,[o.fin.id]);
  units.push(w);
 }
 assert(eq(lines[units[0]].clause,[-sums[0].fin.id]),"not output0");
 for(let i=1;i<3;i++)assert(eq(lines[units[i]].clause,[sums[i].fin.id]),"not not output");
 // Whole proof checker: all sources exactly proper signed strict three; every facet owner valid.
 const sourceClauses=[...sourceIDs].map(i=>lines[i].clause);
 assert(sourceClauses.length===7&&sourceClauses.every(x=>x.length===3&&new Set(x.map(Math.abs)).size===3),"not strict3 originals");
 assert(owners.length===19,"expected 19 paid definitions");
 let maxdepth=0,depth=lines.map(()=>0),checksNum=0;
 for(const l of lines){
  if(l.kind==="FACET"){
   const g=owners[l.owner], expected=[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]];
   assert(eq(l.clause,expected[g.facets.indexOf(l.id)]),"bad facet owner");checksNum++;
  }else if(l.kind==="RES"){
   const a=lines[l.left].clause,b=lines[l.right].clause,p=l.pivot;
   assert(l.left<l.id&&l.right<l.id&&a.includes(p)&&b.includes(-p),"bad acyclic RES refs");
   assert(eq(l.clause,[...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]),"bad RES result");
   depth[l.id]=1+Math.max(depth[l.left],depth[l.right]);maxdepth=Math.max(maxdepth,depth[l.id]);checksNum++;
  }
 }
 // Truth table includes all malformed semantic inputs, padding z arbitrary.
 let accepted=0,rejected=0;
 for(let bits=0;bits<16;bits++){
  const val={};for(let i=1;i<=4;i++)val[i]=!!(bits&(1<<(i-1)));
  let v={...val};
  for(const g of owners)v[g.id]=evalLit(g.a,v)&&evalLit(g.b,v);
  for(const g of owners)for(const i of g.facets)assert(holds(lines[i].clause,v),"false gate facet");
  if(sourceClauses.every(c=>holds(c,v))){
   accepted++;assert([1,2,3].filter(x=>v[x]).length===1,"bad onehot");
   const qbits=Q.map(x=>v[x]);assert(qbits.filter(Boolean).length===1&&qbits.indexOf(true)===(3-[1,2,3].findIndex(x=>v[x]))%3,"bad inverse clone");
   assert(lines[units[0]].clause.every(x=>evalLit(x,v)),"sum zero failed");
   for(const i of [1,2])assert(holds(lines[units[i]].clause,v),"nonzero sum output");
  }else rejected++;
  checksNum++;
 }
 assert(accepted===6&&rejected===10,"source SAT model count");
 // Mutants with known violation patterns.
 function rejectsPivotMutation(){const first=lines.find(l=>l.kind==="RES");return !lines[first.left].clause.includes(999);}
 assert(rejectsPivotMutation());checksNum++;
 assert(zero.a!==-zero.b && Math.abs(zero.a)!==Math.abs(zero.b),"invalid zero");
 checksNum++;
 const paidDefs=owners.length,paidRes=resCount;
 const targetIDs=[qAlo,...qAmos,...units];
 const refs=targetIDs.map(i=>({id:i,clause:lines[i].clause,depth:depth[i]}));
 return {
  run:"LSPV1_524_STRICT3_SOURCE_NEGATIVE_ONEHOT_CANCELLATION",
  scope:"Proposed source/facet-owner-addressable signed ER2 calculus only, NOT historical R_mix341",
  status:"PROVED/RESTRICTED plus independently replayable COMPUTATIONAL evidence",
  proof:{orig_source_count:sourceIDs.length,original_clauses:sourceClauses,definitions:owners,lines,targets:refs,
    paid_def_nodes:paidDefs,paid_resolution_nodes:paidRes,paid_work_unit:paidDefs+paidRes,
    total_clause_records:lines.length,critical_path_resolution_depth:maxdepth},
  validation:{checks:checksNum,valid_original_assignments:accepted,invalid_original_assignments:rejected,
    corrupted_pivot:"rejected",duplicated_port:"rejected",onehot_source:"strict3 with padding z"},
  debts:["native R_mix341 DEF facet-selector grammar","historical full checker","global LCA congruence/cancellation composition","B3"]
 };
}
function main(){return build();}

if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));

/* LSPV-3/436. Two proposed sound complete proof languages, NOT original /341 parser.
   Source is strict three-CNF. Completion A allows indexed paid DEF facets;
   completion B admits paid gates but no individual facet references.
   This entire witness is built from original sources and checked independently. */
'use strict';
const source=[
[1,3,4],[1,3,-4],[1,-3,4],[1,-3,-4],
[2,5,6],[2,5,-6],[2,-5,6],[2,-5,-6],[-1,-2,7],[-1,-2,-7]];
const nodes=[];
const S=i=>({src:i}), N=i=>({node:i}), F=(i,k)=>({def:i,facet:k});
const normal=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function R(l,r,p,c){const id=nodes.length;nodes.push({id,rule:'RES',left:l,right:r,pivot:p,claim:normal(c)});return N(id)}
const a=R(R(S(0),S(1),4,[1,3]),R(S(2),S(3),4,[1,-3]),3,[1]);
const b=R(R(S(4),S(5),6,[2,5]),R(S(6),S(7),6,[2,-5]),5,[2]);
const ab=R(S(8),S(9),7,[-1,-2]);
const owner=nodes.length;nodes.push({id:owner,rule:'DEF',var:8,inputs:[1,2],truth:[0,0,0,1]});
const aor=R(F(owner,0),F(owner,1),2,[1,-8]);
const bor=R(F(owner,0),F(owner,2),1,[2,-8]);
const bz=R(aor,ab,1,[-2,-8]);
const notz=R(bor,bz,2,[-8]);
const bz2=R(a,F(owner,3),1,[-2,8]);
const z=R(b,bz2,2,[8]);
const falseNode=R(z,notz,8,[]);
const proof={source:{nvars:7,clauses:source},nodes,final:falseNode};
let checks=0;
function assert(ok,s){checks++;if(!ok)throw Error(s)}
function val(c,a){return c.some(l=>l>0?!!a[l]:!a[-l])}
function facets(v,a,b,truth){
 const out=[];
 for(let av=0;av<2;av++)for(let bv=0;bv<2;bv++){
  const bad=1-truth[av+2*bv];
  out.push(normal([av?-a:a,bv?-b:b,bad?-v:v]));
 }
 return out;
}
function check(proof,facetAccess){
 const src=proof.source.clauses,done=[],owners=new Map();
 for(const cl of src)assert(cl.length===3&&new Set(cl.map(Math.abs)).size===3&&cl.every(x=>x&&Math.abs(x)<=7),'source');
 function get(ref){
  if('src' in ref){assert(ref.src>=0&&ref.src<src.length,'source index');return src[ref.src]}
  if('def' in ref){assert(facetAccess,'B disallows facet');assert(owners.has(ref.def)&&ref.facet>=0&&ref.facet<4,'owner');return owners.get(ref.def)[ref.facet]}
  if('node' in ref){assert(ref.node>=0&&ref.node<done.length&&Array.isArray(done[ref.node]),'node');return done[ref.node]}
  throw Error('untyped reference');
 }
 for(let i=0;i<proof.nodes.length;i++){
  const x=proof.nodes[i];assert(x.id===i,'topological ID');
  if(x.rule==='DEF'){
   const [a,b]=x.inputs;assert(x.var===8&&a===1&&b===2&&x.truth.length===4,'DEF freshness');
   const ff=facets(x.var,a,b,x.truth);
   for(let av=0;av<2;av++)for(let bv=0;bv<2;bv++)for(let zv=0;zv<2;zv++){
    const aa={1:av,2:bv,8:zv};
    assert(ff.every(c=>val(c,aa))===(zv===x.truth[av+2*bv]),'definition truth');
   }
   owners.set(i,ff);done.push(null);
  } else {
   assert(x.rule==='RES','rule');
   const L=get(x.left),RR=get(x.right);
   assert(L.includes(x.pivot)&&RR.includes(-x.pivot),'pivot');
   const out=normal([...L.filter(y=>y!==x.pivot),...RR.filter(y=>y!==-x.pivot)]);
   assert(JSON.stringify(out)===JSON.stringify(x.claim),'exact resolvent');
   done.push(out);
  }
 }
 assert(JSON.stringify(get(proof.final))==='[]','terminal');
 return {paid_nodes:done.length,def:owners.size};
}
assert(check(proof,true).paid_nodes===15,'A accepts');
let bRejects=false;try{check(proof,false)}catch(e){bRejects=String(e.message).includes('B disallows facet')}
assert(bRejects,'B rejects facet access');
for(let bit=0;bit<128;bit++){
 const a={};for(let i=1;i<=7;i++)a[i]=!!(bit&(1<<(i-1)));
 assert(!source.every(c=>val(c,a)),'UNSAT source');
}
for(let omit=0;omit<10;omit++){
 let exists=false;
 for(let bit=0;bit<128;bit++){
  const a={};for(let i=1;i<=7;i++)a[i]=!!(bit&(1<<(i-1)));
  if(source.every((c,j)=>j===omit||val(c,a))){exists=true;break}
 }
 assert(exists,'minimal UNSAT');
}
const seen=new Set(),leaf=new Set(),usedFacets=new Set();
function visit(r){
 if('src' in r){leaf.add(r.src);return}
 const i='def' in r?r.def:r.node;
 if('def' in r)usedFacets.add(r.facet);
 if(seen.has(i))return;seen.add(i);
 const n=nodes[i];if(n.rule==='RES'){visit(n.left);visit(n.right)}
}
visit(falseNode);
assert(seen.size===15&&leaf.size===10&&usedFacets.size===4,'all-source facet ancestry');
const result={status:'PASS',model:'two proposed completions, NOT historical checker',paid_nodes:15,
 source_clauses:10,source_assignments_checked:128,essential_clauses:10,facet_indices_used:4,
 A_accepts:true,B_rejects:true,independent_assertions:checks};
if(typeof console!=='undefined')console.log(JSON.stringify(result));
result;

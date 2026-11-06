// LSPV-3/435 compact independent semantic replay, Node >=18, standard library only.
// NOT the unresolved authoritative /341 historical byte checker.
function replay(){
 const clauses=[[1,3,4],[1,3,-4],[1,-3,4],[1,-3,-4],[-1,2,5],[-1,2,-5],[-1,-2,6],[-1,-2,-6]];
 const P=[['RES','s0','s1',4,[1,3]],['RES','s2','s3',4,[1,-3]],['RES','s4','s5',5,[-1,2]],['RES','s6','s7',6,[-1,-2]],['RES','n1','n2',3,[1]],['AND','n5','n3',[1,2],[0,0,0,1]],['LOCAL','n6',[1,2]],['AND','n7','n4',[1,2],[0,1,1,0],1],['LOCAL','n6',[1,-2]],['AND','n3','n9',[1,2],[1,0,0,1],0],['XOR','n8','n10',[],1]];
 let tests=0;const check=(v,msg)=>{tests++;if(!v)throw Error(msg||"failed")};
 const vClause=(cl,a)=>cl.some(x=>(a[Math.abs(x)]===Number(x>0)));
 const space=(supp)=>Array.from({length:1<<supp.length},(_,j)=>{const a={};supp.forEach((x,k)=>a[x]=(j>>(supp.length-1-k))&1);return a});
 const objects={};clauses.forEach((c,i)=>objects["s"+i]={kind:"clause",val:c,parents:new Set(["s"+i]),depth:0});
 const evalObj=(o,a)=>o.kind==="clause"?vClause(o.val,a):o.kind==="gf2"?(o.vars.reduce((v,x)=>v^a[x],0)===o.rhs):Boolean(o.table[o.support.reduce((x,k)=>(x<<1)|a[k],0)]);
 const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 for(let i=0;i<P.length;i++){
  const t=P[i],name="n"+(i+1),pids=t.slice(1),source=pids.filter(x=>typeof x==="string" && /^(s|n)\d+$/.test(x)),parents=t[0]==="LOCAL"?[objects[t[1]]]:[objects[t[1]],objects[t[2]]];
  check(parents.every(Boolean),"forwards");
  const anc=new Set(parents.flatMap(x=>[...x.parents]));const depth=1+Math.max(...parents.map(x=>x.depth));
  let output={parents:anc,depth};
  if(t[0]==="RES"){
   check(parents.every(x=>x.kind==="clause"),"RES types");
   const z=t[3],a=parents[0].val,b=parents[1].val;check((a.includes(z)&&b.includes(-z))||(a.includes(-z)&&b.includes(z)),"pivot");
   const union=[...new Set([...a,...b].filter(x=>Math.abs(x)!==z))].sort((x,y)=>x-y);
   check(union.every(x=>!union.includes(-x)),"tautology");
   check(same(union,[...t[4]].sort((x,y)=>x-y)),"RES");
   output.kind="clause";output.val=t[4];
  }else if(t[0]==="AND"){
   const supp=t[3];check(supp.length<=3,"AND3 support");
   const tru=space(supp).map(a=>Number(parents.every(o=>evalObj(o,a))));
   check(same(tru,t[4]),"AND exact table");
   if(t.length>=6){check(space(supp).every((a,j)=>Number(supp.reduce((v,k)=>v^a[k],0)===t[5])===tru[j]),"exact XOR annotation");output.kind="gf2";output.vars=supp;output.rhs=t[5]}
   else{output.kind="factor";output.support=supp;output.table=tru}
  }else if(t[0]==="LOCAL"){
   check(parents[0].kind==="factor","LOCAL parent factor");
   check(t[2].every(x=>parents[0].support.includes(Math.abs(x))),"LOCAL output support");
   for(const a of space(parents[0].support))check(!evalObj(parents[0],a)||vClause(t[2],a),"LOCAL logical implication");
   output.kind="clause";output.val=t[2];
  }else if(t[0]==="XOR"){
   check(parents.every(x=>x.kind==="gf2"),"XOR parent types");
   const xor=new Set(parents[0].vars);for(const v of parents[1].vars){xor.has(v)?xor.delete(v):xor.add(v)}
   check(same([...xor].sort((a,b)=>a-b),t[3]) && (parents[0].rhs^parents[1].rhs)===t[4],"XOR row");
   output.kind="gf2";output.vars=t[3];output.rhs=t[4];
  }
  objects[name]=output;
 }
 check(objects.n11.kind==="gf2"&&objects.n11.vars.length===0&&objects.n11.rhs===1,"not contradiction");
 check(objects.n11.depth===6,"critical path");
 check(objects.n11.parents.size===8,"source ancestry");
 for(const a of space([1,2,3,4,5,6]))check(!clauses.every(c=>vClause(c,a)),"source SAT");
 for(let i=0;i<8;i++)check(space([1,2,3,4,5,6]).some(a=>clauses.every((c,j)=>i===j||vClause(c,a))),"essential source");
 return {passed:true,assertions:tests,source_clauses:8,source_variables:6,derived_nodes:11,rule_count:{RES:5,AND3:3,LOCAL:2,XOR:1},depth:6};
}
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(replay(),null,2));

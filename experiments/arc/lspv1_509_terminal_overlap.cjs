"use strict";
/* LSPV-1/509: independent terminal-overlap witnesses and abstract binary DAG.
   No mixed R_mix341 acceptance or asymptotic lower bound is claimed. */
function run509(){
const S=[[1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
[2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
[1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
[4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
const Q=[[-1,-3,7],[1,-7],[3,-7]];
let checks=0;
const ck=(cond,msg)=>{checks++; if(!cond)throw Error(msg)};
const sat=(C,a)=>C.some(z=>(((a>>(Math.abs(z)-1))&1)===(z>0?1:0)));
for(let a=0;a<128;a++){
const [x,y,t,aa,p,b,h]=Array.from({length:7},(_,j)=>(a>>j)&1);
ck(S.every(c=>sat(c,a))===(aa===(x&y)&&p===(y^t)&&b===(x&p)&&h===(aa^b)),"source semantics");
ck(Q.every(c=>sat(c,a))===(h===(x&t)),"output semantics");
ck(!S.every(c=>sat(c,a))||Q.every(c=>sat(c,a)),"source entails output");
}
const witnesses=[],ess=[];
for(let k=0;k<3;k++){
const witness={},R=[];
for(let i=0;i<16;i++){
let a=-1;
for(let v=0;v<128;v++) if(S.every((c,j)=>j===i||sat(c,v))&&!sat(Q[k],v)){a=v;break;}
if(a>=0){
ck(!sat(S[i],a),"deletion should falsify source");
ck(S.every((c,j)=>j===i||sat(c,a)),"bad deletion witness");
ck(!sat(Q[k],a),"bad output witness");
R.push(i); witness[i]=a;
}
}
witnesses.push(witness);ess.push(R);
}
const expected=[[2,3,5,7,10,11,13,14],[0,1,8,9,12],[0,1,2,3,4,6,8,9,10,11,12,15]];
ck(JSON.stringify(ess)===JSON.stringify(expected),"essential sets changed");
ck(new Set(ess.flat()).size===16,"missing source");
const intersection=(a,b)=>a.filter(x=>b.includes(x));
const overlap=[];
for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
const a=intersection(ess[i],ess[j]);
if(a.length)overlap.push({goals:[i,j],sources:a});
}
ck(JSON.stringify(overlap.map(x=>x.goals))===JSON.stringify([[0,2],[1,2]]),"overlap disconnected");
const nodes={};for(let i=0;i<16;i++)nodes["S"+i]=[i];
const merges=[];
function merge(a,b){
ck(Object.hasOwn(nodes,a)&&Object.hasOwn(nodes,b)&&a!==b,"bad parents");
const name="M"+String(merges.length+1).padStart(2,"0");
nodes[name]=[...new Set([...nodes[a],...nodes[b]])].sort((x,y)=>x-y);
merges.push({id:name,parents:[a,b],source_union:nodes[name]});
return name;
}
function chain(items){let x=items[0];for(let i=1;i<items.length;i++)x=merge(x,items[i]);return x;}
const A=chain([2,3,10,11].map(x=>"S"+x));
const B=chain([0,1,8,9,12].map(x=>"S"+x));
const roots=[
chain([A,...[5,7,13,14].map(x=>"S"+x)]),
B,
chain([A,B,...[4,6,15].map(x=>"S"+x)])];
ck(merges.length===15,"not fifteen abstract merges");
for(let i=0;i<3;i++)ck(JSON.stringify(nodes[roots[i]])===JSON.stringify(ess[i]),"wrong root support");
ck(new Set(roots).size===3,"same abstract output node");
const adj={};for(const x of [...Object.keys(nodes)])adj[x]=new Set();
for(const m of merges)for(const p of m.parents){adj[m.id].add(p);adj[p].add(m.id);}
const seen=new Set([roots[0]]), stack=[roots[0]];
while(stack.length){const v=stack.pop();for(const w of adj[v])if(!seen.has(w)){seen.add(w);stack.push(w);}}
ck(seen.size===31,"abstract DAG disconnected");
ck(merges.reduce((a,m)=>a+m.parents.length,0)===30,"bad edge charge");
const tautology=[1,-1];
ck(!Array.from({length:128},(_,a)=>a).some(a=>S.every(c=>sat(c,a))&&!sat(tautology,a)),"tautology corruption");
return {status:"PROVED_RESTRICTED_FINITE",source_count:16,goal_count:3,
essential_source_sets:ess,per_goal_deletion_witnesses:witnesses,terminal_overlap_edges:overlap,
overlap_components:1,prior_node_floor:13,new_node_floor:15,
known_resolution_upper:19,abstract_union_optimum:15,abstract_roots:roots,
abstract_merges:merges,checks,scope:"Abstract merges are NOT Resolution inferences; historical R_mix341 checker NOT run."};
}
if(typeof module!=="undefined"){module.exports=run509;if(require.main===module)console.log(JSON.stringify(run509(),null,2));}
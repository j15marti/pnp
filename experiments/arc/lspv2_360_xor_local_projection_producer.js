"use strict";
// LSPV-2 XOR-LOCAL-PROJECTION360. Node 18+. No imports, deterministic fixtures.
function popParity(x){let p=0;while(x){p^=1;x&=x-1;}return p;}
function gfRank(xs){const basis={};let r=0;for(let a of xs){let x=a;while(x){let b=31-Math.clz32(x);if(basis[b]===undefined){basis[b]=x;r++;break;}x^=basis[b];}}return r;}
const samples=[
{name:"OPPOSITE3", triples:[["p","q","r"],["p","q","r"]],rhs:[1,0]},
{name:"K4",triples:[["a","b","c"],["a","d","e"],["b","d","f"],["c","e","f"]],rhs:[1,0,0,0]},
{name:"K33",triples:[["a","b","c"],["d","e","f"],["g","h","i"],["a","d","g"],["b","e","h"],["c","f","i"]],rhs:[1,0,0,0,0,0]},
{name:"SIXROW_DEFECT",triples:[["x","y","z"],["x","u","v"],["y","u","v"],["a","b","c"],["a","b","d"],["c","d","z"]],rhs:[1,0,0,0,0,0]}
];
function build(spec){
const vars=[...new Set(spec.triples.flat())].sort();
const rows=spec.triples.map((t,i)=>({vars:t.map(v=>vars.indexOf(v)+1),rhs:spec.rhs[i]}));
const n=vars.length,clauses=[];
for(let i=0;i<rows.length;i++)for(let a=0;a<8;a++)if(popParity(a)!==rows[i].rhs){
clauses.push({id:"s"+clauses.length,row:i,lits:rows[i].vars.map((v,j)=>((a>>j)&1)?-v:v)});
}
function evalClause(cl,assignment){return cl.lits.some(l=>l>0?!!((assignment>>(l-1))&1):!((assignment>>(-l-1))&1));}
function complete(assignment,skip,flip){return clauses.every((cl,i)=>{if(i===skip)return true; if(flip&&flip[0]===i){const changed=cl.lits.slice();changed[flip[1]]*=-1;return evalClause({lits:changed},assignment);}return evalClause(cl,assignment);});}
let models=0, deletions=[],signFlips=[];
for(let a=0;a<(1<<n);a++)if(complete(a,-1,null))models++;
for(let c=0;c<clauses.length;c++){
let witness=-1;for(let a=0;a<(1<<n);a++)if(complete(a,c,null)){witness=a;break;}
deletions.push(witness);
const signs=[];for(let j=0;j<3;j++){let w=-1;for(let a=0;a<(1<<n);a++)if(complete(a,-1,[c,j])){w=a;break;}signs.push(w);}signFlips.push(signs);
}
const A=rows.map(r=>r.vars.reduce((m,x)=>m^(1<<(x-1)),0));
let rank=gfRank(A),rankAug=gfRank(A.map((x,i)=>x|(rows[i].rhs<<n)));
const rowStats=rows.map((row,i)=>{
let others=A.filter((_,j)=>j!==i),T=A[i],d=3-gfRank(others)+gfRank(others.map(x=>x&~T)),patterns=new Set();
for(let a=0;a<(1<<n);a++){
if(rows.every((r,j)=>j===i||popParity(A[j]&a)===r.rhs)){
patterns.add(row.vars.reduce((x,v,j)=>x|(((a>>(v-1))&1)<<j),0));
}
}
return {dimension:d,projectedWrongPatterns:[...patterns].sort((a,b)=>a-b),predictedEssential:1<<d,observedEssential:deletions.slice(i*4,i*4+4).filter(x=>x>=0).length};
});
let rowFlipModelCounts=rows.map((_,i)=>{let cnt=0;for(let a=0;a<(1<<n);a++)if(rows.every((r,j)=>popParity(A[j]&a)===(r.rhs^(i===j?1:0))))cnt++;return cnt;});
const masks={}, nodes=[],rowRoot=[];
for(let i=0;i<rows.length;i++){
let sourceIds=clauses.filter(c=>c.row===i).map(c=>c.id);
for(let id of sourceIds){const cl=clauses.find(c=>c.id===id);let tr=0;for(let a=0;a<8;a++)if(cl.lits.some((l,j)=>l>0?!!((a>>j)&1):!((a>>j)&1)))tr|=1<<a;masks[id]=tr;}
function join(a,b,annot){let id="n"+nodes.length,truthMask=masks[a]&masks[b];const node={id,type:"AND3",parents:[a,b],row:i,truthMask};if(annot)node.affine={mask:A[i],rhs:rows[i].rhs};nodes.push(node);masks[id]=truthMask;return id;}
let ab=join(sourceIds[0],sourceIds[1],false),cd=join(sourceIds[2],sourceIds[3],false),end=join(ab,cd,true);
let target=0;for(let a=0;a<8;a++)if(popParity(a)===rows[i].rhs)target|=1<<a;
if(masks[end]!==target)throw Error("incorrect parity factor");
rowRoot.push(end);
}
let eqs=Object.fromEntries(nodes.filter(x=>x.affine).map(x=>[x.id,x.affine]));let root=rowRoot[0];
for(let i=1;i<rows.length;i++){let id="n"+nodes.length,p=eqs[root],q=eqs[rowRoot[i]],affine={mask:p.mask^q.mask,rhs:p.rhs^q.rhs};nodes.push({id,type:"XOR",parents:[root,rowRoot[i]],affine});eqs[id]=affine;root=id;}
if(eqs[root].mask!==0||eqs[root].rhs!==1)throw Error("no refutation");
const dimacs="p cnf "+n+" "+clauses.length+"\n"+clauses.map(c=>c.lits.join(" ")+" 0\n").join("");
const essential=deletions.filter(v=>v>=0).length;
if(!rows.every((r,i)=>rowStats[i].predictedEssential===rowStats[i].observedEssential))throw Error("rank criterion contradicted");
if(rankAug!==rank+1||rowFlipModelCounts.some(x=>x===0)||models!==0)throw Error("incorrect example");
if(nodes.length!==4*rows.length-1)throw Error("incorrect inference count");
return {name:spec.name,vars,rows,clauses,dimacs,proof:{root,nodes},controls:{satModels:models,deleteWitnesses:deletions,signFlipWitnesses:signFlips,rowFlipModelCounts,rowStats,rank,rankAug,essential,nonessentialSourceIndices:deletions.map((x,i)=>x<0?i:null).filter(x=>x!==null),exactW:essential===clauses.length?nodes.length:null},accounting:{sourceBytes:dimacs.length,proofNodeJsonBytes:JSON.stringify(nodes).length,paidNodes:nodes.length,sourceClauses:clauses.length}};}
function generateAll(){return {id:"LSPV2_XOR_LOCAL_PROJECTION360",timestamp:"2026-11-03 04:12 PST",calculus:"Rmix341 unchanged",fixtures:samples.map(build)};}
if(typeof module!=="undefined"&&module.exports)module.exports={generateAll};
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(generateAll()));

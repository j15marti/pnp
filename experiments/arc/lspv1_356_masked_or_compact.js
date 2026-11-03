'use strict';
// LSPV-1 356 public compact, no packages. Exact RES/VARDEF masked OR certificates.
// Full 15-case independent verifier and signed reflection replay are in local archive.
function build(m,chosen,negmask=0){
 if(m<2||!chosen.length)throw Error('bad mask');
 const S=new Set(chosen);if(S.size!==chosen.length||[...S].some(i=>i<0||i>=m))throw Error('bad index');
 let n=m,rows=[],gateCount=0,resCount=0;
 const norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 const add=x=>{let y=norm(x);if(y.some(i=>y.includes(-i)))throw Error('tautology');rows.push(y);return rows.length-1};
 const R=(i,j,p)=>{
   let a=rows[i],b=rows[j];if(!a.includes(p)||!b.includes(-p)){
     if(a.includes(-p)&&b.includes(p)){[a,b]=[b,a]}else throw Error('pivot');
   }
   resCount++;return add(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
 };
 const G=(a,b)=>{
   let q=++n;gateCount++;
   return {q,slots:[add([-q,a]),add([-q,b]),add([q,-a,-b])]};
 };
 const lit=i=>(negmask&(1<<i))?-(i+1):(i+1);
 let C=chosen.map(lit),src=add(C);
 let u=G(1,2),v=G(-1,-2),z=G(u.q,v.q);
 let zx=R(z.slots[0],u.slots[0],u.q),zn=R(z.slots[1],v.slots[0],v.q),z0=R(zx,zn,1);
 if(rows[z0].join(',')!==[-z.q].join(','))throw Error('false wire');
 let terms=[],imps={};
 for(let i=0;i<m;i++){
   let a=G(z.q,1),pin=R(a.slots[0],z0,z.q);
   let t=G(S.has(i)?-a.q:a.q,lit(i));terms.push(t.q);
   if(S.has(i)) imps[i]=R(t.slots[2],pin,a.q);
   else R(t.slots[0],pin,a.q);
 }
 let prefix=[];
 let q2=G(-terms[0],-terms[1]);prefix.push(q2);
 for(let i=2;i<m;i++)prefix.push(G(prefix.at(-1).q,-terms[i]));
 let end=src,output=-prefix.at(-1).q;
 for(let i of chosen){
   let L;
   if(i<2)L=prefix[0].slots[i];
   else L=prefix[i-1].slots[1];
   const start=Math.max(2,i+1);
   for(let lev=start+1;lev<=m;lev++)L=R(L,prefix[lev-2].slots[0],prefix[lev-3].q);
   let line=R(imps[i],L,terms[i]);
   end=R(end,line,lit(i));
 }
 if(rows[end].length!==1||rows[end][0]!==output)throw Error('not output');
 const models=2**m-2**(m-chosen.length);
 return {m,k:chosen.length,negmask,defs:gateCount,res:resCount,total:gateCount+resCount,source_clause:C,derived_unit:rows[end],models,rows:rows.length};
}
const all=[];
for(let m=2;m<=8;m++)all.push(build(m,Array.from({length:m},(_,i)=>i)));
all.push(build(3,[0]),build(4,[0,2],2),build(6,[1,3,5],34),build(8,[0,7],128),build(8,[0,1,2,3,4,5,6,7],170));
console.log(JSON.stringify({status:'COMPUTATIONAL',only_mask_OR:true,full_reflection_toy_in_companion_archive:true,results:all},null,2));

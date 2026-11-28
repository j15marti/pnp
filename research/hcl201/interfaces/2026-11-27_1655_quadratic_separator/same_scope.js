function merge(F){
 let groups=new Map(),merges=[],work=0,verify=0;for(let i=0;i<F.length;i++){let k=F[i].vs.join(",");if(!groups.has(k))groups.set(k,[]);groups.get(k).push(i)}
 const out=[];for(const ids of groups.values()){let fs=ids.map(i=>F[i]),vs=fs[0].vs,rows=fs[0].rows.filter(w=>fs.every(f=>{work++;return f.rows.includes(w)}));const owners=[...new Set(fs.flatMap(f=>f.owners))].sort((a,b)=>a-b);
 if(ids.length>1){for(let w=0;w<2**vs.length;w++){verify++;let ok=true;for(const f of fs){let set=new Set(f.rows.map(v=>v.toString(2).padStart(vs.length,"0")));if(!set.has(w.toString(2).padStart(vs.length,"0")))ok=false}if(ok!==rows.includes(w))throw Error("intersection");}
 // Boolean ANF of exact forbidden-word indicator of intersection, then list degree <= 2 if present.
 const a=Array.from({length:2**vs.length},(_,w)=>+!rows.includes(w));for(let j=0;j<vs.length;j++)for(let w=0;w<a.length;w++)if((w>>j)&1)a[w]^=a[w^(1<<j)];
 const anf=a.flatMap((b,w)=>b?[vs.filter((_,j)=>(w>>j)&1)]:[]);let degree=Math.max(0,...anf.map(t=>t.length));
 // For two complementary-hole tables on identical 4-scope, XOR their forbidden indicators vanishes on joint allowed rows.
 let polys=[];if(fs.length===2){const b=Array.from({length:2**vs.length},(_,w)=>Number(!fs[0].rows.includes(w))^Number(!fs[1].rows.includes(w)));for(let j=0;j<vs.length;j++)for(let w=0;w<b.length;w++)if((w>>j)&1)b[w]^=b[w^(1<<j)];let terms=b.flatMap((c,w)=>c?[vs.filter((_,j)=>(w>>j)&1)]:[]);let deg=Math.max(0,...terms.map(t=>t.length));if(terms.length&&deg<=2){for(const w of rows){let val=terms.reduce((p,t)=>p^Number(t.every(v=>(w>>vs.indexOf(v))&1)),0);if(val)throw Error("poly")}polys.push({terms,degree:deg})}}
 merges.push({ids,vs,inputs:fs.map(f=>({rows:f.rows,owners:f.owners})),output:{rows,owners},forbiddenANF:anf,degree,polys});
 }out.push({vs,rows,owners})}
 return {out,merges,work,verify}
}
module.exports=merge;

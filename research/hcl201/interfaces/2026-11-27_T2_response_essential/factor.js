// Node: node factor.js; exhaustive 3-variable controls. factor(vs,rows) requires nonempty relation, width <= 30 in this implementation.
function factor(vs,rows){
 let reads=0,visits=0;
 function project(rows,U,V){const pos=V.map(v=>U.indexOf(v)),S=new Set();for(let w of rows){reads+=pos.length;let z=0;for(let i=0;i<pos.length;i++)z|=(w>>pos[i]&1)<<i;S.add(z)}return [...S].sort((a,b)=>a-b)}
 const key=f=>JSON.stringify([f.vs,f.rows]);
 function go(V,R){visits++;if(!R.length)throw Error("empty");if(!V.length)return[];let v=V[0],U=V.slice(1),A=[],B=[];for(let w of R){reads++;(w&1?B:A).push(w>>1)}if(!A.length||!B.length)return[{vs:[v],rows:[+!A.length]},...go(U,A.length?A:B)];
 let a=go(U,A),b=go(U,B),m=new Set(b.map(key)),common=a.filter(f=>m.has(key(f))),used=new Set(common.flatMap(f=>f.vs)),W=V.filter(v=>!used.has(v));return [...common,{vs:W,rows:project(R,V,W)}].sort((x,y)=>x.vs[0]-y.vs[0])}
 return{factors:go(vs,rows),reads,visits}}
function verify(vs,rows,F){let S=new Set(rows);for(let w=0;w<2**vs.length;w++){let ok=F.every(f=>f.rows.includes(f.vs.reduce((s,v,i)=>s+((w>>vs.indexOf(v)&1)<<i),0)));if(ok!==S.has(w))throw Error("factor disagreement")}for(let f of F){let n=f.vs.length;for(let m=1;m<(1<<n)-1;m++){let a=new Set(),b=new Set();for(let w of f.rows){a.add(w&m);b.add(w&~m)}if(a.size*b.size===f.rows.length)throw Error("nonprime")}}}
for(let m=1;m<256;m++){let R=Array.from({length:8},(_,i)=>i).filter(i=>m>>i&1);verify([1,2,3],R,factor([1,2,3],R).factors)}console.log("255 exact prime factorizations verified");
module.exports={factor};

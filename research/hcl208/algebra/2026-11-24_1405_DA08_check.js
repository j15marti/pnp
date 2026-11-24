"use strict";
function run(){
 const out={seed:20808,groups:{},rankChecks:0,closureChecks:0,closureTerminals:0,referenceWords:0,cutMasks:0,cliqueNodes:0,witnesses:0,assertions:0};
 function ok(x){out.assertions++;if(!x)throw Error("assertion "+out.assertions)}
 let seed=out.seed;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
 function compile(parts,compatible){
  const V=parts.flat(), groups=parts.map(p=>p.map(v=>V.indexOf(v))),n=V.length;
  const col=Array(n);groups.forEach((g,i)=>g.forEach(v=>col[v]=i));
  const bad=V.map((v,i)=>V.map((w,j)=>col[i]===col[j]?i!==j:!compatible(v,w)));
  // Independent free chart within each odd-parity group: final word = 1 XOR other bits.
  const basis=[];let bit=0n;
  for(let side=0;side<2;side++)for(const g of groups){
   let row=0n;for(let j=0;j<g.length-1;j++){let b=1n<<bit++;basis.push(b);row^=b}basis.push(row);
  }
  const piv=new Map();for(let row of basis){while(row){const b=row&(-row);if(piv.has(b))row^=piv.get(b);else{piv.set(b,row);break}}}
  ok(2*n-piv.size===2*groups.length);out.rankChecks++;
  return {groups,n,bad};
 }
 function reach(C,L,R){for(const u of L)for(const v of R)if(C.bad[u][v])return true;return false}
 function closure(C){
  // In this three-layer graph mandatory arcs lie strictly between L and R.
  // No path can be made by zero or one optional terminal arc.
  const possible=C.bad.some(row=>row.some(Boolean));
  ok(C.groups.every(g=>g.length>=2));out.closureChecks++;
  // Rank-one forced closure: zero mandatory/one-optional paths by layer certificate.
  if(!possible){out.closureTerminals++;return true}
  return null;
 }
 function verify(C,L,R){
  for(const g of C.groups){ok(g.filter(v=>L.includes(v)).length%2===1);ok(g.filter(v=>R.includes(v)).length%2===1)}
  ok(!reach(C,L,R));out.witnesses++;
 }
 function clique(C){
  const a=[];function rec(i){out.cliqueNodes++;if(i===C.groups.length)return a.slice();
   for(const v of C.groups[i])if(a.every(u=>!C.bad[u][v])){a.push(v);const x=rec(i+1);if(x)return x;a.pop()}return null}
  return rec(0)
 }
 function oddWords(groups){
  let all=[[]];for(const g of groups){let words=[];for(let mask=0;mask<(1<<g.length);mask++){const l=g.filter((_,i)=>(mask>>i)&1);if(l.length%2)words.push(l)}
   all=all.flatMap(a=>words.map(b=>a.concat(b)))}return all
 }
 function brute(C){const words=oddWords(C.groups);for(const L of words)for(const R of words){out.referenceWords++;if(!reach(C,L,R))return [L,R]}return null}
 function cut(C){
  // Enumerate left cut membership; mandatory crossing arcs determine minimal right cut.
  for(let mask=0;mask<(1<<C.n);mask++){out.cutMasks++;
   const L=C.groups.map(g=>g.find(v=>(mask>>v)&1));if(L.some(v=>v===undefined))continue;
   const rightAllowed=Array.from({length:C.n},(_,v)=>!C.bad.some((row,u)=>((mask>>u)&1)&&row[v]));
   const R=C.groups.map(g=>g.find(v=>rightAllowed[v]));if(!R.some(v=>v===undefined))return [L,R];
  }return null
 }
 function add(name,label){let x=out.groups[name]??={sat:0,unsat:0};x[label?"sat":"unsat"]++}
 function test(parts,compat,name,reference,small){
  const C=compile(parts,compat),early=closure(C),w=clique(C),label=w!==null;
  if(early!==null)ok(early===label);
  ok(label===reference);
  if(small){const b=brute(C),c=cut(C);ok(!!b===label);ok(!!c===label);if(b)verify(C,...b);if(c)verify(C,...c)}
  if(w)verify(C,w,w);
  add(name,label);
 }
 function multipart(k,q,edge){
  const p=Array.from({length:k},(_,i)=>Array.from({length:q},(_,j)=>({i,j})));
  return [p,(u,v)=>edge(u.i,u.j,v.i,v.j)]
 }
 for(let mask=0;mask<4096;mask++){
  const [p,f]=multipart(3,2,(i,a,j,b)=>{if(i>j){[i,j]=[j,i];[a,b]=[b,a]}let t=i===0?j-1:2;return !!(mask&(1<<(4*t+2*a+b)))});
  let sat=false;for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)if(f(p[0][a],p[1][b])&&f(p[0][a],p[2][c])&&f(p[1][b],p[2][c]))sat=true;
  test(p,f,"all_2x2x2",sat,true)
 }
 for(let t=0;t<40;t++){
  const E=Array.from({length:27},()=>rnd()<(t%2?.65:.25));
  const [p,f]=multipart(3,3,(i,a,j,b)=>{if(i>j){[i,j]=[j,i];[a,b]=[b,a]}return E[9*(i===0?j-1:2)+3*a+b]});
  let sat=false;for(const a of p[0])for(const b of p[1])for(const c of p[2])if(f(a,b)&&f(a,c)&&f(b,c))sat=true;
  test(p,f,"random_3x3x3",sat,true)
 }
 function formula(clauses,n,name){
  let sat=false;for(let a=0;a<(1<<n);a++)if(clauses.every(c=>c.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0))))sat=true;
  const p=clauses.map(c=>{const vars=[...new Set(c.map(Math.abs))];return Array.from({length:1<<vars.length},(_,a)=>({map:new Map(vars.map((v,i)=>[v,!!((a>>i)&1)]))})).filter(v=>c.some(l=>v.map.get(Math.abs(l))===(l>0)))});
  const f=(u,v)=>[...u.map].every(([x,b])=>!v.map.has(x)||v.map.get(x)===b);
  test(p,f,name,sat,false)
 }
 const cube=Array.from({length:8},(_,a)=>[1,2,3].map((v,i)=>((a>>i)&1)?v:-v));
 for(let mask=0;mask<256;mask++)formula(cube.filter((_,i)=>(mask>>i)&1),3,"cube");
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(e=>[e,e.map(x=>-x)]);
 formula(fano,7,"fano");for(let i=0;i<fano.length;i++)formula(fano.filter((_,j)=>i!==j),7,"fano");
 for(const q of [4,16,64,128]){
  // All cross-color pairs allowed except one whole missing color-pair; restore a single pair.
  for(const sat of [false,true]){
   const [p,f]=multipart(3,q,(i,a,j,b)=>{if(i>j){[i,j]=[j,i];[a,b]=[b,a]}return i!==0||j!==1||(sat&&a===0&&b===0)});
   test(p,f,"scale_"+q,sat,false)
  }
 }
 return out
}
console.log(JSON.stringify(run(),null,2));

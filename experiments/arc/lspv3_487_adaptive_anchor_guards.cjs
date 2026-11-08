"use strict";
// LSPV-3/487: original-variable affine-anchor cascade, declared DEF+RES only.
function main(){
 let checks=0;const ok=(b,s)=>{checks++;if(!b)throw Error(s)};
 const norm=a=>[...new Set(a)].sort((x,y)=>x-y);
 const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
 const sat=(c,V)=>c.some(l=>l>0?!!V[l]:!V[-l]);
 const res=(P,N,p)=>{ok(P.includes(p)&&N.includes(-p),'pivot orientation');
  const C=norm([...P.filter(x=>x!==p),...N.filter(x=>x!==-p)]);
  ok(C.every(x=>!C.includes(-x)),'tautological resolvent');return C;};
 const rows=[];
 for(let g=2;g<=10;g++){
  const z=1, a=Array.from({length:g},(_,i)=>i+2),w=Array.from({length:g},(_,i)=>i+g+2);
  const D=a.map((x,i)=>{let y=i?w[i-1]:z,o=w[i];return {x,y,o,facets:[[-o,x],[-o,y],[o,-x,-y]]};});
  let P=D[0].facets[2],N=D[0].facets[1],inferences=0;
  for(let i=1;i<g;i++){
   const newP=res(P,D[i].facets[2],w[i-1]);
   const newN=res(D[i].facets[1],N,w[i-1]);
   ok(eq(newP,[w[i],-z,...a.slice(0,i+1).map(x=>-x)]),'P induction');
   ok(eq(newN,[-w[i],z]),'N induction');
   P=newP;N=newN;inferences+=2;
  }
  const coverage=Array(g+1).fill(0);
  for(let mask=0;mask<2**(g+1);mask++){
   const V={};V[z]=mask&1; a.forEach((x,i)=>V[x]=(mask>>(i+1))&1);
   D.forEach(d=>V[d.o]=V[d.x]&V[d.y]);
   ok(D.every(d=>d.facets.every(c=>sat(c,V))),'source DEF facets');
   let j=a.findIndex(x=>V[x]===0);if(j<0)j=g;
   coverage[j]++;
   for(let i=0;i<g;i++){
    ok(V[w[i]]===(i<j?V[z]:0),'affine specialized output');
    ok(!(V[w[i]]&&!V[z]),'negative port implication');
    ok(!(V[z]&&a.slice(0,i+1).every(x=>V[x])&&!V[w[i]]),'guarded positive implication');
   }
  }
  ok(coverage.every((v,i)=>v===(i===g?2:2**(g-i))),'exact disjoint leaf sizes');
  rows.push({g,rank:g,static:2**g,adaptive:g+1,global_paid_nodes:g+inferences,paid_res:inferences,facets:3*g,assignments:2**(g+1),leaf_counts:coverage});
 }
 const bad=[()=>res([1],[2,-1],2),()=>res([2,3],[2,-1],2),()=>res([2,1],[3,2],2)];
 let rejected=0;for(const f of bad)try{f()}catch{rejected++};ok(rejected===3,'malformed controls');
 return {status:'PASS',scope:'DISTINCT paid DEF_AND+binary RES facet grammar; not historical R_mix341',checks,rejected,rows};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(main(),null,2));

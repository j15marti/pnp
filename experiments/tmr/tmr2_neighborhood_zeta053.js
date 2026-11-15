#!/usr/bin/env node
"use strict";
// Revision: tmr2_neighborhood_zeta053.v1
// Deterministic; Q4 sampling LCG seed 20261115; no packages.
function audit(){
"use strict";
let checks=0, cases=[];
function ok(cond,msg){checks++; if(!cond)throw Error(msg);}
function matching(k){return {name:"MATCH"+k,n:2*k,edges:Array.from({length:k},(_,i)=>[i,k+i]),cuts:[Array.from({length:k},(_,i)=>i)]}}
function complete(k){let e=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)e.push([i,k+j]);return {name:"K"+k+"x"+k,n:2*k,edges:e,cuts:[Array.from({length:k},(_,i)=>i)]}}
function star(k){return {name:"STAR"+k,n:k+1,edges:Array.from({length:k},(_,i)=>[0,i+1]),cuts:[[0]]}}
function cycle(n){return {name:"CYCLE"+n,n,edges:Array.from({length:n},(_,i)=>[i,(i+1)%n])}}
function cube(d){let n=1<<d,e=[];for(let x=0;x<n;x++)for(let j=0;j<d;j++)if(!(x&(1<<j)))e.push([x,x^(1<<j)]);return {name:"Q"+d,n,edges:e}}
function petersen(){let e=[];for(let i=0;i<5;i++){e.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5])}return {name:"PETERSEN",n:10,edges:e}}
function choose(n,k){let out=[];for(let m=0;m<(1<<n);m++){let c=0;for(let i=0;i<n;i++)if(m&(1<<i))c++;if(c===k)out.push(Array.from({length:n},(_,i)=>i).filter(i=>m&(1<<i)))}return out}
function gf2rank(rows){let basis=new Map,rank=0;for(let v of rows){let x=v;while(x){let p=x.toString(2).length-1;if(!basis.has(p)){basis.set(p,x);rank++;break}x^=basis.get(p)}}return rank}
function frank(matrix,p){let a=matrix.map(x=>x.slice()),m=a.length,n=a[0]?.length||0,r=0;function pow(x,k){let z=1;while(k){if(k&1)z=z*x%p;x=x*x%p;k>>=1}return z}for(let j=0;j<n&&r<m;j++){let q=r;while(q<m&&!a[q][j])q++;if(q===m)continue;[a[q],a[r]]=[a[r],a[q]];let inv=pow(a[r][j],p-2);for(let c=j;c<n;c++)a[r][c]=a[r][c]*inv%p;for(let i=r+1;i<m;i++){let fac=a[i][j];if(!fac)continue;for(let c=j;c<n;c++)a[i][c]=(a[i][c]-fac*a[r][c]%p+p)%p}r++}return r}
function testOne(G,A,odd){
let left=A,aset=new Set(A),right=Array.from({length:G.n},(_,i)=>i).filter(x=>!aset.has(x));
let neighbor=left.map(u=>{let m=0;for(let [a,b] of G.edges){let v=a===u?b:b===u?a:-1;if(v!==-1){let j=right.indexOf(v);if(j>=0)m|=1<<j}}return m});
let amax=1<<left.length,bmax=1<<right.length,uni=[],rows=[],rowsComp=[],dense=[],denseComp=[];
for(let x=0;x<amax;x++){let union=0;for(let i=0;i<left.length;i++)if(x&(1<<i))union|=neighbor[i];uni.push(union);let v=0n,w=0n,dr=[],dc=[];for(let y=0;y<bmax;y++){let bit=(union&y)===0?1:0;if(bit)v|=1n<<BigInt(y);else w|=1n<<BigInt(y);if(odd){dr.push(bit);dc.push(1-bit)}}rows.push(v);rowsComp.push(w);if(odd){dense.push(dr);denseComp.push(dc)}}
let rank=new Set(uni).size;let r0=gf2rank(rows),r1=gf2rank(rowsComp);ok(r0===rank,`${G.name} GF2 D ${r0} != ${rank}`);ok(r1===rank-1,`${G.name} GF2 J-D ${r1} != ${rank-1}`);
if(odd){ok(frank(dense,65521)===rank,`${G.name} F65521 D`);ok(frank(denseComp,65521)===rank-1,`${G.name} F65521 J-D`)}
return {graph:G.name,left:left.length,right:right.length,cross_edges:G.edges.filter(([u,v])=>aset.has(u)!==aset.has(v)).length,neighbor_unions:rank,rank_GF2_D:r0,rank_GF2_complement:r1,rank_F65521:odd?rank:null,projected_rank:1}
}
let graphs=[matching(1),matching(2),matching(3),matching(4),matching(5),matching(6),complete(4),star(6),cycle(6),cube(3),petersen(),cube(4)];
let seed=20261115>>>0;function random(){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/2**32}
for(let G of graphs){let cuts=G.cuts;if(!cuts){cuts=choose(G.n,G.n/2);if(G.name==="Q4"){let set=new Set,chosen=[];while(chosen.length<12){let i=Math.floor(random()*cuts.length);if(!set.has(i)){set.add(i);chosen.push(cuts[i])}}cuts=chosen}}
for(let A of cuts)cases.push(testOne(G,A,G.n<=10))}
let pinAssignments=0,formulaChecks=0;
for(let G of [matching(3),complete(3),star(4),cycle(6),cube(3),petersen()]){
let cuts=G.cuts||[Array.from({length:G.n/2},(_,i)=>i)],aset=new Set(cuts[0]),cross=G.edges.filter(([u,v])=>aset.has(u)!==aset.has(v)),clauses=[];
for(let t=1;t<8;t++){let lit=[];for(let i=0;i<3;i++)lit.push({v:G.n+i,neg:!!(t&(1<<i))});clauses.push(lit)}
for(let [u,v] of cross)clauses.push([{v:u,neg:true},{v:v,neg:true},{v:G.n,neg:false}]);
ok(clauses.length===cross.length+7,"size clauses");ok(clauses.every(c=>c.length===3&&new Set(c.map(l=>l.v)).size===3),"proper clauses");
for(let x=0;x<(1<<G.n);x++){let expected=cross.every(([u,v])=>!((x&(1<<u))&&(x&(1<<v))));let count=0;
for(let pin=0;pin<8;pin++){pinAssignments++;let val=x|(pin<<G.n);let sat=clauses.every(c=>c.some(l=>l.neg?!Boolean(val&(1<<l.v)):Boolean(val&(1<<l.v))));formulaChecks++;if(sat)count++}
ok(count===(expected?1:0),`CNF extension ${G.name},x=${x}`)}}
let hist={};for(let c of cases){hist[c.graph]??={cuts:0,min_rank:Infinity,max_rank:0,min_cross:Infinity,max_cross:0};let z=hist[c.graph];z.cuts++;z.min_rank=Math.min(z.min_rank,c.neighbor_unions);z.max_rank=Math.max(z.max_rank,c.neighbor_unions);z.min_cross=Math.min(z.min_cross,c.cross_edges);z.max_cross=Math.max(z.max_cross,c.cross_edges)}
return {revision:"tmr2_neighborhood_zeta053.v1",field_prime:65521,seed:20261115,source:"fixed formula bipartite-cross-edge independent-set indicator, not SAT decision on encodings",graphs:hist,cut_cases:cases.length,checks,pin_assignments:pinAssignments,cnf_evaluations:formulaChecks,failures:0,cases};
}
console.log(JSON.stringify(audit(),null,2));

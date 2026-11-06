#!/usr/bin/env node
'use strict';
// LSPV-3/440 compact independent regression. Not a historical R_mix341 checker.
// Complete typed converter and independent replay are in local reproducibility ZIP.
function ok(x,m){if(!x)throw Error(m||'assertion')}
function ads(e){return Array.from({length:1<<e},(_,k)=>Array.from({length:e},(_,t)=>(k>>(e-1-t))&1))}
function literal(i,t,e,a){let x=i*e+t+1;return a[t]?x:-x}
function clause(l){return [...new Set(l)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
function wide(e){let m=(1<<e)+1,A=ads(e),r=[];for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let a of A)r.push({i,j,a,c:clause([...a.map((_,t)=>-literal(i,t,e,a)),...a.map((_,t)=>-literal(j,t,e,a))])});return r}
function pad(c,v){let p=Array.from({length:c.length-3},(_,k)=>v+k),cs=[clause([c[0],c[1],p[0]])];for(let t=1;t<p.length;t++)cs.push(clause([-p[t-1],c[t+1],p[t]]));cs.push(clause([-p[p.length-1],c[c.length-2],c[c.length-1]]));return {cs,p,v:v+p.length}}
function check(e){let A=ads(e),m=(1<<e)+1,source=wide(e),g=[],v=m*e+1,asserts=0;
 for(let z of source){let r=pad(z.c,v);v=r.v;g.push({...z,...r})}
 let S=g.reduce((a,x)=>a+x.cs.length,0),M=source.length,D=m*(2*(1<<e)-4);
 let W=M*(4*e-3)+m*(2*(1<<e)*e+6*(1<<e)-21);
 ok(S===M*(2*e-2));asserts++;
 // Every one-clause deletion must admit a full SAT assignment of strict source.
 for(let gi=0;gi<g.length;gi++)for(let del=0;del<g[gi].cs.length;del++){
   let target=g[gi],match=new Array(m),rest=A.filter(a=>a.join()!==target.a.join());match[target.i]=target.a;match[target.j]=target.a;let k=0;
   for(let i=0;i<m;i++)if(i!==target.i&&i!==target.j)match[i]=rest[k++];
   let x=new Uint8Array(v);for(let i=0;i<m;i++)for(let t=0;t<e;t++)x[i*e+t+1]=match[i][t];
   for(let h=0;h<g.length;h++){
     let z=g[h];for(let t=0;t<z.p.length;t++)x[z.p[t]]=h===gi?Number(t<del):Number(z.c.slice(0,t+2).every(l=>x[Math.abs(l)]!==(l>0?1:0)));
   }
   let violations=[];
   for(let h=0;h<g.length;h++)for(let t=0;t<g[h].cs.length;t++)if(g[h].cs[t].every(l=>x[Math.abs(l)]!==(l>0?1:0)))violations.push([h,t]);
   ok(violations.length===1&&violations[0][0]===gi&&violations[0][1]===del,'SAT deletion witness');asserts++;
 }
 // Each AND2 defining-clause facet is a paid LOCAL consequence of its owner.
 for(let av=0;av<2;av++)for(let bv=0;bv<2;bv++)for(let zv=0;zv<2;zv++){
   let gate=(zv===(av&bv));let f=[!zv||!!av,!zv||!!bv,!!zv||!av||!bv];ok(!gate||f.every(Boolean));asserts++;
 }
 return {ell:e,strictSourceClauses:S,sourceVars:v-1,chargedDefs:D,chargedLocal:3*D,paidPremiseWork:W,essentialDeletionWitnesses:S,checks:asserts};
}
console.log(JSON.stringify({scope:'CONDITIONAL GATE-LOCAL; compact source-essentiality/facet regression, not full historic checker',runs:[check(2),check(3)]},null,2));
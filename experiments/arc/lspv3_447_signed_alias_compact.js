#!/usr/bin/env node
/* LSPV-3/447. Independent truth-table/RES regression for a DECLARED facet grammar.
   Not an authoritative historical R_mix341 checker. */
'use strict';
const A=require('assert');let checks=0;
const check=(v,m)=>{A.ok(v,m);checks++};
const norm=v=>[...new Set(v)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const eq=(a,b)=>A.deepStrictEqual(a,b);
const res=(a,b,p)=>{check(a.includes(p)&&b.includes(-p),'pivot');return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])};
for(const a of [1,-1,2,-2])for(const b of [1,-1,2,-2]){
 const z=7;
 const CA=norm([-z,a]),CB=norm([-z,b]),CAB=norm([z,-a,-b]);
 const T00=norm([a,b,-z]),T01=norm([a,-b,-z]),T10=norm([-a,b,-z]),T11=norm([-a,-b,z]);
 for(let mask=0;mask<8;mask++){
  const x=[null,mask&1,(mask>>1)&1],zz=(mask>>2)&1;
  const truth=l=>l===7?zz===1:l===-7?zz===0:l>0?x[l]===1:x[-l]===0;
  const sat=c=>c.some(truth);
  const expected=Number(truth(a)&&truth(b))===zz;
  check([CA,CB,CAB].every(sat)===expected,'conventional exact truth table');
  check([T00,T01,T10,T11].every(sat)===expected,'four-facet exact truth table');
 }
 eq(CAB,T11);checks++;
 if(Math.abs(a)!==Math.abs(b)){eq(res(T00,T01,b),CA);eq(res(T00,T10,a),CB);checks+=2}
 else if(a===b){eq(CA,T00);eq(CB,T00);checks+=2}
 else{eq(CA,T01);eq(CB,T10);checks+=2;
  check(T11.includes(z)&&T11.includes(a)&&T11.includes(-a),'tautology positive-z facet');
  check(!T01.includes(z)&&!T10.includes(z),'pruned facets contain no positive z');
 }
}
console.log(JSON.stringify({status:'PASS',signed_literal_pairs:16,assertions:checks,scope:'separately defined grammar, NOT native historical R_mix341'}));

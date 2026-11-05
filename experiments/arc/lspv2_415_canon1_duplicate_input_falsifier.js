#!/usr/bin/env node
'use strict';
/* LSPV-2/415. Exact reproducer for REFEREE360's DEF/RES branches.
 * Uses native Node, no imports except assert/crypto. Does NOT execute the
 * published Python checker; matches its def_facets and RES logic.
 */
const assert=require('node:assert/strict'), crypto=require('node:crypto');
function canonical(x) {
 if(Array.isArray(x)) return '['+x.map(canonical).join(',')+']';
 if(x!==null&&typeof x==='object')
  return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
 return JSON.stringify(x);
}
function sortClause(a) {return a.sort((x,y)=>Math.abs(x)-Math.abs(y)||Number(x<0)-Number(y<0));}
function defFacets(a,b,z,truth) {
 let facets=[];
 for(const av of [0,1])for(const bv of [0,1]) {
  const zv=1-truth[av|(bv<<1)];
  facets.push(sortClause([[a,av],[b,bv],[z,zv]].map(([v,bit])=>bit===0?v:-v)));
 }
 return facets;
}
function rawRes(l,r,p) {
 if(!((l.includes(p)&&r.includes(-p))||(l.includes(-p)&&r.includes(p)))) throw Error('pivot');
 const out=sortClause([...new Set([...l,...r].filter(x=>Math.abs(x)!==p))]);
 if(new Set(out.map(Math.abs)).size!==out.length)throw Error('tautological output');
 return out;
}
function isClause(c) {return new Set(c.map(Math.abs)).size===c.length;}
const source={nvars:1,clauses:[[1]]};
const truth=[0,1,0,1];
const facets=defFacets(1,1,2,truth);
assert.deepEqual(facets,[[1,1,-2],[1,-1,-2],[1,-1,2],[-1,-1,2]]);
const c1=rawRes(facets[1],[1],1),c2=rawRes(facets[2],[1],1),c3=rawRes(c1,c2,2);
assert.deepEqual([c1,c2,c3],[[-2],[2],[]]);
const nodes=[
 {id:0,rule:'DEF',var:2,inputs:[1,1],truth},
 {id:1,rule:'RES',left:{node:0,view:'clause',facet:1},right:{src:0,view:'clause'},pivot:1,clause:c1},
 {id:2,rule:'RES',left:{node:0,view:'clause',facet:2},right:{src:0,view:'clause'},pivot:1,clause:c2},
 {id:3,rule:'RES',left:{node:1,view:'clause'},right:{node:2,view:'clause'},pivot:2,clause:c3}
];
const proof={format:'Rmix341-CANON1',source,source_sha256:crypto.createHash('sha256').update(canonical(source),'ascii').digest('hex'),nodes,final:{node:3,view:'clause'}};
assert.equal(proof.source_sha256,'99dc3cc7aaa4c4237ca3167e6f3d6f2c8de57df6c7cc31de2450e328029a422a');
assert.equal(Buffer.byteLength(canonical(proof),'ascii'),615);
const valuation={1:1,2:1}; 
function clauseTrue(c){return c.some(l=>valuation[Math.abs(l)]===Number(l>0));}
assert(clauseTrue(source.clauses[0])&&clauseTrue(facets[1])&&clauseTrue(facets[2]));
assert(!clauseTrue(c1)); // NO sound resolution inference can yield this!
assert(!isClause(facets[1])&&!isClause(facets[2]));
for(let mask=0;mask<16;mask++){
 const t=[0,1,2,3].map(j=>(mask>>j)&1);
 assert(defFacets(1,2,3,t).every(isClause));
}
console.log(JSON.stringify({status:'PASS',sourceSAT:true,sourceHash:proof.source_sha256,paidNodes:4,bytes:615,broken:facets.slice(1,3),repairRejects:true,witness:proof}));

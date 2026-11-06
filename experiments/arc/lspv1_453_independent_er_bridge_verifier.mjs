#!/usr/bin/env node
// Independent signed source, paid gate-facet, and strict RES verifier.
// No imports from the producer. This verifies the local compiler, not a final
// UNSAT root or the authoritative historical R_mix341 certificate grammar.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const paths=process.argv.slice(2);
if(!paths.length)throw Error('Pass one or more producer raw JSON files');
const sort=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0)-(y<0));
const eq=(a,b)=>assert.deepEqual(sort(a),sort(b));
function check(o){
 const ell=o.ell,n=2**ell,m=o.pigeons,bit=(i,t)=>i*ell+t+1;
 assert.equal(o.holes,n);assert.equal(o.pigeons,m);assert.equal(o.bit_vars,m*ell);
 let checks=0,steps=new Map(),gates=new Map();
 const signed=(i,t,h)=>((h>>t)&1)?bit(i,t):-bit(i,t);
 const groups=[],gadgetRecords=[];let varidx=m*ell;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let h=0;h<n;h++){
   const wide=[];for(let t=0;t<ell;t++)wide.push(-signed(i,t,h));
   for(let t=0;t<ell;t++)wide.push(-signed(j,t,h));
   let z=[];for(let t=0;t<2*ell-3;t++)z.push(++varidx);
   const gs=[[wide[0],wide[1],z[0]]];
   for(let t=1;t<z.length;t++)gs.push([-z[t-1],wide[t+1],z[t]]);
   gs.push([-z[z.length-1],wide[wide.length-2],wide[wide.length-1]]);
   groups.push(...gs);gadgetRecords.push({i,j,h,z,gs});
 }
 const gateOutputs=[];
 for(let i=0;i<m;i++){
   const prefix=new Map();
   for(let depth=2;depth<=ell;depth++)for(let p=0;p<(1<<depth);p++){
     const key=(depth-1)+':'+(p&((1<<(depth-1))-1));
     const first=(depth===2?signed(i,0,p):prefix.get(key));
     const second=signed(i,depth-1,p),out=++varidx;
     gateOutputs.push({out,inputs:[first,second]});
     prefix.set(depth+':'+p,out);
   }
   for(let h=0;h<n;h++)gates.set(i+':'+h,prefix.get(ell+':'+h));
 }
 assert.equal(o.total_vars,varidx);
 assert.equal(o.sources,groups.length);assert.equal(o.def_gates,gateOutputs.length);
 assert.equal(o.defs.length,gateOutputs.length);
 o.defs.forEach((g,k)=>{
   assert.equal(g.gate,k+1);assert.equal(g.out,gateOutputs[k].out);
   assert.deepEqual(g.inputs,gateOutputs[k].inputs);assert.equal(g.facets.length,3);
   checks+=4;
 });
 let numRes=0,sourceidx=0;
 const actualFacet=new Map();
 for(const node of o.steps){
   assert.equal(node.id,steps.size+1);assert.deepEqual(node.clause,sort(node.clause));
   assert.ok(node.clause.every(l=>l!==0&&Number.isInteger(l)&&Math.abs(l)<=varidx));
   if(node.kind==='src'){
     assert.deepEqual(node.clause,sort(groups[sourceidx++]));
     checks+=3;
   }else if(node.kind==='facet'){
     const g=o.defs[node.gate-1];assert.ok(g);assert.ok(g.facets.includes(node.id));
     const k=g.facets.indexOf(node.id),[a,b]=g.inputs,out=g.out;
     eq(node.clause,k===0?[-out,a]:k===1?[-out,b]:[out,-a,-b]);
     actualFacet.set(node.id,g.gate);checks+=4;
   }else if(node.kind==='res'){
     const [a,b]=node.parents;assert.ok(a<node.id&&b<node.id);assert.notEqual(a,b);
     let A=steps.get(a),B=steps.get(b);assert.ok(A&&B);
     const p=node.pivot;
     assert.ok((A.clause.includes(p)&&B.clause.includes(-p))||(A.clause.includes(-p)&&B.clause.includes(p)));
     eq(node.clause,[...A.clause.filter(l=>Math.abs(l)!==Math.abs(p)),...B.clause.filter(l=>Math.abs(l)!==Math.abs(p))]);
     numRes++;checks+=7;
   }else throw Error('unrecognized node kind '+node.kind);
   assert.ok(!node.clause.some(l=>node.clause.includes(-l)));
   steps.set(node.id,node);checks+=2;
 }
 assert.equal(sourceidx,groups.length);assert.equal(actualFacet.size,3*gateOutputs.length);
 assert.equal(o.res_nodes,numRes);
 assert.equal(o.atleast.length,m);assert.equal(o.uniqueness.length,n*m*(m-1)/2);
 for(let i=0;i<m;i++){
   const row=steps.get(o.atleast[i]);assert.ok(row&&row.kind==='res');
   eq(row.clause,Array.from({length:n},(_,h)=>gates.get(i+':'+h)));checks+=4;
 }
 let idx=0;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let h=0;h<n;h++){
   const row=steps.get(o.uniqueness[idx++]);assert.ok(row&&row.kind==='res');
   eq(row.clause,[-gates.get(i+':'+h),-gates.get(j+':'+h)]);checks+=4;
 }
 if(ell===2){
   let valid=0;
   for(let mask=0;mask<(1<<(m*ell));mask++){
     let hits=0;
     for(let i=0;i<m;i++){
       let h=0;for(let t=0;t<ell;t++)h|=((mask>>(i*ell+t))&1)<<t;
       for(let j=0;j<i;j++){
         let jh=0;for(let t=0;t<ell;t++)jh|=((mask>>(j*ell+t))&1)<<t;
         if(jh===h)hits++;
       }
     }
     if(hits===0)valid++;
     checks++;
   }
   assert.equal(valid,m===n?24:0);
   if(m===n){
     const assignment=new Map();
     for(let i=0;i<m;i++)for(let t=0;t<ell;t++)assignment.set(bit(i,t),(i>>t)&1);
     for(const g of gadgetRecords){
       let found=false;
       for(let mask=0;mask<2**g.z.length;mask++){
         const assign=new Map(assignment);
         g.z.forEach((z,j)=>assign.set(z,(mask>>j)&1));
         const truth=lit=>((lit>0?assign.get(lit):1-assign.get(-lit))===1);
         if(g.gs.every(C=>C.some(truth))){
           g.z.forEach(z=>assignment.set(z,assign.get(z)));found=true;break;
         }
       }
       assert.ok(found);checks++;
     }
     assert.ok(groups.every(C=>C.some(lit=>(lit>0?assignment.get(lit):1-assignment.get(-lit))===1)));
     checks+=groups.length;
   }
 }
 return {ell,holes:n,sources:sourceidx,paidDefs:gateOutputs.length,paidRES:numRes,
  checkedSteps:steps.size,derivedUnary:o.atleast.length+o.uniqueness.length,checks};
}
for(const p of paths){
 const obj=JSON.parse(fs.readFileSync(p,'utf8'));
 const out=check(obj);console.log(JSON.stringify({path:p,...out}));
}

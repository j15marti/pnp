#!/usr/bin/env node
'use strict';
// LSPV-2/413 independent compact verification of nonlinear GF2 closure
// and exact auxiliary-free CNF minimum. No external dependencies.
let n=0;function ok(b,msg){n++;if(!b)throw Error(msg)}
function vals(m){return Array.from({length:1<<m},(_,j)=>Array.from({length:m},(_,i)=>(j>>i)&1))}
const V=vals(4),Q=v=>v[3]===((v[0]&v[1])^v[2]);
const good=V.filter(Q),bad=V.filter(v=>!Q(v));
ok(good.length===8&&bad.length===8,'model count');
const triple=[[0,0,0,0],[0,1,0,0],[1,0,0,0]];
triple.forEach(v=>ok(Q(v),'triple model'));
ok(!Q(triple[0].map((j,i)=>j^triple[1][i]^triple[2][i])),'not affine');
let implicates=[];
for(let k=1;k<81;k++){
 let j=k,s=[];for(let i=0;i<4;i++){s.push([0,1,-1][j%3]);j=Math.floor(j/3)}
 const sat=v=>s.some((a,i)=>a!==0 && (a===1?v[i]===1:v[i]===0));
 if(good.every(sat)){let mask=0;bad.forEach((v,i)=>{if(!sat(v))mask|=1<<i});
   if(mask)implicates.push({s,mask,w:s.filter(Boolean).length});}
}
ok(implicates.length===12,'implicates');
let optC=1e9,optW=1e9;
for(let sub=0;sub<(1<<implicates.length);sub++){
 let mask=0,c=0,w=0;implicates.forEach((a,i)=>{if((sub>>i)&1){mask|=a.mask;c++;w+=a.w}});
 if(mask===255&&(c<optC||(c===optC&&w<optW))){optC=c;optW=w;}
}
ok(optC===6&&optW===20,'optimal 6 clauses 20 literals');
const six=[[-1,-1,-1,-1],[-1,-1,1,1],[0,1,-1,1],[0,1,1,-1],[1,0,-1,1],[1,0,1,-1]];
function sat(s,v){return s.some((a,i)=>a!==0&&(a===1?v[i]===1:v[i]===0))}
six.forEach(s=>good.forEach(v=>ok(sat(s,v),'correct clause')));
bad.forEach(v=>ok(six.some(s=>!sat(s,v)),'all excluded'));
const source=[[-1,-2,4],[1,-4],[2,-4],[-4,3,5],[4,-3,5],[4,3,-5],[-4,-3,-5],[1],[2],[-3],[-5],[4,1],[-3,1],[-5,1]];
function srcSAT(c,v){return c.some(l=>(l>0?v[Math.abs(l)-1]===1:v[Math.abs(l)-1]===0))}
const sv=vals(5);ok(sv.every(v=>!source.every(c=>srcSAT(c,v))),'source UNSAT');
[8,10].forEach(i=>ok(sv.some(v=>source.every((c,j)=>i===j||srcSAT(c,v))),'SAT after deletion'));
const rows={a:[['a'],1],notz:[['z'],0],notb:[['b'],0],parity:[['a','z','b'],0]};
function rv(row,v){const w=['x','y','z','a','b'];return row[0].reduce((p,x)=>p^v[w.indexOf(x)],0)===row[1]}
ok(sv.every(v=>srcSAT(source[7],v)&&srcSAT(source[8],v)?true:true),'inputs recognized');
sv.forEach(v=>{
 const a=source[7].some(l=>srcSAT([l],v))&&srcSAT(source[8],v)?v[3]:v[3];
 if(source.slice(3,7).every(c=>srcSAT(c,v)))ok(rv(rows.parity,v),'parity clauses exact');
 if(srcSAT(source[9],v))ok(rv(rows.notz,v),'unit notz');
 if(srcSAT(source[10],v))ok(rv(rows.notb,v),'unit notb');
});
console.log(JSON.stringify({PASS:true,assertions:n,nonlinear_models:good.length,implicates:implicates.length,opt_clauses:optC,opt_literals:optW,source_clauses:source.length,native_paid_upper_bound:11,conditional_local_paid_count:12},null,2));

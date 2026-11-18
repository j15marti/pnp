#!/usr/bin/env node
// TMR-4/080. Complete, standalone, finite exact source certificate.
// No preselected target colorings, external packages or floating point arithmetic.
'use strict';
const W=[
'>>>','>><','><>','><<','<>>','<><','<<>',
'->> >->','->> >-<','->> >>-','->> ><-','->> <->','->> <>-',
'->< >->','->< >-<','->< >>-','->< ><-','->< <->','->< <>-',
'-<> >->','-<> >-<','>-> >>-','>-> ><-','>-> <>-','>-< >>-'];
const R=(x,y)=>{const d=(y-x+5)%5;return d===1||d===3;};
function source(spec){
 const parts=spec.split(' '),edges=[];
 for(let j=0;j<parts.length;j++)for(let h=0;h<3;h++){
   if(parts[j][h]==='>')edges.push([h,3+j]);
   if(parts[j][h]==='<')edges.push([3+j,h]);
 }
 return {n:3+parts.length,edges};
}
function sig(graph){
 const a=Array(graph.n).fill(0),sum=Array(25).fill(0);
 let visited=0;
 function rec(i){
  if(i===graph.n){
   visited++;
   if(graph.edges.every(([u,v])=>R(a[u],a[v]))){
    const p=(a[1]-a[0]+5)%5,q=(a[2]-a[0]+5)%5;
    sum[5*p+q]++;
   }
   return;
  }
  for(let c=0;c<5;c++){a[i]=c;rec(i+1);}
 }
 rec(0);
 if(sum.some(x=>x%5))throw Error('diagonal gauge failed');
 return {row:sum.map(x=>x/5),visited};
}
function detExact(sourceRows){
 const a=sourceRows.map(r=>r.map(BigInt));
 let prev=1n,sign=1n;
 for(let k=0;k<a.length-1;k++){
  if(a[k][k]===0n){
   let j=k+1;while(j<a.length&&a[j][k]===0n)j++;
   if(j===a.length)return 0n;
   [a[k],a[j]]=[a[j],a[k]];sign=-sign;
  }
  const pivot=a[k][k];
  for(let i=k+1;i<a.length;i++){
   for(let j=k+1;j<a.length;j++){
    const numerator=a[i][j]*pivot-a[i][k]*a[k][j];
    if(numerator%prev!==0n)throw Error('nonexact division');
    a[i][j]=numerator/prev;
   }
   a[i][k]=0n;
  }
  prev=pivot;
 }
 return sign*a[a.length-1][a.length-1];
}
const graphs=W.map(source);
const base=graphs.map(sig),rows=base.map(x=>x.row);
const determinant=detExact(rows);
if(determinant!==-8064n)throw Error('bad 25x25 determinant: '+determinant);
const C=rows.map(x=>rows.map(y=>5*x.reduce((z,v,i)=>z+v*y[i],0)));
let glueAssignments=0;
for(let i=0;i<25;i++){
 const j=(i+1)%25,delta=graphs[i].n-3;
 const joined={n:graphs[i].n+graphs[j].n-3,
   edges:graphs[i].edges.concat(graphs[j].edges.map(([u,v])=>[
     u<3?u:u+delta,v<3?v:v+delta]))};
 const test=sig(joined);
 if(5*test.row.reduce((a,b)=>a+b,0)!==C[i][j])throw Error('glued count '+i);
 glueAssignments+=test.visited;
}
// C=5 M M^T, so determinant is automatically 5^25 det(M)^2 != 0.
const result={witnesses:25,determinant:String(determinant),
    independent_single_assignments:base.reduce((s,x)=>s+x.visited,0),
    independently_checked_gluings:25,independent_glue_assignments:glueAssignments,
    pairwise_connection_entries:625,full_rank:25,unexpected_failures:0,
    scope:'exact finite linear-compositional count-interface certificate, not machine lower bound'};
console.log(JSON.stringify(result));

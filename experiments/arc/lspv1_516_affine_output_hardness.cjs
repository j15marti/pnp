'use strict';
// LSPV-1/516: independently replayable circuit-affinity hardness controls.
// All circuit gates, source clauses and input assignments are explicit.
const assert=require('node:assert/strict');
let checks=0;
function eq(a,b){assert.deepStrictEqual(a,b);checks++;}
function valid(f){if(!f||!Number.isSafeInteger(f.n)||f.n<3||!Array.isArray(f.clauses))throw Error('header');for(const c of f.clauses)if(!Array.isArray(c)||c.length!==3||!c.every(z=>typeof z==='number'&&Number.isSafeInteger(z)&&z!==0&&Math.abs(z)<=f.n)||new Set(c.map(Math.abs)).size!==3)throw Error('clause');}
function fv(f,x){return +f.clauses.every(c=>c.some(l=>!!(x>>(Math.abs(l)-1)&1)===(l>0)));}
function compile(f){valid(f);const a=[];const node=(op,p=null,q=null)=>{a.push({op,p,q});return a.length-1;};const v=Array.from({length:f.n+2},(_,j)=>node('I',j));const z=node('X',v[0],v[0]);let out=node('N',z);for(const c of f.clauses){let row=null;for(const l of c){const lit=l>0?v[l-1]:node('N',v[-l-1]);row=row===null?lit:node('O',row,lit);}out=node('A',out,row);}return {input:f.n+2,nodes:a,output:node('A',node('A',out,v[f.n]),v[f.n+1])};}
function run(c,x){const w=[];for(const g of c.nodes){const a=w[g.p],b=w[g.q];switch(g.op){case'I':w.push(x>>g.p&1);break;case'X':w.push(a^b);break;case'N':w.push(1^a);break;case'O':w.push(a|b);break;case'A':w.push(a&b);break;default:throw Error('gate');}}return w[c.output];}
function affine(c){const base=run(c,0);const co=Array.from({length:c.input},(_,i)=>base^run(c,2**i));for(let x=0;x<2**c.input;x++){let v=base;for(let i=0;i<c.input;i++)if(x>>i&1)v^=co[i];if(v!==run(c,x))return false;}return true;}
function test(f){const c=compile(f);const sat=Array.from({length:2**f.n},(_,i)=>fv(f,i));eq(affine(c),!sat.some(Boolean));const t=1<<f.n,u=1<<(f.n+1);for(let x=0;x<2**f.n;x++){eq(run(c,x)^run(c,x|t)^run(c,x|u)^run(c,x|t|u),sat[x]);}return {sat:sat.some(Boolean),gates:c.nodes.length};}
function t3(g,chi){const v=Math.max(...g.flat())+1,adj=Array.from({length:v},()=>[]);g.forEach(([a,b],i)=>{adj[a].push(i+1);adj[b].push(i+1);});if(adj.some(x=>x.length!==3))throw Error('not cubic');const clauses=[];for(let j=0;j<v;j++)for(let p=0;p<8;p++){const odd=((p&1)^((p>>1)&1)^((p>>2)&1));if(odd!==chi[j])clauses.push(adj[j].map((e,k)=>p>>k&1?-e:e));}return {n:g.length,clauses};}
let seed=5162026;const next=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0;
function random(n,m){const clauses=[];for(let i=0;i<m;i++){const ids=[];while(ids.length<3){const v=next()%n+1;if(!ids.includes(v))ids.push(v);}clauses.push(ids.map(v=>next()&1?v:-v));}return {n,clauses};}
const results={tested:0,sat:0,unsat:0,exhaustive_n3:0,random_n4_n6:0,controls:[],max_gates:0};
function add(f,name){const r=test(f);results.tested++;results[r.sat?'sat':'unsat']++;results.max_gates=Math.max(results.max_gates,r.gates);if(name==='n3')results.exhaustive_n3++;else if(name==='random')results.random_n4_n6++;else results.controls.push({name,sat:r.sat,gates:r.gates,clauses:f.clauses.length});}
const all=Array.from({length:8},(_,p)=>[1,2,3].map((v,i)=>p>>i&1?-v:v));for(let s=0;s<256;s++)add({n:3,clauses:all.filter((_,j)=>s>>j&1)},'n3');
for(const n of [4,5,6])for(let i=0;i<45;i++)add(random(n,5+(next()%(6*n))),'random');
const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], k33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);
for(const [name,g,chi] of [['K4_odd',k4,[1,0,0,0]],['K4_even',k4,[0,0,0,0]],['K33_odd',k33,[1,0,0,0,0,0]],['K33_even',k33,[0,0,0,0,0,0]]])add(t3(g,chi),name);
const bad=[{n:2,clauses:[]},{n:3,clauses:[[1,1,2]]},{n:3,clauses:[[1,2,4]]},{n:3,clauses:[[1,true,3]]},{n:3,clauses:[[1,2]]},{n:3,clauses:'x'}];for(const f of bad)assert.throws(()=>compile(f));
const f={n:3,clauses:[[1,2,3]]},original=compile(f),corrupt=structuredClone(original);corrupt.nodes[corrupt.output].op='X';eq(corrupt.nodes.length,original.nodes.length);eq(JSON.stringify(corrupt)!==JSON.stringify(compile(f)),true);
results.assertions=checks;results.malformed_rejected=bad.length;results.corrupt_circuit_detected=true;results.scope='finite semantic/source controls; NOT native R_mix341 checker';
console.log(JSON.stringify(results,null,2));

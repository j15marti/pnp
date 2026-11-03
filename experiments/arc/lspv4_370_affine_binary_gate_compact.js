/* LSPV4-370 | standalone binary-affine branching falsifier, no packages.
 * Uses exhaustive small truth-table semantic checking, not an SAT oracle in proofs.
 * Node convention: [leftIndex,rightIndex,truthTableBits], bit (2*a+b).
 */
"use strict";
function run() {
let ck=0,cases=0,models=0,maxLeaves=0,seed=3702026;
function rnd(n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n;}
function pop(x){let c=0;while(x){x&=x-1;c++}return c;}
function av(mask,n,x){return ((pop((mask&((1<<n)-1))&x)&1)^(mask>>n&1));}
function tv(t,a,b){return t>>(2*a+b)&1;}
function anf(t){let c=tv(t,0,0),u=tv(t,1,0)^c,v=tv(t,0,1)^c,w=tv(t,1,1)^tv(t,1,0)^tv(t,0,1)^c;return [c,u,v,w];}
function assert(b,msg){ck++;if(!b)throw Error(msg);}
function feasible(cs,n){for(let x=0;x<(1<<n);x++)if(cs.every(z=>av(z[0],n,x)===z[1]))return true;return false;}
function audit(n,nodes){
 let leaves=[{cs:[],ms:Array.from({length:n},(_,i)=>1<<i)}],g=0,B=1<<n;
 for(const [i,j,t] of nodes){let [c,u,v,w]=anf(t);g+=w;let next=[];
  for(const z of leaves){let A=z.ms[i],D=z.ms[j];if(!w){next.push({cs:z.cs,ms:z.ms.concat((c*B)^(u*A)^(v*D))});continue;}
   for(let a=0;a<=1;a++){const cs=z.cs.concat([[A,a]]);if(feasible(cs,n))next.push({cs,ms:z.ms.concat(((c^(u&a))*B)^((v^a)*D))});}
  }
  leaves=next;assert(leaves.length<=2**g,"branch bound");
 }
 for(let x=0;x<1<<n;x++){const actual=Array.from({length:n},(_,i)=>x>>i&1);
  for(const [i,j,t] of nodes)actual.push(tv(t,actual[i],actual[j]));
  const hit=leaves.filter(z=>z.cs.every(a=>av(a[0],n,x)===a[1]));assert(hit.length===1,"unique affine partition");
  assert(hit[0].ms.length===actual.length,"wire count");
  for(let k=0;k<actual.length;k++)assert(av(hit[0].ms[k],n,x)===actual[k],"gate semantics");
  models++;
 }
 assert(leaves.length<=2**g,"final cap");cases++;maxLeaves=Math.max(maxLeaves,leaves.length);
 return {nonlinear:g,leaves:leaves.length};
}
let nonlinearTables=0;for(let t=0;t<16;t++){nonlinearTables+=anf(t)[3];audit(2,[[0,1,t]]);}
assert(nonlinearTables===8,"8 of 16 are nonlinear");
for(let g=1;g<=5;g++){const v=audit(2*g,Array.from({length:g},(_,i)=>[2*i,2*i+1,8]));assert(v.leaves===2**g,"independent tight example");}
for(let c=0;c<64;c++){const n=2+rnd(4),len=1+rnd(10),nodes=[];
 for(let j=0;j<len;j++)nodes.push([rnd(n+j),rnd(n+j),rnd(16)]);
 audit(n,nodes);
}
function parse(s){const a=s.trim().split(/\n/),clauses=[];let n=null,m=null;
 for(const line of a){const t=line.trim();if(!t||t.startsWith("c "))continue;let p=t.split(/\s+/);
  if(n===null){assert(p.length===4&&p[0]==="p"&&p[1]==="cnf","header");n=+p[2];m=+p[3];assert(Number.isInteger(n)&&n>=0&&n<=16&&Number.isInteger(m)&&m>=0,"header numbers");}
  else {let z=p.map(Number);assert(z.every(Number.isInteger)&&z.length&&z.at(-1)===0,"clause ending");assert(z.slice(0,-1).every(x=>x&&Math.abs(x)<=n),"literal range");clauses.push(z.slice(0,-1));}
 }
 assert(n!==null&&clauses.length===m,"clause count");return {n,clauses};
}
function countSat(s){let {n,clauses}=parse(s),total=0;for(let x=0;x<1<<n;x++)if(clauses.every(c=>c.some(l=>Boolean(x&(1<<(Math.abs(l)-1)))===(l>0))))total++;return total;}
const labels=[countSat("p cnf 1 1\n1 0"),countSat("p cnf 1 2\n1 0\n-1 0"),countSat("p cnf 1 1\n-1 0")];
assert(labels.join()==="1,0,1","both labels");
const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function parity(charge){let ct=0;for(let x=0;x<64;x++){if(charge.every((z,v)=>e.reduce((s,edge,i)=>s+((edge.includes(v))?(x>>i&1):0),0)%2===z))ct++;}return ct;}
assert(parity([1,0,0,0])===0 && parity([0,0,0,0])===8,"K4 parity XOR countercontrol");
let bad=["","p cnf 1 2\n1 0","p cnf 1 1\n2 0","p cnf 1 1\n1","p cnf -1 0","p cnf 1 1\n0 0","p cnf x y","p cnf 1 0\n1 0"];
for(const s of bad){let rejected=false;try{parse(s);}catch(e){rejected=true;}assert(rejected,"reject malformed");}
return {run_id:"LSPV4-AFFINE-BINARY-FACTOR-370",checks:ck,cases,models,nonlinearTables,affineTables:16-nonlinearTables,maxLeaves,tightIndependentLeaves:[2,4,8,16,32],bothLabelModels:labels,oddEvenK4Models:[0,8],malformedRejected:bad.length};
}
globalThis.__lspv4_370_result=run();
if(typeof console!=="undefined")console.log(JSON.stringify(globalThis.__lspv4_370_result,null,2));

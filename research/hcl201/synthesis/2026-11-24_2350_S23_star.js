// S23 actual star projection and same-guard comparison
const fs=require('fs'),data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
function run(data){
let out=[],checks=0;
const ok=x=>{checks++;if(!x)throw Error('assertion '+checks);};
const nae=t=>t!==0&&t!==7;
function owner(o){return {scope:o.t,allowed:[1,2,3,4,5,6]};}
function solve(n,owners,initial,cap=4*n*n){
 let meter={nodes:0,scans:0,patterns:0,forces:0},unknown=false;
 function recurse(w){
  if(meter.nodes>=cap){unknown=true;return null;}meter.nodes++;
  let again=true;while(again){again=false;for(let o of owners){
   meter.scans++;let valid=o.allowed.filter(a=>{meter.patterns++;return o.scope.every((v,i)=>w[v]<0||w[v]===(a>>i&1));});
   if(!valid.length)return null;
   for(let i=0;i<o.scope.length;i++){let v=o.scope[i],p=valid[0]>>i&1;if(w[v]<0&&valid.every(a=>(a>>i&1)===p)){w[v]=p;meter.forces++;again=true;break;}}
   if(again)break;
  }}
  let v=owners.flatMap(o=>o.scope).find(v=>w[v]<0);if(v===undefined)return w;
  for(let p=0;p<2;p++){let z=w.slice();z[v]=p;let q=recurse(z);if(q)return q;if(unknown)return null;}return null;
 }
 let witness=recurse(initial.slice());return {label:witness?'SAT':unknown?'UNKNOWN':'UNSAT',witness,meter};
}
for(let {id,n,O,pins} of data.concat([{id:'Fano',n:7,O:[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t})),pins:[-1]},{id:'Fano-minus-one',n:7,O:[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t})),pins:[-1]}])){
 for(let pin of pins){
  let w=Array(n).fill(-1);if(pin!==-1)w[0]=pin;
  let owners=O.map(owner),direct=solve(n,owners,w);
  // Run unconditional local closure before choosing the star: at most one actual pin in these sources; no local forced bits.
  for(let o of owners){let live=o.allowed.filter(a=>o.scope.every((v,i)=>w[v]<0||w[v]===(a>>i&1)));ok(live.length>0);for(let i=0;i<o.scope.length;i++)if(w[o.scope[i]]<0)ok(live.some(a=>a>>i&1)&&live.some(a=>!(a>>i&1)));}
  let v=Array.from({length:n},(_,i)=>i).filter(i=>w[i]<0).sort((a,b)=>owners.filter(o=>o.scope.includes(a)).length-owners.filter(o=>o.scope.includes(b)).length||a-b)[0];
  let B=owners.filter(o=>o.scope.includes(v)),A=owners.filter(o=>!o.scope.includes(v)),scope=[...new Set(B.flatMap(o=>o.scope).filter(u=>u!==v))].sort((a,b)=>a-b);
  let allowed=[],lifts={},localTests=0;
  for(let k=0;k<(1<<scope.length);k++){let z=w.slice();scope.forEach((u,i)=>z[u]=k>>i&1);
   for(let bit=0;bit<2;bit++){z[v]=bit;let pass=B.every(o=>{localTests++;return o.allowed.includes(o.scope.reduce((r,u,i)=>r|(z[u]<<i),0));});if(pass){allowed.push(k);lifts[k]=bit;break;}}
  }
  let combined=solve(n,[...A,{scope,allowed}],w);
  if(combined.witness){let z=combined.witness;let k=scope.reduce((r,u,i)=>r|(z[u]<<i),0);z[v]=lifts[k];ok(z[v]!==undefined);ok(owners.every(o=>o.allowed.includes(o.scope.reduce((r,u,i)=>r|(z[u]<<i),0))));if(pin!==-1)ok(z[0]===pin);}
  if(direct.label!=='UNKNOWN'&&combined.label!=='UNKNOWN')ok(direct.label===combined.label);
  out.push({id,pin,v,starOwners:B.length,boundary:scope,allowed:allowed.length,localTests,direct:{label:direct.label,...direct.meter},combined:{label:combined.label,...combined.meter},witness:combined.witness});
 }
}
return {checks,out};
}
if(require.main===module)console.log(JSON.stringify(run(data),null,2));

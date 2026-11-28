module.exports=function run(compile,corpus,registry,L){
const M=x=>(x%3+3)%3;
function solve(A,V,H=[],cap=20000000){
const n=V.length,ix=new Map(V.map((v,i)=>[v,i])),P=new Map,steps=[],initialRows=A.length;let ops=0,scans=0;
function add(a,b){let r=new Uint8Array(n+1);for(let [v,k] of a){if(!ix.has(v))throw Error("unknown coordinate");r[ix.get(v)]=M(r[ix.get(v)]+k)}r[n]=M(b);
for(let j=0;j<n;j++)if(r[j]){if(P.has(j)){let q=P.get(j),c=r[j];for(let k=j;k<=n;k++){r[k]=M(r[k]-c*q[k]);ops++}}else{if(r[j]===2)for(let k=j;k<=n;k++){r[k]=M(2*r[k]);ops++}P.set(j,r);return true}}return !r[n]}
for(let r of A)if(!add(r.a,r.b))return{status:"UNSAT",reason:"linear",ops,scans,steps};
for(let l of H)if(!add([[Math.abs(l),1]],+(l>0)))return{status:"UNSAT",reason:"guard",ops,scans,steps};
let rounds=0;
while(ops<cap){
rounds++;let piv=[...P.keys()].sort((a,b)=>b-a);
for(let j of piv){let r=P.get(j);for(let k of piv)if(k<j){let q=P.get(k),c=q[j];if(c)for(let t=j;t<=n;t++){q[t]=M(q[t]-c*r[t]);ops++}}}
let groups=new Map,forced=[];
for(let i=0;i<n;i++){
let q=P.get(i),a=[],b=q?q[n]:0;
if(q){for(let j=0;j<n;j++){scans++;if(j!==i&&q[j])a.push([V[j],M(-q[j])])}}
else a=[[V[i],1]];
if(!a.length){if(b===2)return{status:"UNSAT",reason:"nonBoolean",coordinate:V[i],ops,scans,steps,rank:P.size};forced.push([V[i],b]);continue}
let k=a[0][1];a=a.map(([v,c])=>[v,M(k*c)]);let f=M(k*(2-b)),key=JSON.stringify(a);if(!groups.has(key))groups.set(key,{a,forbid:new Map});let g=groups.get(key);if(!g.forbid.has(f))g.forbid.set(f,V[i]);
}
let duplicate=0,newrows=[];
for(let g of groups.values()){
let f=[...g.forbid.keys()];if(f.length===3)return{status:"UNSAT",reason:"parallel-cover",cover:{a:g.a,forbid:[...g.forbid]},ops,scans,steps,rank:P.size};
if(f.length===2){let b=[0,1,2].find(x=>!f.includes(x));newrows.push({a:g.a,b,witness:[...g.forbid]});duplicate++}}
steps.push({round:rounds,rank:P.size,forms:groups.size,forced,dualForbid:duplicate,newrows});
if(!newrows.length)return{status:"UNKNOWN",ops,scans,steps,rank:P.size,initialRows};
for(let r of newrows)if(!add(r.a,r.b))return{status:"UNSAT",reason:"parallel-contraction",ops,scans,steps,rank:P.size};
}
return{status:"UNKNOWN",reason:"cap",ops,scans,steps,rank:P.size};
}
function matrix(G,n){let V=[...new Set(n.root)].filter(x=>x!==n.gauge).sort((a,b)=>a-b),A=[],checks=0;G.types.forEach((t,v)=>{if(t!=="B")return;let m=new Map,b=2;for(let j=0;j<4;j++){let p=4*v+j,x=n.root[p],s=n.phase[p];if(x===n.gauge)b-=s^n.gbit;else{b-=s;m.set(x,M((m.get(x)||0)+(s?-1:1)))}}let a=[...m].filter(x=>x[1]).sort((u,v)=>u[0]-v[0]);let f=n.F[A.length];for(let z=0;z<2**f.s.length;z++){checks++;let lhs=M(a.reduce((q,[v,k])=>q+k*(z>>f.s.indexOf(v)&1),0));if((lhs===M(b))!==f.a.includes(z))throw Error("local ternary equivalence") }A.push({a,b:M(b),id:v})});return{V,A,checks}}
let out=[];for(let id of ["JOINT-24","RANDOM-3CNF-40"]){let x=corpus.instances.find(x=>x.id===id),r=registry.instances.find(x=>x.alias==="EB-"+id),G=compile(x),s=JSON.stringify(G.network)+"\n",map=JSON.stringify(G.source_map)+"\n";if(L.sha(s)!==r.sha256||s.length*8!==r.N_bits||L.sha(x.dimacs)!==r.source_cnf.sha256||L.sha(map)!==r.source_map_sha256)throw Error("auth");
let n=L.normal(G.network),C=L.cnf(n.F),early={occupancy:L.occ(n.F).forced,up:L.up(C).A.size,affine:L.affine(n.F,[]),binary:L.binary(C,[])},m=matrix(G.network,n),root=solve(m.A,m.V);
let top=id==="JOINT-24"?[618,250,546,578]:[17,362,34,234],guards=top.map((v,i)=>top.slice(0,i).map(x=>-x).concat(v)).concat([top.map(x=>-x)]);let t=Date.now(),runs=guards.map(H=>({H,...solve(m.A,m.V,H)}));out.push({id,instance:r.instance_id,N:r.N_bits,early,variables:m.V.length,rows:m.A.length,localChecks:m.checks,root,runs,ms:Date.now()-t})}return out;
}

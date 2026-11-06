// LSPV-4/443 self-contained original Tseitin 3CNF and branch correctness control.
// No claim of ETH proof, resolution-size hardness, or universal FLMV compiler.
import assert from 'node:assert/strict';
const graphs=[
 {name:'K4',adj:[[1,2,3],[0,2,3],[0,1,3],[0,1,2]]},
 {name:'Cube',adj:Array.from({length:8},(_,v)=>[v^1,v^2,v^4])}
];
let tests=0,assertions=0,leaves=0;
function check(p,s){assert.ok(p,s);assertions++;}
function formula(adj,odd){
 const edges=[];
 for(let v=0;v<adj.length;v++)for(const u of adj[v])if(v<u)edges.push([v,u]);
 edges.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const id=new Map(edges.map((e,i)=>[e.join(','),i+1]));
 const out=[];
 for(let v=0;v<adj.length;v++){
  const x=adj[v].map(u=>id.get([Math.min(u,v),Math.max(u,v)].join(','))).sort((a,b)=>a-b);
  check(x.length===3,'degree');
  for(let p=0;p<2;p++)for(let q=0;q<2;q++){
   const z=p^q^1^(odd&&v===0?1:0);
   out.push([p?-x[0]:x[0],q?-x[1]:x[1],z?-x[2]:x[2]]);
  }
 }
 return {n:edges.length,C:out};
}
function value(C,m){return C.every(c=>c.some(l=>Boolean((m>>(Math.abs(l)-1))&1)===(l>0)));}
function sat(n,C){for(let m=0;m<2**n;m++)if(value(C,m))return true;return false;}
function cut(C,assn){const out=[];for(const c of C){
 if(c.some(l=>assn.has(Math.abs(l)) && assn.get(Math.abs(l))===(l>0)))continue;
 out.push(c.filter(l=>!assn.has(Math.abs(l))));
 }return out;}
for(const g of graphs)for(const odd of [false,true]){
 const {n,C}=formula(g.adj,odd);
 check(C.length===4*g.adj.length,'4H');check(n===3*g.adj.length/2,'3H/2');
 const root=sat(n,C);check(root===!odd,'parity label');
 let statuses=[];
 for(let mask=0;mask<8;mask++){
  const assigned=new Map([1,2,3].map((v,j)=>[v,Boolean((mask>>j)&1)]));
  const child=cut(C,assigned);let ans=sat(n,child);
  for(let a=0;a<2**n;a++){
   if([1,2,3].every((v,j)=>Boolean((a>>(v-1))&1)===Boolean((mask>>j)&1)))
    check(value(C,a)===value(child,a),'restriction semantics');
  }
  statuses.push(ans);leaves++;
 }
 check(statuses.some(Boolean)===root,'complete OR');
 check(statuses.every(x=>!x)===!root,'all UNSAT required');
 tests++;
}
// One failed branch cannot justify UNSAT of a satisfiable parent.
const C=[[1,2,3]];
check(!sat(3,cut(C,new Map([[1,false],[2,false],[3,false]])))&&sat(3,C),'one-branch hostile control');
console.log(JSON.stringify({status:'PASS',tests,leaves,assertions,graphs:['K4','cube'],original_labels:['SAT','UNSAT'],scope:'finite proper cubic Tseitin controls only'}));

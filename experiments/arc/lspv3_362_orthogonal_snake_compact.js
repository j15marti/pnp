"use strict";
// LSPV-3 ORTHOGONAL-SNAKE-BACKDOOR362 compact standalone reproducer.
// node experiments/arc/lspv3_362_orthogonal_snake_compact.js
// Fixed Rmix341, strict signed binary Resolution only. No new inference rule.
const crypto=require("crypto");
let assertions=0;
const ok=(x,msg)=>{assertions++;if(!x)throw Error(msg||"assertion failed");};
const norm=z=>{let a=[...new Set(z)].sort((x,y)=>Math.abs(x)-Math.abs(y)||Number(x<0)-Number(y<0));ok(!a.some(x=>a.includes(-x)),"tautology");return a;};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sat=(cl,a)=>cl.some(x=>Boolean(a[Math.abs(x)-1])===(x>0));
function produce(r){
 ok(Number.isInteger(r)&&r>=2,"invalid size");
 const n=r*r,b=n+1,H=[],V=[];
 for(let row=0;row<r;row++)for(let j=0;j<r;j++)H.push(row*r+(row%2?r-1-j:j)+1);
 for(let col=0;col<r;col++)for(let j=0;j<r;j++)V.push((col%2?r-j-1:j)*r+col+1);
 const S=[];
 for(let [guard,p] of [[b,H],[-b,V]]){
   S.push(norm([guard,p[0]]));
   for(let i=0;i<n-1;i++)S.push(norm([guard,-p[i],p[i+1]]));
   S.push(norm([guard,-p[n-1]]));
 }
 const D=[],nodes=[];
 for(let block=0;block<2;block++){
   const path=block===0?H:V,guard=block===0?b:-b,offset=block*(n+1);
   let left=["s",offset];
   for(let i=0;i<n;i++){
     const right=["s",offset+i+1];
     const out=i===n-1?norm([guard]):norm([guard,path[i+1]]);
     nodes.push({left,right,pivot:path[i],out});left=["d",nodes.length-1];
   }
 }
 nodes.push({left:["d",n-1],right:["d",2*n-1],pivot:b,out:[]});
 for(const node of nodes){
   const inp=p=>p[0]==="s"?S[p[1]]:D[p[1]];
   let a=inp(node.left),c=inp(node.right),x=node.pivot;
   ok((a.includes(x)&&c.includes(-x))||(a.includes(-x)&&c.includes(x)),"invalid pivot");
   const z=norm([...a,...c].filter(t=>Math.abs(t)!==x));
   ok(same(z,node.out),"incorrect result"); D.push(z);
 }
 ok(same(D.at(-1),[]),"not refuted");
 let signs=0;
 for(let block=0;block<2;block++){
   const p=block===0?H:V,off=block*(n+1);
   for(let i=0;i<=n;i++){
     const a=Array(n+1).fill(0);a[b-1]=block;
     for(let j=0;j<n;j++)a[p[j]-1]=i===n?1:(i===0?0:Number(j<i));
     for(let j=0;j<S.length;j++)ok(sat(S[j],a)===(j!==off+i),"not a unique deletion SAT witness");
     for(let j=0;j<S[off+i].length;j++){
       let c=S[off+i].slice();c[j]=-c[j];ok(sat(c,a),"sign repair failed");signs++;
     }
   }
 }
 const edges=new Set();
 const key=(u,v)=>[Math.min(u,v),Math.max(u,v)].join(":");
 for(const p of [H,V])for(let i=1;i<p.length;i++)edges.add(key(p[i-1],p[i]));
 for(let i=0;i<r;i++)for(let j=0;j<r;j++){
   let z=i*r+j+1;if(i+1<r)ok(edges.has(key(z,z+r)),"vertical grid edge missing");
   if(j+1<r)ok(edges.has(key(z,z+1)),"horizontal grid edge missing");
 }
 const dimacs="p cnf "+b+" "+S.length+"\n"+S.map(c=>c.join(" ")+" 0\n").join("");
 return {r,n,m:S.length,paid:nodes.length,bits:8*Buffer.byteLength(dimacs),sha256:crypto.createHash("sha256").update(dimacs).digest("hex"),deletions:S.length,sign_flips:signs};
}
let sizes=[2,3,4,5,6,8,12,16],cases=sizes.map(produce);
ok(cases.every(t=>t.paid===t.m-1),"not source floor");
console.log(JSON.stringify({id:"LSPV3_ORTHOGONAL_SNAKE_BACKDOOR362",model:"unchanged Rmix341 strict Resolution",type:"deterministic exhaustive source-deletion witnesses and signs, all pivots replayed",fixtures:cases,totals:{nodes:cases.reduce((s,t)=>s+t.paid,0),deletions:cases.reduce((s,t)=>s+t.deletions,0),sign_flips:cases.reduce((s,t)=>s+t.sign_flips,0)},assertions,all_pass:true},null,2));
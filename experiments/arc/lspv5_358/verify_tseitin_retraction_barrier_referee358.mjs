#!/usr/bin/env node
"use strict";
let assertions=0; const check=(x,m)=>{assertions++;if(!x)throw new Error(m)};
const graphs={
 K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 K33:[6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],
 cube:[8,[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]],
 Petersen:[10,[[0,1],[1,2],[2,3],[3,4],[4,0],[5,7],[7,9],[9,6],[6,8],[8,5],[0,5],[1,6],[2,7],[3,8],[4,9]]]
};
function valid(h,edges){
 if(!Number.isInteger(h)||h<=0)return false; const seen=new Set(); const deg=Array(h).fill(0),adj=Array.from({length:h},()=>[]);
 for(const e of edges){if(!Array.isArray(e)||e.length!==2)return false;const [u,v]=e;if(!Number.isInteger(u)||!Number.isInteger(v)||u<0||v<0||u>=h||v>=h||u===v)return false;const k=u<v?`${u},${v}`:`${v},${u}`;if(seen.has(k))return false;seen.add(k);deg[u]++;deg[v]++;adj[u].push(v);adj[v].push(u)}
 if(deg.some(d=>d!==3))return false; const reach=new Set([0]),q=[0];while(q.length){const u=q.pop();for(const v of adj[u])if(!reach.has(v)){reach.add(v);q.push(v)}}return reach.size===h;
}
function clauses(vs,rhs){const out=[];for(let row=0;row<8;row++){const b=[row&1,(row>>1)&1,(row>>2)&1];if((b[0]^b[1]^b[2])!==rhs)out.push(vs.map((v,i)=>b[i]?-v:v))}return out}
const truth=(c,a)=>c.some(l=>(a[Math.abs(l)-1]===1)===(l>0));
const cases={};
for(const [name,[h,edges]] of Object.entries(graphs)){
 check(valid(h,edges),"valid graph");const inc=Array.from({length:h},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});cases[name]={};
 for(const odd of [true,false]){const charge=Array(h).fill(0);if(odd)charge[0]=1;const cnf=[];let local=0;
  for(let v=0;v<h;v++){const cs=clauses(inc[v],charge[v]);check(cs.length===4,"four clauses");cnf.push(...cs);for(let row=0;row<8;row++){const a=Array(edges.length).fill(0);inc[v].forEach((e,i)=>a[e-1]=(row>>i)&1);const rel=(((row&1)^((row>>1)&1)^((row>>2)&1))===charge[v]);check(cs.every(c=>truth(c,a))===rel,"local parity");local++}}
  let models=0;for(let row=0;row<2**edges.length;row++){const a=Array.from({length:edges.length},(_,i)=>(row>>i)&1);if(cnf.every(c=>truth(c,a)))models++}
  let mask=0n,rhs=0;for(let v=0;v<h;v++){let r=0n;for(const e of inc[v])r^=1n<<BigInt(e-1);mask^=r;rhs^=charge[v]}
  check(mask===0n&&rhs===(odd?1:0),"final affine contradiction/control");check(models===(odd?0:2**(edges.length-h+1)),"model count");cases[name][odd?"odd":"even"]={models,local,finalRhs:rhs};
 }
 check(4*h-1===3*h+(h-1),"node accounting");
}
const bad=[[4,[[0,1],[0,1]]],[4,[[0,0],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],[4,[[0,1],[0,2],[0,3]]],[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,4]]],[0,[]]];
for(const [h,e] of bad)check(!valid(h,e),"malformed rejected");
console.log(JSON.stringify({run:"LSPV5_REFEREE358_INDEPENDENT",assertions,cases,malformedRejected:bad.length},null,2));

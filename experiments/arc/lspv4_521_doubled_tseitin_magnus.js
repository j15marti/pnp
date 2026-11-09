#!/usr/bin/env node
'use strict';
// Independent verifier, not a native FLMV/Rmix341 or link isotopy computation.
const assert=require('assert/strict'),crypto=require('crypto');
const graphs={
K4:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
prism:[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]],
cube:Array.from({length:8},(_,a)=>Array.from({length:8-a-1},(_,d)=>a+1+d).filter(b=>((a^b).toString(2).match(/1/g)||[]).length===1).map(b=>[a,b])).flat(),
Petersen:[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,5+i]),...Array.from({length:5},(_,i)=>[5+i,5+((i+2)%5)])]
};
function make(name,charge){
 let edges=graphs[name].map(([a,b])=>[Math.min(a,b),Math.max(a,b)]).sort((p,q)=>p[0]-q[0]||p[1]-q[1]);
 let verts=[...new Set(edges.flat())].sort((a,b)=>a-b);
 const edgeOf=Object.fromEntries(verts.map(v=>[v,[]]));
 edges.forEach(([u,v],i)=>{edgeOf[u].push(i+1);edgeOf[v].push(i+1)});
 for(const v of verts)assert.equal(edgeOf[v].length,3);
 const src=[];
 for(const v of verts){
  const [a,b,c]=edgeOf[v].sort((x,y)=>x-y);
  for(let y=0;y<2;y++)for(let z=0;z<2;z++){
   const x=(charge&&v===verts[0]?1:0)^y^z^1;
   const clause=[x?-a:a,y?-b:b,z?-c:c];src.push(clause,clause.slice());
  }
 }
 return {edges,verts,src};
}
function pooled(src){
 const polys=new Map();
 for(const [a,b,c] of src)for(const row of [[a,b,c],[a,c,b],[b,c,a],[c,b,a]]){
  const key=row.join(':');polys.set(key,(polys.get(key)||0)^1);
 }
 return [...polys.values()].filter(x=>x!==0).length;
}
function satcount(n,cls){
 let out=0;
 for(let a=0;a<2**n;a++){
  if(cls.every(C=>C.some(z=>((((a>>>(Math.abs(z)-1))&1)!==0)===(z>0)))))out++;
 }
 return out;
}
function encoding(n,cls){
 const w=Math.floor(Math.log2(n))+1;
 const header='N='+n+';M='+cls.length+';W='+w+'\n';
 return header+cls.flat().map(x=>(x<0?'1':'0')+(Math.abs(x)-1).toString(2).padStart(w,'0')).join('');
}
let cases=0,controls=0,details=[];
for(const name of Object.keys(graphs)){
 const even=make(name,false),odd=make(name,true),E=even.edges.length,H=even.verts.length;
 assert.equal(even.src.length,8*H);assert.equal(odd.src.length,8*H);
 const a=encoding(E,even.src),b=encoding(E,odd.src);
 assert.equal(a.length,b.length);assert.notEqual(a,b);
 assert.equal(pooled(even.src),0);assert.equal(pooled(odd.src),0);
 assert.equal(satcount(E,even.src),2**(E-H+1));
 assert.equal(satcount(E,odd.src),0);
 cases+=2;
 details.push({graph:name,even_sha256:crypto.createHash('sha256').update(a).digest('hex'),odd_sha256:crypto.createHash('sha256').update(b).digest('hex')});
}
{
 let F=make('K4',true).src;
 assert.equal(pooled(F.slice(0,-1)),4);controls++;
 let G=F.map(C=>C.slice());G[0][0]=-G[0][0];assert.ok(pooled(G)>0);controls++;
}
console.log(JSON.stringify({verifier:'independent JS',cases,controls,details,verification:'PASS'},null,2));

#!/usr/bin/env node
/* LSPV-4 independent refutation-DAG audit; standard Node.js, no dependencies.
   Run: node lspv4_358_proof_slack_replay.js
   Optional cross-check: node lspv4_358_proof_slack_replay.js producer_raw.json
   Every named step is checked as genuine signed, binary Resolution. */
'use strict';
const fs=require('fs');
const input=process.argv[2]?JSON.parse(fs.readFileSync(process.argv[2],'utf8')):null;
const computed=[];let checks=0;
function ok(x,msg='failed'){checks++;if(!x)throw Error(msg)}
function canon(A){return [...new Set(A)].sort((a,b)=>a-b)}
const seed=[[-2,-3],[-1,2],[1,3],[-1,-2,3],[1,2,-3]].map(canon);
function resolve(A,B,p){
  A=A.slice();B=B.slice();
  if(A.includes(p)&&B.includes(-p)){A.splice(A.indexOf(p),1);B.splice(B.indexOf(-p),1)}
  else if(A.includes(-p)&&B.includes(p)){A.splice(A.indexOf(-p),1);B.splice(B.indexOf(p),1)}
  else throw Error('bad pivot');
  const C=canon(A.concat(B));
  for(const l of C)if(C.includes(-l))throw Error('tautological resolvent');
  return C;
}
function split(s){
  let src=seed.map(x=>x.slice()),steps=[];
  for(let i=1;i<=s;i++){
    const C=src.shift(),z=i+3,L=canon(C.concat(z)),R=canon(C.concat(-z));
    src.unshift(R);src.unshift(L);steps.push({C,L,R,z});
  }
  const val=src.map(x=>x.slice()),parents=[];
  const idx=new Map(src.map((C,i)=>[JSON.stringify(C),i]));
  function calc(a,b,p){const id=val.length;val.push(resolve(val[a],val[b],p));parents.push([a,b,p]);return id}
  const lookup=C=>{let q=idx.get(JSON.stringify(C));ok(q!==undefined);return q};
  for(const t of steps.reverse())idx.set(JSON.stringify(t.C),calc(lookup(t.L),lookup(t.R),t.z));
  let a=calc(lookup(seed[0]),lookup(seed[3]),3);
  let b=calc(a,lookup(seed[1]),2);
  let c=calc(lookup(seed[0]),lookup(seed[4]),2);
  let d=calc(c,lookup(seed[2]),3);
  calc(b,d,1);
  return {src,val,parents};
}
function horn(t){
  const src=[[1]];for(let i=1;i<t;i++)src.push([-i,i+1]);src.push([-t]);
  const val=src.map(x=>x.slice()),parents=[];
  let prev=0;
  for(let i=1;i<=t;i++){
    const C=resolve(val[prev],val[i],i);
    parents.push([prev,i,i]);prev=val.length;val.push(C);
  }
  return {src,val,parents};
}
function selector(k){
  let next=3*k+1,leaves=[];
  function tree(l,r,guard){
    if(r-l===1){leaves.push({j:l,guard});return {j:l,guard}}
    const z=next++,mid=Math.floor((l+r)/2);
    return {z,guard,left:tree(l,mid,guard.concat(z)),right:tree(mid,r,guard.concat(-z))};
  }
  const root=tree(0,k,[]);ok(next===4*k);
  let src=[],index=new Map();
  for(let leaf of leaves)for(let i=0;i<5;i++){
    index.set(leaf.j+':'+i,src.length);
    src.push(canon(leaf.guard.concat(seed[i].map(l=>(l<0?-1:1)*(Math.abs(l)+3*leaf.j)))));
  }
  let val=src.map(x=>x.slice()),parents=[];
  function infer(a,b,p){let id=val.length;val.push(resolve(val[a],val[b],p));parents.push([a,b,p]);return id}
  function emit(node){
    if(node.j!==undefined){
      const at=i=>index.get(node.j+':'+i),v=i=>3*node.j+i;
      const a=infer(at(0),at(3),v(3)),b=infer(a,at(1),v(2));
      const c=infer(at(0),at(4),v(2)),d=infer(c,at(2),v(3));
      return infer(b,d,v(1));
    }
    return infer(emit(node.left),emit(node.right),node.z);
  }
  emit(root);return {src,val,parents};
}
function audit(d){
  const {src,val,parents}=d,m=src.length,q=parents.length,V=m+q;
  ok(V===val.length);ok(JSON.stringify(val[V-1])==='[]');
  const paths=Array(V).fill(0),outdeg=Array(V).fill(0),regs=Array(V).fill(1),leaves=Array(V).fill(1);
  paths[V-1]=1;
  for(let i=0;i<q;i++){
    const [a,b,p]=parents[i];ok(a<m+i&&b<m+i);
    ok(JSON.stringify(resolve(val[a],val[b],p))===JSON.stringify(val[m+i]));
    outdeg[a]++;outdeg[b]++;
    regs[m+i]=regs[a]===regs[b]?regs[a]+1:Math.max(regs[a],regs[b]);
    leaves[m+i]=leaves[a]+leaves[b];
  }
  for(let i=q-1;i>=0;i--){const [a,b]=parents[i];paths[a]+=paths[m+i];paths[b]+=paths[m+i]}
  ok(paths.every(x=>x>0));
  const beta=2*q-V+1,delta=0;
  ok(outdeg.slice(0,-1).reduce((a,x)=>a+x-1,0)===beta);
  ok(Math.max(...paths)<=2**beta);
  const U=paths.reduce((a,x)=>a+x,0);
  ok(U<=V*2**beta);
  ok(regs[V-1]<=Math.floor(Math.log2(leaves[V-1]))+1);
  return {m,q,beta,delta,original_nodes:V,unfolded_nodes:U,
    source_occurrence_copies:paths.slice(0,m).reduce((a,x)=>a+x,0),
    largest_node_multiplicity:Math.max(...paths),
    unfold_leaves:leaves[V-1],strahler_registers:regs[V-1]};
}
function truth(F,n){
  for(let x=0;x<2**n;x++)
    if(F.every(C=>C.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0))))return x;
  return null;
}
function controls(src,n){
  ok(truth(src,n)===null);
  for(let i=0;i<src.length;i++){
    const F=src.filter((_,j)=>j!==i);ok(truth(F,n)!==null);
    for(let j=0;j<src[i].length;j++){
      const G=src.map(c=>c.slice());G[i][j]*=-1;ok(truth(G,n)!==null);
    }
  }
}
let idx=0;
for(let s=0;s<=8;s++){
  const d=split(s),stat=audit(d),row=input?.rows[idx++];
  if(!input)idx++;
  if(row)for(const key of Object.keys(stat))ok(stat[key]===row[key],s+' '+key);
  computed.push({family:'fresh_split',s,...stat});
  controls(d.src,3+s);
}
for(const k of [1,2,3,4,8]){
  const d=selector(k),row=input?.rows[idx++],stat=audit(d);
  if(!input)idx++;
  if(row)for(const key of Object.keys(stat))ok(stat[key]===row[key],'selector '+k+' '+key);
  computed.push({family:'selector_gated',k,...stat});
  if(k<=2)controls(d.src,4*k-1);
}
for(const t of [2,3,4,8,16]){
  const d=horn(t),row=input?.rows[idx++],stat=audit(d);
  if(!input)idx++;
  if(row)for(const key of Object.keys(stat))ok(stat[key]===row[key],t+' '+key);
  computed.push({family:'horn',t,...stat});
  if(t<=8)controls(d.src,t);
}
if(input)ok(idx===input.rows.length);
for(const [a,b,p] of [[[1],[-1],1],[[1,2],[-1],1]])
  ok(resolve(a,b,p).length===(a.length===1?0:1));
try{resolve([1],[-1],2);throw Error('forgery passed')}
catch(e){ok(e.message==='bad pivot')}
console.log(JSON.stringify({independent_js_assertions:checks,rows:idx,status:'PASS',computed},null,2));

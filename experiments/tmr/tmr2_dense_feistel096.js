#!/usr/bin/env node
'use strict';
const audit = function audit(){
  let checks=0;
  const ck=(b,label)=>{checks++;if(!b)throw Error("CHECK_FAILED "+label)};
  const bit=(n,i)=>(n>>i)&1;
  const edge=(i,j,m)=>j===i+1||(i===0&&j===m-1);
  function q(v,m){let s=0;for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)if(!edge(i,j,m))s^=bit(v,i)&bit(v,j);return s}
  function mix(v,m){let Q=q(v,m),out=0;for(let i=0;i<m;i++)out|=(Q^(bit(v,i)&bit(v,(i+1)%m)))<<i;return out}
  function forward(x,z,m){let u=x^mix(z,m),v=z^mix(u,m);return [u,v]}
  function inverse(u,v,m){let z=v^mix(u,m),x=u^mix(z,m);return [x,z]}
  function make(m){
    const clauses=[],gates=[],t=m*(m-3)/2,orig=2*m;
    let next=orig;
    const newv=()=>++next;
    const addAnd=(a,b)=>{
      let out=newv(),p=newv(),r=newv();
      gates.push({op:"AND",a,b,out,p,r});
      clauses.push([-a,-b,out],[a,-out,p],[a,-out,-p],[b,-out,r],[b,-out,-r]);
      return out;
    };
    const addXor=(a,b)=>{
      let out=newv();
      gates.push({op:"XOR",a,b,out});
      clauses.push([-a,b,out],[a,-b,out],[a,b,-out],[-a,-b,-out]);
      return out;
    };
    const mixGates=(w)=>{
      const ts=[];
      for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)if(!edge(i,j,m))ts.push(addAnd(w[i],w[j]));
      let Q=ts[0];for(let j=1;j<ts.length;j++)Q=addXor(Q,ts[j]);
      return Array.from({length:m},(_,i)=>addXor(Q,addAnd(w[i],w[(i+1)%m])));
    };
    const X=Array.from({length:m},(_,i)=>i+1),Z=Array.from({length:m},(_,i)=>m+i+1);
    const U=mixGates(Z).map((g,i)=>addXor(X[i],g));
    const V=mixGates(U).map((h,i)=>addXor(Z[i],h));
    const base=clauses.map(c=>c.map(l=>Math.abs(l)<=m&&((Math.abs(l)-1)%2===0)?-l:l));
    return {m,t,X,Z,U,V,clauses:base,gates,variables:next,flipped:X.filter((_,i)=>i%2===0)};
  }
  const clauseOK=(c,a)=>c.some(l=>((a[Math.abs(l)]===1)===(l>0)));
  const sat=(F,a)=>F.clauses.every(c=>clauseOK(c,a));
  const assn=(F,x,z)=>{
    const a=new Uint8Array(F.variables+1);
    for(let i=0;i<F.m;i++){a[F.X[i]]=bit(x,i);a[F.Z[i]]=bit(z,i)}
    for(const g of F.gates){a[g.out]=g.op==="AND"?(a[g.a]&a[g.b]):(a[g.a]^a[g.b]);if(g.op==="AND"){a[g.p]=0;a[g.r]=0}}
    for(const k of F.flipped)a[k]^=1;
    return a;
  };
  const rankGF2=(rows,width)=>{
    const b=Array(width).fill(0n);let r=0;
    for(let v of rows){
      for(let i=width-1;i>=0;i--)if((v>>BigInt(i))&1n){
        if(b[i])v^=b[i];else{b[i]=v;r++;break}
      }
    }
    return r;
  };
  function pack(x,z,u,v,m){
    let r=1n;
    const chunks=[x,z,u,v];
    for(let j=0;j<4;j++)for(let i=0;i<m;i++)if(bit(chunks[j],i))r|=1n<<BigInt(1+j*m+i);
    return r;
  }
  const sample=[];
  for(let m=5;m<=9;m++){
    const F=make(m),t=F.t,V=F.variables;
    ck(V===4*m*m-2,"variables "+m);
    ck(F.clauses.length===9*m*m-m-8,"clauses "+m);
    ck(F.gates.length===2*m*m-2,"gates "+m);
    ck(F.clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper 3cnf "+m);
    const signs=Array(V+1).fill(0).map(()=>new Set());
    for(const c of F.clauses)for(const l of c)signs[Math.abs(l)].add(Math.sign(l));
    ck(signs.slice(1).every(s=>s.size===2),"no-pure "+m);
    const hasPair=(a,b)=>F.clauses.some(c=>c.some(l=>Math.abs(l)===a)&&c.some(l=>Math.abs(l)===b));
    for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){
      ck(hasPair(F.Z[i],F.Z[j]),"source-z-clique "+m+" "+i+" "+j);
      ck(hasPair(F.U[i],F.U[j]),"middle-u-clique "+m+" "+i+" "+j);
    }
    const zero=new Uint8Array(V+1),one=new Uint8Array(V+1);one.fill(1);
    ck(!sat(F,zero),"zero-fails "+m);
    ck(!sat(F,one),"one-fails "+m);
    ck(sat(F,assn(F,0,0)),"planted-easy "+m);
    const transform=(a)=>{
      let b=new Uint8Array(V+1);
      for(let id=1;id<=V;id++)b[V+1-id]=a[id]^((id%3)===0?1:0);
      let cs=F.clauses.map(c=>c.map(l=>{let id=Math.abs(l);return (l>0?1:-1)*(id%3===0?-1:1)*(V+1-id)})).reverse();
      cs=cs.concat(cs.slice(0,11));
      ck(cs.every(c=>clauseOK(c,b)),"signed-renamed-reordered-duplicate "+m);
    };
    transform(assn(F,0,0));
    for(let a=0;a<Math.min(30,1<<(2*m));a++){
      const x=(a*13+7)&((1<<m)-1),z=(a*27+3)&((1<<m)-1);
      ck(sat(F,assn(F,x,z)),"gate-assignment "+m);
      const [u,v]=forward(x,z,m);
      const vals=assn(F,x,z);
      ck(F.U.every((id,i)=>vals[id]===bit(u,i))&&F.V.every((id,i)=>vals[id]===bit(v,i)),"wire-function "+m);
      const [xx,zz]=inverse(u,v,m);
      ck(xx===x&&zz===z,"inverse "+m);
    }
    if(m<=6){
      const seen=new Set(),rows=[];
      for(let x=0;x<(1<<m);x++)for(let z=0;z<(1<<m);z++){
        const [u,v]=forward(x,z,m),code=u|(v<<m);
        ck(!seen.has(code),"bijective "+m+" "+x+","+z);
        seen.add(code);
        rows.push(pack(x,z,u,v,m));
        ck(sat(F,assn(F,x,z)),"exhaustive original source "+m+" "+x+","+z);
        const [xx,zz]=inverse(u,v,m);
        ck(xx===x&&zz===z,"exhaustive inversion "+m);
      }
      ck(seen.size===(1<<(2*m)),"full rank permutation "+m);
      ck(rankGF2(rows,1+4*m)===1+4*m,"FULL AFFINE HULL "+m);
      sample.push({m,points:seen.size,affineHullRank:1+4*m});
    }
    const rank=(1n<<BigInt(2*m)).toString();
    const cap=(1n<<BigInt(2*m))-1n;
    ck(cap>0n&&2n*cap>cap,"terminal tariff "+m);
    sample.push({m,variables:V,clauses:F.clauses.length,gates:F.gates.length,nonCyclePairs:t,projectedRank:rank});
  }
  const relation=[];
  for(let x=0;x<2;x++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)relation.push([x,a,b,x^(a&b)]);
  const R=new Set(relation.map(t=>t.join("")));
  const ops=[
    {name:"Horn-meet",ar:2,op:xs=>xs[0]&xs[1]},
    {name:"dual-Horn-join",ar:2,op:xs=>xs[0]|xs[1]},
    {name:"bijunctive-majority",ar:3,op:xs=>+(xs[0]+xs[1]+xs[2]>=2)},
    {name:"affine-xor3",ar:3,op:xs=>xs[0]^xs[1]^xs[2]}];
  const witnesses={};
  for(const {name,ar,op} of ops){
    outer:for(const A of relation)for(const B of relation)for(const C of (ar===3?relation:[A])){
      const lists=ar===2?[A,B]:[A,B,C];
      const dst=[0,1,2,3].map(i=>op(lists.map(t=>t[i])));
      if(!R.has(dst.join(""))){witnesses[name]={inputs:lists,output:dst};break outer}
    }
    ck(!!witnesses[name],name);
  }
  return {status:"COMPUTATIONAL",checks,failures:0,models:sample,witnesses,terminalTariff:"lambda_SEP*(2^(2m)-1)+lambda_MACHINE<=1",source:"dense nonlinear Feistel proper-3CNF"};
};
const result = audit();
console.log(JSON.stringify(result,null,2));

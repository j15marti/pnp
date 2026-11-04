#!/usr/bin/env node
"use strict";
/* LSPV-2/375 public compact reproducer.
   Full Python producer, separately written JS referee and 336 sign-flip
   fixtures are in the conversation's reproducibility archive.
   This compact script tests existing graph sources, not a new hard family.
   This is a SAT-preserving INPUT COMPILER, not an Rmix341 proof rule. */
function parse(s) {
  const lines=s.split(/\r?\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith("c "));
  if(!lines.length) throw Error("missing header");
  const h=lines.shift().split(/\s+/);
  if(h.length!==4||h[0]!=="p"||h[1]!=="cnf"||!/^\d+$/.test(h[2])||!/^\d+$/.test(h[3])) throw Error("header");
  const n=Number(h[2]), m=Number(h[3]); if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m))throw Error("size");
  const tok=lines.join(" ").split(/\s+/).filter(Boolean), cls=[];let c=[];
  for(const t of tok) {
    if(!/^-?(?:0|[1-9]\d*)$/.test(t)||t==="-0")throw Error("literal");
    const v=Number(t);if(!Number.isSafeInteger(v)||Math.abs(v)>n)throw Error("range");
    if(v===0){cls.push(c);c=[];}else c.push(v);
  }
  if(c.length||cls.length!==m)throw Error("clause count");
  return {n,cls};
}
function emit(n,cs){return "p cnf "+n+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" "+(c.length?"0":"0")+"\n").join("");}
function recognized(n,cs){
  if(!cs.length||cs.length%4)return false;
  const groups=new Map(),inc=new Map();
  for(const c of cs){
    if(c.length!==3||new Set(c.map(Math.abs)).size!==3)return false;
    const ids=c.map(Math.abs).sort((a,b)=>a-b),key=ids.join(",");
    const pat=ids.map(v=>c.find(l=>Math.abs(l)===v)<0?1:0);
    if(!groups.has(key))groups.set(key,[]);
    groups.get(key).push(pat);
  }
  const h=groups.size;if(h<4||h%2||cs.length!==4*h||n!==3*h/2)return false;
  let odd=0,ix=0;
  for(const [key,ps] of groups){
    if(ps.length!==4||new Set(ps.map(p=>p.join(""))).size!==4)return false;
    const vals=new Set(ps.map(p=>(p[0]^p[1]^p[2])));
    if(vals.size!==1)return false;
    odd^=1^ps[0][0]^ps[0][1]^ps[0][2];
    for(const v of key.split(",").map(Number)){
      if(!inc.has(v))inc.set(v,[]);
      inc.get(v).push(ix);
    }ix++;
  }
  if(!odd||inc.size!==n)return false;
  const es=[];for(let v=1;v<=n;v++){
    const ends=inc.get(v);if(!ends||ends.length!==2||ends[0]===ends[1])return false;
    es.push(ends.slice().sort((a,b)=>a-b));
  }
  if(new Set(es.map(x=>x.join(","))).size!==n)return false;
  const connected=(skip)=>{
    const seen=new Set([0]),stack=[0];
    while(stack.length){const u=stack.pop();
      for(let j=0;j<es.length;j++){if(j===skip)continue;
        const [a,b]=es[j],w=a===u?b:b===u?a:null;
        if(w!==null&&!seen.has(w)){seen.add(w);stack.push(w);}
      }
    }return seen.size===h;
  };
  if(!connected(-1))return false;
  for(let j=0;j<es.length;j++)if(!connected(j))return false;
  return true;
}
function compile(text){
  const {n,cls}=parse(text),z=n+1;
  const suffix=recognized(n,cls)?[[z],[-z]]:[[z]];
  return emit(z,cls.concat(suffix));
}
function models(n,cs){
  let ans=0;for(let a=0;a<2**n;a++)if(cs.every(c=>c.some(l=>!!(a&(2**(Math.abs(l)-1)))===(l>0))))ans++;
  return ans;
}
function tseitin(v,edges,odd){
 const inc=Array.from({length:v},()=>[]);
 edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
 const out=[];
 for(let i=0;i<v;i++)for(let mask=0;mask<8;mask++){
   if((((mask&1)+((mask>>1)&1)+((mask>>2)&1))%2)===(1^(odd&&i===0?1:0))){
     out.push(inc[i].map((x,j)=>(mask&(1<<j))?-x:x));
   }
 }return emit(edges.length,out);
}
function ok(c,m){if(!c)throw Error(m)}
const graphs=[
 ["K4",4,Array.from({length:4},(_,u)=>Array.from({length:4},(_,v)=>[u,v]).filter(([a,b])=>a<b)).flat()],
 ["K33",6,Array.from({length:3},(_,u)=>Array.from({length:3},(_,j)=>[u,j+3])).flat()],
 ["cube",8,Array.from({length:8},(_,u)=>Array.from({length:8},(_,v)=>[u,v]).filter(([a,b])=>a<b&&((a^b).toString(2).split("1").length===2))).flat()]
];
const out=[];for(const [name,h,e] of graphs){
  const orig=parse(tseitin(h,e,true)),compiled=parse(compile(emit(orig.n,orig.cls)));
  ok(recognized(orig.n,orig.cls),"recognition "+name);
  ok(compiled.cls.length===orig.cls.length+2,"two units");
  ok(JSON.stringify(compiled.cls.slice(0,-2))===JSON.stringify(orig.cls),"original prefix");
  const z=orig.n+1;
  ok(JSON.stringify(compiled.cls.slice(-2))===JSON.stringify([[z],[-z]]),"RES one-node certificate");
  ok(models(orig.n,orig.cls)===0&&models(compiled.n,compiled.cls)===0,"UNSAT");
  const even=parse(tseitin(h,e,false)),evOut=parse(compile(emit(even.n,even.cls)));
  ok(evOut.cls.length===even.cls.length+1,"SAT branch");
  ok(models(even.n,even.cls)===models(evOut.n,evOut.cls),"SAT model preservation");
  out.push({name,h,source_clauses:orig.cls.length,native_mixed_nodes_prior_341:4*h-1,compiled_nodes:1});
}
let rejected=0;for(const s of ["","p cnf 1 1\n2 0\n","p cnf 1 1\n1\n","p cnf 1 0\np cnf 1 0\n"]){try{compile(s)}catch(e){rejected++}}
ok(rejected===4,"malformed controls");
console.log(JSON.stringify({status:"PASS",scope:"public compact K4/K33/cube replay",cases:out,malformed_rejected:rejected}));

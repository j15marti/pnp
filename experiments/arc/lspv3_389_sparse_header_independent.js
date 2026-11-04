#!/usr/bin/env node
// Independent source-indexed BigInt DIMACS and strict Resolution verifier.
'use strict';
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
const a=JSON.parse(fs.readFileSync(process.argv[2]||'389_raw.json','utf8'));
let checks=0,rejected=0;
function check(c,m){assert.ok(c,m);checks++}
function parse(s){
 const lines=s.trim().split(/\r?\n/);
 if(!/^p cnf [1-9][0-9]* (1|2)$/.test(lines[0]))throw Error('header');
 const [, ,V,M]=lines[0].split(' '), max=BigInt(V), m=Number(M);
 if(lines.length!==m+1)throw Error('clause count');
 let cs=[];
 for(const row of lines.slice(1)){
   const parts=row.split(' ');
   if(parts.pop()!=='0'||!parts.length)throw Error('terminator');
   cs.push(parts.map(t=>{
     if(!/^-?[1-9][0-9]*$/.test(t))throw Error('signed literal');
     const v=BigInt(t),abs=v<0n?-v:v;
     if(abs>max)throw Error('variable out of range');
     return v;
   }));
 }
 return {max,cs};
}
function sat(p,assignment){return p.cs.every(cl=>cl.some(x=>assignment(x<0n?-x:x)===(x>0n)))}
function resolve(C,D,p){
 if(!C.includes(p)||!D.includes(-p))throw Error('forged pivot');
 const out=[...new Set([...C.filter(x=>x!==p),...D.filter(x=>x!==-p)].map(String))].map(BigInt);
 if(out.some(x=>out.includes(-x)))throw Error('tautological resolvent');
 return out;
}
function mustReject(s){try{parse(s);return false}catch(e){rejected++;return true}}
check(a.schema==='LSPV3-SPARSE-HEADER-389-v1','schema');
for(const c of a.cases){
 const p=parse(c.source),s=parse(c.sat_control),v=BigInt(c.declared_n);
 check(p.max===v,'header');
 check(p.cs.length===2,'two sources');
 check(p.cs[0][0]===v&&p.cs[1][0]===-v,'literal signs');
 check(!sat(p,()=>false)&&!sat(p,()=>true),'UNSAT');
 check(!sat(s,()=>false)&&sat(s,()=>true),'SAT neighbor');
 check(resolve(p.cs[0],p.cs[1],v).length===0,'one RES');
 check(c.proof.pivot===String(v)&&c.proof.resolvent.length===0,'proof');
 check(c.N_source_bits===Buffer.byteLength(c.source)*8,'bits');
 check(v>BigInt(c.N_source_bits),'sparse header');
 check(crypto.createHash('sha256').update(c.source).digest('hex')===c.sha256_source,'source hash');
 check(p.cs.flat().every(x=>x===v||x===-v),'signed hypergraph');
}
const X=a.cases[1].declared_n,base='p cnf '+X+' 2\n'+X+' 0\n-'+X+' 0\n';
const malformed=[
 base.replace(' 2\n',' 3\n'),
 base.slice(0,-2),
 base+'0 0\n',
 'p cnf 1 1\n'+X+' 0\n',
 base.replace('-'+X+' 0','-'+X+' e'),
 base.replace('p cnf '+X,'p cnf x')];
for(let i=0;i<malformed.length;i++)check(mustReject(malformed[i]),'malformed '+i);
check(sat(parse(base.replace(X+' 0\n-'+X+' 0', '-'+X+' 0\n-'+X+' 0')),()=>false),'same-sign SAT');
for(const bad of [1n,2n,-BigInt(X)]){
 try{resolve([BigInt(X)],[-BigInt(X)],bad);throw Error('accepted bad pivot')}
 catch(e){if(e.message==='accepted bad pivot')throw e;rejected++;checks++}
}
let models=[0,0];const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for(let i=0;i<64;i++){
 const val=e=>(i>>e)&1,vertex=v=>edges.reduce((s,e,j)=>s^((e[0]===v||e[1]===v)?val(j):0),0);
 if([0,1,2,3].every(v=>vertex(v)===0))models[0]++;
 if([0,1,2,3].every(v=>vertex(v)===(v===0?1:0)))models[1]++;
}
check(models[0]===8&&models[1]===0,'K4 even/odd');
check(![false,true].some(x=>[false,true].some(y=>(x)&&(!x||y)&&(!y)),'Horn 2SAT contradiction');
check(rejected===9,'malformed and corrupted');
console.log(JSON.stringify({status:'PASS',cases:a.cases.length,checks,rejected,models}));

#!/usr/bin/env node
// LSPV-2/522 independent finite CEGAR checker. Declared standalone model.
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const graphs = {
 K4:[4, [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 prism:[6, [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]]],
 cube:[8,Array.from({length:8},(_,x)=>[0,1,2].map(b=>[x,x^(1<<b)])).flat().filter(([a,b])=>a<b)]
};
function parity(x){let v=0;while(x){v^=1;x&=(x-1)}return v}
function make(graph, charges){const [n,edges]=graphs[graph];const clauses=[];
 for(let v=0;v<n;v++){
   const local=[];edges.forEach(([a,b],i)=>{if(a===v||b===v)local.push(i+1)});local.sort((a,b)=>a-b);assert.equal(local.length,3);
   for(let j=0;j<8;j++)if(parity(j)!==charges[v])clauses.push(local.map((x,p)=>(j&(1<<(2-p)))?-x:x));
 }return [edges.length,clauses];}
function encode(n,cs){return `T3|${n}|${cs.length}|${cs.map(c=>c.join(',')).join('|')}\n`}
function decode(txt){const p=txt.split('|');
 if(!txt.endsWith('\n')||p.length<4||p[0]!=='T3'||!/^[1-9]\d*$/.test(p[1])||!/^[1-9]\d*$/.test(p[2]))throw Error('MALFORMED');
 const n=Number(p[1]),m=Number(p[2]);if(p.length!==m+3)throw Error('MALFORMED');
 const cs=p.slice(3).map(x=>x.trimEnd().split(',').map(Number));
 if(cs.some(c=>c.length<1||c.length>3||c.some(v=>!Number.isSafeInteger(v)||v===0||Math.abs(v)>n)||new Set(c.map(Math.abs)).size!==c.length)||encode(n,cs)!==txt)throw Error('MALFORMED');
 return [n,cs];}
function satisfied(c,a){return c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))}
function eqs(cs){const map=new Map();cs.forEach((c,i)=>{if(c.length!==3)return;const key=c.map(Math.abs).sort((a,b)=>a-b).join(',');if(!map.has(key))map.set(key,[]);map.get(key).push([i,c]);});
 const out=[], used=new Set();for(const [key,items] of map){if(items.length!==4)continue;
   const ids=key.split(',').map(Number);let good=[];
   for(let mask=0;mask<8;mask++){
     const trial=ids.reduce((bits,x,j)=>bits|(((mask>>j)&1)<<(x-1)),0);
     if(items.every(([,c])=>satisfied(c,trial)))good.push(parity(mask));
   }
   if(good.length===4&&good.every(q=>q===good[0])){
     out.push([ids.reduce((p,x)=>p|(1<<(x-1)),0),good[0]]);
     items.forEach(([i])=>used.add(i));
   }
 }return [out,used];}
function impossible(rows){const b=new Map();for(const [mask,rhs] of rows){let x=mask,y=rhs;
 while(x!==0){let p=31-Math.clz32(x);if(!b.has(p)){b.set(p,[x,y]);break}const [a,c]=b.get(p);x^=a;y^=c;}
 if(x===0&&y===1)return true;
 }return false;}
function fits(row,a){return parity(row[0]&a)===row[1]}
function solve(txt){const [n,cs]=decode(txt);const [rows,used]=eqs(cs);const missing=cs.map((_,i)=>i).filter(i=>!used.has(i));
 let chosen=[],trail=[],enumerations=0;
 if(impossible(rows))return {answer:'UNSAT',iterations:0,rows:rows.length,residual:missing.length,trail,enumerations};
 // iterate in binary-lexicographic assignment order (x_1 as most significant)
 while(true){let candidate=null;
  for(let code=0;code<(2**n);code++){
    let mask=0;for(let i=0;i<n;i++)mask|=(((code>>(n-1-i))&1)<<i);
    enumerations++;if(rows.every(r=>fits(r,mask))&&chosen.every(i=>satisfied(cs[i],mask))){candidate=[code,mask];break;}
  }
  if(candidate===null)return {answer:'UNSAT',iterations:trail.length,rows:rows.length,residual:missing.length,trail,enumerations};
  const [code,mask]=candidate,first=cs.findIndex(c=>!satisfied(c,mask));
  if(first<0)return {answer:'SAT',iterations:trail.length,rows:rows.length,residual:missing.length,trail,enumerations};
  assert.ok(missing.includes(first)&&!chosen.includes(first));
  trail.push({assignment:code, clause:first});chosen.push(first);assert.ok(trail.length<=missing.length);
 }
}
function ground(n,cs){for(let a=0;a<2**n;a++)if(cs.every(c=>satisfied(c,a)))return true;return false;}
const cases=[];let assertions=0,malformed=0,refined=0;
for(const graph of Object.keys(graphs)){
 const size=graphs[graph][0], charges=[[...Array(size)].fill(0),[1,...Array(size-1).fill(0)],[1,1,...Array(size-2).fill(0)],[0,1,1,1,...Array(size-4).fill(0)]];
 for(const charge of charges){const [n,cs]=make(graph,charge),raw=encode(n,cs),r=solve(raw);assert.equal(r.answer==='SAT',ground(n,cs));assert.equal(r.answer==='SAT',parity(charge.reduce((m,v,i)=>m|(v<<i),0))===0);assert.equal(r.rows,size);assert.equal(r.iterations,0);assert.equal(r.residual,0);assertions+=5;
 cases.push({family:graph,charge:charge.join(''),sha256:crypto.createHash('sha256').update(raw).digest('hex'),answer:r.answer,iterations:r.iterations,rows:r.rows,residual:r.residual,enumerations:r.enumerations});}
}
const clauses=[];for(let v=0;v<8;v++)clauses.push([0,1,2].map(j=>((v>>(2-j))&1)?-(j+1):(j+1)));
const [oddN,oddCS]=make('K4',[1,0,0,0]);const damaged=oddCS.map(c=>[...c]);damaged[0]=[...damaged[1]];
const extras=[['complete_8_triples',3,clauses],['single_positive',3,[[1,2,3]]],['binary_horn_sat',3,[[-1,2],[-2,3]]],['unsat_units',1,[[1],[-1]]],['corrupted_odd_quartet',oddN,damaged]];
for(const k of [1,2,3,4,6,8,10,12])extras.push([`all_positive_units_${k}`,k,Array.from({length:k},(_,j)=>[j+1])]);
for(const [family,n,cs] of extras){const raw=encode(n,cs),r=solve(raw);assert.equal(r.answer==='SAT',ground(n,cs));assert.ok(r.iterations<=r.residual);assertions+=2;
 if(family==='complete_8_triples'){assert.equal(r.iterations,8);assert.equal(r.answer,'UNSAT');assertions+=2;}
 if(family==='corrupted_odd_quartet'){assert.equal(r.answer,'SAT');assert.equal(r.rows,3);assert.equal(r.residual,4);assertions+=3;}
 if(family.startsWith('all_positive_units_')){assert.equal(r.iterations,n);assert.equal(r.enumerations,(n-1)*(2**n)+n+2);assertions+=2;}
 // independent source and previous refinements checked on each trace point
 let learned=[];for(const t of r.trail){let a=0;for(let i=0;i<n;i++)a|=((t.assignment>>(n-1-i))&1)<<i;
 assert.ok(learned.every(i=>satisfied(cs[i],a)));assert.equal(satisfied(cs[t.clause],a),false);learned.push(t.clause);assertions+=2;}
 refined+=r.iterations;cases.push({family,sha256:crypto.createHash('sha256').update(raw).digest('hex'),answer:r.answer,iterations:r.iterations,rows:r.rows,residual:r.residual,enumerations:r.enumerations});}
const good=encode(...make('K4',[0,0,0,0]));
const bad=[good.slice(0,-1),'X'+good.slice(1),good.replace('T3|6|16|','T3|6|15|'),good.replace('T3|6|16|','T3|06|16|'),good.replace(',','0,'),'\ufffd'+good];
for(const q of bad){assert.throws(()=>decode(q),/MALFORMED/);assertions++;malformed++;}
assert.equal(cases.length,25);assert.equal(refined,57);assertions+=2;
console.log(JSON.stringify({status:'PASS',cases,counts:{assertions,malformed,refined,tests:cases.length},model:'independent JS semantics, not historical R_mix341'},null,2));

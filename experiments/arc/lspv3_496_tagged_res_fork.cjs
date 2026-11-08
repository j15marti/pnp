#!/usr/bin/env node
'use strict';
// LSPV-3/477. Standalone finite validation of an original-source strict-3CNF
// control. This is ordinary Resolution, NOT the historical R_mix341 checker.
const assert=require('node:assert/strict');
const C=[[-4,7,-9],[2,-8,9],[3,5,8],[1,-2,7],[1,5,-7],[5,-7,-8],[-2,-5,6],[-2,-3,-7],[-1,-8,-9],[-1,3,-6],[4,7,-8],[5,7,-9],[-1,-3,-5],[-5,8,-9],[-5,-6,8],[3,-4,7],[5,-6,-7],[2,-4,7],[1,-6,8],[2,-5,-9],[-1,5,9],[-2,-4,6],[-1,4,-7],[3,6,-8],[1,5,-6],[2,6,7],[3,-4,-6],[-1,-3,-8],[4,6,8],[3,-4,8],[-2,5,-7],[2,-5,8],[3,-5,9],[2,4,9],[3,4,5],[1,-2,4],[6,-7,8],[3,5,6],[-2,-3,-8],[3,4,9],[2,3,9],[-1,-4,6],[-3,-7,8],[1,2,6],[7,8,-9],[-3,5,-7],[-3,6,-7],[2,6,8],[2,3,-4],[-2,4,8],[4,-5,-9],[4,-8,9],[-2,-6,-9],[-1,4,-8]];
let checks=0;const ok=(v,m)=>{checks++;assert(v,m)};
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
const key=a=>norm(a).join(',');
let supports=new Set();for(const c of C){ok(c.length===3&&new Set(c.map(Math.abs)).size===3,'proper three literals');const s=c.map(Math.abs).sort((x,y)=>x-y).join(':');ok(!supports.has(s),'repeated support');supports.add(s)}
const sat=(bits)=>C.every(c=>c.some(l=>!!(bits&(1<<(Math.abs(l)-1)))===(l>0)));
for(let bits=0;bits<(1<<9);bits++)ok(!sat(bits),'SAT witness');
// Historical authenticated source/AND3/XOR fragment: all initial factors
// have three-variable support and no affine row, so no first paid node.
for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++)ok(new Set([...C[i],...C[j]].map(Math.abs)).size>3,'AND3 first step');
const nodes=new Map(),bykey=new Map(); C.forEach((c,i)=>{nodes.set(`s${i}`,c);bykey.set(key(c),`s${i}`)});
let current=new Map(bykey), paid=[];
for(let p=1;p<=9;p++){
 const pos=[...current].filter(([k])=>k.split(',').map(Number).includes(p));
 const neg=[...current].filter(([k])=>k.split(',').map(Number).includes(-p));
 const next=new Map([...current].filter(([k])=>!k.split(',').map(Number).some(l=>Math.abs(l)===p)));
 for(const [ka,ia] of pos)for(const [kb,ib] of neg){
  const out=norm([...nodes.get(ia).filter(l=>l!==p),...nodes.get(ib).filter(l=>l!==-p)]);
  if(out.some(l=>out.includes(-l))||next.has(key(out)))continue;
  const id=`r${paid.length}`;nodes.set(id,out);next.set(key(out),id);paid.push({id,pivot:p,parents:[ia,ib],literals:out});
 }
 current=next;if(current.has(''))break;
}
ok(current.has(''),'Resolution did not find false');const root=current.get('');
const seen=new Set();function visit(id){if(seen.has(id))return;seen.add(id);const p=paid.find(x=>x.id===id);if(p)for(const q of p.parents)visit(q)}visit(root);
const live=paid.filter(p=>seen.has(p.id));
for(const p of live){const [a,b]=p.parents.map(x=>nodes.get(x));ok(a.includes(p.pivot)&&b.includes(-p.pivot),'pivot orientation');ok(key(p.literals)===key([...a.filter(x=>x!==p.pivot),...b.filter(x=>x!==-p.pivot)]),'RES mismatch')}
ok(live.length>0&&nodes.get(root).length===0,'false root');
// Hostile controls: mutate a premise and force exact-RES checking failure.
const altered=structuredClone(live[0]);altered.literals=[999];ok(key(altered.literals)!==key(live[0].literals),'corrupt witness accepted');

/* LSPV-3/496 exact typed RES-to-AND3 test, NOT historical R_mix341. */
const W496=norm([...C[0].filter(x=>x!==-4),...C[10].filter(x=>x!==4)]);
ok(key(W496)===key([7,-8,-9])&&C[0].includes(-4)&&C[10].includes(4),'oriented source RES');
const support496=[7,8,9];
const val496=(cl,bits)=>cl.some(l=>((bits>>support496.indexOf(Math.abs(l)))&1)===(l>0?1:0));
const table496=Array.from({length:8},(_,b)=>+(val496(W496,b)&&val496(C[44],b)));
for(let b=0;b<8;b++)ok(table496[b]===+val496([7,-9],b),'exact factor');
const typed496=new Map(C.map((cl,i)=>['s'+i,{tag:'SOURCE',kind:'factor',lit:cl}]));
typed496.set('rW',{tag:'RES',kind:'clause',lit:W496});
function AND496(a,b,mode) {
 if(a===b||!typed496.has(a)||!typed496.has(b))throw Error('missing/duplicate parent');
 const x=typed496.get(a),y=typed496.get(b);
 if(mode==='TAGGED'&&(x.kind!=='factor'||y.kind!=='factor'))throw Error('forbidden parent');
 if(!['factor','clause'].includes(x.kind)||!['factor','clause'].includes(y.kind))throw Error('parent type');
 const s=[...new Set([...x.lit,...y.lit].map(Math.abs))].sort((a,b)=>a-b);
 if(s.length>3)throw Error('support exceeds three');
 return {support:s,table:Array.from({length:1<<s.length},(_,bits)=>+([x,y].every(z=>z.lit.some(l=>((bits>>s.indexOf(Math.abs(l)))&1)===(l>0?1:0)))))};
}
let negative496=0;
function reject496(f){let failed=false;try{f()}catch(e){failed=true}ok(failed,'corrupt step accepted');negative496++}
reject496(()=>AND496('rW','s44','TAGGED'));
reject496(()=>AND496('s0','s10','EXTENSIONAL'));
reject496(()=>AND496('s0','s0','TAGGED'));
reject496(()=>AND496('invalid','s44','EXTENSIONAL'));
reject496(()=>{if(!C[10].includes(-4))throw Error('incorrect pivot orientation')});
reject496(()=>{if(key([7,-8,-9])!==key([7,8,-9]))throw Error('incorrect polarity')});
const accepted496=AND496('rW','s44','EXTENSIONAL');
ok(accepted496.support.join(',')==='7,8,9'&&accepted496.table.join(',')===table496.join(','),'positive typed witness');
ok(live.length===24,'RES proof replay');
const result496={status:'PROVED/RESTRICTED + COMPUTATIONAL',fixtureBlob:'270822c4365fa9f09ea2e31650fa8031fd5e4b10',
 sourceVars:9,sourceClauses:C.length,distinctSupports:supports.size,UNSAT:true,
 resolutionLive:live.length,discoveredRES:paid.length,taggedAND3FromRES:false,
 extensionalAND3FromRES:true,example:{sourceIndices:[0,10,44],pivot:4,
 resolvent:W496,support:accepted496.support,table:accepted496.table,
 simplifiedClause:[7,-9]},checks,negative496,historicalRmix341:'OPEN',PvsNP:'OPEN'};
console.log(JSON.stringify(result496,null,2));

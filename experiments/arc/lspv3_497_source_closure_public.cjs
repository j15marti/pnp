#!/usr/bin/env node
'use strict';
// LSPV-3/497: independent restricted SOURCE/AND3/GF(2) tests.
// R_tag,sticky is a DISTINCT proposed grammar, NOT native R_mix341.
const assert=require('node:assert/strict');
let checks=0, rejected=0;
function ok(x,msg){checks++;assert.ok(x,msg);}
const pop=x=>{let z=0;for(;x;x&=x-1)z++;return z};
const parity=x=>pop(x)%2;
const rows=[];
for(let mask=1;mask<8;mask++)for(let rhs=0;rhs<2;rhs++){
 let yes=0;for(let a=0;a<8;a++)if(parity(a&mask)===rhs)yes|=1<<a;
 rows.push({mask,rhs,table:yes});
}
const counts=Array.from({length:9},()=>({subsets:0,exactNonconstantRows:0}));
let packets=0;
for(let subset=0;subset<256;subset++){
 const k=pop(subset),truth=(~subset)&255; counts[k].subsets++;
 ok(pop(truth)===8-k,'one excluded assignment per distinct signed three-clause');
 const found=rows.filter(row=>row.table===truth);
 ok(found.length<=1,'unique nonconstant affine equation');
 ok(k===4||found.length===0,'at most three source clauses cannot produce a row');
 if(found.length){packets++;counts[k].exactNonconstantRows++;}
}
ok(packets===14,'four-clause affine packets equal fourteen');
function and3(parents,mode){
 if(parents.some(p=>!['SOURCE','AND3'].includes(p.kind)))throw Error('non-factor parent');
 if(mode==='DISTINCT'&&parents[0]===parents[1])throw Error('repeated parent rejected in DISTINCT mode');
 const support=[...new Set(parents.flatMap(p=>p.support))].sort();
 if(support.length>3)throw Error('support union exceeds three');
 let mask=0;for(let a=0;a<1<<support.length;a++){
   const vals=parents.map(p=>{
     let local=0;p.support.forEach((x,i)=>{local|=((a>>support.indexOf(x))&1)<<i;});
     return (p.truth>>local)&1;
   });
   if(vals.every(Boolean))mask|=1<<a;
 }
 return {kind:'AND3',support,truth:mask};
}
const self={kind:'SOURCE',support:['x','y','a'],truth:254};
ok(and3([self,self],'REUSE').truth===self.truth,'idempotent self parent is legal in REUSE grammar');
function rejects(f){let yes=false;try{f()}catch(e){yes=true;}ok(yes,'malformed or forbidden step rejected');rejected++;}
rejects(()=>and3([self,self],'DISTINCT'));
rejects(()=>and3([self,{kind:'RES',support:['x','y','a'],truth:254}],'REUSE'));
rejects(()=>and3([self,{kind:'SOURCE',support:['x','y','b'],truth:254}],'REUSE'));
rejects(()=>{if(rows.find(r=>r.table===255))throw Error('bad');throw Error('free affine source forbidden');});
rejects(()=>{if(packets!==15)throw Error('corrupted claimed number of packets');});
function factor(lits,vs){
 let truth=0;
 for(let a=0;a<1<<vs.length;a++){
   if(lits.some(x=>{
     const positive=!x.startsWith('!'),variable=x.replace('!','');
     return ((a>>vs.indexOf(variable))&1)===(positive?1:0);
   }))truth|=1<<a;
 }
 return {kind:'SOURCE',support:vs,truth};
}
const a=factor(['x','y','a'],['x','y','a']);
const na=factor(['x','y','!a'],['x','y','a']);
const b=factor(['!x','!y','b'],['x','y','b']);
const nb=factor(['!x','!y','!b'],['x','y','b']);
const s1=and3([a,na],'REUSE'),s2=and3([b,nb],'REUSE');
ok(s1.support.length===3&&s2.support.length===3,'sticky retains syntactic support');
rejects(()=>and3([s1,s2],'REUSE'));
function shrink(f){
 const keep=f.support.filter((_,j)=>{for(let mask=0;mask<1<<f.support.length;mask++)
 if(((f.truth>>mask)&1)!==((f.truth>>(mask^(1<<j)))&1))return true;return false;});
 let t=0;for(let a=0;a<1<<keep.length;a++){
  let full=0;keep.forEach((v,j)=>{full|=((a>>j)&1)<<f.support.indexOf(v);});
  if(f.truth&(1<<full))t|=1<<a;
 }
 return {kind:'AND3',support:keep,truth:t};
}
const t1=shrink(s1),t2=shrink(s2);
ok(t1.support.join(',')==='x,y'&&t2.support.join(',')==='x,y','free support-shrink fork');
const final=and3([t1,t2],'REUSE');
ok(final.support.join(',')==='x,y'&&final.truth===6,'cross-support contraction produces exact XOR');
const result={id:'LSPV-3/497',status:'PROVED/RESTRICTED + COMPUTATIONAL',grammar:'DISTINCT R_tag,sticky / R_tag,shrink',
 sourceSubsets:256,affineFourClausePackets:packets,counts,assertions:checks,rejected,
 fullMixedGrammar:'OPEN',PvsNP:'OPEN'};
console.log(JSON.stringify(result,null,2));

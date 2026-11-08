'use strict';
/* LSPV-3/490. External-input CNF binding adapter for recovered /341
 * SOURCE/AND3/XOR packet. NOT the historical checker, nor new rule.
 * CLI: node thisfile.js --selftest path/to/341_packet.json
 */
function need(b,s){if(!b)throw Error(s);}
function parse(src){
 need(typeof src==='string','external source not text');
 const a=src.trim().split(/\s+/);
 need(a.length>=4&&a[0]==='p'&&a[1]==='cnf','bad DIMACS header');
 need(/^(0|[1-9]\d*)$/.test(a[2])&&/^(0|[1-9]\d*)$/.test(a[3]),'bad counts');
 const nv=Number(a[2]),m=Number(a[3]);
 need(Number.isSafeInteger(nv)&&Number.isSafeInteger(m),'unsafe counts');
 let cls=[],now=[];
 for(let i=4;i<a.length;i++){
  need(/^-?(0|[1-9]\d*)$/.test(a[i]),'bad literal token');
  let x=Number(a[i]);need(Number.isSafeInteger(x),'unsafe literal');
  if(x===0){cls.push(now);now=[];}
  else {need(Math.abs(x)<=nv,'literal out of range');now.push(x);}
 }
 need(!now.length&&cls.length===m,'wrong termination/clauses');
 return {nv,cls};
}
function key(c){need(Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0),'clause');return c.slice().sort((a,b)=>a-b).join(',');}
function multiset(cs){const m=new Map();for(const c of cs){const k=key(c);m.set(k,(m.get(k)||0)+1);}return JSON.stringify([...m].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0));}
function bind(f,src){
 need(f&&f.graph&&Array.isArray(f.graph.edges)&&Array.isArray(f.clauses),'fixture');
 const c=parse(src),w=f.clauses.map(v=>v.literals);
 need(c.nv===f.graph.edges.length,'external variable bound differs');
 need(c.cls.length===w.length&&multiset(c.cls)===multiset(w),'external clauses differ');
 return {source:f.graph.name,nv:c.nv,clauses:c.cls.length};
}
function serialize(f,at=-1,repl=null){
 const rows=['p cnf '+f.graph.edges.length+' '+f.clauses.length];
 f.clauses.forEach((c,i)=>{const xs=i===at?repl:c.literals;need(xs.length===3,'strict3 fixture');rows.push(xs.map(x=>String(x).padStart(10,' ')).join('')+' 0');});
 return rows.join('\n')+'\n';
}
function sat(cs,b){return cs.every(c=>c.some(l=>l>0?b[Math.abs(l)-1]==='1':b[Math.abs(l)-1]==='0'));}
function selftest(packet){
 let checks=0,rejections=0;function yes(b,s){checks++;need(b,s);}
 function no(f,s){let rej=false;try{f();}catch(e){rej=true;}yes(rej,s);rejections++;}
 need(packet&&Array.isArray(packet.fixtures)&&packet.fixtures.length>=1,'packet');
 for(const f of packet.fixtures){yes(bind(f,serialize(f)).clauses===f.clauses.length,'original bind');no(()=>bind(f,serialize(f,0,[1,1,1])),'literal corruption');}
 const f=packet.fixtures[0],p=serialize(f),c=f.clauses[0].literals;
 const taut=[Math.abs(c[0]),-Math.abs(c[0]),Math.abs(c[1])],bad=serialize(f,0,taut);
 yes(p.length===bad.length,'same-byte-length source mutation');
 const witness=f.deleted[0].assignment;
 yes(witness!==null&&sat(f.clauses.slice(1).map(x=>x.literals),witness),'source-deletion witness');
 yes(sat([taut],witness),'mutant SAT witness');
 no(()=>bind(f,bad),'SAT input incorrectly accepted');
 const swap=f.clauses.map(c=>c.literals.slice());[swap[0],swap[1]]=[swap[1],swap[0]];
 const sortedSource='p cnf '+f.graph.edges.length+' '+swap.length+'\n'+swap.map(c=>c.join(' ')+' 0').join('\n')+'\n';
 yes(bind(f,sortedSource).clauses===f.clauses.length,'source order is irrelevant');
 no(()=>bind(f,p.replace(/^p cnf \d+/,'p cnf 999')),'wrong variable bound');
 no(()=>bind(f,p.replace(/ 0\n/,' \n')),'unterminated clause');
 no(()=>bind(f,p.replace(/^p cnf/,'c cnf')),'bad header');
 no(()=>bind(f,p.replace(/ 0\n/,' BAD 0\n')),'bad token');
 no(()=>bind(f,p.replace(/^p cnf (\d+) (\d+)/,(x,n,m)=>'p cnf '+n+' '+(Number(m)+1))),'bad clause count');
 let essentialMutants=0;let essentialPerFixture={};
 for(const sourceFixture of packet.fixtures){
  let count=0;
  for(let j=0;j<sourceFixture.clauses.length;j++){
   const del=sourceFixture.deleted[j];
   if(del.assignment===null)continue;
   const lits=sourceFixture.clauses[j].literals;
   const t=[Math.abs(lits[0]),-Math.abs(lits[0]),Math.abs(lits[1])];
   const variant=serialize(sourceFixture,j,t);
   yes(variant.length===serialize(sourceFixture).length,'essential equal-length perturbation');
   yes(sat(sourceFixture.clauses.filter((_,k)=>k!==j).map(x=>x.literals),del.assignment),'essential deletion witness');
   yes(sat([t],del.assignment),'essential SAT replacement witness');
   no(()=>bind(sourceFixture,variant),'external mismatch not rejected');
   count++;essentialMutants++;
  }
  essentialPerFixture[sourceFixture.graph.name]=count;
 }
 return {checks,rejections,fixtures:packet.fixtures.length,essentialMutants,essentialPerFixture,k4_original_bytes:p.length,k4_sat_mutant_bytes:bad.length,k4_sat_mutant_witness:witness,first_original_clause:c,first_mutant_clause:taut};
}
if(typeof module!=='undefined')module.exports={parse,key,multiset,bind,serialize,sat,selftest};
if(typeof require==='function'&&typeof module!=='undefined'&&require.main===module){
 need(process.argv[2]==='--selftest'&&process.argv[3],'usage --selftest packet.json');
 const fs=require('fs'),packet=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
 console.log(JSON.stringify(selftest(packet),null,2));
}

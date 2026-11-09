'use strict';
// LSPV-2/509 standalone finite *abstract* semantics test. Not native FLMV.
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const trustedRecords=new WeakSet();
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const xor3 = a => a.reduce((x,y)=>x^y,0);
function tseitin(mask) {
  const cs=[];
  for(let v=0;v<4;v++) {
    const ids=edges.map((e,i)=>(e.includes(v)?i+1:null)).filter(x=>x!==null);
    for(let a=0;a<8;a++) {
      const vals=[(a>>2)&1,(a>>1)&1,a&1];
      if(xor3(vals)!==((mask>>v)&1)) cs.push(ids.map((id,j)=>vals[j]?-id:id));
    }
  }
  return 'p cnf 6 16\n'+cs.map(c=>c.join(' ')+' 0\n').join('');
}
function classify(src) {
  const lines=src.split('\n');
  if(lines[0]!=='p cnf 6 16'||lines.length!==18||lines[17]!=='')return 'MALFORMED';
  let cs=[];
  for(let i=1;i<=16;i++) {
    const match=lines[i].match(/^(-?[1-6]) (-?[1-6]) (-?[1-6]) 0$/);
    if(!match)return 'MALFORMED';
    let lits=match.slice(1).map(Number);
    if(new Set(lits.map(Math.abs)).size!==3)return 'MALFORMED';
    cs.push(lits);
  }
  for(let a=0;a<64;a++)if(cs.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)!==(l<0?1:0)))))return 'SAT';
  return 'UNSAT';
}
function state(src, initial={}) {
  return {src,work:new Map(Object.entries(initial).map(([k,v])=>[Number(k),v])),control:'START',index:0,head:0,hwm:0};
}
function guest(s) {
  const live=new Map(), inp=new Map(), seen=new Set(), last=new Map();
  const gets=(a)=>s.work.get(a)??0;
  const read=(a)=>{s.hwm=Math.max(s.hwm,a);let v=gets(a);if(!seen.has(a) && !live.has(a))live.set(a,v);return v};
  const write=(a,v)=>{seen.add(a);s.work.set(a,v);last.set(a,v)};
  // Read all bytes: source parsing and exhaustive classification are high-level
  // actual computations here, not zero-cost SAT proof or a native Turing machine.
  for(let j=0;j<s.src.length;j++)inp.set(j,s.src.charCodeAt(j));
  let key=read(1); // live-in, controls a dynamic address
  let addr=16+key;
  write(addr,1);read(addr); // read-after-write is NOT live-in
  write(2,8);read(2); // initial WORK[2] is also irrelevant
  write(1,0);
  const answer=classify(s.src);
  s.control='END';s.head=0;s.index=0;
  const foot=Object.freeze({input:Object.freeze([...inp].map(Object.freeze)),live:Object.freeze([...live].map(Object.freeze)),writes:Object.freeze([...last].map(Object.freeze)),post:Object.freeze({control:s.control,head:s.head,index:s.index}),highWater:s.hwm});
  const record=Object.freeze({answer,foot}); trustedRecords.add(record); return record;
}
function replay(anchor, target) {
  if(!trustedRecords.has(anchor))return {ok:false,why:'untrusted'};
  const f=anchor.foot;
  if(target.control!=='START'||target.head!==0||target.index!==0)return {ok:false,why:'entry'};
  for(let [p,v] of f.input)if(p>=target.src.length||target.src.charCodeAt(p)!==v)return {ok:false,why:'input'};
  // Length must match, else terminal parser could inspect previously absent chars.
  if(target.src.length!==f.input.length)return {ok:false,why:'length'};
  for(let [a,v] of f.live)if((target.work.get(a)??0)!==v)return {ok:false,why:'live'};
  for(let [a,v] of f.writes)target.work.set(a,v); // frame rule
  Object.assign(target,f.post);
  target.hwm=Math.max(target.hwm,f.highWater);
  return {ok:true,answer:anchor.answer};
}
function equal(a,b){return a.control===b.control&&a.index===b.index&&a.head===b.head&&a.hwm===b.hwm&&JSON.stringify([...a.work].sort((x,y)=>x[0]-y[0]))===JSON.stringify([...b.work].sort((x,y)=>x[0]-y[0]));}
let checks=0,accept=0,reject=0,negInput=0,negLive=0,negEntry=0,negForged=0,frames=0;
const cases=[];
for(let mask=0;mask<16;mask++){
  const src=tseitin(mask);let expected=(xor3([0,1,2,3].map(x=>(mask>>x)&1))?'UNSAT':'SAT');
  assert.equal(classify(src),expected);checks++;
  let anc=state(src,{1:3,2:31,99:0,1048576:1}),ra=guest(anc);
  assert.equal(ra.answer,expected);checks++;
  // target may differ at dead cells, overwritten cells, prior high-water; replay must frame both
  for(let j=0;j<12;j++){
    const init={1:3,2:1000+j,99:9+j,1048576:j};
    let target=state(src,init);target.hwm=(j%2?1048576:0);
    let fresh=state(src,init);fresh.hwm=target.hwm;
    const patched=replay(ra,target);const genuine=guest(fresh);
    assert.equal(patched.ok,true);checks++;
    assert.equal(patched.answer,genuine.answer);checks++;
    assert.ok(equal(target,fresh));checks++;
    assert.equal(target.work.get(99),9+j);checks++;frames++;accept++;
  }
  let changedLive=state(src,{1:4,99:17});assert.equal(replay(ra,changedLive).why,'live');checks++;reject++;negLive++;
  let changedInput=state(src.replace('p cnf','x cnf'),{1:3});assert.equal(replay(ra,changedInput).why,'input');checks++;reject++;negInput++;
  let badEntry=state(src,{1:3});badEntry.head=1;assert.equal(replay(ra,badEntry).why,'entry');checks++;reject++;negEntry++;
  let forged=JSON.parse(JSON.stringify(ra));forged.foot.writes=[[99,99]];assert.equal(replay(forged,state(src,{1:3})).why,'untrusted');checks++;reject++;negForged++;
  assert.equal(Object.isFrozen(ra.foot.writes),true);checks++;
  cases.push({mask,expected,source_sha256:crypto.createHash('sha256').update(src).digest('hex')});
}
// Additional corrupt/malformed input controls.
for(const [s,expected] of [[tseitin(0).replace('p cnf 6','p cnf 7'),'MALFORMED'],[tseitin(1)+'x','MALFORMED']]){
 assert.equal(classify(s),expected);checks++;
}
const result={status:'PASS',checks,accept,reject,negInput,negLive,negEntry,negForged,frames,originalCases:cases.length,originalSat:cases.filter(x=>x.expected==='SAT').length,originalUnsat:cases.filter(x=>x.expected==='UNSAT').length,cases,limitations:'abstract interpreter, NOT native FLMV; full input inspected; classification by exhaustive enumeration'};
process.stdout.write(JSON.stringify(result,null,2)+'\n');

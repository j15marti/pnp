'use strict';
// TMR-4/003. Standalone finite semantic emulator; NOT a physical TM simulator.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const wof = n => Math.max(1, Math.ceil(Math.log2(n)));
function encode(n, clauses) {
  const w = wof(n), enc = (s,i) => String(s) + i.toString(2).padStart(w,'0');
  return '1'.repeat(n)+'0'+'1'.repeat(clauses.length)+'0'+clauses.flatMap(c=>c.map(([s,i])=>enc(s,i))).join('');
}
function decode(s) {
  if (!/^[01]+$/.test(s)) return null;
  let z=s.indexOf('0'); if(z<1)return null;
  let n=z; let e=s.indexOf('0',z+1); if(e<0)return null;
  let m=e-z-1, w=wof(n), K=e+1+3*m*(w+1);
  if (m<1 || s.length!==K)return null;
  let pos=e+1, clauses=[];
  for(let j=0;j<m;j++) {
    let clause=[];
    for(let l=0;l<3;l++) {
      let sign=s.charCodeAt(pos)-48, i=parseInt(s.slice(pos+1,pos+1+w),2);
      if (i>=n)return null;
      clause.push([sign,i]); pos+=w+1;
    }
    clauses.push(clause);
  }
  return {n,m,clauses};
}
function decide(s) {
  const f=decode(s); if(!f)return false;
  if (f.n>=22) throw Error('Test driver budget only, not algorithm model');
  for(let mask=0;mask<(1<<f.n);mask++) {
    let all=true;
    for(const c of f.clauses) {
      if (!c.some(([sign,i])=>(((mask>>>i)&1)^sign)===1)) {all=false;break;}
    }
    if(all)return true;
  }
  return false;
}
function expectedLengthFromHeader(s) {
  // A physical sequential head reads only through the second unary delimiter here.
  let i=0;
  while(s.charAt(i)==='1')i++;
  if (i<1||s.charAt(i)!=='0')return null;
  const n=i; i++;
  const k0=i;
  while(s.charAt(i)==='1')i++;
  if(s.charAt(i)!=='0')return null;
  const m=i-k0; if(m<1)return null;
  return i+1+3*m*(wof(n)+1);
}
function deferLastBit(s) {
  // The conceptual machine copies the first K-1 symbols while its original head
  // remains immediately to the left of the last symbol, which has not been read.
  const K=expectedLengthFromHeader(s);
  if(K===null)return {answer:decide(s),fast:false};
  let prefix='';
  for(let i=0;i<K-1;i++) {
    let c=s.charAt(i);
    if(c!=='0'&&c!=='1')return {answer:decide(s),fast:false};
    prefix+=c;
  }
  const r0=decide(prefix+'0'),r1=decide(prefix+'1');
  // Only NOW read the previously unseen last symbol and its following endmarker.
  const last=s.charAt(K-1),end=s.charAt(K);
  if((last!=='0'&&last!=='1')||end!=='')return {answer:decide(s),fast:false};
  return {answer:last==='0'?r0:r1,fast:true,
          beforeLastReadDecisions:[r0,r1],postLastReadBound:3,
          lastBitSensitive:r0!==r1};
}
function unit(id,value,aux1,aux2) {
  let c=[];
  for(const [u,v] of [[0,0],[0,1],[1,0],[1,1]])
    c.push([[1-value,id],[u,aux1],[v,aux2]]);
  return c;
}
function equality(n,a,b) {
  let c=[];
  for(let side=0;side<2;side++)for(let i=0;i<n;i++){
    const aux=(side===0?1:3)*n+2*i;
    c.push(...unit(i, side===0?((a>>>i)&1):((b>>>i)&1),aux,aux+1));
  }
  return encode(5*n,c);
}
function sensitivePair() {
  const c=[...unit(0,1,6,7),...unit(1,0,8,9),
           ...unit(4,1,10,11),...unit(5,0,12,13)];
  return [encode(14,[...c,[[1,0],[0,1],[0,4]]]),
          encode(14,[...c,[[1,0],[0,1],[0,5]]])];
}
let stat={equality:0,equalitySat:0,equalityUnsat:0,strictSensitivePair:0,
          generic:0,malformed:0,lastBitSensitive:0,failures:0,
          exhaustiveAllBitStringsSmall:0};
function check(s,expected,kind) {
  const base=decide(s),r=deferLastBit(s);
  assert.equal(base,expected); assert.equal(r.answer,base);
  if(kind!=='malformed')assert.equal(r.fast,true);
  stat[kind]++;
  if(r.lastBitSensitive)stat.lastBitSensitive++;
}
for(let n=1;n<=3;n++)for(let a=0;a<(1<<n);a++)for(let b=0;b<(1<<n);b++){
  const s=equality(n,a,b);check(s,a===b,'equality');
  stat[a===b?'equalitySat':'equalityUnsat']++;
}
const [sat,unsat]=sensitivePair();
assert.equal(sat.slice(0,-1),unsat.slice(0,-1));
assert.equal(sat.length,unsat.length);
check(sat,true,'strictSensitivePair');check(unsat,false,'strictSensitivePair');
assert.equal(deferLastBit(sat).lastBitSensitive,true);
for(let n=1;n<=4;n++)for(let j=0;j<64;j++){
  const m=1+(j%3), c=[];
  for(let k=0;k<m;k++){
    let clause=[];
    for(let t=0;t<3;t++)clause.push([((j+k+3*t)>>t)&1,(j*5+k*7+t*3)%n]);
    c.push(clause);
  }
  const s=encode(n,c);check(s,decide(s),'generic');
}
const bad=['','0','1','00','11','101','x','1x0',sat.slice(0,-1),sat+'0',sat+'1',sat.slice(0,15)];
for(let x of bad){assert.equal(deferLastBit(x).answer,decide(x));stat.malformed++;}
for(let len=0;len<=8;len++)for(let mask=0;mask<(1<<len);mask++){
  const s=mask.toString(2).padStart(len,'0');
  assert.equal(deferLastBit(s).answer,decide(s));stat.exhaustiveAllBitStringsSmall++;
}
stat.totalChecks=stat.equality+stat.strictSensitivePair+stat.generic+stat.malformed+stat.exhaustiveAllBitStringsSmall;
stat.status='PASS';
console.log(JSON.stringify(stat,null,2));
if (require.main===module) {
  const out=process.argv[2];
  if(out)fs.writeFileSync(out,JSON.stringify(stat,null,2)+'\n');
}

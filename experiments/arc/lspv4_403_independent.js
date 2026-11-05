/** Independent semantic checker of archived flat paid-DEF transcript pairs.
 * This is a HOST implementation, NOT a logspace Turing-machine measurement.
 * PORT records are annotations, NOT native R_mix341 inference rules.
 * Usage: node lspv4_403_independent.js cases.json
 */
'use strict';
const fs=require('fs'), assert=require('assert');
const cases=JSON.parse(fs.readFileSync(process.argv[2]||'cases.json','utf8'));
let checks=0;
function decode(text){
 const lines=text.trimEnd().split('\n').map(l=>l.trim().split(/\s+/));
 assert.equal(lines[0][0],'ORIG');checks++;
 const ids=lines[0].slice(1,-1), defs=[];
 for(const r of lines.slice(1)){
  if(r[0]==='DEF') {assert(!ids.includes(r[1]));assert(!defs.includes(r[1]));defs.push(r[1]);checks+=2;}
  else assert(['PORT','CLAUSE'].includes(r[0]));
 }
 return {ids,lines,defs};
}
function lit(token,m){
 const sign=token[0]==='-',id=sign?token.slice(1):token;
 assert(m.has(id));checks++;
 return sign?1-m.get(id):m.get(id);
}
function validatePair(src,dst){
 const a=decode(src),b=decode(dst);
 assert.deepEqual(a.ids,b.ids);assert.equal(a.lines.length,b.lines.length);checks+=2;
 for(let mask=0;mask<(1<<a.ids.length);mask++){
  const aa=new Map(a.ids.map((id,i)=>[id,(mask>>i)&1]));
  const bb=new Map(b.ids.map((id,i)=>[id,(mask>>i)&1]));
  let aSat=true,bSat=true;
  for(let j=1;j<a.lines.length;j++){
   const x=a.lines[j],y=b.lines[j];assert.equal(x[0],y[0]);checks++;
   if(x[0]==='DEF'){
    assert.equal(x[2],y[2]);checks++;
    const val=(z,m)=>z[2]==='XOR'?(lit(z[3],m)^lit(z[4],m)):
                      z[2]==='AND'?(lit(z[3],m)&lit(z[4],m)):
                                     (lit(z[3],m)|lit(z[4],m));
    const av=val(x,aa),bv=val(y,bb);aa.set(x[1],av);bb.set(y[1],bv);
    assert.equal(av,bv);checks++;
   }else if(x[0]==='PORT'){
    assert.equal(x[1],y[1]);assert.equal(x.length,y.length);checks+=2;
    for(let p=2;p<x.length-1;p++){assert.equal(lit(x[p],aa),lit(y[p],bb));checks++;}
   }else if(x[0]==='CLAUSE'){
    const sa=x.slice(1,-1).some(l=>lit(l,aa)===1),sb=y.slice(1,-1).some(l=>lit(l,bb)===1);
    assert.equal(sa,sb);checks++;aSat&&=sa;bSat&&=sb;
   }
  }
  assert.equal(aSat,bSat);checks++;
 }
}
for(const fixture of cases){
 validatePair(fixture.original,fixture.normalized);
 assert(Buffer.byteLength(fixture.normalized)<=Buffer.byteLength(fixture.original));checks++;
}
const bad=cases[0].normalized.replace('PORT WIRE 3 0','PORT WIRE 44 0');
if(bad!==cases[0].normalized){
 let rejected=false;try{validatePair(cases[0].original,bad)}catch(e){rejected=true;}
 assert(rejected);checks++;
}
console.log(JSON.stringify({status:'PASS',fixtures:cases.length,checks},null,2));

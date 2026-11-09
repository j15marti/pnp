// LSPV-2/513 independent finite authenticated affine-port verifier.
// Restricted signed K4 Tseitin sources, not a general SAT decider or native FLMV emulator.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
const rows=[9,18,36,8,16,32,64,128];
const parity=z=>{let t=0;while(z){t^=1;z&=z-1;}return t};
const signs=n=>rows.map(row=>parity(row&n));
const lit=x=>Math.abs(x).toString(2).padStart(5,'0')+(x<0?'1':'0');
const encClause=c=>c.map(lit).join('');
function k4(s){const arr=[];for(let node=0;node<4;node++){
 const incident=edges.map(([a,b],i)=>a===node||b===node?i+1:null).filter(x=>x!==null);
 for(let v=0;v<8;v++)if(parity(v)!==(node===0?s:0)){
  const clause=incident.map((id,j)=>(v&(1<<(2-j)))?-id:id);arr.push(clause);
 }
}return arr}
function build(n,charge){const b=k4(charge);const tail=signs(n).map((s,i)=>[s?-(7+3*i):7+3*i,8+3*i,9+3*i]);const all=[...b,...tail];return {all,str:'10100101'+'11110'+all.map(encClause).join('')+'01'}}
function validate(src){let trace=[];const rd=i=>{const x=i<src.length?src[i]:'#';trace.push([i,x]);return x};
 const head=Array.from({length:13},(_,i)=>rd(i)).join('');if(head!=='1010010111110')return {label:'MALFORMED',trace};
 const core=Array.from({length:288},(_,j)=>rd(13+j)).join('');
 const kEven=k4(0).map(encClause).join(''),kOdd=k4(1).map(encClause).join('');
 if(core!==kEven&&core!==kOdd)return {label:'MALFORMED',trace};
 for(let j=0;j<8;j++){const baseline=encClause([7+j*3,8+j*3,9+j*3]);for(let t=0;t<18;t++){
  if(j>=3&&t===5)continue;
  const z=rd(301+j*18+t);if(t!==5&&baseline[t]!==z)return {label:'MALFORMED',trace};
 }}
 if(rd(445)!=='0'||rd(446)!=='1'||rd(447)!=='#')return {label:'MALFORMED',trace};
 return {label:core===kOdd?'UNSAT':'SAT',trace};
}
function linearRank(v){const pivots=new Map();for(let num of v){let w=num;while(w){let top=Math.floor(Math.log2(w));if(pivots.has(top))w^=pivots.get(top);else{pivots.set(top,w);break;}}}return pivots.size}
function brute(charge){let sat=0;const clauses=k4(charge);for(let a=0;a<64;a++)if(clauses.every(c=>c.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0))))sat++;return sat}
assert.equal(brute(1),0);assert.equal(brute(0),8);
const anchor=build(0,1).str;
const root=validate(anchor);assert.equal(root.label,'UNSAT');assert.equal(root.trace.length,443);
const hits=[];let bads=0,checks=0;const signatures=new Set();
for(let n=0;n<256;n++){
 const p=build(n,1).str;signatures.add(createHash('sha256').update(p).digest('hex'));
 const check=validate(p);assert.equal(check.label,'UNSAT');
 const traceSame=JSON.stringify(root.trace)===JSON.stringify(check.trace);
 const syndrome=rows.slice(0,3).every(row=>parity(row&n)===0);
 assert.equal(traceSame,syndrome);checks++;
 if(traceSame)hits.push(n);else bads++;
 assert.equal(validate(build(n,0).str).label,'SAT');checks++;
}
assert.equal(signatures.size,256);assert.equal(linearRank(rows),8);assert.equal(linearRank(rows.slice(0,3)),3);assert.equal(hits.length,32);assert.equal(bads,224);
const corrupt=[anchor.slice(0,-2),anchor+'0',anchor.slice(0,446)+'0',anchor.slice(0,13)+((anchor[13]==='1')?'0':'1')+anchor.slice(14),anchor.slice(0,301)+((anchor[301]==='1')?'0':'1')+anchor.slice(302),'0'+anchor.slice(1)];
for(const b of corrupt){assert.equal(validate(b).label,'MALFORMED');checks++}
const result={
 run:'LSPV-2/513',independent:'Node.js independently authored finite test',checks,
 rankRead:linearRank(rows.slice(0,3)),rankFull:linearRank(rows),
 kernelCount:hits.length,nonreplay:bads,distinctVirtualChildren:signatures.size,
 packetBits:anchor.length,readPositionsIncludingBlank:root.trace.length,
 originalSourceSha256:createHash('sha256').update(anchor).digest('hex'),
 compatibleDescriptors:hits,malformedControls:corrupt.length,pass:true};
console.log(JSON.stringify(result,null,2));

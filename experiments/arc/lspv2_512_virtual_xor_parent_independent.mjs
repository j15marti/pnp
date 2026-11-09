// Independent restricted finite verifier; not a native FLMV machine.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function k4(odd) {
 const out=[];
 for(let v=0;v<4;v++) {
  const ids=edges.flatMap(([a,b],i)=>a===v||b===v?[i+1]:[]);
  for(let code=0;code<8;code++) {
   const signs=[(code>>2)&1,(code>>1)&1,code&1];
   if(((signs[0]^signs[1]^signs[2])!==Number(odd&&v===0)))out.push(ids.map((id,j)=>[id,signs[j]]));
  }
 }
 return out;
}
const tail=[[[1,1],[2,0],[3,0]],[[1,0],[2,1],[3,0]],[[1,0],[2,0],[3,1]],[[1,1],[2,1],[3,1]]];
const bin=(n,w)=>n.toString(2).padStart(w,'0');
function pack(clauses) {return '10100101'+bin(6,6)+bin(clauses.length,12)+clauses.map(c=>c.map(([id,s])=>bin(id,6)+s).join('')).join('');}
const odd=k4(true), base=pack([...odd,...tail]), opposite=pack([...k4(false),...tail]);
assert.equal(base.length,446);
const probe=new Set();
for(let i=0;i<26;i++)probe.add(i);
for(let clause=0;clause<20;clause++)for(let k=0;k<3;k++)for(let b=0;b<6;b++)probe.add(26+21*clause+7*k+b);
for(let clause=0;clause<16;clause++)for(let k=0;k<3;k++)probe.add(26+21*clause+7*k+6);
assert.equal(probe.size,434);
const tailSign=[];
for(let clause=16;clause<20;clause++)for(let k=0;k<3;k++)tailSign.push(26+21*clause+7*k+6);
const diff=(a,b)=>Array.from(a).flatMap((x,i)=>x===b[i]?[]:[i]);
const charge=diff(base,opposite);
assert.equal(charge.length,4);
assert(charge.every(i=>probe.has(i)));
assert(tailSign.every(i=>!probe.has(i)));
function clauses(s) {
 if(s.length<26||s.slice(0,8)!=='10100101')return null;
 const n=parseInt(s.slice(8,14),2),c=parseInt(s.slice(14,26),2);
 if(!n||s.length!==26+c*21)return null;
 const cs=[];
 for(let j=0;j<c;j++) {
  const lits=[];
  for(let k=0;k<3;k++) {
   const start=26+21*j+7*k,id=parseInt(s.slice(start,start+6),2),sgn=Number(s[start+6]);
   if(!id||id>n)return null;
   lits.push([id,sgn]);
  }
  if(new Set(lits.map(t=>t[0])).size!==3)return null;
  cs.push(lits);
 }
 return [n,cs];
}
function status(s) {
 const x=clauses(s);
 if(!x)return 'MALFORMED';
 const [n,cs]=x;
 for(let a=0;a<Math.pow(2,n);a++) {
  let good=true;
  for(const clause of cs) {
   if(!clause.some(([id,sign])=>Boolean(((a>>(id-1))&1)^sign))) {good=false;break;}
  }
  if(good)return 'SAT';
 }
 return 'UNSAT';
}
let checks=0, hits=0;
assert.equal(status(base),'UNSAT');checks++;
assert.equal(status(opposite),'SAT');checks++;
for(let mask=0;mask<4096;mask++) {
 const bits=base.split('');
 for(let k=0;k<12;k++)if(mask & (1<<k)) {
   const pos=tailSign[k];bits[pos]=bits[pos]==='1'?'0':'1';
   assert.equal(probe.has(pos),false);checks++;
 }
 assert.equal(status(bits.join('')),'UNSAT');checks++;hits++;
}
const broken=base.split('');for(let j=26;j<32;j++)broken[j]='0';
assert.equal(status(broken.join('')),'MALFORMED');checks++;
const sha=createHash('sha256').update(base).digest('hex');
assert.equal(sha,'cf0a51a3c282641bc0ab462361cdb28bea26d23360c0088796442fc238eafb6f');checks++;
const result={run:'LSPV-2/512',independent:'Node.js',bit_length:446,unique_reads:434,tail_sign_unread:12,distinct_virtual_children:hits,charge_flip_positions:charge.length,sha256:sha,assertions:checks,malformed_control:'MALFORMED',positive_control:'SAT',negative_control:'UNSAT',all_input_transform:false};
console.log(JSON.stringify(result,null,2));

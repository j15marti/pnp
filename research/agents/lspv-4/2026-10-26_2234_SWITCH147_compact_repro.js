'use strict';
// LSPV-4 / ARC-SWITCH-VS-MACHINE-SPACE147. Node >=16; no dependencies.
// Separate typed inputs x,z are combined with gamma(q),gamma(m) on one
// physically scanned read-only tape; indexed bit accesses and tape moves
// for THIS deterministic reader are both charged. No SAT decider is claimed.
let assertions=0;
function ok(b,msg='assertion'){assertions++;if(!b)throw Error(msg+' #'+assertions)}
function gamma(n){ok(Number.isInteger(n)&&n>=1);let b=n.toString(2);return '0'.repeat(b.length-1)+b}
function makeRecord(active,names,signs,q){let w=Math.floor(Math.log2(q))+1;return String(active)+names.map((v,i)=>v.toString(2).padStart(w,'0')+String(signs[i])).join('')}
function ref(x,z,q,m){const w=Math.floor(Math.log2(q))+1,stride=1+3*(w+1);ok(x.length===m*stride&&z.length===q);for(let c=0;c<m;c++){let off=c*stride;if(x[off]==='0')continue;const names=[],signs=[];for(let j=0;j<3;j++){let base=off+1+j*(w+1);names.push(parseInt(x.slice(base,base+w),2));signs.push(Number(x[base+w]))}if(new Set(names).size!==3||names.some(v=>v<1||v>q))return false;if(!names.some((v,j)=>Number(z[v-1])===signs[j]))return false}return true}
function readMachine(s){let pos=0,head=0,probes=0;const read=(i)=>{ok(i>=0&&i<s.length,'source bounds');head+=Math.abs(i-pos);pos=i;probes++;return s[i]==='1'};
  // Sequential source-length and endmarker discovery, charged first.
  for(let i=0;i<s.length;i++)read(i);
  function g(offset){let zeros=0;while(offset+zeros<s.length&&!read(offset+zeros))zeros++;if(offset+zeros>=s.length||zeros>s.length.toString(2).length+1)return [null,offset+zeros];let n=1,i=offset+zeros+1;for(let j=0;j<zeros;j++){if(i>=s.length)return [null,i];n=2*n+Number(read(i++))}return [n,i]}
  let [q,p]=g(0);if(q===null||q<3||q>s.length)return {answer:false,malformed:true};let m;[m,p]=g(p);if(m===null||m<1||m>s.length)return {answer:false,malformed:true};const w=Math.floor(Math.log2(q))+1,stride=1+3*(w+1),n=m*stride;if(p+n+q!==s.length)return {answer:false,malformed:true};
  let answer=true;for(let c=0;c<m;c++){let off=p+c*stride,active=read(off),names=[],signs=[];for(let j=0;j<3;j++){let base=off+1+j*(w+1),v=0;for(let k=0;k<w;k++)v=2*v+Number(read(base+k));names.push(v);signs.push(Number(read(base+w)))}if(!active)continue;if(new Set(names).size!==3||names.some(v=>v<1||v>q)){answer=false;break}let sat=false;for(let j=0;j<3;j++)if(Number(read(p+n+names[j]-1))===signs[j])sat=true;if(!sat){answer=false;break}}
  let width=Math.floor(Math.log2(s.length+1))+1;return {answer,malformed:false,q,m,recordBits:n,inputBits:s.length,probes,headMoves:head,indexProxy:probes*(2*width+1),registerCeiling:24*width+16};
}
function verify(x,z,q,m){return readMachine(gamma(q)+gamma(m)+x+z)}
let cases=0,accepted=0,rejected=0;
for(let x=0;x<1024;x++){let xb=x.toString(2).padStart(10,'0');for(let z=0;z<8;z++){let zb=z.toString(2).padStart(3,'0'),want=ref(xb,zb,3,1),got=verify(xb,zb,3,1);ok(want===got.answer,'exact semantics');ok(got.probes<=2*got.inputBits+3,'probes bound');if(got.answer)accepted++;else rejected++;cases++}}
let seed=14720261026>>>0;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
for(const [q,m] of [[3,2],[5,3],[7,5],[16,8]]){let w=Math.floor(Math.log2(q))+1,n=m*(1+3*(w+1));for(let t=0;t<600;t++){let x,z;if(t%5===0){x=Array(m).fill(makeRecord(1,[1,2,3],[1,1,0],q)).join('');z='0'.repeat(q)}else if(t%5===1){x=Array(m).fill(makeRecord(1,[0,2,3],[1,1,0],q)).join('');z='0'.repeat(q)}else if(t%5===2){x=Array(m).fill(makeRecord(0,[0,0,0],[0,0,0],q)).join('');z='1'.repeat(q)}else{x=Array.from({length:n},()=>rnd()<0.5?'0':'1').join('');z=Array.from({length:q},()=>rnd()<0.5?'0':'1').join('')}let want=ref(x,z,q,m),got=verify(x,z,q,m);ok(want===got.answer,'seeded semantics');ok(got.probes<=2*got.inputBits+3*m,'probe cap');if(got.answer)accepted++;else rejected++;cases++}}
let a=gamma(3)+gamma(1)+makeRecord(1,[1,2,3],[1,1,0],3)+'000';ok(verify(makeRecord(1,[1,2,3],[1,1,0],3),'000',3,1).answer);
for(const s of [a.slice(0,-1),a+'0','0','0000','1111','']){let r=readMachine(s);ok(!r.answer&&r.malformed,'malformed length/header')}
const travel=[];for(const m of [4,8,16,32,64,128,256]){let q=m,x=Array(m).fill(makeRecord(1,[1,2,3],[1,1,0],q)).join(''),z='0'.repeat(q),r=verify(x,z,q,m);let K=2**Math.ceil(Math.log2(q+3*m)),h=Math.log2(K),switches=(K/2)*h*(h+1)/2;ok(r.answer&&ref(x,z,q,m));ok(r.headMoves>=m*r.recordBits/3);travel.push({m,recordBits:r.recordBits,L:r.inputBits,switches,probes:r.probes,headMoves:r.headMoves,indexProxy:r.indexProxy,registerCeiling:r.registerCeiling})}
let result={run:'ARC-SWITCH-VS-MACHINE-SPACE147',exhaustivePairs:8192,cases,accepted,rejected,assertions,failures:0,seed:'fixed LCG 14720261026',travel,limits:'supplied witness; direct verifier only; sequential head moves are one specific itinerary; no SAT decision or ARC edge'};
if(require.main===module)console.log(JSON.stringify(result,null,2));
module.exports={gamma,ref,readMachine,verify};

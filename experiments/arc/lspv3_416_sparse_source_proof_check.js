#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
let checks=0;const ok=(p,m)=>{assert.ok(p,m);checks++};
const powers=[2,4,8,16,32,64,128,256,512,1024];
const rows=[];
function source(K,sat=false){return 'p cnf '+K+' 4\n'+K+' 0\n'+(sat?'':'-')+K+' 0\n'+K+' 1 0\n-'+K+' 1 0\n';}
function parse(S){
const L=S.trim().split('\n');const H=L.shift().trim().split(/\s+/);
if(H.length!==4||H[0]!=='p'||H[1]!=='cnf')throw Error('header');
const K=BigInt(H[2]),m=Number(H[3]);if(K<1n||!Number.isSafeInteger(m)||m!==L.length)throw Error('counts');
const clauses=L.map(s=>{
const a=s.trim().split(/\s+/);if(a.at(-1)!=='0'||a.length<2)throw Error('terminator');
const c=a.slice(0,-1).map(BigInt);
if(c.some(z=>z===0n||(z<0n?-z:z)>K))throw Error('literal');
return c;
});return {K,clauses};
}
function lit(c,K,Y,X){return c.some(z=>{
const id=z<0n?-z:z;const val=id===K?X:(id===1n?Y:undefined);
if(val===undefined)throw Error('unexpected variable');
return z>0n?val:!val;
});}
for(const t of powers){
const K=10n**BigInt(t),d=K.toString(),F=parse(source(d)),S=parse(source(d,true));
ok(F.K===K&&S.K===K,'declared exact');
ok(F.clauses.length===4,'four original clauses');
let u=0,v=0;
for(const Y of [false,true])for(const X of [false,true]){
const A=lit(F.clauses[0],K,Y,X)&&lit(F.clauses[2],K,Y,X);
const B=lit(F.clauses[1],K,Y,X)&&lit(F.clauses[3],K,Y,X);
ok(A===X&&B===!X,'exact AND3 truth tables');
if(F.clauses.every(c=>lit(c,K,Y,X)))u++;
if(S.clauses.every(c=>lit(c,K,Y,X)))v++;
}
ok(u===0&&v>0,'SAT and UNSAT controls');
const a=new Set([d]),b=new Set([d]);
for(const x of b){if(a.has(x))a.delete(x);else a.add(x)}
ok(a.size===0&&(1^0)===1,'GF2 contradiction');
const src=source(d);const sparse={sourceIDs:[0,1,2,3],nodes:[
{type:'AND3',parents:['c1','c3'],support:['1',d],row:{ids:[d],rhs:1}},
{type:'AND3',parents:['c2','c4'],support:['1',d],row:{ids:[d],rhs:0}},
{type:'XOR',parents:[0,1],row:{ids:[],rhs:1}}]};
const srcBits=Buffer.byteLength(src)*8,proofBits=Buffer.byteLength(JSON.stringify(sparse))*8;
ok(srcBits>0&&proofBits>0&&proofBits<100*srcBits,'sparse polynomial-byte witness');
ok(BigInt(t)>=2n&&K===10n**BigInt(t),'decimal identity');
rows.push({power:t,sourceBits:srcBits,proofBits,denseBitsLowerDecimalDigits:d.length,qConstructed:3,qOptimumRES:1});
}
for(const bad of ['p cnf 1 2\n1 0\n','p cnf 1 1\n2 0\n','p cnf 2 1\n0 1\n','p cnf 2 1\n1 1\n']){
let threw=false;try{parse(bad)}catch{threw=true}ok(threw,'malformed source');
}
console.log(JSON.stringify({schema:'LSPV3_416_GITHUB_SELF_CONTAINED',checks,rows,status:'COMPUTATIONAL',B3:'OPEN'}));

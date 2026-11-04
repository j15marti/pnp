// Independent LSPV-3/404 finite checker. Run: node lspv3_404_independent_support_verify.js
'use strict';
const assert=require('assert'),bit=(t,a,b)=>(t>>((a<<1)|b))&1;
const depends=(t,i)=>[0,1].some(a=>[0,1].some(b=>bit(t,a,b)!==bit(t,a^(i===0),b^(i===1))));
const G=Array.from({length:16},(_,i)=>i).filter(t=>depends(t,0)&&depends(t,1));
assert.strictEqual(G.length,10);
const evaluate=(nodes,root,x)=>{const val=[];for(const g of nodes)val.push(g.kind==='input'?x[g.var]:bit(g.table,val[g.a],val[g.b]));return val[root];};
const mask=nodes=>{const m=[];nodes.forEach((g,i)=>{if(g.kind==='input'){if(!Number.isInteger(g.var)||g.var<0)throw Error('bad input');m.push(1<<g.var);}else{if(g.kind!=='gate'||!Number.isInteger(g.a)||!Number.isInteger(g.b)||g.a>=i||g.b>=i||g.a<0||g.b<0||!G.includes(g.table))throw Error('bad gate');if(m[g.a]&m[g.b])throw Error('overlap');m.push(m[g.a]|m[g.b]);}});return m;};
function tree(n,tables){const nd=Array.from({length:n},(_,i)=>({kind:'input',var:i}));let ids=Array.from({length:n},(_,i)=>i),k=0;while(ids.length>1){const next=[];for(let j=0;j<ids.length;j+=2){if(j+1===ids.length){next.push(ids[j]);continue;}nd.push({kind:'gate',a:ids[j],b:ids[j+1],table:tables[k++]});next.push(nd.length-1);}ids=next;}assert.strictEqual(k,n-1);return {nd,root:ids[0]};}
let circuits=0,assignments=0;
function test(n,ts){const {nd,root}=tree(n,ts),m=mask(nd);assert.strictEqual(m[root],(1<<n)-1);circuits++;let effects=0;for(let a=0;a<(1<<n);a++){const x=Array.from({length:n},(_,i)=>(a>>i)&1),orig=evaluate(nd,root,x);assignments++;for(let i=0;i<n;i++){const y=x.slice();y[i]^=1;if(orig!==evaluate(nd,root,y))effects|=1<<i;}}assert.strictEqual(effects,(1<<n)-1);}
for(let n=2;n<=4;n++){const idx=Array(n-1).fill(0);for(let p=0;p<10**(n-1);p++){let q=p;for(let j=0;j<n-1;j++){idx[j]=q%10;q=Math.floor(q/10);}test(n,idx.map(z=>G[z]));}}
const xo=[{kind:'input',var:0},{kind:'gate',a:0,b:0,table:6}];for(const x of [0,1])assert.strictEqual(evaluate(xo,1,[x]),0);assert.throws(()=>mask(xo));
const ab=[{kind:'input',var:0},{kind:'input',var:1},{kind:'gate',a:0,b:1,table:8},{kind:'gate',a:0,b:2,table:14}];for(const a of [0,1])for(const b of [0,1])assert.strictEqual(evaluate(ab,3,[a,b]),a);assert.throws(()=>mask(ab));
assert.throws(()=>mask([{kind:'input',var:-1}]));assert.throws(()=>mask([{kind:'input',var:0},{kind:'input',var:1},{kind:'gate',a:0,b:1,table:0}]));
console.log(JSON.stringify({gate_tables:G,circuits,assignments,negative_controls:2,malformed_rejected:2,status:'independent finite checks passed'}));

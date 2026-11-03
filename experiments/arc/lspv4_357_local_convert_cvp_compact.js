#!/usr/bin/env node
// LSPV-4 357: CONDITIONAL large LOCAL-CONVERT rule-validity experiment.
// This does not define or change the accepted fixed Rmix341 grammar.
'use strict';
function evalCircuit(gs){
 if(!Array.isArray(gs)||!gs.length)throw Error('gates');
 let v=[];
 for(let i=0;i<gs.length;i++){
  let g=gs[i],op=g&&g[0],ar={C0:0,C1:0,NOT:1,AND:2,OR:2,XOR:2}[op];
  if(ar===undefined||g.length!==ar+1)throw Error('gate type/arity');
  for(let p of g.slice(1))if(!Number.isInteger(p)||p<0||p>=i)throw Error('gate reference');
  v.push(op==='C0'?0:op==='C1'?1:op==='NOT'?1-v[g[1]]:
         op==='AND'?(v[g[1]]&v[g[2]]):op==='OR'?(v[g[1]]|v[g[2]]):(v[g[1]]^v[g[2]]));
 }
 return v[v.length-1]===1;
}
function source(s){
 let a=s.trim().split(/\s+/);
 if(a.length!==6||a[0]!=='p'||a[1]!=='cnf'||a[2]!=='1'||a[3]!=='1'||a[5]!=='0'||!['1','-1'].includes(a[4]))throw Error('source');
 return a[4];
}
function legal(s,gates){source(s);return evalCircuit(gates)}
function chain(g){let c=[['C0'],['C1']];for(let i=2;i<g;i++)c.push([i%3===0?'XOR':'AND',i-1,1]);return c;}
let rows=[],yes=0,no=0;
for(let g of [2,4,8,16,32,64,128,256,512,1024,4096]){
 let gs=chain(g),val=legal('p cnf 1 1\n1 0\n',gs);
 rows.push({g,valid:val,encoded_record_bytes:Buffer.byteLength(JSON.stringify(gs))});
 if(val)yes++;else no++;
}
function rejects(s,c){try{legal(s,c);return false}catch(_){return true}}
let bad=0;
for(let [s,c] of [
 ['p cnf 1 2\n1 0\n',chain(16)],
 ['p cnf 1 1\n1\n',chain(16)],
 ['p cnf 1 1\n1 0\n',[['NOT',0]]],
 ['p cnf 1 1\n1 0\n',[['C1'],['AND',1,0]]]
])if(rejects(s,c))bad++;
if(yes===0||no===0||bad!==4)throw Error('controls failed');
console.log(JSON.stringify({status:'PASS',cases:rows.length,valid:yes,invalid:no,malformed_rejections:bad,rows},null,2));

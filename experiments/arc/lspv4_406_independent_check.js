'use strict';
// Independent no-dependency exact checker for LSPV-4/406.
// Test grammar is a declared *semantic* paid-DEF encoding,
// NOT an authenticated native LOCAL-CONVERT port grammar.
const assert=require('assert');
function encoded(q,b,j){
 const w=Math.max(1,Math.ceil(Math.log2(q)));
 return 'Q'+String(q).padStart(5,'0')+':'+b.join('')+':A'+j.toString(2).padStart(w,'0');
}
function evaluate(code,x){
 const m=/^Q([0-9]{5}):([01]+):A([01]+)$/.exec(code);
 if(!m)throw Error('grammar');
 const q=Number(m[1]),w=Math.max(1,Math.ceil(Math.log2(q)));
 if(q<1||q>99999||m[2].length!==q||m[3].length!==w||code.length!==9+q+w)throw Error('length');
 const j=parseInt(m[3],2);
 if(j>=q)throw Error('index');
 const a=[];
 for(const op of m[2])a.push((op==='0'?[0,0]:[1,1])[x]);
 return a[j]&a[j];
}
function countModels(clauses,n){
 let count=0;
 for(let a=0;a<(1<<n);a++){
  if(clauses.every(C=>C.some(l=>((a>>(Math.abs(l)-1))&1)===Number(l>0))))count++;
 }
 return count;
}
assert.equal(countModels([[1]],1),1);
assert.equal(countModels([[1],[-1]],1),0);
let cases=0,assignments=0;
for(let q=1;q<=12;q++){
 const signatures=new Set(),sizes=new Set();
 for(let mask=0;mask<2**q;mask++){
  const b=Array.from({length:q},(_,i)=>(mask>>(q-i-1))&1);
  let signature='';
  for(let j=0;j<q;j++){
   const code=encoded(q,b,j);sizes.add(code.length);
   for(let x=0;x<=1;x++){
    assert.equal(evaluate(code,x),b[j]);assignments++;
   }
   cases++;signature+=evaluate(code,1);
  }
  signatures.add(signature);
 }
 assert.equal(signatures.size,2**q);
 assert.equal(sizes.size,1);
 assert.equal([...sizes][0],9+q+Math.max(1,Math.ceil(Math.log2(q))));
}
for(const bad of ['', 'Q00001:0:A9', 'Q00003:010:A11',
                  'Q00002:02:A0','Q00002:01:B0',
                  'Q00002:01:A','Q00000::A0',
                  'Q00001:0:A00','Q00001:0:A0\n']){
 assert.throws(()=>evaluate(bad,1));
}
assert.equal(cases,90114);assert.equal(assignments,180228);
process.stdout.write('PASS q<=12; '+cases+' index probes, '+assignments+' assignment checks, 9 malformed controls\n');

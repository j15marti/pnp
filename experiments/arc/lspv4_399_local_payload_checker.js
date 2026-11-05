// LSPV-4/399 independent exact finite checker; declared hypothetical R_chain, NOT native R_mix341.
const assert=require('assert');
function chain(m,flip=0){return Array.from({length:m},(_,i)=>({left:i,negative:(i+1===flip)}));}
function check(g){let vals=[false,true];for(let i=0;i<g.length;i++){const c=g[i];
 if(c.left!==i||typeof c.negative!=='boolean')throw Error('malformed');
 vals=vals.map((v,k)=>v&&(c.negative?!Boolean(k):Boolean(k)));
}return vals[1]===true;}
const sizes=[1,2,3,4,8,16,32,64,128,256,512,1024,2048];
let good=0,bad=0;
for(const m of sizes){assert(check(chain(m)));good++;
 for(let j=1;j<=m;j++){assert(!check(chain(m,j)));bad++;}}
assert.deepStrictEqual([good,bad],[13,4098]);
assert.throws(()=>check([{left:17,negative:false}]));
console.log(JSON.stringify({status:"COMPUTATIONAL",model:"R_chain, not native R_mix341",valid:good,mutants_rejected:bad}));

// Run with node BA08_supplement.js PATH_TO_BA08_check.js
const fs=require('fs'),vm=require('vm');
const base=fs.readFileSync(process.argv[2],'utf8');
const extra=String.raw`
const before={...stats};
const allpairs={SAT:0,UNSAT:0,unknown:0},dense={SAT:0,UNSAT:0,unknown:0};
function table(mask,rows){return {rows,terms:Array.from({length:4},(_,j)=>j).filter(j=>mask>>j&1).map(j=>event(2,j,1n))}}
for(let a=0;a<16;a++)for(let b=0;b<16;b++)compare(2,[table(a,[1n,2n]),table(b,[3n,2n])],allpairs);
for(let k=0;k<64;k++){
 let a=BigInt(1+rnd(15)),b=BigInt(1+rnd(15));while(a===b)b=BigInt(1+rnd(15));
 let c=BigInt(1+rnd(15)),e=BigInt(1+rnd(15));while(c===e)e=BigInt(1+rnd(15));
 compare(4,[table(1+rnd(14),[a,b]),table(1+rnd(14),[c,e])],dense);
}
console.log(JSON.stringify({allpairs,dense,stats:Object.fromEntries(Object.keys(stats).map(k=>[k,stats[k]-before[k]]))},null,2));`;
let logs=[];vm.runInNewContext(base+'\n'+extra,{console:{log:x=>logs.push(x)}});console.log(logs.at(-1));

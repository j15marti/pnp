/* Exact finite linear-sketch audit; node permutation-rank.js */
const audit=function permAudit(){
 function permutations(a){if(!a.length)return [[]];return a.flatMap((v,i)=>permutations(a.filter((_,j)=>i!==j)).map(p=>[v,...p]))}
 let P=permutations([0,1,2,3]).map(p=>p.reduce((w,v,i)=>w|(v<<(2*i)),0)),D=new Set();for(let a of P)for(let b of P)if(a!==b)D.add(a^b);
 let parity=x=>{let b=0;while(x){b^=1;x&=x-1}return b};
 let H=Array.from({length:256},(_,i)=>i).filter(i=>!parity(i&0x55)&&!parity(i&0xaa));
 if(D.size!==63||H.length!==64||H.some(x=>x&&!D.has(x)))throw Error("difference-span");
 let sketches=P.map(x=>x&63);if(new Set(sketches).size!==24)throw Error("rank 6 sketch");
 // Check a guard that is a rank-6 equality sketch accepts precisely the 24 diagonal pairs.
 let accepted=0;for(let x of P)for(let y of P){let ok=(x&63)===(y&63);if(ok!==(x===y))throw Error("bad guard");accepted+=+ok}
 return {encoding:"PERM-PAIR-AFFINE-v1: r=4, each permutation encoded by 4 consecutive 2-bit identifiers (0..3), least significant block first. Pair = 16 bits; this is map block only, not compiled CNF length.",permutations:P,nonzeroDifferences:[...D].sort((a,b)=>a-b),differenceSpaceBasis:[5,10,17,34,65,130],differenceSpaceDimension:6,exactMinimumInjectiveLinearSketchRank:6,witnessRows:[1,2,4,8,16,32],verifiedPairs:576,accepted,sketches};
};
console.log(JSON.stringify(audit(),null,2));

const control = function control(){
 const bit=i=>1n<<BigInt(i), xor=a=>a.reduce((x,y)=>x^y,0n);
 function basis(a){let b=[];for(let x of a){for(let y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((x,y)=>x>y?-1:1);}}return b;}
 let out=[];
 // For each 4-cycle component, one triangle's two distinct port deletions
 // have tags 0 or a private unit. Other shores and all cut tags are zero.
 // There are two perfect skeleton matchings and one local matching per selector.
 for(let k of [1,2,4,8,16,32,64]){
   let offsets=Array.from({length:k},(_,i)=>bit(i));
   let movedRank=basis(offsets).length;
   // Keeping selector offsets gives pairwise independent one-dimensional
   // regional spaces, so their shared intersections and U0 are zero.
   let keptRank=0;
   let n=1n<<BigInt(k), target=n-1n;
   // Build one matching per cycle choosing the needed selector.
   let choices=offsets.map(x=>(target&x)!==0n?x:0n);
   if(xor(choices)!==target||movedRank!==k)throw Error("control");
   // Independent exhaustive matching support for small k.
   let enumerated=null;
   if(k<=8){let support=new Set([0n]);for(let u of offsets)support=new Set([...support].flatMap(x=>[x,x^u]));if(BigInt(support.size)!==n||!support.has(target)||support.has(bit(k)))throw Error("support");enumerated=support.size;}
   out.push({components:k,rawSharedRank:0,keepSharedRank:keptRank,moveSharedRank:movedRank,selectorRank:0,satTarget:target.toString(),unsatTarget:bit(k).toString(),enumerated,attainableCount:n.toString()});
 }
 return out;
};
console.log(JSON.stringify(control(), null, 2));

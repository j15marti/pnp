// Independent finite set/affine checks; node independent_audit.js
const audit=()=>{
 let checks=0;function ok(b){checks++;if(!b)throw Error("check "+checks);}
 const key=S=>[...S].sort((a,b)=>a-b).join(",");
 const eq=(A,B)=>key(A)===key(B);
 const project=(S,M)=>new Set([...S].map(x=>x&M));
 const product=(A,B)=>new Set([...A].flatMap(x=>[...B].map(y=>x|y)));
 const union=xs=>new Set(xs.flatMap(x=>[...x]));
 let splits=0;
 for(let s=1;s<256;s++){let S=new Set(Array.from({length:8},(_,i)=>i).filter(i=>(s>>i)&1));for(let M=1;M<7;M++){let A=project(S,M),B=project(S,7^M),P=product(A,B);ok((S.size===A.size*B.size)===eq(S,P));if(eq(S,P))splits++;}}
 const parity=new Set([0,3,5,6]);for(const M of [3,5,6])ok(project(parity,M).size===4);ok(!eq(parity,product(project(parity,1),project(parity,6))));
 let state=26112611;const rnd=n=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state%n;};
 const choose=(M)=>new Set(Array.from({length:16},(_,i)=>i).filter(i=>(i&~M)===0&&rnd(3)>0));
 for(let t=0;t<400;t++){
   let A=choose(3),B=choose(12),C=choose(12);
   ok(eq(union([product(A,B),product(A,C)]),product(A,union([B,C]))));
   let P=product(A,B),M=rnd(16),r=rnd(16)&M,Y=rnd(16);
   let direct=project(new Set([...P].filter(x=>(x&M)===r)),Y);
   const cut=(S,X)=>project(new Set([...S].filter(x=>(x&M&X)===(r&M&X))),Y&X);
   ok(eq(direct,product(cut(A,3),cut(B,12))));
 }
 // All subspaces of GF(2)^6, translated by all cosets, validate NAND^3 bound.
 let spaces=new Map([["0",new Set([0])]]);for(let k=0;k<6;k++){let L=[...spaces.values()];for(let H of L)for(let x=1;x<64;x++)if(!H.has(x)){let J=union([H,new Set([...H].map(y=>y^x))]);spaces.set(key(J),J);}}
 let P=new Set(Array.from({length:64},(_,i)=>i).filter(x=>[0,2,4].every(j=>((x>>j)&3)!==3)));
 let contained=0,max=0;for(let H of spaces.values())for(let a=0;a<64;a++){let C=new Set([...H].map(x=>x^a));if([...C].every(x=>P.has(x))){contained++;max=Math.max(max,C.size);ok(C.size<=8);}}
 ok(P.size===27);ok(max===8);
 return {checks,splits,randomCases:400,subspaces:spaces.size,containedTranslatedCosetsWithMultiplicity:contained,maxContainedCoset:max};
};
console.log(JSON.stringify(audit(),null,2));

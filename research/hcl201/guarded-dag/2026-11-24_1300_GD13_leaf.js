"use strict";
function leafExperiment(){
 let stats={cases:0,interfaceWords:0,referenceWords:0,witnessChecks:0,assertions:0};
 function assert(p){stats.assertions++;if(!p)throw Error("leaf assertion")}
 const bit=i=>1n<<BigInt(i),hi=x=>x.toString(2).length-1;
 function par(x){let c=0;while(x){c^=1;x&=x-1n}return c}
 function add(B,m,c){while(m){let i=hi(m),v=B.get(i);if(!v){B.set(i,[m,c]);return true}m^=v[0];c^=v[1]}return c===0}
 function reduce(B,m,c=0){for(let i of [...B.keys()].sort((a,b)=>b-a))if(m&bit(i)){let v=B.get(i);m^=v[0];c^=v[1]}return [m,c]}
 function lift(B){let x=0n;for(let i of [...B.keys()].sort((a,b)=>a-b)){let [m,c]=B.get(i);if(par(m&x)!==c)x|=bit(i)}return x}
 // local observation space is F2^d, exact enabled observation word is h.
 function row(d,I,h,z){let B=new Map();for(let i=0;i<I.length;i++)assert(add(B,I[i],Number((z>>BigInt(i))&1n)));let same=I.every((m,i)=>par(m&h)===Number((z>>BigInt(i))&1n));let total=1n<<BigInt(d-I.length),on=same?1n:0n,off=total-on,w=null;
 if(off){if(same){let found=false;for(let i=0;i<d;i++){if(reduce(B,bit(i))[0]){assert(add(B,bit(i),par(h&bit(i))^1));found=true;break}}assert(found)}w=lift(B);assert(w!==h&&I.every((m,i)=>par(m&w)===Number((z>>BigInt(i))&1n)));stats.witnessChecks++}
 if(on){assert(I.every((m,i)=>par(m&h)===Number((z>>BigInt(i))&1n)));stats.witnessChecks++}
 return {on,off,w};
 }
 let seed=915372;function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>8}
 for(let d=1;d<=9;d++)for(let q=0;q<20;q++){let B=new Map(),I=[];let mask=(1<<d)-1,r=q%(Math.min(4,d)+1),h=BigInt(random()&mask);
 while(I.length<r){let m=BigInt(random()&mask);if(reduce(B,m)[0]){add(B,m,0);I.push(m)}}
 stats.cases++;for(let z=0n;z<(1n<<BigInt(r));z++){stats.interfaceWords++;let a=row(d,I,h,z),on=0n,off=0n;
 for(let x=0n;x<(1n<<BigInt(d));x++){stats.referenceWords++;if(I.every((m,i)=>par(m&x)===Number((z>>BigInt(i))&1n))){if(x===h)on++;else off++}}
 assert(a.on===on&&a.off===off);
 }}
 let wide=[];for(let d of [64,128,256,1024]){let I=[1n,bit(d-1)],h=0n,rows=[];for(let z=0n;z<4n;z++){let a=row(d,I,h,z);rows.push({z:String(z),on:String(a.on),off:String(a.off)});}let sum=rows.reduce((s,a)=>s+BigInt(a.off),0n);assert(sum===(1n<<BigInt(d))-1n);wide.push({d,r:2,rows,nonreachCount:String(sum)})}
 return {seed:915372,stats,wide};
}
console.log(JSON.stringify(leafExperiment(),null,2));

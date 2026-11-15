// TMR-1/054. Exact count-preserving width-three CNF compiler and Anthropic bit encoding.
// Node >=18, no deps. Revision TMR1_DENSITY4_STACK054_v1. Seed 20261115.
(function () {
"use strict";
const SEED=20261115;let state=SEED>>>0,checks=0,sourceAssignments=0,fullAssignments=0,controls=0;
function rng(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
function ok(b,m){checks++;if(!b)throw Error(m);}
function fv(f,a,b){return (f>>((a<<1)|b))&1;}
function output(c,x){let w=x.slice();for(const g of c.gates)w.push(fv(g.f,w[g.a],w[g.b]));return w[c.out];}
function compile(c){
 const q=c.q,G=c.gates.length,V=q+G,all=[],used=new Set(),lit=(i,p)=>[i,!!p];
 for(let j=0;j<G;j++){const {a,b,f}=c.gates[j],z=q+j;used.add(a);used.add(b);
   for(let u=0;u<2;u++)for(let v=0;v<2;v++)
     all.push([lit(a,u===0),lit(b,v===0),lit(z,fv(f,u,v)===1)]);
 }
 all.push([lit(c.out,true)]);if(c.out<q)used.add(c.out);
 const missing=[];for(let i=0;i<q;i++)if(!used.has(i)){
   missing.push(i);all.push([lit(i,true),lit(i,false),lit(i,true)]);
 }
 const seen=new Set(),clauses=[];
 for(const cl of all){const s=JSON.stringify(cl);if(!seen.has(s)){seen.add(s);clauses.push(cl);}}
 return {V,m:clauses.length,clauses,missing};
}
function sat(cs,a){return cs.every(c=>c.some(([i,p])=>a[i]===(p?1:0)));}
function encode(H){
 const k=3,n=H.V,w=Math.floor(Math.log2(2*n))+1,bits=[1,1,1,0,...Array(n).fill(1),0];
 for(const cl of H.clauses)for(let j=0;j<k;j++){
   const t=j<cl.length?2*cl[j][0]+1+Number(cl[j][1]):0;
   for(let b=0;b<w;b++)bits.push((t>>>b)&1);
 }
 return {bits,w};
}
function decode(bits){
 let p=0,k=0,n=0;while(bits[p]===1){p++;k++;}ok(bits[p++]===0,"k delimiter");
 while(bits[p]===1){p++;n++;}ok(bits[p++]===0,"n delimiter");
 const w=Math.floor(Math.log2(2*n))+1;ok((bits.length-p)%(k*w)===0,"word divisibility");
 const clauses=[];while(p<bits.length){const cl=[];for(let j=0;j<k;j++){
   let t=0;for(let b=0;b<w;b++)t+=bits[p++]*(2**b);
   if(t){ok(t<=2*n,"slot in range");cl.push([Math.floor((t-1)/2),(t&1)===0]);}
 }clauses.push(cl);}return {k,n,clauses};
}
function verify(c,label){
 const H=compile(c),V=H.V,G=c.gates.length,u=H.missing.length;
 ok(V>=4&&H.m>=2,"Anthropic minima");
 ok(H.m<=4*G+u+1,"sharper literal tax");
 ok(H.m<=4*V,"density four");
 ok(H.clauses.every(cl=>cl.length<=3),"width three");
 ok(new Set(H.clauses.map(JSON.stringify)).size===H.m,"outer list NoDup");
 ok(new Set(H.clauses.flatMap(cl=>cl.map(l=>l[0]))).size===V,"AllOccur");
 const e=encode(H),d=decode(e.bits);
 ok(d.k===3&&d.n===V&&JSON.stringify(d.clauses)===JSON.stringify(H.clauses),"exact bit decode");
 ok(e.bits.length===V+5+3*H.m*e.w,"exact source bit length");
 let nSat=0,expected=0;
 for(let x=0;x<2**c.q;x++){
   const a=Array.from({length:c.q},(_,i)=>(x>>i)&1),v=output(c,a);
   expected+=v;let ext=0;
   for(let z=0;z<2**G;z++){
     const b=Array.from({length:G},(_,i)=>(z>>i)&1);
     if(sat(H.clauses,a.concat(b))){ext++;nSat++;}
     fullAssignments++;
   }
   ok(ext===v,"unique extension at x="+x+" case "+label);sourceAssignments++;
 }
 ok(nSat===expected,"exact total count");if(label==="control")controls++;
 return {V,m:H.m,unusedInputCount:u,count:nSat,encodedBits:e.bits.length,label};
}
const cases=[],add=(g,o,q=4,label="control")=>cases.push({q,gates:g,out:o,label});
add([],0);
add([{a:0,b:0,f:6}],4); // repeated input, zero XOR
add([{a:0,b:1,f:6}],4); // XOR
add([{a:0,b:1,f:7}],4); // NAND
add([{a:0,b:1,f:8}],4); // AND
add([{a:0,b:1,f:1},{a:4,b:2,f:14}],5); // composite and ignored bits
add([{a:0,b:1,f:8},{a:0,b:2,f:8},{a:4,b:5,f:14}],6); // shared input
add([{a:0,b:1,f:0},{a:4,b:4,f:15}],5); // constant and dead gate
add([{a:0,b:1,f:9},{a:4,b:2,f:6},{a:5,b:3,f:14}],6);
add([{a:0,b:2,f:7},{a:1,b:3,f:7},{a:4,b:5,f:8}],6); // DISJ2
for(let f=0;f<16;f++)for(let a=0;a<4;a++)for(let b=0;b<4;b++)
 add([{a,b,f}],4,4,"all-gates");
for(let t=0;t<160;t++){
 const q=4+rng()%2,G=rng()%6,g=[];
 for(let j=0;j<G;j++)g.push({a:rng()%(q+j),b:rng()%(q+j),f:rng()%16});
 add(g,rng()%(q+G),q,"seeded");
}
let maxV=0,totalClauses=0,maxDensity=0,maxInputBits=0;const examples=[];
for(const c of cases){
 const r=verify(c,c.label);
 maxV=Math.max(maxV,r.V);totalClauses+=r.m;
 maxDensity=Math.max(maxDensity,r.m/r.V);maxInputBits=Math.max(maxInputBits,r.encodedBits);
 if(examples.length<8)examples.push(r);
}
const budgets=[64,256,1024,4096].map(V=>{
 const m=4*V,w=Math.floor(Math.log2(2*V))+1,encodedBits=V+5+3*m*w;
 const expM=3*m/Math.sqrt(Math.log2(m)),bound=12*V/Math.sqrt(Math.log2(V/3));
 ok(expM<=bound,"density exponent budget");
 return {V,m,encodedBits,expMoverV:expM/V,safeBoundOverV:bound/V};
});
const result={revision:"TMR1_DENSITY4_STACK054_v1",seed:SEED,source:"experiments/tmr/tmr1_density4_stack054.js",status:"COMPUTATIONAL",circuits:cases.length,controls,sourceAssignments,fullAssignments,assertions:checks,failures:0,maxV,totalClauses,maxDensity,maxInputBits,examples,budgets};
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
return result;
})()
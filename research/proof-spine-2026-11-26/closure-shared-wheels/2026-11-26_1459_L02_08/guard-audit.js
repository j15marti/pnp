const r=(function guardAudit(){
let checks=0;const assert=x=>{checks++;if(!x)throw Error("guard check")};let count=0;
for(let h0=0;h0<4;h0++)for(let h1=0;h1<4;h1++)for(let h2=0;h2<4;h2++)for(let h3=0;h3<4;h3++){
let hs=[h0,h1,h2,h3];for(let t=0;t<=4;t++)for(let w=0;w<16;w++){
let s=0;for(let i=0;i<t;i++)s|=(hs[i]>>((w>>i)&1))&1;
let constant=hs.slice(0,t).includes(3),lit=[];for(let i=0;i<t;i++)if(hs[i]===1||hs[i]===2)lit.push([i,hs[i]===2?1:0]);
let positive=constant||lit.some(([i,b])=>((w>>i)&1)===b),negative=!constant&&lit.every(([i,b])=>((w>>i)&1)!==b);
assert(positive===Boolean(s));assert(negative===!s);count++;
}}
let relation=(x,a,b)=>((x^a)===b)||x===1&&a===0;let feasible=[];for(let x=0;x<2;x++)if(relation(x,0,0)&&relation(x,0,0)&&(x^0)===1)feasible.push(x);assert(feasible.length===1&&feasible[0]===1);
return {checks,prefixCases:count,threeOccurrenceCounterexample:{guards:{a:0,b:0,c:0},uniqueSharedBit:1,requiredExceptions:2},scope:"local algebraic prefix identity exhaustive; degree-three guard example checked on projected relations; no arbitrary physical guard native solver executed"}})();
console.log(JSON.stringify(r,null,2));

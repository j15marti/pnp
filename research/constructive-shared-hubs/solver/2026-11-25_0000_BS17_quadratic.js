function run(){
let seed=20261125,assertions=0,probes=0;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)},ok=x=>{assertions++;if(!x)throw Error("assert "+assertions)};
function q(w,k){let z=(w&((1<<k)-1))&(w>>k),p=0;while(z){z&=z-1;p^=1}return p}
let out=[];for(let i=0;i<240;i++){let k=1+rnd(7),a=rnd(1<<(2*k)),d=rnd(2*k+1),v=Array.from({length:d},()=>rnd(1<<(2*k))),target=rnd(2);let best=null;function test(w){probes++;if(q(w,k)===target&&best===null)best=w}test(a);for(let j=0;j<d;j++){test(a^v[j]);for(let h=0;h<j;h++)test(a^v[j]^v[h])}let brute=false;for(let w=0;w<(1<<d);w++){let z=a;for(let j=0;j<d;j++)if((w>>j)&1)z^=v[j];if(q(z,k)===target){brute=true;break}}ok(brute===(best!==null));if(best!==null)ok(q(best,k)===target);out.push({k,d,target,sat:brute})}
return {assertions,probes,sat:out.filter(x=>x.sat).length,unsat:out.filter(x=>!x.sat).length,seed:20261125,jobs:out};
}
console.log(JSON.stringify(run(),null,2));

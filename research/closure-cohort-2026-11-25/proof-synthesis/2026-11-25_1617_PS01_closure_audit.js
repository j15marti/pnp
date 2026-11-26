function closureAudit(){
let seed=92814317;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
const out={seed,roots:500,comparisons:0,forces:0,removed:0,rejections:0,rounds:0,guarded:0};
function xorParity(a){let z=0;while(a){a&=a-1;z^=1}return z}
function reduce([a,b],B){for(let i=30;i>=0;i--)if((a>>>i&1)&&B.has(i)){let [x,y]=B.get(i);a^=x;b^=y}return[a,b]}
function insert(row,B){let [a,b]=reduce(row,B);if(!a)return b?-1:0;B.set(31-Math.clz32(a),[a,b]);return 1}
function close(G,H){const B=new Map();for(let h of H)if(insert(h,B)<0)return {bad:true};let C=G.map(g=>g.slice());while(true){out.rounds++;let change=false,D=[];for(let g of C){let alt=g.map(e=>reduce(e,B)),F=new Map(),inconsistent=false;for(let [a,b] of alt)if(insert([a,b^1],F)<0){inconsistent=true;break}if(inconsistent){out.removed++;continue}if(!F.size)return{bad:true};if(F.size===1){let [[a,b]]=[...F.values()];let z=insert([a,b^1],B);if(z<0)return{bad:true};if(z>0){out.forces++;change=true}out.removed++;continue}D.push(alt)}C=D;if(!change)return{bad:false,B,C}}}
function sat(G,x){return G.every(g=>g.some(([a,b])=>xorParity(a&x)===b))}
for(let t=0;t<out.roots;t++){let n=2+rand(6),G=Array.from({length:1+rand(8)},()=>Array.from({length:1+rand(4)},()=>[rand(1<<n),rand(2)])),H=Array.from({length:rand(3)},()=>[rand(1<<n),rand(2)]);if(H.length)out.guarded++;let R=close(G,H);if(R.bad)out.rejections++;for(let x=0;x<1<<n;x++){let a=sat(G,x)&&H.every(([v,b])=>xorParity(v&x)===b),b=!R.bad&&sat(R.C,x)&&[...R.B.values()].every(([v,b])=>xorParity(v&x)===b);if(a!==b)throw Error("closure altered support");out.comparisons++}}
return out}
console.log(JSON.stringify(closureAudit(),null,2));
